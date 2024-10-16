import numpy as np
import pandas as pd

# 加载预测结果
predicted_df = pd.read_csv('/Users/suenyvan/Desktop/DataSet2/solarPrediction/14day/14day_predicted_for_2017.csv', header=None)

# 加载实际结果
actual_df = pd.read_csv('/Users/suenyvan/Desktop/DataSet2/solarPrediction/14day/solar_data_normalized_cleaned.csv')
actual_data = actual_df.iloc[6439:6794, 3:].values  # 6440-6794行，第四列到最后一列

# 确保预测数据和实际数据的行数相同
if len(predicted_df) == len(actual_data):
    # 计算误差
    errors = predicted_df.values - actual_data
    mse = np.mean(np.square(errors))
    rmse = np.sqrt(mse)
    mae = np.mean(np.abs(errors))


    print("Mean Squared Error (MSE):", mse)
    print("Root Mean Squared Error (RMSE):", rmse)
    print("Mean Absolute Error (MAE):", mae)
else:
    print("Error: The number of rows in the predicted and actual data does not match.")
