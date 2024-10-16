def trim_file(input_file, output_file, max_lines):
    # 打开原始文件和输出文件
    with open(input_file, 'r') as f_in, open(output_file, 'w') as f_out:
        # 读取并写入指定行数
        for i in range(max_lines):
            try:
                line = next(f_in)
                f_out.write(line)
            except StopIteration:
                # 如果行数不足，提前结束循环
                break

# 指定文件路径和最大行数
input_file_path = '/Users/suenyvan/Desktop/DataSet2/9.13Sun_early1Hour/Schedulersession.log'
output_file_path = '/Users/suenyvan/Desktop/DataSet2/9.13Sun_early1Hour/Schedulersessioncut2.log'
max_line_number = 205252

# 调用函数
trim_file(input_file_path, output_file_path, max_line_number)
