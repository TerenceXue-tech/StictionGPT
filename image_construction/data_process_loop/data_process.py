import pandas as pd
import numpy as np
import scipy.io
import matplotlib.pyplot as plt
# 加载 .mat 文件
file_path = r'/home/xtc/NewDisk/file/StictionGPT/data/ISDB/isdb10.mat'
mat_data = scipy.io.loadmat(file_path)

# 提取 'cdata' 数据
cdata = mat_data['cdata']

# 提取 chemicals 场景的第七个 loop 数据
scene_name = "chemicals"
loop_index = "loop26"

# Access the data
chemicals_data = cdata[scene_name][0][0]  # 提取 chemicals 场景数据
loop7_data = chemicals_data[loop_index]  # 提取第七个 loop 数据
print(loop7_data)
PV=loop7_data[0][0][0][0][4]
OP=loop7_data[0][0][0][0][5]
t=loop7_data[0][0][0][0][6]
SP=loop7_data[0][0][0][0][7]
t = np.squeeze(t)  # 时间
PV = np.squeeze(PV)  # 过程变量
OP = np.squeeze(OP)  # 控制器输出
SP = np.squeeze(SP)  # 设定点

##plot PV-t, SP-t, OP-t
# 绘制 PV 和 SP 的时间序列图
plt.plot(t, PV, label="Process Variable (PV)")

plt.xlabel("Time (s)")
plt.ylabel("Value")
plt.title("System Response and Controller Output")
plt.legend()
plt.grid()
plt.show()

plt.plot(t, OP, label="Controller Output (OP)", color="orange", alpha=0.7)
plt.show()

# 绘制滞回曲线
plt.plot(OP, PV, label="Hysteresis Loop (OP vs. PV)", marker="o", markersize=4, linestyle="None")
plt.xlabel("Controller Output (OP)")
plt.ylabel("Process Variable (PV)")
plt.title("Hysteresis Loop")
plt.grid()
plt.legend()
plt.show()
