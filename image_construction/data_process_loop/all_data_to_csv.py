"""从数据中提取出各个场景各个loop的描述"""


import scipy.io

# 加载 .mat 文件
file_path = r'/home/xtc/NewDisk/file/StictionGPT/data/ISDB/isdb10.mat'
mat_data = scipy.io.loadmat(file_path)

# 提取 'cdata' 数据
cdata = mat_data['cdata']

# 查看数据类型、形状和部分内容
print("Type of cdata:", type(cdata))
print("Shape of cdata:", cdata.shape)
print("type of one element:", cdata[0].dtype,cdata[0].shape)
# 访问第一个元素
element = cdata[0]

# 提取字段数据
buildings_data = element['buildings']
chemicals_data = element['chemicals']
pulpPapers_data = element['pulpPapers']
power_data = element['power']
mining_data = element['mining']
metals_data = element['metals']
testdata = element['testdata']

# 查看字段的内容和类型
print("Buildings data type:", buildings_data.dtype,buildings_data.shape)
print("Buildings data type:", buildings_data[0].dtype,buildings_data[0].shape)
print("Buildings data type:", buildings_data[0][0].dtype,buildings_data[0][0].shape)
#取出一个loop
building_element = buildings_data[0][0]
# 查看字段的内容
loop1_data = building_element['loop1']
loop2_data = building_element['loop2']

# 打印内容
print("Loop1 data type and shape:", type(loop1_data), loop1_data.shape if hasattr(loop1_data, 'shape') else 'No shape')
print("Loop1 content:", loop1_data)
print("Loop1 despription content:", loop1_data[0][0][0][0])
print("Loop1 brief despription content:", loop1_data[0][0][0][1])

import pandas as pd

# Function to extract loop descriptions for each scene (e.g., buildings, chemicals, etc.)
def extract_loop_descriptions(data):
    descriptions = []
    for scene_name in data.dtype.names:  # 遍历每个场景
        scene_data = data[scene_name][0][0]  # 获取场景数据
        for loop_name in scene_data.dtype.names:  # 遍历每个 loop
            loop_data = scene_data[loop_name][0]  # 获取 loop 数据
            # 提取 Comments 和 BriefComments
            comments = loop_data[0][0][0][0]  # 取出 Comments
            brief_comments = loop_data[0][0][0][1]  # 取出 BriefComments
            dynamic_type = loop_data[0][0][0][2]  # 取出动态类型
            sample_T = loop_data[0][0][0][3]  # 取出采样时间
            # 添加到描述列表中
            descriptions.append({
                "Scene": scene_name,
                "Loop": loop_name,
                "Comments": comments,
                "BriefComments": brief_comments,
                "dynamic_type":dynamic_type,
                "sample_T":sample_T
            })
    return descriptions

# Extract descriptions from 'cdata'
loop_descriptions = extract_loop_descriptions(cdata)

# Convert to a pandas DataFrame
df = pd.DataFrame(loop_descriptions)

# Save and display the table for the user
output_path = "./data/loop_descriptions.csv"
df.to_csv(output_path, index=False)