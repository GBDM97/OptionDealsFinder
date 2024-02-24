from selenium import webdriver
from selenium.webdriver.chrome.options import Options

driver = ''

def start():
    global driver
    chrome_options = Options()
    driver = webdriver.Chrome(chrome_options)
    driver.get('https://portal.clear.com.br/login')

def getDriver():
    global driver
    if driver:
        return driver
    else:
        return None