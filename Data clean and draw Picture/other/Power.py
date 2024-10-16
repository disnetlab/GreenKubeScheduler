import matplotlib.pyplot as plt
import pandas as pd

# 读取CSV文件
df = pd.read_csv('/Users/suenyvan/Desktop/pa/other/cost.csv')

plt.figure(figsize=(16, 9), dpi=500)

# 提取功耗数据
power_data = df['Power']

# 绘制折线图，并添加标签用于图例
plt.plot(power_data, label='Cluster power consumption', linewidth=1)

# 设置纵坐标标签
plt.yticks(range(0, 1601, 400), fontsize=30)
time_labels = ['0', '4', '8', '12', '16', '20', '24']
plt.xticks(ticks=[i * (len(df) // 6) for i in range(7)], labels=time_labels, fontsize=30)

# 设置标题和横纵坐标标签
plt.xlabel('Time (hours)', fontsize=30)
plt.ylabel('Power(W)', fontsize=30)

# 添加图例
plt.legend(fontsize=30)

# 调整布局并保存图表
plt.tight_layout()
plt.savefig('/Users/suenyvan/Desktop/pa/other/sunny_cloudy.pdf')

