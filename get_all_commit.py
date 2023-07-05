

from git import Repo
import time,os,json
import utils,tqdm


def get_all_commits(folder_path):
    repo = Repo(folder_path)

    all_data = []
    # 遍历commit历史记录
    for commit in repo.iter_commits():
        data = {}
        data['sha'] = commit.hexsha
        data['Message'] = commit.message
        all_data.append(data)
        # print(data)
    return all_data




true_data_path = utils.true_repos_path
with open(true_data_path,'r',encoding='utf-8') as f:
    data =json.load(f)

save_path = utils.commits_path

commit_data = {}


for item in tqdm.tqdm(data['items']):
    name = str(item['id'])
    save_folder = os.path.join(utils.repo_dir_path,name)

    commit_data[name] = get_all_commits(save_folder)



with open(save_path,'w',encoding='utf-8') as f:
    json.dump(commit_data,f)
