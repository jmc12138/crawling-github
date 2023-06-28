from datetime import datetime, timedelta
import requests
import tqdm,utils,re
from fake_useragent import UserAgent

import urllib3,os,json,time
urllib3.disable_warnings()

 ## 因为github api 请求有速率限制 有的时候会爬不下来 ，这个代码就是搜索爬不下来的日期再爬一遍


def date_generator(start_date, end_date):
    current_date = start_date
    while current_date <= end_date:
        yield  current_date.strftime("%Y-%m-%d")
        current_date += timedelta(days=1)



key = 'SSL'
# SSL+created%3A2023-01-01

url_str = lambda x: f'https://api.github.com/search/repositories?q={key}+created%3A{x}&sort=starts&page=1&per_page=100'

unmatched_str = 'Your search did not match any repositories'




filter_date = []

pattern = r"\d{4}-\d{2}-\d{2}"


for path in utils.get_all_files(utils.repo_json_dir_path):
    with open(path,'r',encoding='utf-8') as f:
        data = json.load(f)
    if "message" in data or len(data['items']) != int(data['total_count']):
        filter_date.append(re.findall(pattern, path)[0])

     



start_idx = 0
current_idx = 0
# while True:
#     try:

#         for date_idx in tqdm.tqdm(range(start_idx,len(filter_date))):
#             date = filter_date[date_idx]
#             json_path = os.path.join(utils.repo_json_dir_path,f'{key}_{date}.json')
#             url = url_str(date)
#             current_idx = date_idx
#             response = requests.get(url,headers = utils.get_headers(),verify=False)
#             response_dict = response.json()
#             all_dict = utils.get_all_json(response_dict,url)

#             with open(json_path,'w',encoding='utf-8') as f:
#                 json.dump(all_dict,f)
#             time.sleep(utils.sleep_time)
        
#         break
#     except:
#         print('')
#         print('重试！')
#         start_idx = current_idx
#         time.sleep(5)

for date_idx in tqdm.tqdm(range(start_idx,len(filter_date))):
    date = filter_date[date_idx]
    json_path = os.path.join(utils.repo_json_dir_path,f'{key}_{date}.json')
    url = url_str(date)

    current_idx = date_idx
    response = requests.get(url,headers = utils.get_headers(),verify=False)
    response_dict = response.json()
    if 'message' in response_dict:
        print(response_dict['message'])

    print(len(response_dict['items']))
    all_dict = utils.get_all_json(response_dict,url)

    with open(json_path,'w',encoding='utf-8') as f:
        json.dump(all_dict,f)

        