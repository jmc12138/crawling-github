

import utils,time

import json,os,tqdm,utils,copy,sys
from functools import partial
from p_tqdm import p_map,p_umap
import multiprocessing
import threading
import asyncio,openai,aiohttp



async def async_get_gpt_ans(_str):
    max_token_len = 4000
    _str = utils.crop_string_to_token(_str,max_token_len)
    # openai.log = "debug"

    openai.api_key = "sk-Mxf9RVb3QOTKl2ULJFiS4xj9FoBRsU3oisc6OwxMSJciY0wf"
    openai.api_base = "https://api.chatanywhere.com.cn/v1"
    # openai.api_key = "sk-7QaU4osZkxiqW2B7F0B4AfB318F34b64912aB5C3E195A312"
    # openai.api_base = "https://api.open.passingai.com/v1"
    async with aiohttp.ClientSession() as session:
        completion = await openai.ChatCompletion.acreate(model="gpt-3.5-turbo", messages=[{"role": "user", "content": _str}],timeout = 3)
    ans = completion.choices[0].message.content

    ans4 = ans[:4].lower()
    if 'true' in ans4: 
        return 1,ans
    if 'fals' in ans4: 
        return 0,ans

    return 0,ans





async def get_ans(id,sha,message):
    path = os.path.join(utils.commits_dir,f'{id}_{sha}.json')
    path = os.path.join(utils.commits_dir,path)
    question = f'{message} The above is the commit message of a commit on GitHub. answer with only True or False:  Is this a commit  of vulnerability patch?'
    isTrue,ans = await async_get_gpt_ans(question)
    save_dict = {'id':id,'sha':sha,'isTrue':isTrue,'message':message,'ans':ans}
    with open(path,'w',encoding='utf-8') as f:
        json.dump(save_dict,f)
    



async def task(items):
    len_items = len(items)
    pid = os.getpid()
    for idx,item in enumerate(items):
        sha = item['sha']
        id = item['id']
        path = os.path.join(utils.commits_dir,f'{id}_{sha}.json')
        if not os.path.exists(path):


            try:
                task = asyncio.ensure_future(get_ans(id,sha,item['Message']))
                await asyncio.wait_for(task, timeout=3) 
            except Exception as e:
                print(e)
                try:
                    task.cancel()  # 取消超时的协程
                    await task  # 等待被取消的协程真正结束
                except asyncio.CancelledError:
                    pass
            print(f"processs{pid}:  {idx}/{len_items}")

def main(items):
    loop = asyncio.get_event_loop()
    loop.run_until_complete(task(items))         

if __name__ == '__main__':

    with open(utils.commits_path,'r',encoding='utf-8') as f:
        commits_data = json.load(f)


    data = []

    for id,items in commits_data.items():
        for item in items:
            item.update({'id':id})
            data.append(item)

    print(' 数据准备完成==============')

    num_processes = 8
    chunk_size = len(data) // num_processes
    chunks = [data[i:i+chunk_size] for i in range(0, len(data), chunk_size)]

    # main(chunks[0])    
    pool = multiprocessing.Pool(processes=num_processes)
    # 将任务分配给各个进程
    results = pool.map(main,chunks)
    # 关闭进程池
    pool.close()
    pool.join()
    print('处理完成')