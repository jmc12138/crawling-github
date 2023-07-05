
import utils,time

import json,os,tqdm,utils,copy,sys
from functools import partial
from p_tqdm import p_map,p_umap
import multiprocessing
import threading
import asyncio
import glob

paths =glob.glob(os.path.join(utils.commits_dir,'*.json'))

true_data = {}
all_ans = {}
for path in tqdm.tqdm(paths):
    with open(path,'r',encoding='utf-8') as f:
        data = json.load(f)
    id = data['id']
    if id not in true_data:
        true_data[id] = []
    if data['isTrue']:
        true_data[id].append({"sha": data['sha'],'message':data['message'], "isTrue": data['isTrue']})
    if id not in all_ans:
        all_ans[id] = []

    all_ans[id].append(data)

with open(utils.ans_commits_path,'w',encoding='utf-8') as f:
    json.dump(all_ans,f)


with open(utils.true_commits_path,'w',encoding='utf-8') as f:
    json.dump(true_data,f)

