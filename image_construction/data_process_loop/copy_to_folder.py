import os
import shutil

def copy_files_with_extension(src_dir, dst_dir, file_extension):
    # 遍历源目录及其子目录
    for root, dirs, files in os.walk(src_dir):
        for file in files:
            # 检查文件扩展名
            if file.endswith(file_extension):
                # 获取源文件的相对路径
                relative_path = os.path.relpath(root, src_dir)
                # 构建目标子文件夹路径
                dst_subfolder = os.path.join(dst_dir, relative_path)
                
                # 如果目标子文件夹不存在，创建它
                if not os.path.exists(dst_subfolder):
                    os.makedirs(dst_subfolder)
                
                # 构建源文件的完整路径
                src_file = os.path.join(root, file)
                # 构建目标文件的完整路径
                dst_file = os.path.join(dst_subfolder, file)
                
                # 复制文件到目标子文件夹
                shutil.copy(src_file, dst_file)
                print(f"复制: {src_file} -> {dst_file}")

# 使用示例
src_directory = '/home/shangchao/Downloads/StictionGPT/fig'  # 源文件夹
dst_directory = '/home/shangchao/Downloads/StictionGPT/fig_sigmoid'  # 目标文件夹
extension = '_norm_S.svg'  # 你想要复制的文件扩展名

copy_files_with_extension(src_directory, dst_directory, extension)
