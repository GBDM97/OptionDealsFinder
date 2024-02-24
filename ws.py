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

def queryPrices(driver):
    l = optionCodes.get()
    ii = 0
    for i in l:
        for v in i:
            if ii < 15:
                quoteSnapshotWS(v['code'],driver)
                ii += 1
                if ii == 1000 or ii == 2000 or ii == 3000:
                    time.sleep(1)
    ret = getWSMessages(driver)
    while ret[-1]['arguments'][0] != l[-1][-1]['code']:
        ret = getWSMessages(driver)
    return ret

