import matplotlib.pyplot as plt
import numpy as np

# 数据：baselines 和 weather conditions
baselines = ['DD-S', 'DD-C', 'DL-S', 'DL-C', 'GSOP-S', 'GSOP-C', 'GSWP-S', 'GSWP-C']

# Total Energy for each baseline
total_energy = [4147349, 4147349, 4147796, 4147796, 2492597, 2537722, 2492594, 2537603]

# Green and Brown energy shares
green_energy_share = [29.13, 27.02, 29.62, 27.36, 45.39, 41.53, 48.33, 43.14]
brown_energy_share = [70.87, 72.98, 70.38, 72.64, 54.61, 58.47, 51.67, 56.86]

# Brown and Green energy values corresponding to the total energy
brown_energy_values = [2939374.24, 3026637.90, 2919173.80, 3012769.12, 1361133.73, 1483752.57, 1287939.70, 1442824.52]
green_energy_values = [1207974.76, 1120711.10, 1228622.20, 1135026.88, 1131463.27, 1053969.43, 1204654.30, 1094778.48]

# 设置柱状图的宽度和间距
bar_width = 0.35
gap_between_colors = 50000  # 增加灰色和绿色之间的空隙
index = np.arange(len(baselines)) / 2  # 减少基线之间的距离

# 创建图形
fig, ax = plt.subplots(figsize=(16, 9), dpi=500)

# 绘制灰色部分（棕色能源）
brown_bars = ax.bar(index, brown_energy_values, bar_width, label='Brown energy', color='gray')

# 绘制绿色部分（绿色能源），并在底部加上灰色部分的高度，增加空隙
green_bars = ax.bar(index, green_energy_values, bar_width, bottom=[val + gap_between_colors for val in brown_energy_values], label='Green energy', color='lightgreen')

# 添加百分比标签
for i in range(len(brown_energy_values)):
    ax.text(i / 2, brown_energy_values[i] / 2, f'{brown_energy_share[i]:.2f}%', ha='center', va='center', color='white', fontsize=20)
    ax.text(i / 2, brown_energy_values[i] + gap_between_colors + green_energy_values[i] / 2, f'{green_energy_share[i]:.2f}%', ha='center', va='center', color='black', fontsize=20)

# 设置 x 轴和 y 轴的标签
ax.set_xlabel('4 Baselines test results in sunny and cloudy days', fontsize=25)
ax.set_ylabel('Energy Consumption (W)', fontsize=25)

# 调整 y 轴不显示科学计数
ax.get_yaxis().get_major_formatter().set_useOffset(False)

# 设置 x 轴的刻度
ax.set_xticks(index)
ax.set_xticklabels(baselines, fontsize=25)

# 调整图例字体大小
ax.legend(fontsize=20, title="Note: -S = Sunny day, -C = Cloudy day",title_fontsize=20)

# 添加布局调整
plt.tight_layout()

# 保存图像
plt.savefig('/Users/suenyvan/Desktop/pa/finialresultcompare/final_energy_chart_with_gap_adjusted.png')
