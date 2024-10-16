import csv
from datetime import datetime, timedelta

# 输入和输出文件路径
input_file = '/Users/suenyvan/Desktop/DataSet2/solarPrediction/solar_data.csv'
output_file = '/Users/suenyvan/Desktop/DataSet2/solarPrediction/solar_data_full.csv'

# 打开输入文件
with open(input_file, 'r') as infile:
    reader = csv.reader(infile)
    rows = list(reader)

# 打开输出文件
with open(output_file, 'w', newline='') as outfile:
    writer = csv.writer(outfile)

    # 写入标题行
    writer.writerow(['year', 'month', 'day'] + rows[0][1:])

    # 处理每一年的数据
    for i in range(0, len(rows[1:]), 365):
        year_rows = rows[i + 1:i + 366]  # 获取一年内的365行数据
        year = year_rows[0][0]  # 获取年份

        # 生成这一年的日期
        start_date = datetime(year=int(year), month=1, day=1)
        for j, row in enumerate(year_rows):
            date = start_date + timedelta(days=j)
            month = date.month
            day = date.day
            writer.writerow([year, month, day] + row[1:])

print("文件处理完成！")