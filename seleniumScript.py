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
    actions.move_by_offset(216,138)
    actions.click()
    actions.perform()
    actions.move_by_offset(-216,-138)
    actions.click()
    actions.perform()
    actions.move_by_offset(163,65)
    actions.click()
    actions.perform()
    actions.move_by_offset(462,155)
    actions.click()
    actions.perform()
    driver.find_element(By.CSS_SELECTOR, '[placeholder="Novo ativo"]').send_keys(ticker)
    actions.move_by_offset(0, 70)
    time.sleep(0.1)
    actions.click()
    actions.perform()
    actions.move_by_offset(305, 260)
    actions.click()
    actions.perform()
    actions.move_by_offset(-930, -550)
    actions.click()
    actions.perform()
    time.sleep(0.1)
    prices = [i.text for i in driver.find_elements(By.CSS_SELECTOR, '[class="sc-hTtIkV enEDrO"]')[9:]]
    print(prices)

executeNewAssetInfoFlow('EMBR3')
