# change pod name var
pod_name = "279253711324"  # Example pod name

# log path
log_file = "/Users/suenyvan/Desktop/pa/pendingtime/sun15MinSchedulersessionCut.log"

def extract_time(log_line):
    """从日志行中提取时间部分"""
    try:
        timestamp = log_line.split(" ")[1]  # cut time
        return timestamp
    except Exception as e:
        print(f"Error extracting time: {e}")
        return None

def process_logs(log_file, pod_name):
    pending_start_time = None
    log_entries = []
    found_success_first = False
    found_any_pending = False

    with open(log_file, mode='r', encoding='utf-8') as file:
        # read log line by line
        for log_line in file:
            # check match "Unable to schedule pod" 
            if f'Unable to schedule pod; no fit; waiting" pod="default/{pod_name}" err=' in log_line:
                found_any_pending = True  # find any pending
                if pending_start_time is None:
                    pending_start_time = extract_time(log_line)
                found_success_first = False  # restart
            
            # check "Successfully bound pod" 
            if f'Successfully bound pod to node" pod="default/{pod_name}" node=' in log_line:
                pending_end_time = extract_time(log_line)
                if pending_start_time:
                    log_entries.append((pending_start_time, pending_end_time))
                    pending_start_time = None  # reset pending status and check next pending
                found_success_first = False  # keep going next 
                
    # if pending status in the end
    if pending_start_time:
        print(f"Pod {pod_name} 仍在 pending，未找到绑定记录，pending 开始时间: {pending_start_time}")
        log_entries.append((pending_start_time, None))
    
    # if peding equsl 0
    if not found_any_pending and found_success_first:
        print(f"Pod {pod_name} 从头到尾都没有 pending，pending 时间为 0")

    return log_entries

# fix logs
pending_times = process_logs(log_file, pod_name)

# display pending time
for start, end in pending_times:
    if start and end:
        print(f"Pod {pod_name} pending 时间: {start} 到 {end}")
    elif start:
        print(f"Pod {pod_name} 从 {start} 开始 pending，直到END")
    else:
        print(f"Pod {pod_name} 直接成功绑定于 {end}")
