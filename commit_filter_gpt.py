

from git import Repo
import time,os,json
import utils,tqdm





commit_path = os.path.join(utils.github_dataset_path,'all_commits.json')
with open(commit_path,'r',encoding='utf-8') as f:
    commit_data = json.load(f)


all_data = {}



# e.g. https://github.com/x2on/OpenSSL-for-iPhone
for item in tqdm.tqdm(commit_data):
    for commit in item:

        desc = commit['description']
        question = f'Here is some information about a repository if this repository has any connection to the SSL protocol Just answer True or False {desc}'

        ans = utils.get_gpt_ans2(question)
        all_data[id] = ans
        if ans:
            true_filter['items'].append(data)
            true_filter['total_count'] += 1
        else:
            false_filter['items'].append(data)
            false_filter['total_count'] += 1


