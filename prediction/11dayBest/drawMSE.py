import matplotlib.pyplot as plt

# 数据
days = [7, 10, 11, 12, 14, 18, 21, 28, 60]
mse_values = [0.007616588528843667, 0.007282950472646485, 0.007160127280347881, 0.007391519646808716,
              0.007374492713012732, 0.007762929423110326, 0.007762929423110326, 0.008233543518118723, 0.008623191395246714]
rmse_values = [0.08727306874886243, 0.08534020431570624, 0.0846175353005976, 0.08597394748881033,
               0.08587486659676818, 0.08810748789467514, 0.08810748789467514, 0.09073887545103655, 0.09286114039385213]
mae_values = [0.04536775254611216, 0.04193727037399634, 0.04207874969405862, 0.041434373109112306,
              0.04143739767960459, 0.04366745816251607, 0.04366745816251607, 0.04447886790640914, 0.04522713300631599]

# 绘制MSE图
plt.figure(figsize=(10, 7),dpi=200)
plt.plot(days, mse_values, marker='o', linestyle='-', color='b')
plt.title('Mean Squared Error (MSE) by Days')
plt.xlabel('Days')
plt.ylabel('MSE')
plt.grid(True)
plt.savefig('mse.png')


# 绘制RMSE图
plt.figure(figsize=(10, 7),dpi=200)
plt.plot(days, rmse_values, marker='o', linestyle='-', color='r')
plt.title('Root Mean Squared Error (RMSE) by Days')
plt.xlabel('Days')
plt.ylabel('RMSE')
plt.grid(True)
plt.savefig('RMSE.png')


# 绘制MAE图
plt.figure(figsize=(10, 7),dpi=200)
plt.plot(days, mae_values, marker='o', linestyle='-', color='g')
plt.title('Mean Absolute Error (MAE) by Days')
plt.xlabel('Days')
plt.ylabel('MAE')
plt.grid(True)
plt.savefig('MAE.png')

