# 修正错误，添加缺失的乘法运算符
import numpy as np
import matplotlib.pyplot as plt

# 参数设置
fs = 1000  # 采样频率 (Hz)
t = np.linspace(0, 1, fs, endpoint=False)  # 时间轴

# 信号频率
f1 = 50   # 主要频率1
f2 = 120  # 主要频率2

# 初相随时间的周期性变化
mod_freq = 5  # 初相变化的频率 (Hz)
alpha = np.pi / 4  # 初相变化的幅度 (最大相位偏移 π/4)

# 生成周期性变化的初相
phi_t = alpha * np.sin(2 * np.pi * mod_freq * t)  # 相位调制项

# 构造信号，包含周期性变化的相位
signal = 5 + 2 * np.sin(2 * np.pi * f1 * t + phi_t) + 0.5 * np.sin(2 * np.pi * f2 * t + phi_t)

# 1. 均值归零
signal_zero_mean = signal - np.mean(signal)

# 2. 归一化到 [-1, 1] 区间
signal_normalized = signal_zero_mean / np.max(np.abs(signal_zero_mean))

# 3. FFT 分析
N = len(signal_normalized)
fft_result = np.fft.fft(signal_normalized)
freqs = np.fft.fftfreq(N, 1/fs)

# 4. 找到主频
magnitude = np.abs(fft_result)
peak_idx = np.argmax(magnitude[:N // 2])  # 仅查看正频率部分
f_peak = freqs[peak_idx]
print(f"主频为: {f_peak:.2f} Hz")

# 5. 提取一个周期
cycle_samples = int(fs / f_peak)  # 计算周期对应的采样点数
first_cycle = signal_normalized[:cycle_samples]

# 6. 延拓信号
num_repeats = 5  # 延拓5个周期
extended_signal = np.tile(first_cycle, num_repeats)

# 7. 可视化
plt.figure(figsize=(12, 6))
plt.subplot(3, 1, 1)
plt.plot(t, signal, label="原始信号")
plt.title("原始信号")
plt.xlabel("Time (s)")
plt.ylabel("Amplitude")
plt.legend()

plt.subplot(3, 1, 2)
plt.plot(t[:len(signal_normalized)], signal_normalized, label="均值归零+归一化信号", linestyle="--")
plt.title("均值归零+归一化信号")
plt.xlabel("Time (s)")
plt.ylabel("Amplitude")
plt.legend()

plt.subplot(3, 1, 3)
plt.plot(np.arange(len(extended_signal)) / fs, extended_signal, label="延拓信号")
plt.title("延拓信号")
plt.xlabel("Time (s)")
plt.ylabel("Amplitude")
plt.legend()

plt.tight_layout()
plt.show()

