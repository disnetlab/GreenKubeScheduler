import numpy as np
import matplotlib.pyplot as plt

predicted_values = np.array([0.8587,0.9163,0.9257,0.8626,0.7489,0.5763,0.3483,0.1403,0.0000,0.0000,0.0000,0.0000,0.0000,0.0000,0.0000,0.0000,0.0000,0.0000,0.0000,0.0000,0.0948,0.2982,0.5015,0.6799])



# 实际的值
actual_values = np.array([0.9052346570397112,0.9819494584837545,0.9954873646209387,0.9512635379061372,0.8393501805054152,0.6597472924187726,0.45126353790613716,0.2075812274368231,0.0009025270758122744,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.10379061371841156,0.3185920577617328,0.5631768953068592,0.7409747292418772])

# 创建时间轴（1到24小时）
hours = np.arange(0, 24)

# 绘制折线图
plt.figure(figsize=(10, 6), dpi=200)
plt.plot(hours, predicted_values, label='predict Value', marker='o')
plt.plot(hours, actual_values, label='actual Value', marker='x')
plt.title('predict 12.30')
plt.xlabel('hour')
plt.ylabel('radiation')

y_min = 0  # 可以调整为实际需要的最小值
y_max = 1  # 可以调整为实际需要的最大值
plt.yticks(np.arange(y_min, y_max + 0.1, 0.1))

plt.legend()
plt.grid(True)
plt.savefig('/Users/suenyvan/Desktop/DataSet2/solarPrediction/11day/12.30.png')
