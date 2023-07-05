# 根据star数筛选仓库
# 废弃不用，下次直接向github爬取时只爬stars>50的项目
import json,os,tqdm,utils



repo_path = utils.all_repos_path
root_path = utils.repo_json_dir_path

stars = 50
repo_star_path = utils.repos_path
with open(repo_path,'r',encoding='utf-8') as f:
    data = json.load(f)

filter = {'total_count':0,'items':[]}

for item in tqdm.tqdm(data['items']):
    if item['stargazers_count'] >= stars:
        filter['items'].append(item)
        filter['total_count'] += 1


with open(repo_star_path,'w',encoding='utf-8') as f:
    json.dump(filter,f)  


count = filter['total_count']
print(f'total_count: {count}')