import h5py
import pandas as pd
import matplotlib.pyplot as plt

# 读取 HDF5 文件
file_path = '/home/xtc/NewDisk/file/StictionGPT/data/SISO_datasets/SISO-SAMP.h5'
group_name = 'FIC02_0'  # 选择数据组

# 解析 HDF5 文件
with h5py.File(file_path, 'r') as h5_file:
    group = h5_file[group_name]

    # 提取数据
    axis0 = group['axis0'][:].astype(str)  # 行索引
    axis1 = group['axis1'][:].astype(str)  # 列索引
    values = group['block0_values'][:]     # 数据内容

    # 构建 DataFrame
    df = pd.DataFrame(values, index=axis1, columns=axis0)

# 提取列数据
t = df['Time'].values.astype(float)
PV = df['PV'].values.astype(float)
OP = df['OP'].values.astype(float)

# 处理原始数据（示例数据）
OP_raw = OP  # 假设原始数据未经过滤
PV_raw = PV

# 绘制 PV 和 OP 的时间序列图
plt.figure(figsize=(12, 4))
plt.plot(t, PV, label="Process Variable (PV)")
plt.plot(t, OP, label="Controller Output (OP)", color="orange", alpha=0.7)
plt.xlabel("Time (s)")
plt.ylabel("Value")
plt.title("System Response and Controller Output")
plt.legend()
plt.grid()
plt.show()

# 绘制滞回曲线 (OP vs. PV)
plt.figure(figsize=(8, 8))
plt.plot(OP_raw, PV_raw, label="Hysteresis Loop (OP vs. PV)", marker="o", markersize=2, linestyle="None")
plt.xlabel("Controller Output (OP)")
plt.ylabel("Process Variable (PV)")
plt.title("Hysteresis Loop (Unfiltered)")
plt.grid()
plt.legend()
plt.show()
