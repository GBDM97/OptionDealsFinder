from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import time

chrome_options = Options()
chrome_driver = "C:\Program Files\Google\Chrome\Application\chrome.exe"
driver = webdriver.Chrome(chrome_options)
driver.get('https://portal.clear.com.br/login')
actions = ActionChains(driver)

def executeNewAssetInfoFlow(ticker):
    actions.move_by_offset(450,140)
    actions.click()
    actions.perform()
    actions.move_by_offset(-450,-140)
    actions.move_by_offset(400,65)
    actions.click()
    actions.perform()
    actions.move_by_offset(-400,-65)
    actions.move_by_offset(610,215)
    actions.click()
    actions.perform()
    e = driver.find_element(By.CSS_SELECTOR, '[placeholder="Novo ativo"]')
    e.send_keys(ticker[0])
    time.sleep(0.05)
    e.send_keys(ticker[1])
    time.sleep(0.05)
    e.send_keys(ticker[2])
    time.sleep(0.05)
    e.send_keys(ticker[3])
    time.sleep(0.05)
    e.send_keys(ticker[4])
    time.sleep(0.05)
    e.send_keys(' ')
    actions.move_by_offset(-610,-215)
    actions.move_by_offset(620,290)
    time.sleep(2)
    actions.click()
    actions.perform()
    actions.move_by_offset(-620,-290)
    actions.move_by_offset(931,543)
    actions.click()
    actions.perform()
    actions.move_by_offset(-931, -543)
    actions.click()
    actions.perform()
    time.sleep(0.5)
    prices = [i.text for i in driver.find_elements(By.CSS_SELECTOR, '[class="defaultCell bodyCell"]')[8:]]
    print(prices)

executeNewAssetInfoFlow('VBBR3')
