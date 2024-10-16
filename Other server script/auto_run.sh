#!/bin/bash

# 定义Pod名称数组
pods=(
    "286501394514"
    "276205609451"
    "276205682817"
    "279253711324"
    "284994285376"
    "285606169490"
    "285651484130"
    "285756932049"
    "286707440750"
    "286860850513"
    "286893948098"
    "286898147618"
    "286904951031"
    "298311908301"
    "298867645323"
    "299996111841"
    "300543077456"
)
# 定义Pod YAML文件后缀
yaml_suffix="-Pod.yaml"

# 函数：运行Python脚本修改运行时间
run_python_script() {
    python3 auto_changeRunTime.py
}

# 无限循环
while true; do
    # 获取当前所有Pod的状态
    pod_status=$(kubectl get pods --no-headers)

    for pod in "${pods[@]}"; do
        # 检查Pod是否存在
        if ! echo "$pod_status" | grep -q "^$pod "; then
            # Pod不存在，运行Python脚本修改运行时间
            run_python_script
            sleep 1
            # 应用YAML文件
            kubectl apply -f "$pod$yaml_suffix"
        else
            # 获取Pod状态
            status=$(echo "$pod_status" | grep "^$pod " | awk '{print $3}')
            if [ "$status" == "Completed" ]; then
                # Pod已完成，删除Pod
                kubectl delete pod "$pod"
                
                # 运行Python脚本修改运行时间
                run_python_script
                sleep 1
                # 重新应用修改后的YAML文件
                kubectl apply -f "$pod$yaml_suffix"
            fi
        fi
    done
    
    # 等待5秒
    sleep 5
done
