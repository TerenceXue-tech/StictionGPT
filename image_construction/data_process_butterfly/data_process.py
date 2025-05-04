import pandas as pd
import numpy as np
import scipy.io
import matplotlib.pyplot as plt

def normalize_data(data):
    """
    对数据进行最小-最大归一化，使其范围在 [0,1] 之间。
    如果数据的最大值与最小值相等，则返回零数组。
    """
    min_val = np.min(data)
    max_val = np.max(data)
    if max_val == min_val:
        return np.zeros_like(data)
    return (data - min_val) / (max_val - min_val) 
# 加载 .mat 文件
file_path = r'/home/xtc/NewDisk/file/StictionGPT/data/ISDB/isdb10.mat'
mat_data = scipy.io.loadmat(file_path)

# 提取 'cdata' 数据
cdata = mat_data['cdata']

# 提取 chemicals 场景的第七个 loop 数据
scene_name = "pulpPapers"
loop_index = "loop3"

# Access the data
chemicals_data = cdata[scene_name][0][0]  # 提取 chemicals 场景数据
loop7_data = chemicals_data[loop_index]  # 提取第七个 loop 数据
print(loop7_data)
PV=loop7_data[0][0][0][0][6]
OP=loop7_data[0][0][0][0][7]
t=loop7_data[0][0][0][0][4]
SP=loop7_data[0][0][0][0][5]
t = np.squeeze(t)  # 时间
PV = np.squeeze(PV)  # 过程变量
OP = np.squeeze(OP)  # 控制器输出
SP = np.squeeze(SP)  # 设定点

PV=normalize_data(PV)
OP=normalize_data(OP)
# 计算 |OP(k) - PV(k-1)|
OP_shifted = OP[1:]  # OP(k)
PV_shifted = PV[:-1]  # PV(k-1)
diff = np.abs(OP_shifted - PV_shifted)

# 取PV(k)
PV_k = PV[1:]


#
plt.figure(figsize=(8, 8))
plt.plot(PV_k, diff,marker="o", markersize=4, linestyle="None")
plt.xticks([])
plt.yticks([])
plt.show()