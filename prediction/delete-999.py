import csv

# 文件路径
input_file = '/Users/suenyvan/Desktop/DataSet2/solarPrediction/solar_data_normalized.csv'
output_file = '/Users/suenyvan/Desktop/DataSet2/solarPrediction/solar_data_normalized_cleaned.csv'

# 打开原始CSV文件并创建一个新的CSV文件用于保存清理后的数据
with open(input_file, 'r') as csvfile:
    reader = csv.reader(csvfile)
    rows = list(reader)  # 读取所有行

# 写入新的CSV文件，去除包含-999的行
with open(output_file, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    
    # 写入表头
    writer.writerow(rows[0])
    
    # 过滤并写入不包含-999的行
    for row in rows[1:]:
        if '-999.0' not in row:  # 如果该行不包含-999，写入文件
            writer.writerow(row)

print("清理完成，数据已保存为", output_file)
