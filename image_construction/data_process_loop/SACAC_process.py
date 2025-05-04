import os
import numpy as np
import scipy.io
import matplotlib.pyplot as plt
from scipy.signal import butter, filtfilt
import pandas as pd
# 指定输入和输出文件夹
input_dir = r"/home/xtc/NewDisk/file/StictionGPT/data/SACAC"  # 替换为你的CSV文件夹路径

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


def butter_lowpass_filter(data, cutoff=0.1, fs=1.0, order=3):
    """
    应用Butterworth低通滤波。

    参数：
    data (array): 输入数据。
    cutoff (float): 截止频率。
    fs (float): 采样频率。
    order (int): 滤波器阶数。

    返回：
    滤波后的数据。
    """
    nyquist = 0.5 * fs
    normal_cutoff = cutoff / nyquist
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    y = filtfilt(b, a, data)
    return y

# 遍历所有CSV文件
for i, filename in enumerate(os.listdir(input_dir)):
    if filename.endswith(".csv"):
        file_path = os.path.join(input_dir, filename)
        df = pd.read_csv(file_path, sep=";")

        SP = df["SP"]
        PV_raw = df["PV"]
        OP_raw = df["OP"]
        PV = normalize_data(PV_raw)
        OP = normalize_data(OP_raw)
        PV = butter_lowpass_filter(PV)
        OP = butter_lowpass_filter(OP)
        loop_name = filename.split('.')[0]  # 取文件名作为循环名称
        norm_suffix = "_norm"  # 正常化后缀（可根据需要修改）
        filter_suffix = "_filtered"  # 过滤后缀（可根据需要修改）
        output_dir = f"/home/xtc/NewDisk/file/StictionGPT/fig/{loop_name}"
        os.makedirs(output_dir, exist_ok=True)
        # 绘制 PV, SP, OP 的时间序列图
        plt.figure(figsize=(12, 4))
        plt.plot(range(len(PV)), PV)
        plt.plot(range(len(OP)), OP, color="orange", alpha=0.7)
        plt.xticks([])
        plt.yticks([])
        plt.savefig(os.path.join(output_dir, f"{loop_name}_PV_SP_OP_t{norm_suffix}{filter_suffix}_v3.svg"), format="svg")
        plt.clf()

        # 绘制滞回曲线，使用原始数据
        plt.figure(figsize=(8, 8))
        plt.plot(OP, PV, marker="o", markersize=4, linestyle="None")
        plt.xticks([])
        plt.yticks([])
        plt.savefig(os.path.join(output_dir, f"{loop_name}_OP_PV_{norm_suffix}{filter_suffix}_v3.svg"), format="svg")
        plt.clf()

