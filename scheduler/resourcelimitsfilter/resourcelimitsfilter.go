package resourcelimitsfilter

import (
	"context"
	"fmt"

	v1 "k8s.io/api/core/v1"
	"k8s.io/apimachinery/pkg/runtime"
	"k8s.io/kubernetes/pkg/scheduler/framework"
)

type ResourceLimitsFilter struct {
	handle framework.Handle
}

var _ framework.FilterPlugin = &ResourceLimitsFilter{}

const (
	// Name of the plugin
	Name = "ResourceLimitsFilter"
)

func (r *ResourceLimitsFilter) Name() string {
	return Name
}

func (r *ResourceLimitsFilter) Filter(ctx context.Context, cycleState *framework.CycleState, pod *v1.Pod, nodeInfo *framework.NodeInfo) *framework.Status {
	// 计算 Pod 的 limits
	podLimits := computePodLimits(pod)

	// 计算节点的可用资源
	nodeAvailableLimits := computeNodeAvailableLimits(nodeInfo)

	// 检查节点的可用资源是否足够满足 Pod 的 limits
	if podLimits.Memory > nodeAvailableLimits.Memory || podLimits.MilliCPU > nodeAvailableLimits.MilliCPU {
		return framework.NewStatus(framework.Unschedulable, fmt.Sprintf("Node %s does not have enough resources", nodeInfo.Node().Name))
	}

	// 如果节点资源足够，则返回 Success
	return framework.NewStatus(framework.Success, "")
}

// computePodLimits 计算 Pod 的资源 limits
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

// computeNodeAvailableLimits 计算节点的可用资源 limits
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

// New 创建一个新的 ResourceLimitsFilter 插件对象
func New(_ context.Context, _ runtime.Object, handle framework.Handle) (framework.Plugin, error) {
	return &ResourceLimitsFilter{
		handle: handle,
	}, nil
}
