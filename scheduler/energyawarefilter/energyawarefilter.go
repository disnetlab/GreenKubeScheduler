package energyawarefilter

import (
	"context"
	"encoding/json"
	"fmt"
	"io/ioutil"
	"net/http"
	"strconv"
	"strings"

	v1 "k8s.io/api/core/v1"
	"k8s.io/apimachinery/pkg/runtime"
	"k8s.io/kubernetes/pkg/scheduler/framework"
)

type EnergyAwareFilter struct {
	handle framework.Handle
}

var _ framework.FilterPlugin = &EnergyAwareFilter{}

const (
	// Name of the plugin
	Name = "EnergyAwareFilter"
)

func (e *EnergyAwareFilter) Name() string {
	return Name
}

func fetchSolarPower(url string) (float64, error) {
	resp, err := http.Get(url)
	if err != nil {
		return 0, fmt.Errorf("cannot access %s: %v", url, err)
	}
	defer resp.Body.Close()

	if resp.StatusCode != http.StatusOK {
		return 0, fmt.Errorf("unexpected status code: %d", resp.StatusCode)
	}

	body, err := ioutil.ReadAll(resp.Body)
	if err != nil {
		return 0, err
	}

	var data map[string]string
	if err := json.Unmarshal(body, &data); err != nil {
		return 0, err
	}

	predictedStr, exists := data["predicted"]
	if !exists {
		return 0, fmt.Errorf("missing 'predicted' field in the response")
	}

	predictedValue, err := strconv.ParseFloat(predictedStr, 64)
	if err != nil {
		return 0, fmt.Errorf("error parsing 'predicted' value as float: %v", err)
	}

	return predictedValue, nil
}

func fetchEPDUPower(url string) (float64, error) {
	resp, err := http.Get(url)
	if err != nil {
		return 0, fmt.Errorf("cannot access %s: %v", url, err)
	}
	defer resp.Body.Close()

	if resp.StatusCode != http.StatusOK {
		return 0, fmt.Errorf("unexpected status code: %d", resp.StatusCode)
	}

	body, err := ioutil.ReadAll(resp.Body)
	if err != nil {
		return 0, err
	}

	lines := strings.Split(string(body), "\n")
	var totalPower float64
	for _, line := range lines {
		if strings.HasPrefix(line, "epdu_watts") {
			parts := strings.Fields(line)
			if len(parts) < 2 {
				return 0, fmt.Errorf("invalid metric format")
			}
			node := strings.TrimPrefix(parts[0], "epdu_watts{node=\"")
			node = strings.TrimSuffix(node, "\"}")
			if node == "compute2" || node == "compute4" || node == "compute5" || node == "compute6" || node == "compute7" || node == "compute8" {
				value, err := strconv.ParseFloat(parts[1], 64)
				if err != nil {
					return 0, err
				}
				totalPower += value
			}
		}
	}
	return totalPower, nil
}

func energyCheck() (float64, float64, bool) {
	inverterURL := "http://192.168.0.2:7000/metrics"
	epduURL := "http://192.168.0.2:5000/metrics"

	solarPower, err := fetchSolarPower(inverterURL)
	if err != nil {
		fmt.Printf("Error fetching solar power: %v\n", err)
		solarPower = 0
	}
	fmt.Printf("Solar power: %f\n", solarPower)

	epduPower, err := fetchEPDUPower(epduURL)
	if err != nil {
		fmt.Printf("Error fetching EPDU power: %v\n", err)
		epduPower = 0
	}
	fmt.Printf("EPDU power: %f\n", epduPower)

	return solarPower, epduPower, solarPower > epduPower
}

func fetchExceedanceProbability(servicesID string) (float64, error) {
	url := fmt.Sprintf("http://192.168.0.2:6186/%s", servicesID)
	resp, err := http.Get(url)
	if err != nil {
		return 0, fmt.Errorf("cannot access %s: %v", url, err)
	}
	defer resp.Body.Close()

	if resp.StatusCode != http.StatusOK {
		return 0, fmt.Errorf("unexpected status code: %d", resp.StatusCode)
	}

	body, err := ioutil.ReadAll(resp.Body)
	if err != nil {
		return 0, err
	}

	var data map[string]interface{}
	if err := json.Unmarshal(body, &data); err != nil {
		return 0, err
	}

	probability, exists := data["exceedance_probability_cpu_request"].(float64)
	if !exists {
		return 0, fmt.Errorf("missing exceedance_probability_cpu_request in the response")
	}

	return probability, nil
}

