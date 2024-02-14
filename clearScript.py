from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import optionCodes,dataProcess
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
    e = driver.find_element(By.CSS_SELECTOR, '[class="soma-table-body hydrated"]').text
    [(e.send_keys(ticker[i]),time.sleep(0.025)) for i in range(0,len(ticker))]
    actions.move_by_offset(-610,-215)
    e = WebDriverWait(driver, 60).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "[alt='Logo do ativo "+ticker+"']"))
    )
    e.click()
    actions.move_by_offset(931,543)
    actions.click()
    actions.perform()
    actions.move_by_offset(-931, -543)
    actions.click()
    actions.perform()
    

def addAssetsToBroker():
    for ii in optionCodes.get():
        [newAssetFlow(i['code']) for i in ii]

def generateDataSet() -> list[list[dict]]:
    options_dataset = []
    prices_index = 2
    prices = [' 0,77', ' 0,77', ' 0,76', ' 0,77', '-', '-', '-', '-', '-', '-', '-', '-', ' 0,01', ' 0,01', '-', ' 0,06', '-', ' 0,01', '-', ' 0,01', '-', ' 0,01', '-', ' 0,01', '-', ' 0,01', '-', '-', '-', '-', '-', ' 0,22', '-', '-', '-', ' 0,01', '-', '-', '-', '-', '-', '-', '-', ' 0,02', '-', '-', '-', ' 0,22', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '']
    # prices = [i.text for i in driver.find_elements(By.CSS_SELECTOR, '[class="defaultCell bodyCell"]')]
    for ii in optionCodes.get():
        for i in ii:
            new = {}
            if 'strike' in i:
                new = {
                    'code': i['code'],
                    'strike': i['strike'],
                    'buyPrice': prices[prices_index],
                    'sellPrice': prices[prices_index + 1]
                }
            else:
                new = {
                    'code': i['code'],
                    'buyPrice': prices[prices_index],
                    'sellPrice': prices[prices_index + 1]
                }
            options_dataset.append(new)
            prices_index += 4
    return options_dataset

def getLockOutput():
    print(dataProcess.getLockInfo(generateDataSet()))

getLockOutput()
input()
