from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
import optionCodes

chrome_options = Options()
chrome_driver = "C:\Program Files\Google\Chrome\Application\chrome.exe"
driver = webdriver.Chrome(chrome_options)
driver.get('https://portal.clear.com.br/login')
actions = ActionChains(driver)

input()

#verify type 6 is being sent and clean connections for the execution bellow:
'''
    queryObjects(Websocket)
    let messages = [];
    temp1.onmessage = function (e) {
        if(e.data !== '{"type":6}\x1E'){messages.push(e.data);}
    }
'''

driver.execute_script('var messages = [1]; console.log(messages);')

def sendMessage(m):
    driver.execute_script('temp1.send(JSON.stringify('+m+')+\'\x1E\');')

def getWSMessages():
    return driver.execute_script('return messages')

def assetWSQuery(a):
    sendMessage('{"arguments":["'+a+'"],"target":"SubscribeQuote","type":1}')
    sendMessage('{"arguments":["'+a+'"],"target":"UnsubscribeQuote","type":1}')

def queryList():
    l = optionCodes.get()
    [print(i) for i in l]

