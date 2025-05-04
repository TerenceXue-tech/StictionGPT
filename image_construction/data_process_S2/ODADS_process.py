import pickle

file_path = "data/ODADS/data/test.p"

with open(file_path, "rb") as f:
    data = pickle.load(f)

print(type(data))  # 查看数据类型
print(len(data[0]))  # 打印数据内容
print(len(data[0][0]))  # 打印数据内容
print(data[0][0][0])  # 打印数据内容