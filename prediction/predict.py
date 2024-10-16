import numpy as np
import pandas as pd
from tensorflow.keras.models import load_model

# 加载模型
model = load_model('/Users/suenyvan/Desktop/DataSet2/solarPrediction/solar_radiation_cnn_model.h5')

# CSV文件路径
file_path = '/Users/suenyvan/Desktop/DataSet2/solarPrediction/solar_data_normalized_cleaned.csv'

# 指定要读取的行数
start_row = 6547  # 开始行
end_row = 6553    # 结束行

# 从CSV文件读取数据
df = pd.read_csv(file_path, skiprows=range(1, start_row), nrows=end_row - start_row + 1)

# 选择需要的时间段列
columns_needed = [str(i) for i in range(12, 24)] + [str(i) for i in range(0, 12)]
data = df[columns_needed].values

# 重塑数据形状为模型输入形状 (samples, time_steps, features)
data = data.reshape((1, 7, 24))  # 1个样本，7天，24小时数据

# 进行预测
predicted_values = model.predict(data)

# 显示预测结果，不使用科学计数法
print("预测的下一天的24小时辐射值：")
np.set_printoptions(suppress=True)  # 禁用科学计数法
print(predicted_values)
