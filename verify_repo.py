# 验证爬取的仓库全不全

import json,os,tqdm

verify_path = 'verify_repo.json'

def get_all_files(folder_path):
    file_paths = []
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            file_paths.append(file_path)
    return file_paths

verify_json = {'items':[]}

root_path = 'jsons'
for path in tqdm.tqdm(get_all_files(root_path)):
    with open(path,'r',encoding='utf-8') as f:
        data = json.load(f)
    if len(data['items']) != int(data['total_count']):
        data.update({'path':path})
        verify_json['items'].append(data)


print(len(verify_json['items']))

