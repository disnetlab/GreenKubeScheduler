import matplotlib.pyplot as plt
import pandas as pd
from mpl_toolkits.axes_grid1.inset_locator import inset_axes

# 读取CSV文件
df = pd.read_csv('/Users/suenyvan/Desktop/pa/newpredictioncompare/sunny/sunny.csv')

# 提取并简化time列的显示
df['time_simple'] = df['api_time'].str.slice(1, 6)  # 提取时间部分 (如 '00:00')

# 绘制主图表
plt.figure(figsize=(21, 9), dpi=500)
main_ax = plt.gca()  # 获取主轴

# 使用fill_between绘制每个调度器的区域图
plt.fill_between(range(len(df)), df['Early5Min'], color='lightcoral', alpha=0.1)
plt.plot(range(len(df)), df['Early5Min'], color='red', label='Early5Min', linewidth=0.5)

plt.fill_between(range(len(df)), df['Early15Min'], color='lightyellow', alpha=0.1)
plt.plot(range(len(df)), df['Early15Min'], color='orange', label='Early15Min', linewidth=0.5)

plt.fill_between(range(len(df)), df['Early30Min'], color='lightblue', alpha=0.1)
plt.plot(range(len(df)), df['Early30Min'], color='blue', label='Early30Min', linewidth=0.5)

plt.fill_between(range(len(df)), df['Early1Hour'], color='lightskyblue', alpha=0.1)
plt.plot(range(len(df)), df['Early1Hour'], color='deepskyblue', label='Early1Hour', linewidth=0.5)

plt.fill_between(range(len(df)), df['greenpower'], color='lightgreen', alpha=0.1)
plt.plot(range(len(df)), df['greenpower'], color='mediumseagreen', label='Green Power', linewidth=0.5)

# 设置横坐标为0到24小时，分7等份
time_labels = ['0', '4', '8', '12', '16', '20', '24']
plt.xticks(ticks=[i * (len(df) // 6) for i in range(7)], labels=time_labels, fontsize=20)
plt.yticks(range(0, 1601, 400), fontsize=20)

# 设置标题和标签
plt.xlabel('Time (hours)', fontsize=20)
plt.ylabel('Power consumption(W)', fontsize=20)

# 添加图例
legend = plt.legend(fontsize=20)
for leg_line in legend.get_lines():
    leg_line.set_linewidth(3)

# 添加放大的图，使用数值设置宽度和高度
ax_inset = inset_axes(main_ax, width=6, height=4, loc='upper left', bbox_to_anchor=(0.05, 1), bbox_transform=main_ax.transAxes, borderpad=2)

# 只显示8-20点的数据
start_index = int(len(df) * 8 / 24)
end_index = int(len(df) * 20 / 24)

ax_inset.fill_between(range(start_index, end_index), df['Early5Min'].iloc[start_index:end_index], color='lightcoral', alpha=0.1)
ax_inset.plot(range(start_index, end_index), df['Early5Min'].iloc[start_index:end_index], color='red', linewidth=0.5)

ax_inset.fill_between(range(start_index, end_index), df['Early15Min'].iloc[start_index:end_index], color='lightyellow', alpha=0.1)
ax_inset.plot(range(start_index, end_index), df['Early15Min'].iloc[start_index:end_index], color='orange', linewidth=0.5)

ax_inset.fill_between(range(start_index, end_index), df['Early30Min'].iloc[start_index:end_index], color='lightblue', alpha=0.1)
ax_inset.plot(range(start_index, end_index), df['Early30Min'].iloc[start_index:end_index], color='blue', linewidth=0.5)

ax_inset.fill_between(range(start_index, end_index), df['Early1Hour'].iloc[start_index:end_index], color='lightskyblue', alpha=0.1)
ax_inset.plot(range(start_index, end_index), df['Early1Hour'].iloc[start_index:end_index], color='deepskyblue', linewidth=0.5)

ax_inset.fill_between(range(start_index, end_index), df['greenpower'].iloc[start_index:end_index], color='lightgreen', alpha=0.1)
ax_inset.plot(range(start_index, end_index), df['greenpower'].iloc[start_index:end_index], color='mediumseagreen', linewidth=0.5)

# 设置放大图的刻度为 8, 12, 16, 20
zoom_time_ticks = [start_index, int(start_index + (end_index - start_index) / 3), int(start_index + 2 * (end_index - start_index) / 3), end_index]

# 设置放大图的刻度为 8, 12, 16, 20
zoom_time_labels = ['8', '12', '16', '20']
ax_inset.set_xticks(zoom_time_ticks)
ax_inset.set_xticklabels(zoom_time_labels)
# 调整布局并保存图表
plt.tight_layout()
plt.savefig('/Users/suenyvan/Desktop/pa/newpredictioncompare/sunny/sunnycomparepredic_with_zoom_adjusted.png')
