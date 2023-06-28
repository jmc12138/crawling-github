from datetime import datetime, timedelta
import requests
import tqdm,utils
from fake_useragent import UserAgent

import urllib3,os,json,time
urllib3.disable_warnings()


# 按日期爬取github上和关键字相关的仓库 因为github一次最多返回1e3个数据，所以按日期划分开来爬取

def date_generator(start_date, end_date):
    current_date = start_date
    while current_date <= end_date:
        yield  current_date.strftime("%Y-%m-%d")
        current_date += timedelta(days=1)



key = 'SSL'
# SSL+created%3A2023-01-01

url_str = lambda x: f'https://api.github.com/search/repositories?q={key}+created%3A{x}&sort=starts'

unmatched_str = 'Your search did not match any repositories'
ua = UserAgent()

Token = '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'

'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'

tokens = utils.Token()

sleep_time = tokens.sleep_time()

headers = {'User-Agent': ua.random,
               'Authorization': f'token {tokens.next_token()}',
               'Content-Type': 'application/json',
               'method':'GET',
               'Accept': 'application/json'
               }

start_date = datetime(2017, 9, 29)
end_date = datetime(2023, 6, 27)
current_date = start_date
while True:
    try:

        for date in date_generator(start_date, end_date):
            json_path = os.path.join(utils.repo_json_dir_path,f'{key}_{date}.json')
            url = url_str(date)
            current_date = date
            response = requests.get(url,headers = headers,verify=False)
            response_dict = response.json() 
            with open(json_path,'w',encoding='utf-8') as f:
                json.dump(response_dict,f)
            print(f'\r {date}/{end_date}',end='')
            time.sleep(sleep_time)
    except:
        print('')
        print('重试！')
        start_date = current_date
        time.sleep(5)


# for date in date_generator(start_date, end_date):
#     json_path = os.path.abspath(os.path.join(utils.repo_json_dir_path,f'{key}_{date}.json'))
#     url = url_str(date)
#     print(url)
#     current_date = date
#     response = requests.get(url,headers = headers,verify=False)
#     response_dict = response.json() 
#     with open(json_path,'w',encoding='utf-8') as f:
#         json.dump(response_dict,f)
#     print(f'\r {date}/{end_date}',end='')
#     time.sleep(7)