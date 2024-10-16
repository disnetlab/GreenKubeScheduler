import matplotlib.pyplot as plt
import pandas as pd

# 读取CSV文件
df = pd.read_csv('/Users/suenyvan/Desktop/pa/newpredictioncompare/sunny/sunny.csv')

# 提取并简化time列的显示
df['time_simple'] = df['api_time'].str.slice(1, 6)  # 提取时间部分 (如 '00:00')

# 绘制图表
plt.figure(figsize=(21, 10), dpi=500)

# 使用fill_between绘制每个调度器的区域图，保留全部数据
# Default Scheduler - 红色
plt.fill_between(range(len(df)), df['Early5Min'], color='lightcoral', alpha=0.1)
plt.plot(range(len(df)), df['Early5Min'], color='red', label='Early5Min', linewidth=1)

# Default Limit Scheduler - 黄色
plt.fill_between(range(len(df)), df['Early15Min'], color='lightyellow', alpha=0.1)
plt.plot(range(len(df)), df['Early15Min'], color='orange', label='Early15Min', linewidth=1)

# Green Scheduler Without Prediction - 蓝色
plt.fill_between(range(len(df)), df['Early30Min'], color='lightblue', alpha=0.1)
plt.plot(range(len(df)), df['Early30Min'], color='blue', label='Early30Min', linewidth=1)

# Green Scheduler with Prediction (15 Min) - 天蓝色
plt.fill_between(range(len(df)), df['Early1Hour'], color='lightskyblue', alpha=0.1)
plt.plot(range(len(df)), df['Early1Hour'], color='deepskyblue', label='Early1Hour', linewidth=1)

# Green Power - 绿色
plt.fill_between(range(len(df)), df['greenpower'], color='lightgreen', alpha=0.1)
plt.plot(range(len(df)), df['greenpower'], color='mediumseagreen', label='Green Power', linewidth=1)

# 设置x轴的范围只显示8到20
plt.xlim(int(len(df) * 8 / 24), int(len(df) * 20 / 24))

# 自定义x轴刻度为8到20小时
time_labels = ['8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20']
plt.xticks(ticks=[int(len(df) * i / 24) for i in range(8, 21)], labels=time_labels, fontsize=20)

# 设置y轴的刻度
plt.yticks(range(0, 1601, 400), fontsize=20)
plt.ylim(0, 1600)
# 设置标题和标签
plt.xlabel('Time (hours)', fontsize=30)
plt.ylabel('Power consumption(W)', fontsize=30)

# 添加图例
legend = plt.legend(fontsize=25)

# 修改图例中线条的粗细
for leg_line in legend.get_lines():
    leg_line.set_linewidth(3)  # 设置图例中的线条粗细

# 显示图表
plt.tight_layout()
plt.savefig('/Users/suenyvan/Desktop/pa/newpredictioncompare/sunny/sunnycomparepredic_8_20.png')
