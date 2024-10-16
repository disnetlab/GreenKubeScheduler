import numpy as np
import pandas as pd
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, ReLU

# 加载数据
data = pd.read_csv("/Users/suenyvan/Desktop/DataSet2/solarPrediction/date/sorted_solar_data.csv")

# 数据预处理，选择特定日期的所有年份数据
target_date_data = data[(data['month'] == 7) & (data['day'] == 16)]

# 选择辐射数据
radiation_data = target_date_data.iloc[:, 3:]

# 准备时间序列数据集
def create_sequences(data):
    X = []
    for i in range(len(data)-1):  # 使用除最新一年（2016）外的所有数据
        X.append(data.iloc[i].values)
    return np.array(X)

# 1990-2015为训练数据
X_train = create_sequences(radiation_data[:-1])  # 排除最后一年数据，即2016年
num_years = len(radiation_data) - 1  # 排除2016年

# 调整X_train的形状以符合LSTM输入要求
X_train = np.reshape(X_train, (X_train.shape[0], 1, 24))

# 构建LSTM模型
model = Sequential()
model.add(LSTM(50, return_sequences=True, input_shape=(1, 24)))
model.add(LSTM(50))
model.add(Dense(24))  # 预测同一天的24小时数据
model.add(ReLU())  # 确保输出非负
model.compile(optimizer='adam', loss='mean_squared_error')

# 训练模型
model.fit(X_train, X_train, epochs=20, batch_size=32, verbose=2)

# 使用2016年的数据作为输入来预测未来的数据
X_test = radiation_data.iloc[-1].values.reshape(1, 1, 24)  # 2016年数据
y_future_pred = model.predict(X_test)

# 设置打印选项，禁用科学计数法
np.set_printoptions(suppress=True)


# 打印预测结果
print("Predicted Radiation Data for Future 5/8:", y_future_pred.flatten())
