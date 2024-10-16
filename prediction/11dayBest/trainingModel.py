import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Conv1D, Flatten, Dropout
from tensorflow.keras.optimizers import Adam

# read csv
df = pd.read_csv('/Users/suenyvan/Desktop/DataSet2/solarPrediction/11day/solar_data_normalized_cleaned.csv')

# use the past 14 days of 24 hours data as features, predict the radiation value of a certain hour on the 15th day
X, y = [], []
for i in range(len(df) - 11):  # 修改这里以考虑过去21天的数据
    X.append(df.iloc[i:i+11, 3:].values)  # 改为21天的数据
    y.append(df.iloc[i+11, 3:].values)  # 第21天的数据

X = np.array(X)
y = np.array(y)

# set train data and test data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# create CNN model
model = Sequential()
model.add(Conv1D(filters=64, kernel_size=2, activation='relu', input_shape=(11, 24)))
model.add(Dropout(0.5))
model.add(Flatten())
model.add(Dense(128, activation='relu'))
model.add(Dropout(0.5))
#model.add(Dense(24))  # 预测未来一天的24小时
model.add(Dense(24, activation='sigmoid'))  # predict the radiation value of a certain hour on the 8th day, and delete the negative value

# compile model
model.compile(optimizer=Adam(learning_rate=0.001), loss='mse')

# train model
model.fit(X_train, y_train, epochs=100, batch_size=32, validation_data=(X_test, y_test))

# save model
model.save('/Users/suenyvan/Desktop/DataSet2/solarPrediction/11day/solar_radiation_cnn_model.h5')

print("模型训练完成并已保存。success!")
