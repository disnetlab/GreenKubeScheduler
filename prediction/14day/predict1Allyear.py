import numpy as np
import pandas as pd
from tensorflow.keras.models import load_model

np.set_printoptions(suppress=True, precision=6)

# 加载模型
model = load_model('/Users/suenyvan/Desktop/DataSet2/solarPrediction/14day/solar_radiation_cnn_model.h5')

# CSV文件路径
file_path = '/Users/suenyvan/Desktop/DataSet2/solarPrediction/14day/solar_data_normalized_cleaned.csv'

# 读取CSV文件的全部数据
df = pd.read_csv(file_path)

# 初始化一个空列表来保存所有的预测结果
all_predictions = []

# 定义开始和结束行对应2016年12月24日到2017年12月31日的预测周期
start_row = 6426
end_row = 6793

# 循环遍历每一天进行预测
for i in range(start_row, end_row - 13):  # 减13确保有14天数据用于预测
    # 提取14天的数据
    data = df.iloc[i:i+14, 3:].values  # 提取14天数据，确保这里的列选择与模型训练时保持一致

    # 检查数据是否完整
    if data.shape == (14, 24):  # 确保每天都有24小时的数据
        # 重塑数据形状为模型输入形状 (1, 14, 24)
        data = data.reshape((1, 14, 24))

        # 进行预测
        predicted_values = model.predict(data)

        # 将预测结果保存到列表
        all_predictions.append(predicted_values.flatten())  # 使用flatten将二维数组转为一维
    else:
        # 打印出错的行信息
        print(f"Data shape mismatch at index range {i}-{i+14}. Expected (14, 24), got {data.shape}")


# 将所有预测结果转换为NumPy数组方便后续处理


all_predictions = np.array(all_predictions)

np.set_printoptions(suppress=True, precision=6)

# 可选: 将预测结果保存到CSV文件
np.savetxt('/Users/suenyvan/Desktop/DataSet2/solarPrediction/14day/14day_predicted_for_2017.csv', all_predictions, delimiter=",", fmt='%.4f')

# 打印完成信息
print("所有预测已完成并保存到文件。")
