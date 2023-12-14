import os
import pandas as pd

# 输入文件夹和输出文件夹的相对路径
input_folder = 'D:\学习资料\实习\DYDX_data\depthdata'  # 输入文件夹位于当前工作目录下
output_folder = 'D:\学习资料\实习\DYDX_data\depthdata\datafilter'  # 输出文件夹位于当前工作目录下

# 获取输入文件夹中的所有CSV文件
input_files = [f for f in os.listdir(input_folder) if f.endswith('.csv')]

# 遍历每个CSV文件
for input_file in input_files:
    input_file_path = os.path.join(input_folder, input_file)

    # 从CSV文件加载数据
    df = pd.read_csv(input_file_path)

    # 使用groupby和cumcount来分组并获取前3个bid和ask
    df['row_num'] = df.groupby(['Timestamp', 'Type']).cumcount() + 1
    result = df[df['row_num'] <= 3]

    # 删除辅助列row_num
    result = result.drop(columns=['row_num'])

    # 更改输出文件名，加上'_filter'前缀
    output_file = input_file.replace('.csv', '_filter.csv')
    output_file_path = os.path.join(output_folder, output_file)

    # 确保输出文件夹存在
    os.makedirs(output_folder, exist_ok=True)

    # 将处理后的数据保存到新的CSV文件
    result.to_csv(output_file_path, index=False)

    print(f"Processed {input_file} and saved as {output_file}")

print("All files processed.")
