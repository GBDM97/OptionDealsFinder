import re
from datetime import datetime

import filesUtils

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

def assetWeeklyLockInfo(input_data):
    weeksToExpiry = 6 #Enter weeks to expiry of bought assets
    all_lock_combinations = []
    stockPrice = (input_data[0]['buyPrice']+input_data[0]['sellPrice'])/2
    dividedOptions = divideOptionTypes(input_data[1:])
    calls, puts, nextCalls, nextPuts = dividedOptions['calls'], dividedOptions['puts'], dividedOptions['nextCalls'], dividedOptions['nextPuts']
    def iterateOverSide(side, nextWeekSide, isCall):
        for i in side:
            for ii in nextWeekSide:
                try:
                    boughtAssetEntryPrice = ii['sellPrice']
                    soldAssetEntryPrice = i['buyPrice']
                    priceDiff = boughtAssetEntryPrice - soldAssetEntryPrice
                    desagy = ii['sellPrice']-ii['buyPrice']
                    endBuyBalance = (1-(1/weeksToExpiry)) * boughtAssetEntryPrice
                    endSellBalance = 0 if soldAssetEntryPrice <= 0.25 else soldAssetEntryPrice/2
                    boughtAssetProfit = endBuyBalance - boughtAssetEntryPrice - desagy
                    soldAssetProfit = soldAssetEntryPrice - endSellBalance
                    totalEstimatedProfit = boughtAssetProfit + soldAssetProfit
                    if isCall:
                        isOTM = True if i['strike'] > stockPrice and ii['strike'] > stockPrice else False
                    else:
                        isOTM = True if i['strike'] < stockPrice and ii['strike'] < stockPrice else False
                    if totalEstimatedProfit > 0.01 and priceDiff >= 0 and isOTM:
                        all_lock_combinations.append([i['time'] if datetime.fromisoformat(i['time']) < datetime.fromisoformat(ii['time']) 
                        else ii['time'],i['code'],i['buyPrice'],ii['code'],ii['sellPrice'],
                        round(priceDiff,2),round(totalEstimatedProfit,2)])
                except (TypeError, ZeroDivisionError):
                    continue
    iterateOverSide(calls, nextCalls, True)
    iterateOverSide(puts, nextPuts, False)
    return all_lock_combinations

def getLockInfo(l:list[list[dict]], weekly) -> list[dict]:
    outList = []
    for i in l:
        outList.extend(assetWeeklyLockInfo(i)) if weekly else outList.extend(assetLockInfo(i))
    if weekly:
        def sortLast(val):
            return val[-2] 
        outList.sort(key=sortLast)
    return outList

v = getLockInfo(filesUtils.importTestPrices(),True)
filesUtils.exportWeeklyLockOutput(v)
print