import json,os,tqdm,utils

def get_all_files(folder_path):
    file_paths = []
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            file_paths.append(file_path)
    return file_paths

repo_data = {"items": []}
repo_path = utils.all_repos_path
root_path = utils.repo_json_dir_path
for path in tqdm.tqdm(get_all_files(root_path)):
    with open(path,'r',encoding='utf-8') as f:
        data = json.load(f)
    if "message" in data:
        continue
    repo_data['items'].extend(data['items'])

print(len(repo_data['items']))

with open(repo_path,'w',encoding='utf-8') as f:
    json.dump(repo_data,f)  