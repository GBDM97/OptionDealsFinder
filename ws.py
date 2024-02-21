from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
import optionCodes
import time

chrome_options = Options()
chrome_driver = "C:\Program Files\Google\Chrome\Application\chrome.exe"
driver = webdriver.Chrome(chrome_options)
driver.get('https://portal.clear.com.br/login')
actions = ActionChains(driver)

input()

#verify type 6 is being sent and clean connections for the execution bellow:
'''
    delete temp1
    queryObjects(WebSocket)
    let messages = [];
    temp1.addEventListener("message", function (event) {
    let data = "[" + event.data.replace(/\x1E/g, ",");
    data = JSON.parse(data.substring(0, data.length - 1) + "]");
    for (i = 0; i < data.length; i++) {
        if (data[i].target === "QuoteSnapshot") {
            messages.push(data[i]);
        }
    }
    });

'''

def sendMessage(m):
    driver.execute_script('temp1.send(JSON.stringify('+m+')+\'\x1E\');')

def getWSMessages():
    return driver.execute_script('return messages')

def quoteSnapshotWS(a):
    sendMessage('{"arguments":["'+a+'"],"target":"SubscribeQuote","type":1}')
    sendMessage('{"arguments":["'+a+'"],"target":"UnsubscribeQuote","type":1}')

def unsubscribeQuoteWS(a):
    sendMessage('{"arguments":["'+a+'"],"target":"UnsubscribeQuote","type":1}')

def queryList():
    l = optionCodes.get()
    [print(v) for ii, v in enumerate((i for i in l)) if ii < 500]
    #send the ii to ws message

