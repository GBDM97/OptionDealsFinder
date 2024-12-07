import ast
import asyncio
import json
import ws

def sendNotification(driver,i,lastPrice, symbol, inputList):
    driver.execute_script('new Notification("'+symbol+' BREAKOUT",{body:"'
        +str(lastPrice)+'"})')
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

def exportTestList(l):
    with open('Data\\updates.json', 'w') as file:
        json.dump(l, file, indent=2)

def subscribeList(driver):
    inputList = list(importList())
    [ws.subscribeQuote(i['code'],driver) if i['operationType'] == 'dry' else 
    (ws.subscribeQuote(i['soldAsset'],driver), 
     ws.subscribeQuote(i['boughtAsset'],driver)) if i['operationType'] == 'lock' else 
     None for i in inputList]

async def start(driver):
    while True:
        snapshots = await ws.getSnapshots(driver)
        updates = await ws.getUpdates(driver)
        updates.append(snapshots)
        updates = updates[0]
        inputList = list(importList())
        for i in inputList:
            for ii in updates:
                symbol = ii['arguments'][0]['symbol'] if ii['target'] == 'QuoteUpdate' else ii['arguments'][0]
                bestBuyPrice =  ii['arguments'][0]['bestBuyPrice'] if ii['target'] == 'QuoteUpdate' else ii['arguments'][1]['bestBuyPrice']
                bestSellPrice = ii['arguments'][0]['bestSellPrice'] if ii['target'] == 'QuoteUpdate' else ii['arguments'][1]['bestSellPrice']
                lastPrice = ii['arguments'][0]['lastPrice'] if ii['target'] == 'QuoteUpdate' else ii['arguments'][1]['lastPrice']
                if i['operationType'] == 'lock':
                    if not 'boughtAssetCurrExitPrice' in i and not 'soldAssetCurrExitPrice' in i:
                        inputList[inputList.index(i)]['boughtAssetCurrExitPrice'] = i['boughtAssetPrices'][0]
                        inputList[inputList.index(i)]['soldAssetCurrExitPrice'] = i['soldAssetPrices'][1]
                        exportList(inputList)
                    if i['soldAsset'] == symbol and bestSellPrice:
                        inputList[inputList.index(i)]['soldAssetCurrExitPrice'] = bestSellPrice
                        exportList(inputList)
                    if i['boughtAsset'] == symbol and bestBuyPrice:
                        inputList[inputList.index(i)]['boughtAssetCurrExitPrice'] = bestBuyPrice
                        exportList(inputList)
                    result = round(i['boughtAssetCurrExitPrice'] - i['soldAssetCurrExitPrice'],2)
                    operationCost = round(i['boughtAssetPrices'][1] - i['soldAssetPrices'][0],2)
                    if result / operationCost >= i['multiplicationTarget'] and not "notified" in i:
                        inputList[inputList.index(i)]['notified'] = "True"
                        exportList(inputList)
                        ws.sendTwilioMessage(driver,i['soldAsset'])
                elif i['operationType'] == 'dry':
                    if (
                        (i['code'] == symbol and lastPrice) and 
                        ((i['reference'] == ">=" and not 'notified' in i and 
                        lastPrice >= float(i['alertPrice']))
                        or  
                        (i['reference'] == "<=" and not 'notified' in i and
                        lastPrice <= float(i['alertPrice']))
                        )
                        ):
                        sendNotification(driver,i,lastPrice,symbol,inputList)
        ws.clearUpdates(driver)
        ws.clearSnapshots(driver)
        await asyncio.sleep(0.5)

