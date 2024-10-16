import numpy as np
from tensorflow.keras.models import load_model
import pandas as pd

# 加载已经训练好的模型
model = load_model('/Users/suenyvan/Desktop/DataSet2/solarPrediction/date/solar_radiation_lstm_model.h5')  # 替换为你的模型路径

# 读取数据
df = pd.read_csv('/Users/suenyvan/Desktop/DataSet2/solarPrediction/date/sorted_solar_data.csv')

# 转换日期格式，并抽取月和日作为特征
df['date'] = pd.to_datetime(df[['year', 'month', 'day']])
df['month'] = df['date'].dt.month
df['day'] = df['date'].dt.day

# 准备预测数据
month = 8  # 替换为你想要预测的月份
day = 20  # 替换为你想要预测的日期
historical_data = df[(df['month'] == month) & (df['day'] == day)]

if len(historical_data) > 0:
    # 获取该日期的所有历史数据
    hourly_data = historical_data.iloc[:, 3:27].values

    # 准备预测数据
    if len(hourly_data) > 0:
        X_hourly = np.array(hourly_data, dtype=np.float32).reshape(-1, 24, 1)
        X_date = np.array([[month, day]] * len(hourly_data), dtype=np.int32)  # 为每一个样本重复日期特征

        # 使用模型进行预测
        y_pred = model.predict([X_date, X_hourly])

        # 打印预测结果
        print(f'预测结果: {y_pred}')
    else:
        print('没有找到该日期的历史数据')
else:
    print('输入的月份或日期无效')
