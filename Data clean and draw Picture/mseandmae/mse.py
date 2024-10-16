import matplotlib.pyplot as plt

# 数据
days = [7, 10, 11, 12, 14, 18, 21, 28, 60]
mse_values = [0.007616588528843667, 0.007282950472646485, 0.007160127280347881, 0.007391519646808716,
              0.007374492713012732, 0.007762929423110326, 0.007762929423110326, 0.008233543518118723, 0.008623191395246714]
mae_values = [0.04536775254611216, 0.04193727037399634, 0.04207874969405862, 0.041434373109112306,
              0.04143739767960459, 0.04366745816251607, 0.04366745816251607, 0.04447886790640914, 0.04522713300631599]

# 创建图表和两个子图
fig, ax = plt.subplots(2, 1, figsize=(15, 14), dpi=500)

# 绘制MSE图
ax[0].plot(days, mse_values, marker='o', linestyle='-', color='b', label='MSE')  # 设置标签为图例
ax[0].set_xlabel('Days', fontsize=30)
ax[0].set_ylabel('MSE', fontsize=30)
ax[0].tick_params(axis='both', labelsize=20)  # 调整刻度的字号
ax[0].legend(fontsize=30, loc='lower right')  # 添加图例并设置位置在右下角

# 绘制MAE图
ax[1].plot(days, mae_values, marker='o', linestyle='-', color='g', label='MAE')  # 设置标签为图例
ax[1].set_xlabel('Days', fontsize=30)
ax[1].set_ylabel('MAE', fontsize=30)
ax[1].tick_params(axis='both', labelsize=20)  # 调整刻度的字号
ax[1].legend(fontsize=30, loc='lower right')  # 添加图例并设置位置在右下角

# 调整布局并保存图表
plt.tight_layout()
plt.savefig('/Users/suenyvan/Desktop/pa/mseandmae/combined_error_metrics.png')
