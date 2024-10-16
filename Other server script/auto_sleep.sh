#!/bin/bash

# Global Var
#GREEN_ENERGY_URL="http://192.168.0.2:6185/metrics"
GREEN_ENERGY_URL="http://192.168.0.2:7000/metrics"
SERVER_ENERGY_URL="http://192.168.0.2:5000/metrics"
COMPUTE_NODES=("compute2" "compute4" "compute5" "compute6" "compute7" "compute8")
SHUTDOWN_ORDER=("compute7" "compute6" "compute5" "compute2")
CHECK_INTERVAL=30 # Every X Sec to check energy URL
CONSECUTIVE_CHECKS=0
THRESHOLD=2
LOG_FILE="sensitive_operations_log.csv"
EXCLUDED_NAMESPACES=("knative-eventing" "knative-serving" "kourier-system" "kube-node-lease" "kube-public" "kube-system" "scheduler-plugins")
declare -A MAC_ADDRESSES=(
    ["compute2"]="00:26:b9:7d:d1:d1"
    ["compute4"]="b8:ac:6f:8b:b4:36"
    ["compute5"]="bc:30:5b:e3:fc:7b"
    ["compute6"]="00:26:b9:74:72:6d"
    ["compute7"]="b8:ac:6f:94:3f:bc"
)

# Initialize the log file
if [ ! -f $LOG_FILE ]; then
    echo "timestamp,operation" > $LOG_FILE
fi

# Function to log sensitive operations
log_operation() {
    local operation="$1"
    local timestamp=$(date "+%Y-%m-%d %H:%M:%S")
    echo "$timestamp,$operation" >> $LOG_FILE
}

# Get green energy
get_green_energy() {
    #curl -s $GREEN_ENERGY_URL | jq -r '.value'
    curl -s $GREEN_ENERGY_URL | jq -r '.predicted'
}

# Get server power consumption
get_server_energy() {
    curl -s $SERVER_ENERGY_URL
}

# Calculate compute 4 5 6 7 8 total power consumption
calculate_total_power() {
    local server_energy="$1"
    local total_power=0
    for node in "${COMPUTE_NODES[@]}"; do
        local node_power=$(echo "$server_energy" | grep "epdu_watts{node=\"$node\"}" | awk '{print $2}')
        total_power=$(echo "$total_power + $node_power" | bc)
    done
    echo "$total_power"
}

# Check node if have a pod
check_node_for_pods() {
    local node="$1"
    local all_namespaces=$(kubectl get ns -o jsonpath='{.items[*].metadata.name}')
    for ns in $all_namespaces; do
        if [[ ! " ${EXCLUDED_NAMESPACES[@]} " =~ " ${ns} " ]]; then
            local pods=$(kubectl get pods -n "$ns" -o jsonpath="{.items[?(@.spec.nodeName=='$node')].metadata.name}")
            if [ -n "$pods" ]; then
                return 0 # find Pod, return 0
            fi
        fi
    done
    return 1 # dont find Pod, return 1
}

# Check node Networking Ping available and Kubernetes node if Ready
check_node_status() {
    local node="$1"
    ping -c 1 $node > /dev/null 2>&1
    if [ $? -ne 0 ]; then
        return 1 # Node cannot be accessed, return 1
    fi
    local node_status=$(kubectl get nodes $node -o jsonpath='{.status.conditions[?(@.type=="Ready")].status}')
    if [ "$node_status" == "True" ]; then
        return 0 # Node status is Ready, return 0
    else
        return 1 # Node status is NotReady, return 1
    fi
}

# Check and start NotReady node (Wake up)
wake_up_node() {
    local node="$1"
    local mac="${MAC_ADDRESSES[$node]}"
    if [ -n "$mac" ]; then
        echo "Wake Up $node..."
        log_operation "Wake Up $node"
        sudo etherwake -i eno2 $mac
    else
        echo "Cannot find $node MAC address"
    fi
}

