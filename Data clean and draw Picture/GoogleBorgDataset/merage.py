import pandas as pd

# 读取CSV文件
events_df = pd.read_csv('/Users/suenyvan/Desktop/GoogleDataset/new/events_new.csv')
usage_df = pd.read_csv('/Users/suenyvan/Desktop/GoogleDataset/new/usage_new.csv')

# 将需要匹配的列转换为字符串类型，以避免浮点精度问题
events_df['collection_id'] = events_df['collection_id'].astype(str)
events_df['instance_index'] = events_df['instance_index'].astype(str)
events_df['machine_id'] = events_df['machine_id'].astype(str)

usage_df['collection_id'] = usage_df['collection_id'].astype(str)
usage_df['instance_index'] = usage_df['instance_index'].astype(str)
usage_df['machine_id'] = usage_df['machine_id'].astype(str)

# 遍历events_df中的每一行
for index, event_row in events_df.iterrows():
    # 提取匹配值
    collection_id = event_row['collection_id']
    instance_index = event_row['instance_index']
    machine_id = event_row['machine_id']
    
    # 找到usage_df中匹配的行
    matching_rows = usage_df[
        (usage_df['collection_id'] == collection_id) & 
        (usage_df['instance_index'] == instance_index) & 
        (usage_df['machine_id'] == machine_id)
    ]
    
    # 在匹配行中找到第一行没有填充数据的行
    for usage_index, usage_row in matching_rows.iterrows():
        if pd.isna(usage_row['time']):
            # 将事件行的数据填充到使用行
            usage_df.at[usage_index, 'time'] = event_row['time']
            usage_df.at[usage_index, 'type'] = event_row['type']
            usage_df.at[usage_index, 'priority'] = event_row['priority']
            usage_df.at[usage_index, 'cpus_request'] = event_row['cpus_request']
            usage_df.at[usage_index, 'memory_request'] = event_row['memory_request']
            break

# 创建一个新的CSV文件保存更新后的usage_df
usage_df.to_csv('/Users/suenyvan/Desktop/GoogleDataset/new/usage_new_new.csv', index=False)

print("数据追加完成。")
