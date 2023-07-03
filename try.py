import utils
import tqdm,json,os

my_list = [
    {"name": "Alice", "age": 25},
    {"name": "Bob", "age": 30},
    {"name": "Alice", "age": 25},
]

# 使用集合推导式去重
unique_list = [dict(t) for t in {tuple(sorted(d.items())) for d in my_list}]

print(unique_list)