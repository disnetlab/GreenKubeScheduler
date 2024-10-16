import pandas as pd
import matplotlib.pyplot as plt

# 读取CSV文件
csv_file = "/Users/suenyvan/Desktop/pa/pendingtime/pendingtime.csv"
df = pd.read_csv(csv_file)

# 假设总时间是1440分钟（一天的分钟数）
total_time = 1440

# 计算剩余运行时间
df['Remaining running time'] = total_time - df['Pause time(min)']

# 按照 Pause time 升序排序
df = df.sort_values(by='Pause time(min)')

# 设置图表大小
plt.figure(figsize=(30, 20), dpi=500)

# 绘制堆叠柱状图
bars_pause = plt.bar(df['Pod_Name'], df['Pause time(min)'], color='orange', label='Pause time')
bars_remaining = plt.bar(df['Pod_Name'], df['Remaining running time'], bottom=df['Pause time(min)'], color='skyblue', label='Remaining running time')

# 设置 y 轴间隔，并加大字体
plt.yticks(range(0, 1801, 300), fontsize=20, fontweight='bold')

# 添加优先级到 x 轴标签，并加大字体
xticks_labels = [f"{pod}\nPriority: {priority}" for pod, priority in zip(df['Pod_Name'], df['priority'])]
plt.xticks(ticks=range(len(df['Pod_Name'])), labels=xticks_labels, rotation=90, fontsize=30)

# 添加数值标签，显示运行时间而不是总时间
for bar in bars_remaining:
    height = bar.get_height()  # 获取剩余运行时间的高度
    plt.text(bar.get_x() + bar.get_width() / 2.0, bar.get_y() + height, f'{round(height)}', ha='center', va='bottom', fontsize=25, fontweight='bold')

# 添加标签，并加大字体
plt.xlabel('Pod Name with Priority', fontsize=30, fontweight='bold')
plt.ylabel('Time (min)', fontsize=30, fontweight='bold')

# 添加图例，字体调整为 30
plt.legend(prop={'size': 30, 'weight': 'bold'})

# 保存图表
plt.savefig('/Users/suenyvan/Desktop/pa/pendingtime/sundayPending.pdf', bbox_inches='tight')
