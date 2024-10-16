import pandas as pd

# 读取CSV文件
df = pd.read_csv('/Users/suenyvan/Desktop/DataSet2/solarPrediction/solar_data_full_0_1.csv')

# 将-999标记为NaN，方便后续处理
df.replace(-999, float('nan'), inplace=True)

# 找到最大值，忽略NaN值
max_value = df.iloc[:, 3:].max().max()  # 忽略前三列 (year, month, day)

# 对数据进行归一化
df.iloc[:, 3:] = df.iloc[:, 3:].applymap(lambda x: x / max_value if pd.notna(x) else x)

# 将NaN值还原为-999
df.fillna(-999, inplace=True)

# 保存归一化后的数据
df.to_csv('/Users/suenyvan/Desktop/DataSet2/solarPrediction/solar_data_normalized.csv', index=False)

print(f"数据已归一化，最大值为: {max_value}")
