# 验证爬取的仓库全不全

import json,os,tqdm,utils

verify_path = 'verify_repo.json'


verify_json = {'items':[]}


for path in utils.get_all_files(utils.repo_json_dir_path):
    with open(path,'r',encoding='utf-8') as f:
        data = json.load(f)
    if "message" in data:
        data.update({'path':path})
        print(path)
        verify_json['items'].append(data)
print('-------------------------------')
for path in utils.get_all_files(utils.repo_json_dir_path):
    with open(path,'r',encoding='utf-8') as f:
        data = json.load(f)
    if "message" in data:
        continue

    if len(data['items']) != int(data['total_count']):

        print(path)
        data.update({'path':path})
        verify_json['items'].append(data)


print(len(verify_json['items']))
# print(verify_json['items'][0]["path"])

