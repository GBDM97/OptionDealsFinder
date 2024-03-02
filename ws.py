import ast
import optionCodes
import time

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

# '''

def sendMessage(m,driver):
    driver.execute_script('temp1.send(JSON.stringify('+m+')+\'\x1E\');')

def getWSMessages(driver):
    return driver.execute_script('return messages')

def quoteSnapshotWS(a,driver):
    sendMessage('{"arguments":["'+a+'"],"target":"SubscribeQuote","type":1}',driver)
    sendMessage('{"arguments":["'+a+'"],"target":"UnsubscribeQuote","type":1}',driver)

def unsubscribeQuoteWS(a):
    sendMessage('{"arguments":["'+a+'"],"target":"UnsubscribeQuote","type":1}')

def queryPrices(list, driver):
    last = ''
    for index,asset in enumerate(list):
        quoteSnapshotWS(asset,driver)
        index += 1
        if (index == 1000 or index == 2000 or index == 3000 or
        index == 4000 or index == 5000 or index == 6000 or
        index == 7000 or index == 8000):
            input('WS')
        last = asset
    ret = getWSMessages(driver)
    while ret[-1]['arguments'][0] != last:
        ret = getWSMessages(driver)
    return ast.literal_eval(str(ret).replace('null','None'))

