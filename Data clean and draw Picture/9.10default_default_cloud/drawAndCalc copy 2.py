import pandas as pd
import matplotlib.pyplot as plt
import json
from datetime import datetime

# 读取CSV文件
csv_file = '/Users/suenyvan/Desktop/DataSet2/9.10default_default_cloud/metrics_log1.csv'
df = pd.read_csv(csv_file)
df['time_simple'] = df['time'].str.slice(1, 6)

# Plotting the graph
plt.figure(figsize=(16, 9), dpi=500)

plt.plot(range(len(df)), df['epdu_total_power'], label='Cluster power consumption', color='blue')
plt.plot(range(len(df)), df['greenpower'], label='Solar power generation', color='orange')


time_labels = ['07', '08', '09', '10', '11', '12', '13', '14', '15', '16', '17', '18']
num_points = len(df)  # 获取数据点总数
ticks = [int(num_points * i / (len(time_labels) - 1)) for i in range(len(time_labels))]  # 生成相应的 x 轴刻度索引
plt.xticks(ticks=ticks, labels=time_labels, fontsize=25)
plt.xlabel('Time (Hours)',fontsize = 30)
plt.ylabel('Power (Watts)',fontsize = 30)
plt.yticks(range(0, 1601, 400), fontsize=25)
plt.legend(prop={'size': 20, 'weight': 'bold'})  # 同时设置字体大小和加粗




# 添加统计数据为文本
# 添加统计数据为文本

plt.tight_layout()
plt.savefig('/Users/suenyvan/Desktop/DataSet2/9.10default_default_cloud/cut8-18.pdf')


