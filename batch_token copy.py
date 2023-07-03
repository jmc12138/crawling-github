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

start_idx = 4
length = 1

tokens = {}
check_box = lambda x: f"/html/body/div[1]/div[6]/main/div/div/div[2]/div/div/form/div/dl[2]/dd/div/ul/li[{x}]/div/label/div[1]/input"


# from selenium.webdriver.edge.service import Service
from selenium.webdriver.chrome.service import Service
# edge_driver = Service(utils.edgedriver_path)



for i in range(start_idx,start_idx+length):
    # 定位用户名输入框，并填写用户名
    chrome_driver = Service(utils.chromedriver_path)
    # 设置浏览器
    options = webdriver.ChromeOptions()
    # 修改window.navigator.webdriver为undefined，防机器人识别机制，selenium自动登陆判别机制
    options.add_experimental_option('excludeSwitches', ['enable-automation'])
    options.add_argument("--disable-blink-features=AutomationControlled")
    # 更换头部
    options.add_argument('user-agent=' + utils.ua.random)

    # driver = webdriver.Edge(service=edge_driver)
    driver = webdriver.Chrome(options=options,service=chrome_driver)

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

while True:
    a = input('输入 go 继续')
    if a == 'go':
        break
for driver,idx in zip(drivers,range(start_idx,start_idx+length)):
    
    driver.find_element(By.XPATH, "/html/body/div[1]/div[1]/header/div/div[2]/div[4]/deferred-side-panel/user-drawer-side-panel/button/span/span/img").click()
    driver.find_element(By.XPATH, "/html/body/div[1]/div[1]/header/div/div[2]/div[4]/deferred-side-panel/user-drawer-side-panel/div/modal-dialog/div[2]/nav/nav-list/ul/li[16]/a/span[2]").click()
    driver.find_element(By.XPATH, "/html/body/div[1]/div[6]/main/div/div[2]/div[1]/navigation-list/div/nav/nav-list/ul/li[17]/a/span[2]").click()
    driver.find_element(By.XPATH, "/html/body/div[1]/div[6]/main/div/div/div[1]/div/nav/nav-list/ul/li[3]/button/span[2]").click()
    driver.find_element(By.XPATH, "/html/body/div[1]/div[6]/main/div/div/div[1]/div/nav/nav-list/ul/li[3]/ul/li[2]/a/span").click()
    driver.find_element(By.XPATH, "/html/body/div[1]/div[6]/main/div/div/div[2]/div/div/div[1]/div/div/details/summary").click()
    driver.find_element(By.XPATH, "/html/body/div[1]/div[6]/main/div/div/div[2]/div/div/div[1]/div/div/details/details-menu/div/div/div/a[2]").click()
    driver.find_element(By.XPATH, "/html/body/div[1]/div[4]/main/div/div[2]/div/form/password-strength/auto-check/dl/dd/input").send_keys(pwd)
    driver.find_element(By.XPATH, "/html/body/div[1]/div[5]/main/div/sudo-credential-options/div[2]/form/div/div/button").click()
    driver.find_element(By.XPATH, "/html/body/div[1]/div[6]/main/div/div/div[2]/div/div/form/dl/dd/input").send_keys('pwd')
    



    select_element = driver.find_element(By.XPATH, "/html/body/div[1]/div[6]/main/div/div/div[2]/div/div/form/div/dl[1]/dd[1]/select")
    # 使用Select类进行操作
    select = Select(select_element)
    # 根据选项的文本内容选择值
    select.select_by_visible_text("No expiration")

    for i in range(1,20):
        driver.find_element(By.XPATH, check_box(i)).click()
    
    driver.find_element(By.XPATH, "/html/body/div[1]/div[6]/main/div/div/div[2]/div/div/form/p/button").click()
    driver.find_element(By.XPATH, "/html/body/div[1]/div[6]/main/div/div/div[2]/div/div/div[1]/div[3]/div/div/clipboard-copy").click()
    

    # 获取剪贴板的内容
    clipboard_content = pyperclip.paste()
        
    tokens[usremail(i)] = clipboard_content

with open('data.yaml', 'w') as file:
    yaml.safe_dump(tokens, file)



# # 点击注册按钮
# register_button = driver.find_element(By.XPATH, "//button[@type='submit' and contains(text(), 'Sign up for GitHub')]")
# register_button.click()


    time.sleep(1000)
