# 根据star数筛选仓库

import json,os,tqdm,utils



repo_path = utils.last_repos_path
root_path = utils.repo_json_dir_path

stars = 50
repo_star_path = os.path.join(utils.github_dataset_path,f'repo_star{stars}.json')
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