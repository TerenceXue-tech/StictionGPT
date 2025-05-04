import os
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
        PV_raw = np.squeeze(loop_data[0][0][0][0][5])
        OP_raw = np.squeeze(loop_data[0][0][0][0][6])
        t = np.squeeze(loop_data[0][0][0][0][7])
        SP = np.squeeze(loop_data[0][0][0][0][4])

        # 是否进行归一化
        if normalize:
            PV = normalize_data(PV_raw)
            OP = normalize_data(OP_raw)
            PV = butter_lowpass_filter(PV)
            OP = butter_lowpass_filter(OP)
            norm_suffix = "_norm"
        else:
            PV = PV_raw
            OP = OP_raw
            norm_suffix = ""

        # 是否应用滤波
        if apply_filter:
            PV2 = butter_lowpass_filter(PV_raw)
            OP2 = butter_lowpass_filter(OP_raw)
            filter_suffix = "_filtered"
        else:
            filter_suffix = ""
        loop_name="CHEM"
        # 设置图像尺寸
        plt.figure(figsize=(12, 4))

        # 绘制 PV, SP, OP 的时间序列图
        plt.plot(t, PV)
        # plt.plot(t, PV, label="Process Variable (PV)")
        # plt.plot(t, SP, label="Set Point (SP)", linestyle="--", alpha=0.8)
        plt.plot(t, OP, color="orange", alpha=0.7)
        plt.xticks([])
        plt.yticks([])
        # plt.plot(t, OP, label="Controller Output (OP)", color="orange", alpha=0.7)
        # plt.xlabel("Time (s)")
        # plt.ylabel("Value")
        # plt.title("System Response and Controller Output")
        # plt.legend()
        # plt.grid()
        plt.savefig(os.path.join(output_dir, f"{loop_name}{i}_PV_SP_OP_t{norm_suffix}{filter_suffix}_v3.svg"), format="svg")
        # plt.show()
        plt.clf()

        # 绘制滞回曲线，使用原始数据
        plt.figure(figsize=(8, 8))
        plt.plot(OP, PV, marker="o", markersize=4, linestyle="None")
        plt.xticks([])
        plt.yticks([])
        # plt.plot(OP_raw, PV_raw, label="Hysteresis Loop (OP vs. PV)", marker="o", markersize=4, linestyle="None")
        # plt.xlabel("Controller Output (OP)")
        # plt.ylabel("Process Variable (PV)")
        # plt.title("Hysteresis Loop (Unfiltered)")
        # plt.grid()
        # plt.legend()
        plt.savefig(os.path.join(output_dir, f"{loop_name}{i}_OP_PV_raw_v3.svg"), format="svg")
        # plt.show()
        plt.clf()

    except KeyError as e:
        print(f"Error: Key '{e.args[0]}' not found in data. Please check the scene_name and loop_index.")

# 示例调用
file_path = r'/home/xtc/NewDisk/file/StictionGPT/data/ISDB/isdb10.mat'
scene_name = "chemicals"

for i in range(13, 18):
    loop_index = f"loop{i}"
    output_dir = f"./fig/CHEM{i}"
    plot_loop_data(file_path, scene_name, loop_index, output_dir, normalize=True, apply_filter=True)
