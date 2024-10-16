import pandas as pd
import matplotlib.pyplot as plt
import json
from datetime import datetime

# 读取CSV文件
csv_file = '/Users/suenyvan/Desktop/DataSet2/9.10default_default_Sun/metrics_log.csv'
df = pd.read_csv(csv_file)
df['time_simple'] = df['time'].str.slice(1, 6)

# Plotting the graph
plt.figure(figsize=(16, 9), dpi=500)

plt.plot(range(len(df)), df['epdu_total_power'], label='Server power consumption', color='blue')
plt.plot(range(len(df)), df['greenpower'], label='Solar power generation', color='orange')


time_ticks = ['00:00', '04:00', '08:00', '12:00', '16:00', '20:00', '24:00']
plt.xticks(ticks=[i * (len(df) // 6) for i in range(7)], labels=time_ticks, fontsize=25)
#plt.title('Power Consumption Over Time')
plt.xlabel('Time',fontsize = 25)
plt.ylabel('Power (Watts)',fontsize = 25)
plt.yticks(range(0, 1601, 400), fontsize=25)
plt.legend(fontsize=25)



# 添加统计数据为文本
# 添加统计数据为文本

plt.tight_layout()
plt.savefig('/Users/suenyvan/Desktop/DataSet2/9.10default_default_Sun/power_consumption_over_time2.png')


# 第二个图：显示8-20点的数据
plt.figure(figsize=(16, 9), dpi=500)

# 计算8点到20点的索引范围
start_index = int(len(df) * 7 / 24)
end_index = int(len(df) * 20 / 24)

# 绘制图像，仅显示8-20点的数据
plt.plot(range(start_index, end_index), df['epdu_total_power'].iloc[start_index:end_index], label='Server power consumption', color='blue')
plt.plot(range(start_index, end_index), df['greenpower'].iloc[start_index:end_index], label='Solar power generation', color='orange')

# 设置x轴刻度为每小时，从8到20
time_labels_7_20 = [f'{i}:00' for i in range(7, 21)]  # 生成 ['08:00', '09:00', '10:00', ..., '20:00']
hourly_ticks = [int(len(df) * i / 24) for i in range(7, 21)]  # 生成对应刻度

plt.xticks(ticks=hourly_ticks, labels=time_labels_7_20, fontsize=20)

plt.xlabel('Time (Hours)', fontsize=25)
plt.ylabel('Power (Watts)', fontsize=25)
plt.yticks(range(0, 1601, 400), fontsize=25)
plt.legend(fontsize=25)

plt.tight_layout()
plt.savefig('/Users/suenyvan/Desktop/DataSet2/9.10default_default_Sun/power_consumption_over_time_7_to_20.png')