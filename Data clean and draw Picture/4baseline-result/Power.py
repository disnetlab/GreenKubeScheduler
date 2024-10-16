import matplotlib.pyplot as plt
import pandas as pd

# 读取CSV文件
df = pd.read_csv('/Users/suenyvan/Desktop/pa/4baseline-result/Cloud.csv')

# 提取并简化time列的显示
df['time_simple'] = df['api_time'].str.slice(1, 6)  # 提取时间部分 (如 '00:00')

# 绘制图表
plt.figure(figsize=(21, 9), dpi=500)

# 使用fill_between绘制每个调度器的区域图
# Default Scheduler - 红色
plt.fill_between(range(len(df)), df['default_scheduler'], color='lightcoral', alpha=0.1)
plt.plot(range(len(df)), df['default_scheduler'], color='red', label='DD', linewidth=1)

# Default Limit Scheduler - 黄色
plt.fill_between(range(len(df)), df['default_limit_scheduler'], color='lightyellow', alpha=0.1)
plt.plot(range(len(df)), df['default_limit_scheduler'], color='orange', label='DL', linewidth=1)

# Green Scheduler Without Prediction - 蓝色
plt.fill_between(range(len(df)), df['green_scheduler_without_prediction'], color='lightblue', alpha=0.1)
plt.plot(range(len(df)), df['green_scheduler_without_prediction'], color='blue', label='GSOP', linewidth=1)

# Green Scheduler with Prediction (15 Min) - 天蓝色
plt.fill_between(range(len(df)), df['green_scheduler_with_prediction(Early15Min)'], color='lightskyblue', alpha=0.1)
plt.plot(range(len(df)), df['green_scheduler_with_prediction(Early15Min)'], color='deepskyblue', label='GSWP(15Min)', linewidth=1)

# Green Power - 绿色
plt.fill_between(range(len(df)), df['greenpower'], color='lightgreen', alpha=0.1)
plt.plot(range(len(df)), df['greenpower'], color='mediumseagreen', label='Green Power', linewidth=1)

time_labels = ['07', '08', '09', '10', '11', '12', '13', '14', '15', '16', '17', '18']
num_points = len(df)  # 获取数据点总数
ticks = [int(num_points * i / (len(time_labels) - 1)) for i in range(len(time_labels))]  # 生成相应的 x 轴刻度索引
plt.xticks(ticks=ticks, labels=time_labels, fontsize=25)
plt.yticks(range(0, 1601, 400), fontsize=25)

# 设置标题和标签
plt.xlabel('Time (hours)', fontsize=30)
plt.ylabel('Power consumption(W)', fontsize=30)

legend = plt.legend(fontsize=19)

# 遍历图例中的线条并加粗
for leg_line in legend.get_lines():
    leg_line.set_linewidth(3)  # 设置图例中线条的粗细为 3

    
# 显示图表
plt.tight_layout()
plt.savefig('/Users/suenyvan/Desktop/pa/4baseline-result/cut2-7.pdf')
