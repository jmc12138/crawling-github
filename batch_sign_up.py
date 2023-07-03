# 批量注册github账号
import utils,time
import selenium

from selenium import webdriver

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import pyperclip,yaml


start_url = 'https://github.com/join'

usrname = lambda x: f'jmc{x}jmc12138'
usremail = lambda x: f'jmc{x}@jmc12138.anonaddy.com'
pwd = '36133926Jj'
drivers = []

start_idx = 7
length = 1

tokens = {}
check_box = lambda x: f"/html/body/div[1]/div[6]/main/div/div/div[2]/div/div/form/div/dl[2]/dd/div/ul/li[{x}]/div/label/div[1]/input"


from selenium.webdriver.edge.service import Service
# from selenium.webdriver.chrome.service import Service
# edge_driver = Service(utils.edgedriver_path)

data = {}

for i in range(start_idx,start_idx+length):
    # 定位用户名输入框，并填写用户名
    # chrome_driver = Service(utils.chromedriver_path)
    edge_driver = Service(utils.edgedriver_path)
    # 设置浏览器
    options = webdriver.EdgeOptions()
    # 修改window.navigator.webdriver为undefined，防机器人识别机制，selenium自动登陆判别机制
    options.add_experimental_option('excludeSwitches', ['enable-automation'])
    options.add_argument("--disable-blink-features=AutomationControlled")
    # 更换头部
    options.add_argument('user-agent=' + utils.ua.random)

    # driver = webdriver.Chrome(options=options,service=chrome_driver)
    driver = webdriver.Edge(options=options,service=edge_driver)

    # 修改window.navigator.webdriver 值为 undefined
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    drivers.append(driver)

    driver.get(start_url)

    name_input = driver.find_element(By.XPATH, "/html/body/div[1]/div[4]/main/div/div[2]/div/form/auto-check[1]/dl/dd/input")
    name_input.send_keys(usrname(i))
    email_input = driver.find_element(By.XPATH, "/html/body/div[1]/div[4]/main/div/div[2]/div/form/auto-check[2]/dl/dd/input")
    email_input.send_keys(usremail(i))
    pwd_input = driver.find_element(By.XPATH, "/html/body/div[1]/div[4]/main/div/div[2]/div/form/password-strength/auto-check/dl/dd/input")
    pwd_input.send_keys(pwd)

    data[usrname(i)] = pwd

    while True:
        a = input('输入 1 继续')
        if a == '1':
            driver.quit()
            break


    with open('github_account.yaml', 'r') as file:
        yaml_data = yaml.safe_load(file)

    data.update(yaml_data)

    with open('github_account.yaml','w',encoding='utf-8') as f:
        yaml.safe_dump(data,f)
