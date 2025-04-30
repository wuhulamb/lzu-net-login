from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time

def login(count, account_username, account_password):
    print(f"try {count} times")
    time.sleep(10)
    try:
        driver.get("http://10.10.0.166/")
    except:
        global lzu_net
        lzu_net = False
        return True      # break loop
    driver.implicitly_wait(0.5)
    time.sleep(3)
    try:
        login_username = driver.find_element(By.ID, "user_name")
        print(login_username.text)
        return True
    except:
        try:
            print("trying to connect lzu_net ...")
            account = driver.find_element(By.CLASS_NAME, "tab-container")
            account = account.find_element(By.CSS_SELECTOR, '[data="account"]')
            account.click()
            time.sleep(3)
            username = driver.find_element(By.ID, value="username")
            password = driver.find_element(By.ID, value="password")
            login_button = driver.find_element(By.CSS_SELECTOR, '.login[type="button"]')
            username.send_keys(account_username)
            password.send_keys(account_password)
            login_button.click()
            time.sleep(3)
            return True
        except:
            return False

print("lzu_net.py is executed")
chrome_options = Options()
chrome_options.add_argument("--headless")  # 关闭图形界面
chrome_driver_path = "/path/to/chromedriver"
service = Service(chrome_driver_path)
driver = webdriver.Chrome(service=service, options=chrome_options)
driver.set_page_load_timeout(5)

account_username = ""
account_password = ""

count = 1
try_num = 5
lzu_net = True
while count <= try_num:
    if login(count, account_username, account_password):
        break
    count += 1
if not lzu_net:
    print("not in lzu_net")
else:
    if count < try_num:
        print("connect lzu_net successfully")
driver.quit()
