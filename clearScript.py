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
    e = driver.find_element(By.CSS_SELECTOR, '[placeholder="Novo ativo"]')
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
    prices = ["B3SA3", "-", " 12.86", "-", " 12.85", " 13.00", "C", "V", "ABEV3", "-", " 12.92", "-", " 12.85", " 12.95", "C", "V", "ABEVB650", "-", "-", "-", "-", "-", "C", "V", "ABEVB670", "-", "-", "-", "-", "-", "C", "V", "ABEVB690", "-", " 6.98", "-", "-", "-", "C", "V", "ABEVB710", "-", " 7.29", "-", "-", "-", "C", "V", "ABEVB730", "-", "-", "-", "-", "-", "C", "V", "ABEVB750", "-", "-", "-", "-", "-", "C", "V", "ABEVB770", "-", "-", "-", "-", "-", "C", "V", "ABEVB790", "-", "-", "-", "-", "-", "C", "V", "ABEVB810", "-", "-", "-", "-", "-", "C", "V", "ABEVB830", "-", "-", "-", "-", "-", "C", "V", "ABEVB850", "-", "-", "-", "-", "-", "C", "V", "ABEVB870", "-", "-", "-", "-", "-", "C", "V", "ABEVB890", "-", "-", "-", "-", "-", "C", "V", "ABEVB910", "-", "-", "-", "-", "-", "C", "V", "ABEVB930", "-", "-", "-", "-", "-", "C", "V", "ABEVB950", "-", "-", "-", "-", "-", "C", "V", "ABEVB970", "-", "-", "-", "-", "-", "C", "V", "ABEVB990", "-", "-", "-", "-", "-", "C", "V", "ABEVB102", "-", "-", "-", "-", "-", "C", "V", "ABEVB107", "-", " 2.78", "-", "-", " 3.27", "C", "V", "ABEVB112", "-", "-", "-", "-", "-", "C", "V", "ABEVB115", "-", " 2.39", "-", "-", "-", "C", "V", "ABEVB117", "-", " 1.94", "-", "-", "-", "C", "V", "ABEVB120", "-", " 1.58", "-", "-", "-", "C", "V", "ABEVB122", "-", " 1.44", "-", "-", "-", "C", "V", "ABEVB125", "-", " 1.05", "-", "-", "-", "C", "V", "ABEVB127", "-", " 0.79", "-", "-", "-", "C", "V", "ABEVB130", "-", " 0.55", "-", "-", " 0.61", "C", "V", "ABEVB132", "-", " 0.30", "-", "-", " 0.40", "C", "V", "ABEVB135", "-", " 0.08", "-", "-", " 1.59", "C", "V", "ABEVB137", "-", " 0.02", "-", " 0.02", " 0.03", "C", "V", "ABEVB140", "-", " 0.01", "-", "-", " 0.02", "C", "V", "ABEVB142", "-", " 0.01", "-", "-", " 0.02", "C", "V", "ABEVB145", "-", " 0.01", "-", "-", " 0.02", "C", "V", "ABEVB147", "-", " 0.01", "-", "-", " 0.01", "C", "V", "ABEVB150", "-", " 0.01", "-", "-", " 0.01", "C", "V", "ABEVB152", "-", " 0.01", "-", "-", " 0.01", "C", "V", "ABEVB155", "-", " 0.01", "-", "-", " 0.01", "C", "V", "ABEVB157", "-", " 0.01", "-", "-", " 0.01", "C", "V", "ABEVB160", "-", " 0.01", "-", "-", " 0.01", "C", "V", "ABEVB162", "-", " 0.01", "-", "-", " 0.01", "C", "V", "ABEVB167", "-", " 0.02", "-", "-", " 0.01", "C", "V", "ABEVB170", "-", " 0.01", "-", "-", " 0.01", "C", "V", "ABEVB172", "-", " 0.02", "-", "-", " 0.01", "C", "V", "ABEVB177", "-", " 0.02", "-", "-", " 0.01", "C", "V", "ABEVB182", "-", "-", "-", "-", " 0.01", "C", "V", "ABEVB187", "-", " 0.01", "-", "-", " 0.01", "C", "V", "ABEVB192", "-", "-", "-", "-", " 0.01", "C", "V", "ABEVB197", "-", "-", "-", "-", " 0.01", "C", "V", "ABEVB202", "-", "-", "-", "-", " 0.01", "C", "V", "ABEVB207", "-", " 0.01", "-", "-", " 0.01", "C", "V", "ABEVB212", "-", "-", "-", "-", " 0.01", "C", "V", "ABEVB215", "-", "-", "-", "-", " 0.01", "C", "V", "ABEVB217", "-", "-", "-", "-", " 0.01", "C", "V", "ABEVB220", "-", "-", "-", "-", " 0.01", "C", "V", "ABEVB222", "-", "-", "-", "-", " 0.01", "C", "V", "ABEVB225", "-", "-", "-", "-", " 0.01", "C", "V", "ABEVB227", "-", "-", "-", "-", " 0.01", "C", "V", "ABEVB232", "-", "-", "-", "-", " 0.01", "C", "V", "ABEVB237", "-", "-", "-", "-", " 0.01", "C", "V", "ABEVB242", "-", "-", "-", "-", " 0.01", "C", "V", "ABEVB247", "-", "-", "-", "-", " 0.01", "C", "V", "ABEVB252", "-", "-", "-", "-", " 0.01", "C", "V", "ABEVB257", "-", "-", "-", "-", " 0.01", "C", "V", "ABEVB262", "-", "-", "-", "-", " 0.01", "C", "V", "ABEVN650", "-", "-", "-", "-", " 0.01", "C", "V", "ABEVN670", "-", "-", "-", "-", " 0.01", "C", "V", "ABEVN690", "-", "-", "-", "-", " 0.01", "C", "V", "ABEVN710", "-", "-", "-", "-", " 0.01", "C", "V", "ABEVN730", "-", "-", "-", "-", " 0.01", "C", "V", "ABEVN750", "-", " 0.01", "-", "-", " 0.01", "C", "V", "ABEVN770", "-", " 0.01", "-", "-", " 0.01", "C", "V", "ABEVN790", "-", "-", "-", "-", " 0.01", "C", "V", "ABEVN810", "-", "-", "-", "-", " 0.01", "C", "V", "ABEVN830", "-", "-", "-", "-", " 0.01", "C", "V", "ABEVN850", "-", "-", "-", "-", " 0.01", "C", "V", "ABEVN870", "-", "-", "-", "-", "-", "C", "V", "ABEVN890", "-", "-", "-", "-", "-", "C", "V", "ABEVN910", "-", " 0.01", "-", "-", " 0.01", "C", "V", "ABEVN930", "-", "-", "-", "-", " 0.39", "C", "V", "ABEVN950", "-", "-", "-", "-", " 0.02", "C", "V", "ABEVN970", "-", "-", "-", "-", " 0.02", "C", "V", "ABEVN990", "-", " 0.01", "-", "-", " 0.02", "C", "V", "ABEVN102", "-", " 0.01", "-", "-", " 0.01", "C", "V", "ABEVN107", "-", " 0.01", "-", "-", " 0.01", "C", "V", "ABEVN112", "-", " 0.02", "-", "-", " 0.02", "C", "V", "ABEVN115", "-", " 0.01", "-", "-", " 0.02", "C", "V", "ABEVN117", "-", " 0.01", "-", "-", " 0.02", "C", "V", "ABEVN120", "-", " 0.01", "-", "-", " 0.02", "C", "V", "ABEVN122", "-", " 0.01", "-", "-", " 0.01", "C", "V", "ABEVN125", "-", " 0.01", "-", "-", " 0.03", "C", "V", "ABEVN127", "-", " 0.01", "-", "-", " 0.01", "C", "V", "ABEVN130", "-", " 0.02", "-", " 0.01", " 0.07", "C", "V", "ABEVN132", "-", " 0.02", "-", "-", " 0.02", "C", "V", "ABEVN135", "-", " 0.07", "-", " 0.02", " 0.10", "C", "V", "ABEVN137", "-", " 0.24", "-", " 0.21", " 0.39", "C", "V", "ABEVN140", "-", " 0.48", "-", " 0.16", "-", "C", "V", "ABEVN142", "-", " 0.72", "-", " 0.32", "-", "C", "V", "ABEVN145", "-", " 0.99", "-", " 0.60", " 1.05", "C", "V", "ABEVN147", "-", " 1.24", "-", " 0.02", "-", "C", "V", "ABEVN150", "-", " 1.48", "-", " 1.38", "-", "C", "V", "ABEVN152", "-", " 1.76", "-", "-", "-", "C", "V", "ABEVN155", "-", " 2.02", "-", "-", "-", "C", "V", "ABEVN157", "-", " 2.25", "-", "-", "-", "C", "V", "ABEVN160", "-", " 2.36", "-", "-", "-", "C", "V", "ABEVN162", "-", " 2.78", "-", "-", "-", "C", "V", "ABEVN167", "-", " 3.25", "-", "-", "-", "C", "V", "ABEVN170", "-", " 3.19", "-", "-", "-", "C", "V", "ABEVN172", "-", " 3.75", "-", "-", "-", "C", "V", "ABEVN177", "-", " 4.12", "-", "-", "-", "C", "V", "ABEVN182", "-", " 4.65", "-", "-", "-", "C", "V", "ABEVN187", "-", " 5.26", "-", "-", "-", "C", "V", "ABEVN192", "-", "-", "-", "-", "-", "C", "V", "ABEVN197", "-", " 6.22", "-", "-", "-", "C", "V", "ABEVN202", "-", "-", "-", "-", "-", "C", "V", "ABEVN207", "-", " 7.04", "-", "-", "-", "C", "V", "ABEVN212", "-", "-", "-", "-", "-", "C", "V", "ABEVN215", "-", " 7.50", "-", "-", "-", "C", "V", "ABEVN217", "-", "-", "-", "-", "-", "C", "V", "ABEVN220", "-", "-", "-", "-", "-", "C", "V", "ABEVN222", "-", "-", "-", "-", "-", "C", "V", "ABEVN225", "-", " 8.62", "-", "-", "-", "C", "V", "ABEVN227", "-", "-", "-", "-", "-", "C", "V", "ABEVN232", "-", "-", "-", "-", "-", "C", "V", "ABEVN237", "-", "-", "-", "-", "-", "C", "V", "ABEVN242", "-", "-", "-", "-", "-", "C", "V", "ABEVN247", "-", "-", "-", "-", "-", "C", "V", "ABEVN252", "-", "-", "-", "-", "-", "C", "V", "ABEVN257", "-", " 12.22", "-", "-", "-", "C", "V", "ABEVN262", "-", "-", "-", "-", "-", "C", "V", "AERI3", "-", " 0.75", "-", " 0.75", " 0.76", "C", "V", "AERIB600", "-", "-", "-", "-", "-", "C", "V", "AERIB700", "-", "-", "-", "-", "-", "C", "V", "AERIB800", "-", " 0.01", "-", "-", " 0.03", "C", "V", "AERIB900", "-", " 0.01", "-", "-", " 0.01", "C", "V", "AERIB99", "-", " 0.01", "-", "-", " 0.01", "C", "V", "AERIB110", "-", " 0.01", "-", "-", "-", "C", "V", "AERIB120", "-", "-", "-", "-", " 0.22", "C", "V", "AERIB130", "-", "-", "-", "-", " 0.01", "C", "V", "AERIB140", "-", "-", "-", "-", "-", "C", "V", "AERIB149", "-", "-", "-", "-", " 0.02", "C", "V", "AERIN600", "-", "-", "-", "-", " 0.22", "C", "V", "AERIN700", "-", " 0.02", "-", "-", "-", "C", "V", "AERIN800", "-", " 0.03", "-", " 0.03", "-", "C", "V", "AERIN900", "-", " 0.15", "-", "-", " 0.24", "C", "V", "AERIN99", "-", "-", "-", "-", "-", "C", "V", "AERIN110", "-", "-", "-", "-", "-", "C", "V", "AERIN120", "-", "-", "-", "-", "-", "C", "V", "AERIN130", "-", "-", "-", "-", "-", "C", "V", "AERIN140", "-", "-", "-", "-", "-", "C", "V", "AERIN149", "-", " 0.63", "-", "-", "-", "C", "V", "MGLU3", "-", " 2.02", "-", " 2.02", " 2.04", "C", "V"]
    # e = driver.find_element(By.CSS_SELECTOR, '[class="soma-table-body hydrated"]').text.replace(',','.').split("\n")
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
