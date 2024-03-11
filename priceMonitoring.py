import ast
import asyncio
import json
import ws

def sendNotification(driver,i,ii, inputList):
    driver.execute_script('new Notification("'+ii['arguments'][0]['symbol']+' BREAKOUT",{body:"'
        +str(ii['arguments'][0]['lastPrice'])+'"})')
    inputList[inputList.index(i)]['notified'] = 'True'
    exportList(inputList)

def importList():
    with open('Data\\priceMonitoring.json', 'r') as file:
        return ast.literal_eval(file.read())

def exportList(l):
    with open('Data\\priceMonitoring.json', 'w') as file:
        json.dump(l, file, indent=2)

def importUpdatesTestList():
    with open('Data\\updates.json','r') as file:
        return ast.literal_eval(file.read().replace('null','None'))

async def start(driver):
    inputList = list(importList())
    [ws.subscribeQuote(i['code'],driver) for i in inputList]
    while True:
        inputList = list(importList())
        updates = await ws.getUpdates(driver)
        ws.clearUpdates(driver)
        for i in inputList:
            for ii in updates:
                if (
                    (i['code'] == ii['arguments'][0]['symbol'] and ii['arguments'][0]['lastPrice']) and 
                    ((i['reference'] == ">" and not 'notified' in i and 
                     float(i['alertPrice']) < ii['arguments'][0]['lastPrice'])
                    or  
                    (i['reference'] == "<" and not 'notified' in i and
                     float(i['alertPrice']) > ii['arguments'][0]['lastPrice'])
                     )
                     ):
                    sendNotification(driver,i,ii,inputList)
        await asyncio.sleep(0.5)

