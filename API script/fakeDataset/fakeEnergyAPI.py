"""
from flask import Flask, jsonify
import csv

app = Flask(__name__)

# read csv
with open('ganglia-metrics-update.csv', 'r') as file:
    reader = csv.reader(file)
    data = list(reader)


counter = 0
@app.route('/metrics', methods=['GET'])
def get_metrics():
    global counter
    row = data[counter]
    counter = (counter + 1) % len(data)
    return jsonify({
        'timestamp': row[0],
        'value': row[1]
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6185)
"""


from flask import Flask, jsonify
import csv
import threading
import time

app = Flask(__name__)

# 读取csv文件
with open('ganglia-metrics-update8.9.csv', 'r') as file:
#with open('ganglia-metrics-update-alwaysEnough.csv', 'r') as file:
    reader = csv.reader(file)
    data = list(reader)

counter = 0

def update_metrics():
    global counter
    while True:
        time.sleep(150)  # 每150秒更新一次
        counter = (counter + 1) % len(data)

@app.route('/metrics', methods=['GET'])
def get_metrics():
    row = data[counter]
    return jsonify({
        'timestamp': row[0],
        'value': row[1]
    })

if __name__ == '__main__':
    # 启动定时任务线程
    threading.Thread(target=update_metrics, daemon=True).start()
    app.run(host='0.0.0.0', port=6185)

