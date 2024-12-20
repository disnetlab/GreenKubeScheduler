import csv
import requests
import time
from datetime import datetime

def fetch_metrics_5000(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        metrics = response.text
        return metrics
    except requests.exceptions.RequestException as e:
        print(f"Error fetching metrics from {url}: {e}")
        return None

def calculate_total_power(metrics, nodes):
    total_power = 0
    for line in metrics.split('\n'):
        if line.startswith('epdu_watts'):
            parts = line.split()
            node = parts[0].split('=')[1].strip('{}"')
            if node in nodes:
                power = float(parts[1])
                total_power += power
    return total_power

def fetch_metrics_6185(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return data
    except requests.exceptions.RequestException as e:
        print(f"Error fetching metrics from {url}: {e}")
        return None

def write_to_csv(file_name, data):
    with open(file_name, 'a', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(data)

def main():
    url_5000 = 'http://127.0.0.1:5000/metrics'
    url_6185 = 'http://127.0.0.1:7000/metrics'
    nodes = ['compute2', 'compute4', 'compute5', 'compute6', 'compute7', 'compute8']
    csv_file = 'metrics_log.csv'

    # 检查文件是否存在，如果不存在则写入 CSV 文件头
    try:
        with open(csv_file, 'x', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow(['time', 'epdu_total_power', 'real_power', 'api_time'])
    except FileExistsError:
        pass

    while True:
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        metrics_5000 = fetch_metrics_5000(url_5000)
        if metrics_5000:
            total_power = calculate_total_power(metrics_5000, nodes)
        else:
            total_power = 'N/A'

        metrics_6185 = fetch_metrics_6185(url_6185)
        real_power = metrics_6185.get('real', 'N/A') if metrics_6185 else 'N/A'  # 选择并保留'real'字段的值
        api_time = metrics_6185.get('time', 'N/A') if metrics_6185 else 'N/A'  # 获取API时间

        data_row = [current_time, total_power, real_power, api_time]
        write_to_csv(csv_file, data_row)

        time.sleep(5)

if __name__ == '__main__':
    main()

