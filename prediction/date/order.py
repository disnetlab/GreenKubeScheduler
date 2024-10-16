import pandas as pd

# 读取CSV文件
df = pd.read_csv('/Users/suenyvan/Desktop/DataSet2/solarPrediction/date/solar_data_normalized_cleaned.csv')

# 转换日期格式，并抽取月和日作为特征
df['date'] = pd.to_datetime(df[['year', 'month', 'day']])
df['month'] = df['date'].dt.month
df['day'] = df['date'].dt.day

# 按月和日排序
df_sorted = df.sort_values(by=['month', 'day'])

# 保存重新排序后的数据到一个新的CSV文件
df_sorted.to_csv('/Users/suenyvan/Desktop/DataSet2/solarPrediction/date/sorted_solar_data.csv', index=False)

print("数据已按日期重新排序并保存。")