func (e *EnergyAwareFilter) Filter(ctx context.Context, cycleState *framework.CycleState, pod *v1.Pod, nodeInfo *framework.NodeInfo) *framework.Status {
	// Check current energy status
	solarPower, epduPower, energySufficient := energyCheck()

	fmt.Printf("Solar Power: %f, EPDU Power: %f, Energy Sufficient: %v\n", solarPower, epduPower, energySufficient)

	if !energySufficient {
		// Green energy insufficient, directly return success
		return framework.NewStatus(framework.Success, "")
	}

	servicesID := pod.Labels["servicesID"]
	if servicesID == "" {
		return framework.NewStatus(framework.Unschedulable, "servicesID label is missing")
	}

	exceedanceProbability, err := fetchExceedanceProbability(servicesID)
	if err != nil {
		return framework.NewStatus(framework.Error, fmt.Sprintf("Error fetching exceedance probability: %v", err))
	}
	fmt.Printf("Exceedance Probability: %f\n", exceedanceProbability)

	if exceedanceProbability <= 0.001 {
		// Probability less than or equal to 0.001, use request-based scheduling
		return framework.NewStatus(framework.Success, "")
	} else if exceedanceProbability > 0.01 {
		// Probability greater than 0.01, use limit-based scheduling
		podLimits := computePodLimits(pod)
		if exceedsLimits(podLimits, nodeInfo) {
			return framework.NewStatus(framework.Unschedulable, fmt.Sprintf("Node %s does not have enough resources", nodeInfo.Node().Name))
		}
		return framework.NewStatus(framework.Success, "")
	} else {
		// Probability between 0.001 and 0.01, adjust scheduling based on probability range
		adjustedRequest := adjustRequestBasedOnProbability(exceedanceProbability, pod)
		fmt.Printf("Adjusted CPU Request: %dm\n", adjustedRequest.MilliCPU)
		fmt.Printf("Adjusted Memory Request: %dMi\n", adjustedRequest.Memory/1024/1024) // Convert from bytes to Mi
		if exceedsAdjustedRequest(adjustedRequest, nodeInfo) {
			return framework.NewStatus(framework.Unschedulable, fmt.Sprintf("Node %s does not have enough resources", nodeInfo.Node().Name))
		}
		return framework.NewStatus(framework.Success, "")
	}
}

func adjustRequestBasedOnProbability(probability float64, pod *v1.Pod) framework.Resource {
	// Calculate the adjusted request based on the probability
	var adjustedRequest framework.Resource
	for _, container := range pod.Spec.Containers {
		if container.Resources.Requests != nil {
			requests := container.Resources.Requests
			limits := container.Resources.Limits
			if requests.Cpu().MilliValue() >= 0 && limits.Cpu().MilliValue() > 0 {
				requestIncrement := (limits.Cpu().MilliValue() - requests.Cpu().MilliValue()) / 10
				requestStep := int((probability - 0.001) / 0.0009)
				adjustedRequest.MilliCPU += requests.Cpu().MilliValue() + int64(requestStep)*requestIncrement
			}
			if requests.Memory().Value() >= 0 && limits.Memory().Value() > 0 {
				memoryIncrement := (limits.Memory().Value() - requests.Memory().Value()) / 10
				memoryStep := int((probability - 0.001) / 0.0009)
				adjustedRequest.Memory += requests.Memory().Value() + int64(memoryStep)*memoryIncrement
			}
		}
	}
	fmt.Printf("Requests CPU: %dm, Memory: %dMi\n", adjustedRequest.MilliCPU, adjustedRequest.Memory/1024/1024) // Convert from bytes to Mi
	return adjustedRequest
}

func exceedsAdjustedRequest(adjustedRequest framework.Resource, nodeInfo *framework.NodeInfo) bool {
	nodeAvailableLimits := computeNodeAvailableLimits(nodeInfo)
	if adjustedRequest.Memory > nodeAvailableLimits.Memory {
		return true
	}
	if adjustedRequest.MilliCPU > nodeAvailableLimits.MilliCPU {
		return true
	}
	return false
}

// calculate pod limit computePodLimits
func computePodLimits(pod *v1.Pod) framework.Resource {
	var limits framework.Resource
	for _, container := range pod.Spec.Containers {
		if container.Resources.Limits != nil {
			limits.Memory += container.Resources.Limits.Memory().Value()
			limits.MilliCPU += container.Resources.Limits.Cpu().MilliValue()
		}
	}
	return limits
}

// computeNodeAvailableLimits calculates the available resource limits of a node
func computeNodeAvailableLimits(nodeInfo *framework.NodeInfo) framework.Resource {
	totalLimits := nodeInfo.Allocatable
	usedLimits := framework.Resource{}

	for _, pod := range nodeInfo.Pods {
		podSpec := pod.Pod.Spec
		for _, container := range podSpec.Containers {
			if container.Resources.Limits != nil {
				usedLimits.Memory += container.Resources.Limits.Memory().Value()
				usedLimits.MilliCPU += container.Resources.Limits.Cpu().MilliValue()
			}
		}
	}

	availableLimits := framework.Resource{
		Memory:   totalLimits.Memory - usedLimits.Memory,
		MilliCPU: totalLimits.MilliCPU - usedLimits.MilliCPU,
	}

	return availableLimits
}

func exceedsLimits(podLimits framework.Resource, nodeInfo *framework.NodeInfo) bool {
	nodeAvailableLimits := computeNodeAvailableLimits(nodeInfo)
	if podLimits.Memory > nodeAvailableLimits.Memory {
		return true
	}
	if podLimits.MilliCPU > nodeAvailableLimits.MilliCPU {
		return true
	}
	return false
}

// New EnergyAwareFilter plugin object
func New(_ context.Context, _ runtime.Object, handle framework.Handle) (framework.Plugin, error) {
	return &EnergyAwareFilter{
		handle: handle,
	}, nil
}
