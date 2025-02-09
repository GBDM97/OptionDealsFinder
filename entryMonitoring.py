from datetime import datetime
import json
import time
import clearScript
import optionCodes
import dataProcess
import ws

pricesList = []
currentOptions = optionCodes.importWeeklyCurrent()
notifiedLockOperations = []
subscribedAssets = []
allWeeklyAssets = []

def exportWeeklyLockOutput(l):
    with open('Data\\weeklyLockOutput.json', "w") as file:
        json.dump(l, file, indent=2)

def sendNewLockNotification(driver, operation):
    driver.execute_script('new Notification("'+operation[1]+' '+operation[3]+'")')
        
def subscribeAssets(driver,l):
    [(ws.subscribeQuote(i,driver),subscribedAssets.append(i)) for i in l 
     if i not in subscribedAssets]
    print

def pauseListUpdate():
    if not allWeeklyAssets:
        return True
    return datetime.now().minute == 0 

def isL2PresentOnL1(l1,l2):
    if l1 == [] or l2 == []:
        return False
    for i in l2:
        if i in l1:
            continue
        else:
            return False
    return True

def filterUnderAssets(l):
    return sorted(list(filter(lambda obj: obj['arguments'][0] in optionCodes.underlyingWeeklyAssets, l)), 
           key=lambda obj1: obj1['arguments'][0])

def orderPrices(ref,p):
    orderedPrices = []
    for i in ref:
        for ii in p:
            if i == ii['arguments'][0]:
                orderedPrices.append(ii)
    return orderedPrices

def run(driver, symbol, buyPrice, sellPrice, sendingTime):
# def run(symbol, buyPrice, sellPrice):
    global allWeeklyAssets
    weeklyFiltered = []
    
    if symbol == 'VALEM580W1':
        print
    for i,v in enumerate(pricesList):
        if v['arguments'][0] == symbol:
            if not buyPrice and not sellPrice:
                return
            if buyPrice:
                v['arguments'][1]['bestBuyPrice'] = buyPrice
            if sellPrice:
                v['arguments'][1]['bestSellPrice'] = sellPrice
            break
        elif i == len(pricesList)-1:
            pricesList.append({'arguments':[symbol,{'bestBuyPrice':buyPrice,"bestSellPrice":sellPrice,"sendingTime":sendingTime}]})
            break
    if (symbol in optionCodes.underlyingWeeklyAssets and pauseListUpdate() and 
        isL2PresentOnL1([i['arguments'][0] for i in pricesList],optionCodes.underlyingWeeklyAssets)):
        optionCodes.updateOptionsList('',True,filterUnderAssets(pricesList))
        weeklyFiltered = optionCodes.importWeeklyFiltered()
        allWeeklyAssets = [item["code"] for sublist in weeklyFiltered for item in sublist]
        subscribeAssets(driver,allWeeklyAssets)
    if not pricesList:
        pricesList.append({'arguments':[symbol,{'bestBuyPrice':buyPrice,"bestSellPrice":sellPrice}]})
    if isL2PresentOnL1([i['arguments'][0] for i in pricesList], allWeeklyAssets):
        assetsInputData = clearScript.generateDataSet('', True, orderPrices(allWeeklyAssets,pricesList))
        lockOutput = dataProcess.getLockInfo(assetsInputData, True)
        for i in lockOutput:
            if (i[6] < 0.03 and dataProcess.verifyOptType(i[1][4]) and dataProcess.verifyOptType(i[3][4]) 
            and [i[1],i[3]] not in notifiedLockOperations):
                sendNewLockNotification(driver, i)
                notifiedLockOperations.append([i[1],i[3]])
        exportWeeklyLockOutput(lockOutput)