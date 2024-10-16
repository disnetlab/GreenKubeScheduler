import pandas as pd

# 读取CSV文件
df = pd.read_csv('/Users/suenyvan/Desktop/DataSet2/solarPrediction/solar_data_normalized_cleaned.csv')

# 打印数据集信息，查看列数和每列的非空值计数
print(df.info())

# 检查数据集中是否有任何缺失值
if df.isnull().any().any():
    print("存在缺失值")
else:
    print("没有缺失值")

# 检查特定的时间数据列
hourly_columns = df.columns[3:]  # 假设从第4列开始是小时数据
print("小时数据列数:", len(hourly_columns))

# 确保所有行在小时数据列都有数据
if (df[hourly_columns].isnull().any(axis=1)).any():
    print("某些行在小时数据列中存在缺失值")
else:
    print("所有行在小时数据列中的数据都是完整的")
