import json
import re
from datetime import datetime
from selenium.webdriver.common.by import By
import browser
from filesUtils import *
import urllib.parse

callCodes = ['A','B','C','D','E','F','G','H','I','J','K','L']
def verifyOptType(s):
        return any(map(lambda x: x == (re.search("[a-zA-Z]+",s[::-1]).group(0)[0]),callCodes))

def divideOptionTypes(data):
    curr_call_code = data[0]['code'][4]
    curr_put_code = ''
    curr_week_code = data[0]['code'][-2:] if len(data[0]['code']) > 8 else 'W3'
    next_call_code = ''
    next_put_code = ''
    next_week_code = ''
    for i in data:
        if i['code'][4] != curr_call_code:
            curr_put_code = i['code'][4]
            break
    for i in data:
        if i['code'][-2:] != curr_week_code:
            if (i['code'][-2:] != 'W1' and
                i['code'][-2:] != 'W2' and
                i['code'][-2:] != 'W4' and
                i['code'][-2:] != 'W5'):
                next_week_code = 'W3'
                next_call_code = i['code'][4]
                next_put_code = data[-1]['code'][4]
                break
            next_week_code = i['code'][-2:]
            next_call_code = i['code'][4]
            next_put_code = data[-1]['code'][4]
            break
    calls = []
    puts = []
    nextCalls = []
    nextPuts = []
    for i in data:
        if i['code'][-2:] == curr_week_code or (len(i['code']) < 9 and curr_week_code == 'W3'):
            if i['code'][4] == curr_call_code:
                calls.append(i)
            if i['code'][4] == curr_put_code:
                puts.append(i)
        if i['code'][-2:] == next_week_code or (len(i['code']) < 9 and next_week_code == 'W3'):
            if i['code'][4] == next_call_code:
                nextCalls.append(i)
            if i['code'][4] == next_put_code:
                nextPuts.append(i)
    return {'calls':calls,'puts':puts,'nextCalls':nextCalls,'nextPuts':nextPuts}

def assetLockInfo(input_data:list[dict]) -> list[dict]:
    all_lock_combinations = []
    stockPrice = (input_data[0]['buyPrice']+input_data[0]['sellPrice'])/2
    data = input_data[1:]
    for ii,vv in enumerate(data): 
        for i,v in enumerate(data):
            try:
                strikeDiff = abs(vv['strike']-v['strike'])
                indexDiff = abs(i-ii)
                if (vv['code'] != v['code'] and vv['strike'] < v['strike'] and indexDiff > 1):
                    itype = verifyOptType(v['code'])
                    iitype = verifyOptType(vv['code'])
                    if itype and iitype and v['strike'] > stockPrice and vv['strike'] > stockPrice:
                        profit = (strikeDiff-(vv['sellPrice']-v['buyPrice']))/(vv['sellPrice']-v['buyPrice'])
                        if profit <= 1:
                            continue
                        all_lock_combinations.append([
                        v['time'] if datetime.fromisoformat(v['time']) < datetime.fromisoformat(vv['time'])
                        else vv['time'], vv['strike'],vv['code']+"("+str(vv['strike'])+")",vv['sellPrice'],
                        v['code']+"("+str(v['strike'])+")",v['buyPrice'],
                        profit,
                        round(((v['strike']-stockPrice)/stockPrice)*100,3), stockPrice])
                    if not itype and not iitype and v['strike'] < stockPrice and vv['strike'] < stockPrice:
                        profit = (strikeDiff-(v['sellPrice']-vv['buyPrice']))/(v['sellPrice']-vv['buyPrice'])
                        if profit <= 1:
                            continue
                        all_lock_combinations.append([
                        v['time'] if datetime.fromisoformat(v['time']) < datetime.fromisoformat(vv['time']) 
                        else vv['time'], v['strike'],v['code']+"("+str(v['strike'])+")",v['sellPrice'],
                        vv['code']+"("+str(vv['strike'])+")",vv['buyPrice'],
                        profit,
                        round(((stockPrice-vv['strike'])/stockPrice)*100,3), stockPrice])
            except (TypeError, ZeroDivisionError):
                continue
    return list(sorted(all_lock_combinations, key=lambda x: x[0],reverse=False))

