import pandas as pd

def expand_real_values(metrics_file, data_file, start_metrics, start_data, end_data):
    # 读取两个CSV文件
    df_metrics = pd.read_csv(metrics_file)
    df_data = pd.read_csv(data_file)

    # 初始化greenpower列，如果尚未存在
    if 'greenpower' not in df_metrics.columns:
        df_metrics['greenpower'] = 0

    # 计算每个数据段应该重复的次数
    repeat_count = 14

    # 获取数据文件中的real值，从指定行开始到结束
    real_values = df_data.loc[start_data:end_data-1, 'real'].values

    # 为每个real值添加指定的重复次数，并填充到metrics_log文件中指定的位置
    index = 0
    for i, value in enumerate(real_values):
        df_metrics.loc[start_metrics + index:start_metrics + index + repeat_count - 1, 'greenpower'] = value
        index += repeat_count

    # 保存修改后的metrics_log文件
    df_metrics.to_csv(metrics_file, index=False)

# 定义文件路径和起止行号
metrics_log_file = '/Users/suenyvan/Desktop/DataSet2/9.14cloud_early1HourUpdate/metrics_log.csv'
data_file = '/Users/suenyvan/Desktop/DataSet2/9.14cloud_early1HourUpdate/data.csv'
start_metrics_line = 1182  # 从第1300-2行开始，因为pandas的索引从0开始
start_data_line = 84       # 从第93行开始 -2
end_data_line = 218        # 到第219行

# 调用函数
expand_real_values(metrics_log_file, data_file, start_metrics_line, start_data_line, end_data_line)


#5309
#start_metrics_line2 = 5398  #  5309-2 5299-2
#start_data_line2 = 378      # 380-2
#end_data_line2 = 497        # 到第219行


#expand_real_values(metrics_log_file, data_file, start_metrics_line2, start_data_line2, end_data_line2)
