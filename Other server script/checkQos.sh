#!/bin/bash

# 定义要检查的 Pod 名称
PODS=("276205682817" "285651484130" "286501394514" "299996111841")

# 日志文件路径，保存为CSV格式
LOG_FILE="cpu_over_limits.csv"

# 初始化CSV文件并添加表头（如果文件不存在）
if [ ! -f "$LOG_FILE" ]; then
    echo "Timestamp,Total_CPU_Count" > "$LOG_FILE"
fi

# 开始定期检查
while true; do
    # 获取所有Pod的节点
    nodes=()
    for pod in "${PODS[@]}"; do
        node=$(kubectl get pod "$pod" -o jsonpath='{.spec.nodeName}' 2>/dev/null)
        if [ -z "$node" ]; then
            echo "Pod $pod not found or no node assigned, will retry in 30 seconds."
            sleep 30
            continue 2  # 直接跳出外层的 while 循环，等待30秒后再重新检查
        fi

        status=$(kubectl get pod "$pod" -o jsonpath='{.status.phase}' 2>/dev/null)
        if [ "$status" != "Running" ]; then
            echo "Pod $pod is in status $status, not Running, will retry in 30 seconds."
            sleep 30
            continue 2  # 直接跳出外层的 while 循环，等待30秒后再重新检查
        fi

        nodes+=("$node")
    done

    # 检查所有Pod是否在同一个节点上
    unique_nodes=($(echo "${nodes[@]}" | tr ' ' '\n' | sort -u))

    if [ ${#unique_nodes[@]} -ne 1 ]; then
        echo "Pods are not on the same node, will retry in 30 seconds."
        sleep 30
        continue  # 跳过这次循环，直接进入下一次检查
    fi

    # 如果所有 Pod 在同一个节点上，继续执行以下逻辑
    NODE="${unique_nodes[0]}"
    echo "All Pods are on node: $NODE"

    # 初始化 CPU 计数
    total_cpu=0

    # 遍历每个Pod
    for pod in "${PODS[@]}"; do
        # 获取容器名称列表
        containers=$(kubectl get pod "$pod" -o jsonpath='{.spec.containers[*].name}')
        
        # 遍历每个容器
        for container in $containers; do
            echo "Checking logs for Pod: $pod, Container: $container"
            
            # 获取容器日志中最近的 "dispatching hogs" 的 CPU 数量并累加
            cpu_count=$(kubectl logs "$pod" -c "$container" | grep "dispatching hogs" | tail -n 1 | grep -oP '(?<=dispatching hogs: )\d+')
            
            # 如果找到有效的 CPU 计数，则累加到总 CPU 中
            if [ -n "$cpu_count" ]; then
                echo "CPU count for $pod - $container: $cpu_count"
                total_cpu=$((total_cpu + cpu_count))
            else
                echo "No valid CPU count found for Pod: $pod, Container: $container"
            fi
        done
    done

    # 输出总 CPU 数量并将结果写入CSV文件
    timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    echo "$timestamp,$total_cpu" >> "$LOG_FILE"

    # 等待30秒后再次检查
    sleep 30
done

