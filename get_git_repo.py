

from git import Repo
import time,os,json
import utils,tqdm
import shutil



true_data_path = utils.true_repos_path
with open(true_data_path,'r',encoding='utf-8') as f:
    data =json.load(f)

current_item = []

while current_item != data['items'][-1]:
    # e.g. https://github.com/x2on/OpenSSL-for-iPhone
    try:
        for item in tqdm.tqdm(data['items']):
            current_item = item
            url = item['html_url']
            name = str(item['id'])
            save_folder = os.path.join(utils.repo_dir_path,name)

            if os.path.exists(save_folder):
                continue

            Repo.clone_from(url, save_folder)
    except:
        shutil.rmtree(save_folder)
