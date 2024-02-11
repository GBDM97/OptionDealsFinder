from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import json

chrome_options = Options()
chrome_driver = "C:\Program Files\Google\Chrome\Application\chrome.exe"
driver = webdriver.Chrome(chrome_options)
driver.get('https://opcoes.net.br/opcoes/bovespa/B3SA3/json?skip=0&load=8&colsAndUnderlyingInfo=true')
actions = ActionChains(driver)
json_data = driver.execute_script('return JSON.stringify(document.querySelector(\'pre\').textContent)')
parsed_data = json.loads(json_data)
parsed_data = json.loads(parsed_data)

print([[i[0] for i in parsed_data["data"]['expirations'][0]['calls']],[i[0] for i in parsed_data["data"]['expirations'][0]['puts']]])
print(len([i[0] for i in parsed_data["data"]['expirations'][0]['calls']]))
