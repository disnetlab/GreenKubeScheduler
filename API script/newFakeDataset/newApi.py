from flask import Flask, jsonify
import csv
import threading
import time

app = Flask(__name__)

# 读取csv文件
with open('/home/stack/newFakeDataset/data.csv', 'r') as file:
    reader = csv.reader(file)
    next(reader)
    data = list(reader)

counter = 0

def update_metrics():
    global counter
    while True:
        time.sleep(75)  # 每900秒（15分钟）更新一次
        counter = (counter + 1) % len(data)

@app.route('/metrics', methods=['GET'])
def get_metrics():
    row = data[counter]
    #next_row = data[(counter + 1) % len(data)]  # 用模运算来处理循环的情况
    #next_index = (counter + 5) % len(data)
    next_index = (counter + 3) % len(data)
    next_row = data[next_index]  # 获取后五行的数据next_index = (counter + 5) % len(data)
    #next_row = data[next_index]  # 获取后五行的数据
    return jsonify({
        'time': row[0],
        'real': row[1],
        'predicted': next_row[2]
        #'predicted': row[2]
    })
if __name__ == '__main__':
    # 启动定时任务线程
    threading.Thread(target=update_metrics, daemon=True).start()
    app.run(host='0.0.0.0', port=7000)

