from datetime import datetime, timedelta
import requests
import tqdm
import urllib3,os,json,time
urllib3.disable_warnings()




def date_generator(start_date, end_date):
    current_date = start_date
    while current_date <= end_date:
        yield  current_date.strftime("%Y-%m-%d")
        current_date += timedelta(days=1)



key = 'SSL'
# SSL+created%3A2023-01-01

url_str = lambda x: f'https://api.github.com/search/repositories?q={key}+created%3A{x}&sort=starts'

unmatched_str = 'Your search did not match any repositories'

Token = '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'
headers = {'User-Agent': 'Mozilla/5.0',
               'Authorization': f'token {Token}',
               'Content-Type': 'application/json',
               'method':'GET',
               'Accept': 'application/json'
               }

start_date = datetime(2015, 2, 9)
end_date = datetime(2023, 6, 27)
current_date = start_date
while True:
    try:

        for date in date_generator(start_date, end_date):
            json_path = os.path.join('jsons',f'{key}_{date}.json')
            url = url_str(date)
            current_date = date
            response = requests.get(url,headers = headers,verify=False)
            response_dict = response.json() 
            with open(json_path,'w',encoding='utf-8') as f:
                json.dump(response_dict,f)
            print(f'\r {date}/{end_date}',end='')
            time.sleep(7)
    except:
        print('')
        print('重试！')
        start_date = current_date
        time.sleep(5)

