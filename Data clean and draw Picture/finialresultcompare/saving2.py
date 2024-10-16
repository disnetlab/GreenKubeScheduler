import matplotlib.pyplot as plt
import numpy as np

# 定义Baseline和相应的棕色能源节省百分比
algorithms = ['Compare to DD', 'Compare to DL', 'Compare to GSOP']
compare_sunny = [100 * (2939374.24 - 1287939.70) / 2939374.24, 100 * (2919173.80 - 1287939.70) / 2919173.80, 100 * (1361133.73 - 1287939.70) / 1361133.73]
compare_cloudy = [100 * (3026637.90 - 1442824.52) / 3026637.90, 100 * (3012769.12 - 1442824.52) / 3012769.12, 100 * (1483752.57 - 1442824.52) / 1483752.57]

# 设置柱状图的宽度
bar_width = 0.25
index = np.arange(len(algorithms))

# 创建图形
fig, ax = plt.subplots(figsize=(16, 9),dpi=500)

# 绘制Sunny和Cloudy的棕色能源节省柱状图
bars_sunny = ax.bar(index, compare_sunny, bar_width, label='Sunny day', color='lightblue')
bars_cloudy = ax.bar(index + bar_width, compare_cloudy, bar_width, label='Cloudy day', color='pink')

# 添加数值标签
for i, v in enumerate(compare_sunny):
    ax.text(i, v + 1, f'{v:.1f}%', ha='center', va='bottom', fontsize=20, color='black')

for i, v in enumerate(compare_cloudy):
    ax.text(i + bar_width, v + 1, f'{v:.1f}%', ha='center', va='bottom', fontsize=20, color='black')

# 设置 x 轴和 y 轴标签
ax.set_xlabel('Baselines for comparison', fontsize=30)
ax.set_ylabel('Brown energy saving (%)', fontsize=30)
#ax.set_title('Comparison of Brown Energy Saving (%)', fontsize=30)
ax.set_yticks(np.arange(0, 61, 20))
# 设置 x 轴的刻度和标签
ax.set_xticks(index + bar_width / 2)
ax.set_xticklabels(algorithms)

# 添加图例
ax.legend(fontsize=20)
plt.yticks(fontsize=30)
plt.xticks(fontsize=30)
# 显示图形
plt.tight_layout()
plt.savefig('/Users/suenyvan/Desktop/pa/finialresultcompare/saving.pdf')
