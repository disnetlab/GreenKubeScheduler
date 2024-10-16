import pandas as pd

# 读取新的 CSV 文件
updated_usage_df = pd.read_csv('/Users/suenyvan/Desktop/GoogleDataset/new/usage_new_new.csv')

# 将指定的列转换为整数格式
columns_to_convert = ['collection_id', 'instance_index', 'machine_id', 'time', 'type', 'priority']

for column in columns_to_convert:
    updated_usage_df[column] = updated_usage_df[column].astype('Int64')  # 使用 'Int64' 类型保留 NaN 值

# 保存更新后的 DataFrame 到新的 CSV 文件
updated_usage_df.to_csv('/Users/suenyvan/Desktop/GoogleDataset/new/usage_new_new_new.csv', index=False)
