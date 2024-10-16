import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import FuncFormatter

# 定义格式化函数，转换为 K（千）或 M（百万）
def format_yticks(value, tick_number):
    if value >= 1_000_000:
        return f'{value / 1_000_000:.1f}M'
    elif value >= 1_000:
        return f'{value / 1_000:.1f}K'
    else:
        return int(value)

# 调整顺序：先显示所有 -S 的数据，再显示所有 -C 的数据
baselines = ['DD(S)', 'DL(S)', 'GSOP(S)', 'GSWP(S)', 'DD(C)', 'DL(C)', 'GSOP(C)', 'GSWP(C)']

# 根据新的顺序调整 Total Energy 数据
total_energy = [4147349, 4147796, 2492597, 2492594, 4147349, 4147796, 2537722, 2537603]

# 根据新的顺序调整 Green 和 Brown energy shares
green_energy_share = [29.13, 29.62, 45.39, 48.33, 27.02, 27.36, 41.53, 43.14]
brown_energy_share = [70.87, 70.38, 54.61, 51.67, 72.98, 72.64, 58.47, 56.86]

# 根据新的顺序调整 Green 和 Brown energy values
brown_energy_values = [2939374.24, 2919173.80, 1361133.73, 1287939.70, 3026637.90, 3012769.12, 1483752.57, 1442824.52]
green_energy_values = [1207974.76, 1228622.20, 1131463.27, 1204654.30, 1120711.10, 1135026.88, 1053969.43, 1094778.48]

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

# 使用自定义格式化函数，将Y轴改为K（千）、M（百万）
ax.yaxis.set_major_formatter(FuncFormatter(format_yticks))

# 设置 x 轴的刻度
ax.set_xticks(index)
ax.set_xticklabels(baselines, fontsize=25)
plt.yticks(fontsize=20)
# 调整图例字体大小并添加说明
ax.legend(fontsize=20, title="(S) = Sunny day\n(C) = Cloudy day", title_fontsize=20)

# 添加布局调整
plt.tight_layout()

# 保存图像
plt.savefig('/Users/suenyvan/Desktop/pa/finialresultcompare/final_energy_chart_with_gap_adjusted_weather_sorted123.png')
