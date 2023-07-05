import os,json,requests
from datetime import datetime, timedelta
from fake_useragent import UserAgent
import time,yaml
import selenium

import requests
import openai
import tiktoken,aiohttp

github_dataset_path = os.path.abspath(r'../github_dataset/')
repo_json_dir_path = os.path.join(github_dataset_path,'repo_jsons')
all_repos_path = os.path.join(github_dataset_path,'repos.json')
repo_dir_path = os.path.join(github_dataset_path,'repos')

repos_path = os.path.join(github_dataset_path,'repos.json')
true_repos_path = os.path.join(github_dataset_path,'true_repos.json')
false_repos_path = os.path.join(github_dataset_path,'false_repos.json')
ans_repos_path = os.path.join(github_dataset_path,'ans_repos.json')

commits_path =  os.path.join(github_dataset_path,'commits.json')
true_commits_path =  os.path.join(github_dataset_path,'true_commits.json')
false_commits_path =  os.path.join(github_dataset_path,'false_commits.json')
ans_commits_path = os.path.join(github_dataset_path,'ans_commits.json')

commits_dir = os.path.join(github_dataset_path,'commits_json')

log_path = os.path.join(commits_dir,'log.json')

if not os.path.exists(commits_dir):
    os.mkdir(commits_dir)


tokenizer  = tiktoken.encoding_for_model("gpt-3.5-turbo")

def crop_string_to_token(string, target_tokens):
    
    tokens = tokenizer.encode(string)

    if len(tokens) <= target_tokens:
        cropped_string = string
    else:
        cropped_tokens = tokens[:target_tokens]
        cropped_string = tokenizer.decode(cropped_tokens)
    
    return cropped_string

def get_gpt_ans(_str):
    max_token_len = 4000
    _str = crop_string_to_token(_str,max_token_len)
    # openai.log = "debug"

    openai.api_key = "sk-Mxf9RVb3QOTKl2ULJFiS4xj9FoBRsU3oisc6OwxMSJciY0wf"
    openai.api_base = "https://api.chatanywhere.com.cn/v1"
    # openai.api_key = "sk-7QaU4osZkxiqW2B7F0B4AfB318F34b64912aB5C3E195A312"
    # openai.api_base = "https://api.open.passingai.com/v1"
  
    completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=[{"role": "user", "content": _str}],timeout = 3)
    return completion.choices[0].message.content

async def async_get_gpt_ans(_str):
    max_token_len = 4000
    _str = crop_string_to_token(_str,max_token_len)
    # openai.log = "debug"

    openai.api_key = "sk-Mxf9RVb3QOTKl2ULJFiS4xj9FoBRsU3oisc6OwxMSJciY0wf"
    openai.api_base = "https://api.chatanywhere.com.cn/v1"
    # openai.api_key = "sk-7QaU4osZkxiqW2B7F0B4AfB318F34b64912aB5C3E195A312"
    # openai.api_base = "https://api.open.passingai.com/v1"
    async with aiohttp.ClientSession() as session:
        completion = await openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=[{"role": "user", "content": _str}],timeout = 3)
    return completion.choices[0].message.content


def get_gpt_ans2(_str):
    times = 0

    ans = get_gpt_ans(_str)
    ans5 = ans[:4].lower()
    if 'true' in ans5: 
        return 1,ans
    if 'fals' in ans5: 
        return 0,ans

    return 0,ans





edgedriver_path = r'E:\edgedriver\msedgedriver.exe'
chromedriver_path = r'E:\chrome_driver\chromedriver.exe'
class Token():

    def __init__(self) -> None:
        self.tokens = self.__get_tokens()
        self.__sleep_time = 6 / len(self.tokens) + 0.2
        self.tokens_used_count = self.init_count()
        self.max_count = 10

        self.total_index = 0

        self.little_len = len(self.tokens)
        self.current_token = ''
        self.keys =  list(self.tokens.keys())

    def init_count(self):
        return {key: 0 for key in self.tokens.keys()}

    def __get_tokens(self):
        with open('Token.yml','r',encoding='utf-8') as f:
            tokens = yaml.safe_load(f)
        return tokens
    def next_token(self):

        current_key_index = self.total_index %  self.little_len
        # print(current_key_index)
        current_key = self.keys[current_key_index]
        self.current_token = self.tokens[current_key]
        self.total_index += 1
        return self.current_token
    
    def current_token(self):
        return self.current_token

    def sleep_time(self):
        return self.__sleep_time
    


global tokens
global sleep_time
global ua
tokens = Token()
sleep_time = tokens.sleep_time()
ua = UserAgent()

def get_all_json(_dict,surl):
    if _dict['total_count'] <= 100:
        return _dict
    else:
        page_num = _dict['total_count'] // 100 + 1
        for idx in range(2,page_num+1):
            url = surl.replace('&page=1',f'&page={idx}')
            # print(url)
            response = requests.get(url,headers = get_headers(),verify=False)
            response_dict = response.json()
            # print(response_dict.keys())
            # print(response_dict)
            # print(len(response_dict['items']))
            _dict['items'].extend(response_dict['items'])

    return _dict





def get_headers():
    token = tokens.next_token()
    # print(token)
    headers = {'User-Agent': ua.random,
               'Authorization': f'token {token}',
               'Content-Type': 'application/json',
               'method':'GET',
               'Accept': 'application/json'
               }
    time.sleep(sleep_time)
    return headers

def date_generator(start_date, end_date):
    current_date = start_date
    while current_date <= end_date:
        yield  current_date.strftime("%Y-%m-%d")
        current_date += timedelta(days=1)



def get_all_files(folder_path):
    file_paths = []
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            file_paths.append(file_path)
    return file_paths





if __name__ == '__main__':
    print(github_dataset_path)
    print(repo_json_dir_path)
    tokens = Token()
    print(tokens.sleep_time())
    for i in range(52):
        tokens.next_token()