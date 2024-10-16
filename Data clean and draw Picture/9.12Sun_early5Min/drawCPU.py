import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.ticker as ticker

# 读取CSV文件
csv_file = "/Users/suenyvan/Desktop/DataSet2/9.12Sun_early5Min/cpu_over_limits2.csv"
df = pd.read_csv(csv_file)

# 计算超过16的次数和百分比
total_count = len(df)
exceed_count = len(df[df['Total_CPU_Count'] > 16])
exceed_percentage = (exceed_count / total_count) * 100

# 绘制折线图
plt.figure(figsize=(50, 15), dpi=300)
plt.plot(df['Total_CPU_Count'], marker='o', label='Total CPU Count')

# 添加y=16的水平线
plt.axhline(y=16, color='r', linestyle='--', label='Total server vCPU(16)')

# 设置图表标题和标签
plt.title('CPU resources exceed the server limit')
plt.xlabel('Time')
plt.ylabel('CPU Count')

# 设置Y轴间隔为1
plt.gca().yaxis.set_major_locator(ticker.MultipleLocator(1))

# 设置X轴每5分钟显示一个标签
x_ticks = range(0, len(df), 10)  # 每10个点对应5分钟
plt.xticks(ticks=x_ticks, labels=[f"{i//2} min" for i in x_ticks])

# 添加网格和图例
plt.grid(True)
plt.legend()

# 在图表上添加超过16的百分比
plt.text(0.05, 0.95, f'Percentage exceeding 16: {exceed_percentage:.2f}%',
         horizontalalignment='left',
         verticalalignment='center',
         transform=plt.gca().transAxes,
         fontsize=20, color='red')

# 保存图表
plt.savefig('/Users/suenyvan/Desktop/DataSet2/9.12Sun_early5Min/cpu_over_time.png')

