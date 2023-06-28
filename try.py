from tqdm import tqdm
import time

# 定义一个生成器函数
def my_generator(n):
    for i in range(n):
        # 在适当的位置调用 tqdm 函数
        # 设置 desc 参数来描述当前任务
        # tqdm.write(f"Processing item {i+1}")
        yield i
        time.sleep(0.5)

# 使用生成器并显示进度条
for item in tqdm(my_generator(10)):
    # 在此处处理每个生成的项
    time.sleep(0.2)