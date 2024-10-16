package energyawarescheduling

import (
	"context"
	"encoding/json"
	"fmt"
	"io/ioutil"
	"net/http"
	"strconv"
	"strings"
	"sync"
	"time"

	v1 "k8s.io/api/core/v1"
	"k8s.io/apimachinery/pkg/runtime"
	"k8s.io/kubernetes/pkg/scheduler/framework"
)

type EnergyAwareScheduling struct {
	handle framework.Handle

	mu             sync.Mutex     // 互斥锁用于保护计数器
	successCounter map[string]int // 记录每个 Pod 实际调度的次数

}

var _ framework.PermitPlugin = &EnergyAwareScheduling{}

const (
	// Name
	Name = "EnergyAwareScheduling"
)

func (e *EnergyAwareScheduling) Name() string {
	return Name
}

func fetchMetricWithTimestamp(url string) (float64, int, error) {
	resp, err := http.Get(url)
	if err != nil {
		return 0, 0, fmt.Errorf("cannot access %s: %v", url, err)
	}
	defer resp.Body.Close()

	if resp.StatusCode != http.StatusOK {
		return 0, 0, fmt.Errorf("unexpected status code: %d", resp.StatusCode)
	}

	body, err := ioutil.ReadAll(resp.Body)
	if err != nil {
		return 0, 0, err
	}

	var data map[string]string
	if err := json.Unmarshal(body, &data); err != nil {
		return 0, 0, err
	}

	predictedStr, predictedExists := data["predicted"]
	timeStr, timeExists := data["time"]
	if !predictedExists || !timeExists {
		return 0, 0, fmt.Errorf("missing expected fields in the response")
	}

	predicted, err := strconv.ParseFloat(predictedStr, 64)
	if err != nil {
		return 0, 0, err
	}

	// 提取小时数从time字段，假设格式是 "TXX:00:00+10:00"
	timeParts := strings.Split(strings.TrimPrefix(timeStr, "T"), ":")
	if len(timeParts) < 1 {
		return 0, 0, fmt.Errorf("invalid time format")
	}

	hour, err := strconv.Atoi(timeParts[0])
	if err != nil {
		return 0, 0, err
	}

	return predicted, hour, nil
}

/*
func fetchMetric(url string, metricName string) (float64, error) {
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
	var totalValue float64
	for _, line := range lines {
		if strings.HasPrefix(line, metricName) {
			parts := strings.Fields(line)
			if len(parts) < 2 {
				return 0, fmt.Errorf("invalid metric format")
			}
			value := parts[1]
			if value == "None" {
				fmt.Printf("%s: 0\n", metricName)
				totalValue += 0
			} else {
				parsedValue, err := strconv.ParseFloat(value, 64)
				if err != nil {
					return 0, err
				}
				totalValue += parsedValue
			}
		}
	}
	if totalValue == 0 {
		return 0, fmt.Errorf("metric not found")
	}
	return totalValue, nil
}
*/

func fetchMetric(url string, metricName string) (float64, error) {
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
	var totalValue float64
	for _, line := range lines {
		if strings.HasPrefix(line, metricName) {
			parts := strings.Fields(line)
			if len(parts) < 2 {
				return 0, fmt.Errorf("invalid metric format")
			}
			node := strings.TrimPrefix(parts[0], "epdu_watts{node=\"")
			node = strings.TrimSuffix(node, "\"}")
			if node == "compute2" || node == "compute4" || node == "compute5" || node == "compute6" || node == "compute7" || node == "compute8" {
				value := parts[1]
				if value == "None" {
					fmt.Printf("%s: 0\n", metricName)
					totalValue += 0
				} else {
					parsedValue, err := strconv.ParseFloat(value, 64)
					if err != nil {
						return 0, err
					}
					totalValue += parsedValue
				}
			}
		}
	}
	if totalValue == 0 {
		return 0, fmt.Errorf("metric not found")
	}
	return totalValue, nil
}

/*
func fetchPrediction(url string) (float64, float64, error) {
	resp, err := http.Get(url)
	if err != nil {
		return 0, 0, fmt.Errorf("cannot access %s: %v", url, err)
	}
	defer resp.Body.Close()

	if resp.StatusCode != http.StatusOK {
		return 0, 0, fmt.Errorf("unexpected status code: %d", resp.StatusCode)
	}

	body, err := ioutil.ReadAll(resp.Body)
	if err != nil {
		return 0, 0, err
	}

	var data map[string]float64
	if err := json.Unmarshal(body, &data); err != nil {
		return 0, 0, err
	}

	predictedPower, predictedPowerExists := data["predicted_power"]
	averagePower, averagePowerExists := data["average_power"]
	if !predictedPowerExists || !averagePowerExists {
		return 0, 0, fmt.Errorf("missing expected fields in the response")
	}

	return predictedPower, averagePower, nil
}


func checkPrediction() (bool, float64, float64) {
	// Fetch prediction data
	predictionURL := "http://203.101.228.91:12000/prediction"
	predictedPower, averagePower, err := fetchPrediction(predictionURL)
	if err != nil {
		fmt.Printf("Error fetching prediction data: %v\n", err)
		return false, predictedPower, averagePower
	}

	// Print predictedPower and averagePower
	fmt.Printf("Predicted power: %f, Average power: %f\n", predictedPower, averagePower)

	return predictedPower <= averagePower, predictedPower, averagePower
}
*/

