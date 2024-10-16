# -*- coding: utf-8 -*-
from flask import Flask, jsonify
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import LSTM, Dense, Input
from sklearn.ensemble import RandomForestRegressor
import os

app = Flask(__name__)

# 加载数据
data = pd.read_csv('cpu_MS_1439.csv')

# 数据预处理
scaler = MinMaxScaler(feature_range=(0, 1))
data_scaled = scaler.fit_transform(data['cpu_utilization'].values.reshape(-1, 1))

# 创建训练数据集
def create_dataset(dataset, time_step=1):
    X, y = [], []
    for i in range(len(dataset) - time_step - 1):
        a = dataset[i:(i + time_step), 0]
        X.append(a)
        y.append(dataset[i + time_step, 0])
    return np.array(X), np.array(y)

time_step = 100
X, y = create_dataset(data_scaled, time_step)

# 拆分数据集
train_size = int(len(X) * 0.8)
X_train, X_test = X[0:train_size], X[train_size:len(X)]
y_train, y_test = y[0:train_size], y[train_size:len(y)]

# Reshape input to be [samples, time steps, features]
X_train = X_train.reshape(X_train.shape[0], X_train.shape[1], 1)
X_test = X_test.reshape(X_test.shape[0], X_test.shape[1], 1)

# 检查模型文件是否存在
model_path = 'lstm_model.keras'

if not os.path.exists(model_path):
    # 构建 LSTM 模型
    model = Sequential()
    model.add(Input(shape=(time_step, 1)))
    model.add(LSTM(50, return_sequences=True))
    model.add(LSTM(50, return_sequences=False))
    model.add(Dense(1))
    model.compile(optimizer='adam', loss='mean_squared_error')

    # 训练模型
    model.fit(X_train, y_train, epochs=10, batch_size=64, validation_data=(X_test, y_test), verbose=1)

    # 保存模型
    model.save(model_path)

# 功耗数据
load_levels = [0, 0.125, 0.25, 0.375, 0.5, 0.625, 0.75, 0.875, 1]
power_data = [
    [115, 195, 230, 254, 298, 304, 314, 327, 337],
    [116, 195, 230, 253, 295, 300, 313, 329, 342],
    [115, 194, 229, 254, 298, 308, 312, 328, 341],
    [115, 195, 229, 253, 295, 306, 318, 327, 345],
    [115, 194, 230, 254, 229, 306, 314, 331, 341]
]

# 计算每个负载水平的平均功耗
average_power = [np.mean([row[i] for row in power_data]) for i in range(len(load_levels))]

# 训练随机森林模型
rf_model = RandomForestRegressor(n_estimators=100)
rf_model.fit(np.array(load_levels).reshape(-1, 1), average_power)

# 预测下一个值的函数
def predict_next_value(model, data, scaler, time_step):
    start_index = np.random.randint(0, len(data) - time_step)
    last_sequence = data[start_index:start_index + time_step]
    last_sequence = last_sequence.reshape((1, time_step, 1))
    next_value = model.predict(last_sequence)
    return scaler.inverse_transform(next_value)[0, 0]

@app.route('/apache', methods=['GET'])
def apache():
    # 加载已保存的模型
    model = load_model(model_path)

    # 每次请求时重新加载数据并进行预测
    data = pd.read_csv('cpu_MS_1439.csv')
    data_scaled = scaler.fit_transform(data['cpu_utilization'].values.reshape(-1, 1))
    predicted_load = predict_next_value(model, data_scaled, scaler, time_step).astype(float)

    # 查找最近的负载水平
    closest_load = min(load_levels, key=lambda x: abs(x - predicted_load))
    average_load_power = average_power[load_levels.index(closest_load)]

    # 使用随机森林模型预测功耗
    predicted_power = rf_model.predict([[predicted_load]]).astype(float)

    result = {
        'predicted_load': predicted_load,
        'predicted_power': predicted_power[0],
        'average_power': average_load_power
    }
    return jsonify(result)

# 启动 Flask 应用
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=12000)
