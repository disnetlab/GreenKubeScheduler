import pandas as pd
import matplotlib.pyplot as plt

# 定义数据
data = {
    'factors': [0.4, 0.6, 0.8, 1.0, 1.2, 1.4, 1.6],
    'Green Energy/Total Energy (GSWP)': [28.22, 38.12, 43.60, 48.33, 47.34, 47.66, 48.11],
    'Green Energy/Green Energy Provided (GSWP)': [92.56, 94.44, 87.73, 77.93, 68.85, 58.17, 51.78],
    'Green Energy/Total Energy (Default)': [14.91, 22.36, 27.17, 29.13, 30.28, 31.07, 31.65],
    'Green Energy/Green Energy Provided (Default)': [100, 99.98, 91.11, 78.15, 67.68, 59.53, 53.07]
}

# 将数据转换为DataFrame
df = pd.DataFrame(data)

# 设置图表大小和样式
plt.figure(figsize=(16, 9), dpi=500)

# 绘制每一列的数据
plt.plot(df['factors'], df['Green Energy/Total Energy (GSWP)'], marker='o', linestyle='-', label='GSWP Green Energy Utilization\n(Green Power/Total Power)', color='blue')
plt.plot(df['factors'], df['Green Energy/Total Energy (Default)'], marker='o', linestyle='-', label='DD Green Energy Utilization\n(Green Power/Total Power)', color='red')
plt.plot(df['factors'], df['Green Energy/Green Energy Provided (GSWP)'], marker='o', linestyle='--', label='GSWP Green Energy Utilization Efficiency\n(Green Power/Green Power Provided)', color='green')
plt.plot(df['factors'], df['Green Energy/Green Energy Provided (Default)'], marker='o', linestyle='--', label='DD Green Energy Utilization Efficiency\n(Green Power/Green Power Provided)', color='orange')

# 添加标题和轴标签
plt.xlabel('Scaling Factor', fontsize=24)
plt.ylabel('Percentage (%)', fontsize=24)
plt.yticks(fontsize=24)
plt.xticks(fontsize=24)

# 添加图例
plt.legend(prop={'size': 16, 'weight': 'bold'})

# 显示图表
plt.tight_layout()
plt.savefig('/Users/suenyvan/Desktop/pa/factor/factor.pdf')
