# 读取最初的文件内容，并将内容转换为十六进制字符串，保存到文件中


# 以二进制方式读取文件内容
with open('data/WIT00000.TXT', 'rb') as file:
    file_content = file.read()

# 将字节内容转换为十六进制字符串，并用空格隔开
hex_string = ' '.join([f'{byte:02x}'.upper() for byte in file_content])

# 保存到文件中
with open('hex_data/WIT00000_hex.txt', 'w') as file:
    file.write(hex_string)