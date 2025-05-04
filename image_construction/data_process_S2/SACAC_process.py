import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import butter, filtfilt
import pandas as pd
# 指定输入和输出文件夹
input_dir = r"/home/shangchao/Downloads/StictionGPT/data/SACAC"  # 替换为你的CSV文件夹路径

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
        # PV = butter_lowpass_filter(PV)
        # OP = butter_lowpass_filter(OP)
        loop_name = filename.split('.')[0]  # 取文件名作为循环名称
        norm_suffix = "_norm"  # 正常化后缀（可根据需要修改）
        filter_suffix = ""  # 过滤后缀（可根据需要修改）
        output_dir = f"/home/shangchao/Downloads/StictionGPT/fig_sigmoid/{loop_name}"
        os.makedirs(output_dir, exist_ok=True)
                # 计算 |PV(k) - PV(k-1)|
        print(PV)
        PV_k1 = np.array(PV[1:]) # PV(k)
        PV_k0 = np.array(PV[:-1])  # PV(k-1)
        diff = PV_k1-PV_k0

        # 取PV(k)
        OP_k = np.array(OP[:-1])
        # min_len = min(len(OP_k), len(diff))
        # OP_k = OP_k[:min_len]
        # diff = diff[:min_len]
        # print(PV_k1)
        # print(PV_k0)
        # print(diff)
        # print(OP_k)

        
        plt.figure(figsize=(8, 8))
        plt.plot(diff, OP_k, marker="o", markersize=4, linestyle="None")
        # 自动调整轴范围以容纳所有点
        plt.autoscale()
        plt.xticks([])
        plt.yticks([])
        plt.savefig(os.path.join(output_dir, f"{loop_name}{norm_suffix}{filter_suffix}_S2.svg"), format="svg")
        plt.clf()

