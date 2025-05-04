import pandas as pd

# Load the uploaded file
file_path = r'/home/xtc/NewDisk/file/StictionGPT/data/ISDB/loop_descriptions_all.csv'
df = pd.read_csv(file_path)

# Combine the first two columns into a new column
df['combined_col'] = df.iloc[:, 0].astype(str) + df.iloc[:, 1].astype(str)

# Drop the original first two columns
df.drop(df.columns[:6], axis=1, inplace=True)

# 删除第一列存在空值的行
df = df.dropna(subset=[df.columns[0]])
# 交换第一列和第二列
cols = df.columns.tolist()  # 获取所有列名
cols[0], cols[1] = cols[1], cols[0]  # 交换第一列和第二列的列名顺序
df = df[cols]  # 重新排列列
# Count the remaining number of rows
remaining_rows = df.shape[0]
print(remaining_rows)
processed_file_path = r'/home/xtc/NewDisk/file/StictionGPT/data/ISDB/groundtruth_and_all.csv'
df.to_csv(processed_file_path, index=False)