func energyCheck() (float64, float64, bool, int) {
	inverterURL := "http://192.168.0.2:7000/metrics"
	epduURL := "http://192.168.0.2:5000/metrics"

	inverterPower, currentHour, err := fetchMetricWithTimestamp(inverterURL)
	if err != nil {
		fmt.Printf("Error fetching data from %s: %v\n", inverterURL, err)
		inverterPower = 0
	}
	fmt.Printf("Solar power: %f\n", inverterPower)

	epduPower, err := fetchMetric(epduURL, "epdu_watts")
	if err != nil {
		fmt.Printf("Error fetching data from %s: %v\n", epduURL, err)
		epduPower = 0
	}

	fmt.Printf("EPDU power: %f\n", epduPower)

	return inverterPower, epduPower, inverterPower-epduPower > 0, currentHour
}

// Permit framework
func (e *EnergyAwareScheduling) Permit(ctx context.Context, state *framework.CycleState, pod *v1.Pod, nodeName string) (*framework.Status, time.Duration) {

	if _, exists := pod.Labels["descheduler"]; exists {
		fmt.Printf("Pod has descheduler label, bypassing energy check.\n")
		return framework.NewStatus(framework.Success, ""), 0
	}

	solarPower, epduPower, energySufficient, currentHour := energyCheck()

	//use for send it to prediction
	for _, container := range pod.Spec.Containers {
		fmt.Printf("Container name: %s, Image: %s\n", container.Name, container.Image)
	}

	if energySufficient {

		// 更新成功调度次数
		e.mu.Lock()
		e.successCounter[pod.Name]++
		successCount := e.successCounter[pod.Name]
		e.mu.Unlock()
		fmt.Printf("Pod %s has been successfully scheduled %d times\n", pod.Name, successCount)

		fmt.Printf("Sufficient energy: solar power = %f, EPDU power = %f\n", solarPower, epduPower)
		return framework.NewStatus(framework.Success, ""), 0
	}

	priorityStr, exists := pod.Labels["priority"]
	if !exists {
		fmt.Printf("Priority label not found, treating as low priority.\n")
		priorityStr = "1"
	}

	priority, err := strconv.Atoi(priorityStr)
	if err != nil {
		fmt.Printf("Invalid priority value, treating as low priority: %v\n", err)
		priority = 1
	}

	fmt.Printf("Current hour: %d\n", currentHour)

	if priority >= 7 {

		// 更新成功调度次数
		e.mu.Lock()
		e.successCounter[pod.Name]++
		successCount := e.successCounter[pod.Name]
		e.mu.Unlock()
		fmt.Printf("Pod %s has been successfully scheduled %d times\n", pod.Name, successCount)

		fmt.Printf("Not enough energy! solar power = %f, EPDU power = %f\n", solarPower, epduPower)
		fmt.Printf("High priority (%d), deploying despite insufficient energy.\n", priority)
		return framework.NewStatus(framework.Success, ""), 0
	}

	if priority >= 4 && priority <= 6 {
		fmt.Printf("Medium priority (%d)", priority)
		if currentHour >= 22 || currentHour <= 8 {

			// 更新成功调度次数
			e.mu.Lock()
			e.successCounter[pod.Name]++
			successCount := e.successCounter[pod.Name]
			e.mu.Unlock()
			fmt.Printf("Pod %s has been successfully scheduled %d times\n", pod.Name, successCount)

			fmt.Printf("Medium priority (%d) and cheap hours, deploying pod. \n", priority)
			return framework.NewStatus(framework.Success, ""), 0
		} else {

			fmt.Printf("Medium priority (%d) and expensive hours, waiting.... \n", priority)
			return framework.NewStatus(framework.Wait, "Insufficient energy or peak hours"), 2 * time.Second
		}
	}

	//predictionSatisfied, predictedPower, averagePower := checkPrediction()
	//if predictionSatisfied {
	//	fmt.Printf("Predicted power (%f) is less than or equal to average power (%f), deploying.\n", predictedPower, averagePower)
	//	return framework.NewStatus(framework.Success, ""), 0
	//}

	fmt.Printf("Not enough energy! solar power = %f, EPDU power = %f\n", solarPower, epduPower)
	fmt.Printf("Low priority (%d), waiting for energy to recover.\n", priority)
	return framework.NewStatus(framework.Wait, "Insufficient energy"), 2 * time.Second
}

// New EnergyAwareScheduling plugin object
func New(_ context.Context, _ runtime.Object, handle framework.Handle) (framework.Plugin, error) {
	return &EnergyAwareScheduling{handle: handle,
		successCounter: make(map[string]int),
	}, nil
}
