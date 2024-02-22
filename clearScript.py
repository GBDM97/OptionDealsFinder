from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
import optionCodes,dataProcess
import ws

chrome_options = Options()
chrome_driver = "C:\Program Files\Google\Chrome\Application\chrome.exe"
driver = webdriver.Chrome(chrome_options)
driver.get('https://portal.clear.com.br/login')
actions = ActionChains(driver)

input('')

def generateDataSet() -> list[list[dict]]:
    asset_dataset = []
    final_dataset = []
    prices_index = 8
    prices = ws.queryPrices(driver)
    for ii in optionCodes.get()[:5]:
        asset_dataset = []
        for i in ii:
            new = {}
            if 'strike' in i:
                new = {
                    'code': i['code'],
                    'strike': i['strike'],
                    'buyPrice': float(prices[prices_index]) if prices[prices_index]!='-' else '-' ,
                    'sellPrice': float(prices[prices_index+1]) if prices[prices_index+1]!='-' else '-'
                }
            else:
                new = {
                    'code': i['code'],
                    'buyPrice': float(prices[prices_index]) if prices[prices_index]!='-' else '-',
                    'sellPrice': float(prices[prices_index+1]) if prices[prices_index+1]!='-' else '-'
                }
            asset_dataset.append(new)
            prices_index += 5
        final_dataset.append(asset_dataset)
    return final_dataset

def getLockOutput():
    print(dataProcess.getLockInfo(generateDataSet()))

getLockOutput()
input()
