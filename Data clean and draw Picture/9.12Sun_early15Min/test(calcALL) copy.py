from datetime import timedelta
from datetime import datetime

# 你需要分析的所有 pod 名字
pod_names = [
    "300543077456", "299996111841", "298867645323", "298311908301",
    "286904951031", "286898147618", "286893948098", "286860850513",
    "286707440750", "286501394514", "285756932049", "285651484130",
    "285606169490", "284994285376", "279253711324", "276205682817",
    "276205609451"
]

# 读取日志的 .log 文件路径
log_file = "/Users/suenyvan/Desktop/DataSet2/9.12Sun_early15Min/SchedulersessionCut2.log"

def extract_time(log_line):
    """从日志行中提取时间部分"""
    try:
        timestamp = log_line.split(" ")[1]  # 提取日志中的时间部分
        return timestamp
    except Exception as e:
        print(f"Error extracting time: {e}")
        return None

def calculate_time_difference(start_time, end_time):
    """计算两个时间字符串之间的秒数差，并处理跨天情况"""
    time_format = "%H:%M:%S.%f"
    start_dt = datetime.strptime(start_time, time_format)
    end_dt = datetime.strptime(end_time, time_format)

    # 处理跨天情况：如果 end_dt < start_dt，说明跨天了
    if end_dt < start_dt:
        end_dt += timedelta(days=1)  # 加一天

    return (end_dt - start_dt).total_seconds()

def process_logs(log_file, pod_name, end_time_for_last_pending):
    pending_start_time = None
    log_entries = []
    total_pending_time = 0  # 总的 pending 时间（秒）

    with open(log_file, mode='r', encoding='utf-8') as file:
        # 逐行读取日志文件
        for log_line in file:
            # 检查是否匹配到 "Unable to schedule pod" 提示
            if f'Unable to schedule pod; no fit; waiting" pod="default/{pod_name}" err=' in log_line:
                if pending_start_time is None:
                    pending_start_time = extract_time(log_line)
            
            # 检查是否匹配到 "Successfully bound pod" 提示
            if f'Successfully bound pod to node" pod="default/{pod_name}" node=' in log_line:
                pending_end_time = extract_time(log_line)
                if pending_start_time:
                    log_entries.append((pending_start_time, pending_end_time))
                    total_pending_time += calculate_time_difference(pending_start_time, pending_end_time)
                    pending_start_time = None  # 重置 pending 状态以处理下一段 pending

    # 如果到日志结尾仍然在 pending 状态
    if pending_start_time:
        log_entries.append((pending_start_time, end_time_for_last_pending))
        total_pending_time += calculate_time_difference(pending_start_time, end_time_for_last_pending)
    
    return log_entries, total_pending_time

# 设置END时间
end_time_for_last_pending = "10:09:25.896353"

# 用于记录所有 pod 的总 pending 时间
total_pending_time_all_pods = 0

# 处理每个 pod 并计算总的 pending 时间
for pod_name in pod_names:
    pending_times, total_pending_time = process_logs(log_file, pod_name, end_time_for_last_pending)
    
    # 输出每个 pod 的 pending 时间段
    #for start, end in pending_times:
        #print(f"Pod {pod_name} pending 时间: {start} 到 {end}")
    
    # 输出每个 pod 的总 pending 时间并累加
    total_pending_minutes = total_pending_time / 60
    print(f"Pod {pod_name} 总的 pending 时间: {total_pending_minutes:.2f} 分钟")
    total_pending_time_all_pods += total_pending_time

# 输出所有 pod 的总 pending 时间
total_pending_minutes_all_pods = total_pending_time_all_pods / 60
print(f"所有 pod 总的 pending 时间: {total_pending_minutes_all_pods:.2f} 分钟")
