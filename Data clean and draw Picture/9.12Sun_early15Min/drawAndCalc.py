import pandas as pd
import matplotlib.pyplot as plt
import json
from datetime import datetime

# 读取CSV文件
csv_file = '/Users/suenyvan/Desktop/DataSet2/9.12Sun_early15Min/metrics_log.csv'
df = pd.read_csv(csv_file)

# 转换数据类型，确保正确计算
df['epdu_total_power'] = pd.to_numeric(df['epdu_total_power'], errors='coerce')
df['greenpower'] = pd.to_numeric(df['greenpower'], errors='coerce')  # 确保json_data也被转换为数字

# 计算总的能源消耗
total_energy_consumed = df['epdu_total_power'].sum()

# 计算实际使用的太阳能：取服务器功耗和太阳能供应的较小值
df['solar_used'] = df.apply(lambda row: min(row['epdu_total_power'], row['greenpower']) if row['greenpower'] > 0 else 0, axis=1)

# 计算总的实际使用太阳能量和总的供应太阳能量
total_solar_used = df['solar_used'].sum()
total_solar_provided = df['greenpower'].sum()

# 计算太阳能的使用率
solar_utilization_rate = (total_solar_used / total_solar_provided * 100) if total_solar_provided > 0 else 0

# 计算棕色能源使用量
# 仅当服务器功耗大于太阳能供应时计算差值
df['brown_energy_used'] = df.apply(lambda row: row['epdu_total_power'] - row['greenpower'] if row['epdu_total_power'] > row['greenpower'] else 0, axis=1)

# 计算总的棕色能源使用量
total_brown_energy_used = df['brown_energy_used'].sum()



# Plotting the graph
plt.figure(figsize=(20, 10), dpi=200)
plt.plot(df['time'], df['epdu_total_power'], label='Server power consumption', color='blue')
plt.plot(df['time'], df['greenpower'], label='Solar power generation', color='orange')
plt.title('Power Consumption Over Time')
plt.xlabel('Time')
plt.ylabel('Power (Watts)')
plt.yticks(range(0, 2040, 100))
plt.legend()

# 计算蓝线（epdu_total_power）和黄线（greenpower）之间的绝对差值
df['absolute_difference'] = abs(df['epdu_total_power'] - df['greenpower'])

# 计算所有点的绝对差值的总和
total_absolute_difference = df['absolute_difference'].sum()
# 添加统计数据为文本
textstr = f"Total energy consumed: {total_energy_consumed} Watts\n" \
          f"Total brown energy used: {total_brown_energy_used:.2f} Watts\n" \
          f"Total solar energy used: {total_solar_used:.2f} Watts\n" \
          f"Percent of green energy in total power consumption: {total_solar_used/total_energy_consumed* 100:.2f}% Watts\n" \
          f"Percent of brown energy in total power consumption: {total_brown_energy_used/total_energy_consumed* 100:.2f}% Watts\n" \
          f"Total solar energy provided: {total_solar_provided:.2f} Watts\n" \
          f"Solar Utilization Rate(Solar_Use/Solar_provided): {solar_utilization_rate:.2f}%\n" \
          f"Total absolute difference (SUM |blue line - yellow line|): {total_absolute_difference:.2f} Watts"
props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
plt.text(0.05, 0.95, textstr, transform=plt.gca().transAxes, fontsize=12,
         verticalalignment='top', bbox=props)

plt.tight_layout()
plt.savefig('/Users/suenyvan/Desktop/DataSet2/9.12Sun_early15Min/power_consumption_over_time1.png')
