import ast
import asyncio
import ws

def sendNotification(driver,i,ii):
    driver.execute_script('new Notification("'+ii['arguments'][0]+ ' BREAKOUT",{body:"'
        +str(ii['arguments'][1]['lastPrice'])+'"})')
    inputList[inputList.index(i)]['notified'] = True

def importList():
    with open('Data\\priceMonitoring.json', 'r') as file:
        return ast.literal_eval(file.read())

inputList = list(importList())

async def start(driver):
    [ws.subscribeQuote(i['code'],driver) for i in inputList]
    while True:
        updates = ws.getUpdates(driver)
        ws.clearUpdates(driver)
        for i in inputList:
            for ii in updates:
                if ((i['code'] == ii['arguments'][0]) and
                    (i['reference'] == ">" and not 'notified' in i and
                     float(i['alertPrice']) < ii['arguments'][1]['lastPrice'])
                or  (i['code'] == ii['arguments'][0]) and
                    (i['reference'] == "<" and not 'notified' in i and
                     float(i['alertPrice']) > ii['arguments'][1]['lastPrice'])):
                    sendNotification(driver,i,ii)
        await asyncio.sleep(0.5)