def assetWeeklyTHLLockInfo(input_data):
    weeksToExpiry = 6 #Enter weeks to expiry of bought assets
    all_lock_combinations = []
    stockPrice = (input_data[0]['buyPrice']+input_data[0]['sellPrice'])/2
    dividedOptions = divideOptionTypes(input_data[1:])
    calls, puts, nextCalls, nextPuts = dividedOptions['calls'], dividedOptions['puts'], dividedOptions['nextCalls'], dividedOptions['nextPuts']
    def iterateSide(side, nextWeekSide, isCall, removeFilter):
        for i in side:
            for ii in nextWeekSide:
                try:
                    percentDistToStrike = 0
                    firstAssetBoughtPrice = i['sellPrice']
                    firstAssetSoldPrice = i['buyPrice']
                    latterAssetBoughtPrice = ii['sellPrice']
                    latterAssetSoldPrice = ii['buyPrice']
                    conventionalTHLPriceDiff = round(latterAssetBoughtPrice - firstAssetSoldPrice,2) #conventional calendar spreads win with the increase on pricediff between assets
                    reverseTHLPriceDiff = round(latterAssetSoldPrice - firstAssetBoughtPrice,2) #reverse calendar spreads win with the decrease on pricediff between assets
                    latterAssetDesagy = ii['sellPrice']-ii['buyPrice']
                    desagy = latterAssetDesagy + (i['sellPrice']-i['buyPrice'])
                    percentDistToStrike = abs((stockPrice - i['strike'])/stockPrice)

                    if isCall and i['strike'] > stockPrice and ii['strike'] > stockPrice:
                        isOTM = True
                        nearestStrike = i['strike'] if i['strike'] < ii['strike'] else ii['strike']
                        percentageToATM = round((nearestStrike - stockPrice)/stockPrice,3)
                    elif not isCall and i['strike'] < stockPrice and ii['strike'] < stockPrice:
                        isOTM = True
                        nearestStrike = i['strike'] if i['strike'] > ii['strike'] else ii['strike']
                        percentageToATM = round((stockPrice - nearestStrike)/stockPrice,3)
                    else:
                        isOTM = False

                    if i['strike'] == ii['strike']:
                        if not removeFilter:
                            if conventionalTHLPriceDiff <= 0.08 and isOTM:
                                all_lock_combinations.append([i['time'] if datetime.fromisoformat(i['time']) < datetime.fromisoformat(ii['time']) 
                                else ii['time'], i['code']+'('+str(i['strike'])+')',ii['code'],'percentage = ',round(percentDistToStrike,4),'desagy =',round(desagy,2),
                                'conventionalDiff = ',round(conventionalTHLPriceDiff,2)])
                            elif reverseTHLPriceDiff > 0.25:
                                all_lock_combinations.append([i['time'] if datetime.fromisoformat(i['time']) < datetime.fromisoformat(ii['time']) 
                                else ii['time'], i['code']+'('+str(i['strike'])+')',ii['code'],'percentage = ',round(percentDistToStrike,4),'desagy =',round(desagy,2),
                                'reverseDiff = ',round(reverseTHLPriceDiff,2)])
                        else:
                            all_lock_combinations.append([i['time'] if datetime.fromisoformat(i['time']) < datetime.fromisoformat(ii['time']) 
                            else ii['time'], i['code']+'('+str(i['strike'])+')',ii['code'],'percentage = ',round(percentDistToStrike,4),'desagy =',round(desagy,2)])
                except (TypeError, ZeroDivisionError):
                    continue
    iterateSide(calls, nextCalls, True, False)
    iterateSide(puts, nextPuts, False, False)
    return all_lock_combinations

def assetWeeklyCreditLockInfo(input_data):
    outList = []
    callCode = input_data[1]['code'][4]
    calls = []
    puts = []
    stockPrice = (input_data[0]['buyPrice']+input_data[0]['sellPrice'])/2

    def getMargin(firstAsset, secondAsset):
        strike_diff = round(abs(secondAsset['strike'] - firstAsset['strike']),2)
        credit_received = round(abs(secondAsset['buyPrice'] - firstAsset['sellPrice']),2)
        margin_per_contract = (strike_diff * 100) - (credit_received * 100)
        return margin_per_contract

    def iterateSide(side, isCall):
        for i in side:
            for ii in side:
                if i['code'] != ii['code']:
                    try:
                        firstAssetBuyPrice = i['sellPrice']
                        secondAssetSellPrice = ii['buyPrice']
                        priceDiff = round(firstAssetBuyPrice - secondAssetSellPrice, 2)
                        if priceDiff < 0:
                            if isCall and i['strike'] > stockPrice and ii['strike'] > stockPrice:
                                isOTM = True
                                nearestStrike = i['strike'] if i['strike'] < ii['strike'] else ii['strike']
                                percentageToATM = round((nearestStrike - stockPrice)/stockPrice,3)
                            elif not isCall and i['strike'] < stockPrice and ii['strike'] < stockPrice:
                                isOTM = True
                                nearestStrike = i['strike'] if i['strike'] > ii['strike'] else ii['strike']
                                percentageToATM = round((stockPrice - nearestStrike)/stockPrice,3)
                            else:
                                isOTM = False
                            if isOTM:
                                requiredMargin = getMargin(i,ii)
                                multiplicationPercentage = round((priceDiff * -100)/requiredMargin,2)
                                index = percentageToATM+(multiplicationPercentage/2)
                                if (i['code'] == 'PRIOC400W2' and ii['code'] == 'PRIOC390W2') or (ii['code'] == 'PRIOC400W2' and i['code'] == 'PRIOC390W2'):
                                    print
                                if multiplicationPercentage == 0 or percentageToATM < 0.03:
                                    continue
                                outList.append([i['time'] if datetime.fromisoformat(i['time']) < datetime.fromisoformat(ii['time']) 
                                else ii['time'], i['code']+'('+str(i['strike'])+')',ii['code']+'('+str(ii['strike'])+')',
                                percentageToATM, multiplicationPercentage])
                    except (TypeError, ZeroDivisionError):
                        continue

    for i in input_data[1:]:
        if i['code'][4] == callCode:
            calls.append(i)
        else:
            puts.append(i)
    iterateSide(calls, True)
    iterateSide(puts, False)
    return outList

def getLockInfo(l:list[list[dict]], weekly) -> list[dict]:
    outList1 = []
    outList2 = []
    for i in l:
        if weekly:
            outList1.extend(assetWeeklyCreditLockInfo(i))
            outList2.extend(assetWeeklyTHLLockInfo(i))
        else:
            outList1.extend(assetLockInfo(i))
    if weekly:
        def sortLast1(val):
            return val[-1]
        def sortLast2(val):
            return val[-1]
        outList1.sort(key=sortLast1, reverse=True)
        outList2.sort(key=sortLast2, reverse=True)
        exportWeeklyLockOutput(outList1)
        exportWeeklyFilteredOptionsForTHL(outList2)
        return
    exportLockOutput(outList1)

# v = getLockInfo(filesUtils.importTestPrices(),True)
# filesUtils.exportWeeklyLockOutput(v)
# print