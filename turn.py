import csv
import pandas as pd
from datetime import datetime, timedelta
import numpy as np

# 打开CSV文件并读取内容
csv_filename = "for_imu/imu_data_0f.csv"

ids = []
times = []
angle_values = []
times_v2 = []
num = []

with open(csv_filename, "r") as csv_file:
    csv_reader = csv.reader(csv_file)
    
    # 跳过标题行
    next(csv_reader)
    
    for row in csv_reader:
        # 假设CSV文件中的列顺序是ID、Time、X、Y
        id_value = str(row[0])
        time_value = str(row[1])
        angle_value = float(row[2])
        
        ids.append(id_value)
        times.append(time_value)
        angle_values.append(angle_value)


# 提取时间字符串中的数字并转换为整数，存储在列表中
for i in range(0, len(times)):
    num.append(i)

