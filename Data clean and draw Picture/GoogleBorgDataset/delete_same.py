import pandas as pd

# 读取CSV文件
df = pd.read_csv('/Users/suenyvan/Desktop/GoogleDataset/new/events.csv')

# 删除重复行，保留第一次出现的行
df.drop_duplicates(inplace=True)

# 将结果保存到新的CSV文件
df.to_csv('/Users/suenyvan/Desktop/GoogleDataset/new/events_new.csv', index=False)

print("重复行已删除并保存到output.csv")
