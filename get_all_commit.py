

from git import Repo
import time,os,json
import utils,tqdm


def get_all_commits(folder_path):
    repo = Repo(folder_path)
    data = {}
    all_data = []
    # 遍历commit历史记录并打印信息
    for commit in repo.iter_commits():
        data['sha'] = commit.hexsha
        data['Message'] = commit.message
        all_data.append(data)
    return [dict(t) for t in {tuple(sorted(d.items())) for d in all_data}]



stars = 50
true_data_path = os.path.join(utils.github_dataset_path,f'true_repo_star{stars}.json')
with open(true_data_path,'r',encoding='utf-8') as f:
    data =json.load(f)

save_path = os.path.join(utils.github_dataset_path,'all_commits.json')

commit_data = {}


# e.g. https://github.com/x2on/OpenSSL-for-iPhone
for item in tqdm.tqdm(data['items']):
    url = item['html_url']
    name = str(item['id'])
    save_folder = os.path.join(utils.repo_dir_path,name)

    commit_data[name] = get_all_commits(save_folder)

with open(save_path,'w',encoding='utf-8') as f:
    json.dump(commit_data,f)
