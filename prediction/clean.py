import csv

# 文件路径
input_file = '/Users/suenyvan/Desktop/DataSet2/solarPrediction/solardata.txt'
output_file = '/Users/suenyvan/Desktop/DataSet2/solarPrediction/solar_data.csv'

# 读取txt文件数据
with open(input_file, 'r') as file:
    lines = file.readlines()

# 初始化CSV表头
header = ['year'] + [str(hour) for hour in range(12, 24)] + [str(hour) for hour in range(0, 12)]

# 写入CSV文件
with open(output_file, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(header)

    # 初始年份
    start_year = 1990

    for year_index, line in enumerate(lines):
        # 将每行数据拆分为列表
        values = list(map(int, line.strip().split()))

        # 每一年的365天，每天24小时的数据，分割并写入CSV
        for i in range(0, len(values), 24):
            row = [start_year + year_index] + values[i:i + 24]
            writer.writerow(row)

print("转换完成，数据已保存为", output_file)
