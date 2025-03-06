from selenium import webdriver
from selenium.webdriver.chrome.options import Options

driver = ''

def start(url):
    global driver
    driver = webdriver.Chrome()
    driver.get(url)

def getDriver():
    global driver
    if driver:
        return driver
    else:
        return None