import matplotlib.pyplot as plt
import pandas as pd

# 读取CSV文件
df = pd.read_csv('/Users/suenyvan/Desktop/pa/predictdiagram/data.csv')

# 提取并简化time列的显示
df['time_simple'] = df['time'].str.slice(1, 6)  # 提取 'T' 之后的时间部分 (如 '00:00:00')

# 绘制图表
plt.figure(figsize=(16,9), dpi=500)
plt.plot(df['time_simple'], df['real'], label='Real Solar Power', linewidth=3)  # 移除了 marker 参数
plt.plot(df['time_simple'], df['predicted'], label='Predict Solar Power', color = "red", linewidth=3)  # 移除了 marker 参数

# 设置标题和标签
plt.xlabel('Time', fontsize=25)
plt.ylabel('Power (W)', fontsize=25)

# 设置横坐标刻度为每4小时显示一次
time_ticks = ['00:00', '04:00', '08:00', '12:00', '16:00', '20:00', '24:00']
plt.xticks(ticks=[i * (len(df) // 6) for i in range(7)], labels=time_ticks, fontsize=25)
plt.yticks(range(0, 1601, 400), fontsize=25)
# 添加图例
plt.legend(fontsize=25)


# 显示图表
plt.tight_layout()
plt.savefig('/Users/suenyvan/Desktop/pa/predictdiagram/predicted_vs_real.png')
