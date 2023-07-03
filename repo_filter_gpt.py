# 用chatgpt 筛选仓库是否和  协议 相关
# 批量注册github账号
import utils,time
import selenium

from selenium import webdriver

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import pyperclip,yaml

import json,os,tqdm,utils

from selenium.webdriver.edge.service import Service



repo_path = utils.last_repos_path
root_path = utils.repo_json_dir_path
stars = 50
repo_star_path = os.path.join(utils.github_dataset_path,f'repo_star{stars}.json')
with open(repo_star_path,'r',encoding='utf-8') as f:
    repo_data = json.load(f)


true_data_path = os.path.join(utils.github_dataset_path,f'true_repo_star{stars}.json')
false_data_path = os.path.join(utils.github_dataset_path,f'false_repo_star{stars}.json')

all_data_path = os.path.join(utils.github_dataset_path,f'all_data_repo_star{stars}.json')
all_ans_path = os.path.join(utils.github_dataset_path,f'all_ans_repo_star{stars}.json')


true_filter = {'total_count':0,'items':[]}
false_filter = {'total_count':0,'items':[]}
all_data = {}
all_ans = {}


start_idx = 0
current_idx = 0

while current_idx < len(repo_data['items'])-1:
    try:
        with open(true_data_path,'r',encoding='utf-8') as f:
            true_filter = json.load(f)  

        with open(false_data_path,'r',encoding='utf-8') as f:
            false_filter = json.load(f)  


        with open(all_data_path,'r',encoding='utf-8') as f:
            all_data = json.load(f) 
        print(f'获取数据{len(all_data)}条')        
        with open(all_ans_path,'r',encoding='utf-8') as f:
            all_ans = json.load(f) 
        # print(f'获取数据{len(all_data)}条')
    except:
        pass
    try:
        for idx in tqdm.tqdm(range(start_idx,len(repo_data['items']))):
            current_idx = idx
            data = repo_data['items'][idx]
            desc = data['description']
            id = str(data['id'])
            if id in all_data:
                # print(id)
                continue
            question = f'Here is some information about a repository if this repository has any connection to the SSL protocol Just answer True or False {desc}'    
            istrue,ans = utils.get_gpt_ans2(question)
            all_data[id] = istrue
            all_ans[id] = ans
            if istrue:
                true_filter['items'].append(data)
                true_filter['total_count'] += 1
            else:
                false_filter['items'].append(data)
                false_filter['total_count'] += 1
    except Exception as e:
        print(e)
        start_idx = current_idx
        with open(true_data_path,'w',encoding='utf-8') as f:
            json.dump(true_filter,f)  

        with open(false_data_path,'w',encoding='utf-8') as f:
            json.dump(false_filter,f)  

        with open(all_data_path,'w',encoding='utf-8') as f:
            json.dump(all_data,f)  
        time.sleep(5)
        with open(all_ans_path,'w',encoding='utf-8') as f:
            json.dump(all_ans,f)  
        time.sleep(5)
    


with open(true_data_path,'w',encoding='utf-8') as f:
    json.dump(true_filter,f)  

with open(false_data_path,'w',encoding='utf-8') as f:
    json.dump(false_filter,f)  

with open(all_data_path,'w',encoding='utf-8') as f:
    json.dump(all_data,f)  

with open(all_ans_path,'w',encoding='utf-8') as f:
    json.dump(all_ans,f)  