# main
while true; do
    GREEN_ENERGY=$(get_green_energy)
    SERVER_ENERGY=$(get_server_energy)
    TOTAL_POWER=$(calculate_total_power "$SERVER_ENERGY")

    echo "Total_Consumption: $TOTAL_POWER"
    echo "Green_Energy: $GREEN_ENERGY"

    # Check for nodes in Ready,SchedulingDisabled state and uncordon them
    for node in "${COMPUTE_NODES[@]}"; do
        if [ "$node" != "compute8" ]; then
            node_status=$(kubectl get nodes "$node" -o jsonpath='{.status.conditions[?(@.type=="Ready")].status}')
            scheduling_disabled=$(kubectl get nodes "$node" -o jsonpath='{.spec.unschedulable}')
            if [[ "$node_status" == "True" && "$scheduling_disabled" == "true" ]]; then
                echo "Uncordoning $node..."
                log_operation "Uncordon $node"
                kubectl uncordon "$node"
            fi
        fi
    done


    if (( $(echo "$GREEN_ENERGY < $TOTAL_POWER" | bc -l) )); then
        CONSECUTIVE_CHECKS=$((CONSECUTIVE_CHECKS + 1))
        echo "Green energy is insufficient, continuous inspection times: $CONSECUTIVE_CHECKS"

        if [ "$CONSECUTIVE_CHECKS" -ge "$THRESHOLD" ]; then
            echo "$THRESHOLD times Green energy is insufficient, start draining nodes."

            for node in "${SHUTDOWN_ORDER[@]}"; do
                node_status=$(kubectl get nodes $node -o jsonpath='{.status.conditions[?(@.type=="Ready")].status}')
                if [ "$node_status" == "True" ]; then
                    echo "Draining and shutting down $node..."
                    log_operation "Drain $node"
                    kubectl drain "$node" --force --ignore-daemonsets --delete-emptydir-data
                    sleep 100 # Wait for pods to be evicted

                    check_node_for_pods "$node"
                    if [ $? -ne 0 ]; then
                        log_operation "Shutdown $node"
                        ssh stack@$node 'sudo shutdown -h now'
                        sleep 100 # Wait for node shutdown
                    fi
                    break
                fi
            done

            # Check URL times
            CONSECUTIVE_CHECKS=0
        fi
    else
        echo "Green energy is sufficient, Start Server and recovery."
        #log_operation "Close the Descheduler"
        #kubectl delete -f ~/descheduler/kubernetes/cronjob/cronjob.yaml
        CONSECUTIVE_CHECKS=0

        # Check for nodes in Ready,SchedulingDisabled state and uncordon them
        for node in "${COMPUTE_NODES[@]}"; do
            if [ "$node" != "compute8" ]; then
                node_status=$(kubectl get nodes "$node" -o jsonpath='{.status.conditions[?(@.type=="Ready")].status}')
                scheduling_disabled=$(kubectl get nodes "$node" -o jsonpath='{.spec.unschedulable}')
                if [[ "$node_status" == "True" && "$scheduling_disabled" == "true" ]]; then
                    echo "Uncordoning $node..."
                    log_operation "Uncordon $node"
                    kubectl uncordon "$node"
                fi
            fi
        done

        # Check if green energy is enough to start a node or not
        if (( $(echo "$GREEN_ENERGY >= $TOTAL_POWER + 200" | bc -l) )); then
            echo "Green energy is sufficient, check if there are any NotReady nodes..."
            for node in "${COMPUTE_NODES[@]}"; do
                if [ "$node" != "compute8" ]; then
                    ping -c 1 $node > /dev/null 2>&1
                    if [ $? -ne 0 ]; then
                        node_status=$(kubectl get nodes $node -o jsonpath='{.status.conditions[?(@.type=="Ready")].status}')
                        if [ "$node_status" != "True" ]; then
                            wake_up_node "$node"
                            sleep 400 # wait
                            break
                        fi
                    fi
                fi
            done
        fi
    fi

    # wait times
    sleep "$CHECK_INTERVAL"
done

