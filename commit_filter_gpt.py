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

import json,os,tqdm,utils,copy,sys

from selenium.webdriver.edge.service import Service





def get_data():
    with open(utils.true_commits_path,'r',encoding='utf-8') as f:
        true_commits_data = json.load(f)
    with open(utils.false_commits_path,'r',encoding='utf-8') as f:
        false_commits_data = json.load(f)
    with open(utils.ans_commits_path,'r',encoding='utf-8') as f:
        ans_commits_data = json.load(f)
    with open(utils.ans_commits_path,'r',encoding='utf-8') as f:
        ans_commits_data = json.load(f)
    with open(utils.log_path,'r',encoding='utf-8') as f:
        log_data = json.load(f)
    return true_commits_data,false_commits_data,ans_commits_data,log_data

def save_data(true_commits_data,false_commits_data,ans_commits_data,log_data):
    with open(utils.true_commits_path,'w',encoding='utf-8') as f:
        json.dump(true_commits_data,f)
    with open(utils.false_commits_path,'w',encoding='utf-8') as f:
        json.dump(false_commits_data,f)
    with open(utils.ans_commits_path,'w',encoding='utf-8') as f:
        json.dump(ans_commits_data,f)
    with open(utils.log_path,'w',encoding='utf-8') as f:
        log_data = json.dump(log_data,f)


with open(utils.commits_path,'r',encoding='utf-8') as f:
    commits_data = json.load(f)

true_commits_data = {}
false_commits_data = {}
ans_commits_data = {}
log_data = {'shas':[]}
for id in commits_data.keys():
    true_commits_data[id] = []
    false_commits_data[id] = []
    ans_commits_data[id] = []




current_id = 0

sorted_keys = list(commits_data.keys())

sorted_keys.append(1)

while current_id != sorted_keys[-1]:
    count =0
    try:
        true_commits_data,false_commits_data,ans_commits_data,log_data = get_data()
    except:
        pass
    try:
        for id in tqdm.tqdm(sorted_keys,desc='仓库'):
            current_id = id
            range2 = tqdm.tqdm(commits_data[id], desc='commits', leave=False)
            for item in range2:
                if item['sha'] in log_data['shas']:

                    continue
                msg = item['Message']
                question = f'{msg} The above is the commit message of a commit on GitHub. answer with only True or False:  Is this a commit  of vulnerability patch?'
                isTrue,ans = utils.get_gpt_ans2(question)   

                if isTrue:
                    true_commits_data[id].append(item)
                else:
                    false_commits_data[id].append(item)
                ans_item =  copy.deepcopy(item)
                ans_item['ans'] = ans
                ans_commits_data[id].append(ans_item)
                log_data['shas'].append(item['sha'])
                desc = f'commit {count}: {ans}'
                range2.set_description(desc)
                count+=1
                if count %50 == 0:
                    save_data(true_commits_data,false_commits_data,ans_commits_data,log_data)
    except Exception as e:
        print(e)
        save_data(true_commits_data,false_commits_data,ans_commits_data,log_data)


save_data(true_commits_data,false_commits_data,ans_commits_data,log_data)


# for id in tqdm.tqdm(sorted_keys,desc='仓库'):
#     current_id = id
#     for item in tqdm.tqdm(commits_data[id], desc='commits', leave=False):
#         if item in log_data['shas']:
#             continue
#         isTrue,ans = utils.get_gpt_ans2(item['Message'])

#         if isTrue:
#             true_commits_data[id].append(item)
#         else:
#             false_commits_data[id].append(item)
#         ans_item =  copy.deepcopy(item)
#         ans_item['ans'] = ans
#         ans_commits_data[id].append(ans_item)
#         log_data['shas'].append(item['sha'])


