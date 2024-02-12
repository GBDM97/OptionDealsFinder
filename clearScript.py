from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import optionCodes
import time

chrome_options = Options()
chrome_driver = "C:\Program Files\Google\Chrome\Application\chrome.exe"
driver = webdriver.Chrome(chrome_options)
driver.get('https://portal.clear.com.br/login')
actions = ActionChains(driver)
input('')

def newAssetFlow(ticker):
    actions.move_by_offset(400,65)
    actions.click()
    actions.perform()
    actions.move_by_offset(-400,-65)
    actions.move_by_offset(610,215)
    actions.click()
    actions.perform()
    e = driver.find_element(By.CSS_SELECTOR, '[placeholder="Novo ativo"]')
    [(e.send_keys(ticker[i]),time.sleep(0.05)) for i in range(0,len(ticker))]
    e.send_keys(' ')
    actions.move_by_offset(-610,-215)
    time.sleep(1.5)
    e = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "[class='small soma-caption ellipsis hydrated']"))
    )
    e.click()
    actions.move_by_offset(931,543)
    actions.click()
    actions.perform()
    actions.move_by_offset(-931, -543)
    actions.click()
    actions.perform()

def addAssets():
    [newAssetFlow(i) for i in optionCodes.get()]
    time.sleep(0.5)
    prices = [i.text for i in driver.find_elements(By.CSS_SELECTOR, '[class="defaultCell bodyCell"]')[8:]]
    print(prices)

addAssets()

input()