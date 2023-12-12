import pandas as pd
import numpy as np
from datetime import datetime, timedelta
# ---------------------------功能函数-----------------------------------

# 处理角度数据
def angle_process(hexdata):
    rxl = hexdata[1]
    rxh = hexdata[2]
    ryl = hexdata[3]
    ryh = hexdata[4]
    rzl = hexdata[5]
    rzh = hexdata[6]

    # 将两个字节的数据组合为一个16位的整数，然后按比例缩放
    angle_x = (rxh * 256 + rxl) / 32768 * 180
    angle_y = (ryh * 256 + ryl) / 32768 * 180
    angle_z = (rzh * 256 + rzl) / 32768 * 180

    # print('angle_x: ', angle_x)
    # print('angle_y: ', angle_y)
    # print('angle_z: ', angle_z)
    return angle_z


# 处理时间数据
def time_process(hexdata):
    year = hexdata[1]
    month = hexdata[2]
    day = hexdata[3]
    hour = hexdata[4]
    minute = hexdata[5]
    second = hexdata[6]
    # print(str(year) + '-' +str(month) + '-' + str(day) + ' ' + str(hour) + ':' + str(minute) + ':' + str(second))
    return [month, day, hour, minute, second]
# -----------------------------------------------------------------------

# 以二进制方式读取文件内容
with open('for_imu/data/WIT00060.TXT', 'rb') as file:
    file_content = file.read()

# 将字节内容转换为十六进制字符串，并用空格隔开
hex_string = ' '.join([f'{byte:02x}'.upper() for byte in file_content])
# 将字符串按照55分割为数据块
hex_strings = hex_string.split('55')
hex_strings = hex_strings[1:]

hex_strings_final = []
temp_hex_string = ''

#去除字符串前后的空格
for i in range(0,len(hex_strings)):
    hex_strings[i] = hex_strings[i].strip()

# 防止数据中有 55
for hex_string in hex_strings:
    if(len(hex_string) == 29):
        hex_strings_final.append(hex_string)
    elif(len(hex_string) < 29):
        if(len(temp_hex_string) > 0):
            if(len(hex_string)>0):     
                temp_hex_string = temp_hex_string + ' 55 '+  hex_string 
            else:
                temp_hex_string = temp_hex_string + ' 55'
        else:
            temp_hex_string = hex_string
        if(len(temp_hex_string) == 29):
            hex_strings_final.append(temp_hex_string)
            temp_hex_string = ''

        
time = []
angle = []

# 获得时间数据
for hex_string in hex_strings_final:
    hex_strings_split = hex_string.split(' ')
    values = [int(hex_string_split, 16) for hex_string_split in hex_strings_split]
    hex_values = [hex(value) for value in values]

    # 时间数据
    if hex_strings_split[0]=='50':      
        # print(values)
        time.append(time_process(values))
    # 角度数据
    if hex_strings_split[0]=='53':
        # print(values)
        angle.append(angle_process(values))

temp_time = np.sum(np.array(time[1]))
time_list = []
angle_list = []
seconds = 0
time_flag = 0

# 合并同一秒的时间数据和角度数据
for i in range(0,len(time)):
    if(np.sum(np.array(time[i])) == temp_time and time_flag == 0):
        time_list.append(time[i])
        angle_list.append(angle[i])
        time_flag = 1
    elif(np.sum(np.array(time[i])) != temp_time and time_flag == 1):
        seconds = seconds + 1
        temp_time = np.sum(np.array(time[i]))
        time_flag = 0
       
print(time_list)
print(len(angle_list))

times_v2 = []
# 提取字符串中的数字并转换为整数，存储在列表中
for i in range(0, len(time_list)):
    temp = [int(num) for num in str(time_list[i]).strip('[]').split(', ')]
    times_v2.append(temp)


# 将列表中的数字转换为日期时间对象
for i in range(0, len(times_v2)):
    times_v2[i] = datetime(year=2023, month=times_v2[i][0], day=times_v2[i][1], hour=times_v2[i][2], minute=times_v2[i][3], second=times_v2[i][4]) -  timedelta(minutes=3, seconds=6)


# 将数据保存为csv文件
data = {'ID':'0f', 'Time': times_v2, 'Angle': angle_list}
df = pd.DataFrame(data)
# 保存时tagid要进行更改
df.to_csv('for_imu/imu_data_01.csv', index=False, encoding='utf-8')





