import os
import cairosvg
from PIL import Image

for i in range(1,3):
    # 指定SVG文件夹路径
    input_folder = f"/home/xtc/NewDisk/file/LLaMA-Factory/data/Stiction_data/SA-PAP{i}"  # 修改为你的SVG文件夹路径
    output_folder = input_folder  # 修改为存放JPG的文件夹
    # 检查 BAS 目录是否存在
    if not os.path.exists(input_folder):
        print(f"警告：{input_folder} 目录不存在，跳过")
        continue

    # 遍历文件夹中的所有SVG文件
    for filename in os.listdir(input_folder):
        if filename.endswith("_OP_PV_raw_v3.svg"):
            svg_path = os.path.join(input_folder, filename)
            png_path = os.path.join(output_folder, filename.replace(".svg", ".png"))
            jpg_path = os.path.join(output_folder, filename.replace(".svg", ".jpg"))

            # 将SVG转换为PNG
            cairosvg.svg2png(url=svg_path, write_to=png_path)

            # 使用PIL转换PNG为JPG
            with Image.open(png_path) as img:
                rgb_img = img.convert("RGB")
                rgb_img.save(jpg_path, quality=100)


        elif filename.endswith("_norm_filtered_v3.svg"):
            svg_path = os.path.join(input_folder, filename)
            png_path = os.path.join(output_folder, filename.replace(".svg", ".png"))
            jpg_path = os.path.join(output_folder, filename.replace(".svg", ".jpg"))

            # 将SVG转换为PNG
            cairosvg.svg2png(url=svg_path, write_to=png_path)

            # 使用PIL转换PNG为JPG
            with Image.open(png_path) as img:
                rgb_img = img.convert("RGB")
                rgb_img.save(jpg_path, quality=100)       



print("所有SVG文件已成功转换为JPG！")
