import numpy as np
import matplotlib.pyplot as plt

predicted_values = np.array([0.4737,0.5251,0.5398,0.5117,0.4445,0.3180,0.1746,0.0178,0.0000,0.0000,0.0000,0.0000,0.0000,0.0000,0.0000,0.0000,0.0000,0.0000,0.0000,0.0000,0.0024,0.1240,0.2654,0.4087])



# 实际的值
actual_values = np.array([0.5216606498194946,0.7581227436823105,0.776173285198556,0.7328519855595668,0.4657039711191336,0.44945848375451264,0.1371841155234657,0.030685920577617327,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.12364620938628158,0.3285198555956679,0.5207581227436823])

# 创建时间轴（1到24小时）
hours = np.arange(0, 24)

# 绘制折线图
plt.figure(figsize=(10, 6), dpi=200)
plt.plot(hours, predicted_values, label='predict Value', marker='o')
plt.plot(hours, actual_values, label='actual Value', marker='x')
plt.title('predict 8.2')
plt.xlabel('hour')
plt.ylabel('radiation')

y_min = 0  # 可以调整为实际需要的最小值
y_max = 1  # 可以调整为实际需要的最大值
plt.yticks(np.arange(y_min, y_max + 0.1, 0.1))

plt.legend()
plt.grid(True)
plt.savefig('/Users/suenyvan/Desktop/DataSet2/solarPrediction/11dayBest/8.2.png')
