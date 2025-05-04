import os
import pandas as pd
import numpy as np
import scipy.io
import matplotlib.pyplot as plt
from scipy.signal import butter, filtfilt

def normalize_data(data):
    """
    对数据进行最小-最大归一化，使其范围在 [0,1] 之间。
    """
    return (data - np.min(data)) / (np.max(data) - np.min(data))

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

def plot_loop_data(file_path, scene_name, loop_index, output_dir, normalize=False, apply_filter=True):
    """
    绘制给定场景和循环索引的系统响应、误差和滞回曲线图。
    可选择是否对 PV 和 OP 数据进行归一化和滤波。

    参数：
    file_path (str): .mat 文件路径。
    scene_name (str): 场景名称。
    loop_index (str): 循环索引（如 'loop7'）。
    output_dir (str): 输出图像的保存目录。
    normalize (bool): 是否进行归一化。
    apply_filter (bool): 是否应用滤波。

    返回：
    None
    """
    # 创建输出目录
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # 加载 .mat 文件
    mat_data = scipy.io.loadmat(file_path)

    # 提取 'cdata' 数据
    cdata = mat_data['cdata']

    # 提取指定场景和循环数据
    try:
        scene_data = cdata[scene_name][0][0]  # 提取指定场景数据
        loop_data = scene_data[loop_index]  # 提取指定循环数据

        # 提取 PV, OP, t, SP 数据
        PV_raw = np.squeeze(loop_data[0][0][0][0][4])
        OP_raw = np.squeeze(loop_data[0][0][0][0][5])
        t = np.squeeze(loop_data[0][0][0][0][6])
        SP = np.squeeze(loop_data[0][0][0][0][7])

        # 是否进行归一化
        if normalize:
            PV = normalize_data(PV_raw)
            OP = normalize_data(OP_raw)
            norm_suffix = "_norm"
        else:
            PV = PV_raw
            OP = OP_raw
            norm_suffix = ""

        # 是否应用滤波
        if apply_filter:
            PV = butter_lowpass_filter(PV)
            OP = butter_lowpass_filter(OP)
            filter_suffix = "_filtered"
        else:
            filter_suffix = ""


        loop_name="POW"

        # 计算 |PV(k) - PV(k-1)|
        PV_k1 = PV[1:]  # PV(k)
        PV_k0 = PV[:-1]  # PV(k-1)
        diff = PV_k1-PV_k0

        # 取PV(k)
        OP_k = OP[:-1]
        #
        plt.figure(figsize=(8, 8))
        plt.plot(diff, OP_k, marker="o", markersize=4, linestyle="None")
        plt.xticks([])
        plt.yticks([])
        plt.savefig(os.path.join(output_dir, f"{loop_name}{i}{norm_suffix}{filter_suffix}_S2.svg"), format="svg")
        plt.clf()

    except KeyError as e:
        print(f"Error: Key '{e.args[0]}' not found in data. Please check the scene_name and loop_index.")

# 示例调用
file_path = r'/home/shangchao/Downloads/StictionGPT/data/ISDB/isdb10.mat'
scene_name = "power"

for i in range(1, 5):
    loop_index = f"loop{i}"
    output_dir = f"./fig_sigmoid/POW{i}"
    plot_loop_data(file_path, scene_name, loop_index, output_dir, normalize=1, apply_filter=0)
