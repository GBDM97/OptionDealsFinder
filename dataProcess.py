import re
from datetime import datetime

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
        if i['code'][-2:] != curr_week_code or curr_week_code == 'W3':
            next_week_code = i['code'][-2:] if curr_week_code != 'W3' else 'W4'
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
    all_lock_combinations = []
    dividedOptions = divideOptionTypes(input_data[1:])
    calls, puts, nextCalls, nextPuts = dividedOptions['calls'], dividedOptions['puts'], dividedOptions['nextCalls'], dividedOptions['nextPuts']
    def iterateOverSide(side, nextWeekSide):
        for i in side:
            for ii in nextWeekSide:
                try:
                    priceDiff = ii['sellPrice']-i['buyPrice']
                    if priceDiff < 0.1 and priceDiff > 0:
                        all_lock_combinations.append([i['time'] if datetime.fromisoformat(i['time']) < datetime.fromisoformat(ii['time']) 
                        else ii['time'],i['code'],i['buyPrice'],ii['code'],ii['sellPrice'],
                        ((ii['sellPrice']-i['buyPrice'])*100)/((ii['sellPrice']+i['buyPrice'])/2), priceDiff])
                except (TypeError, ZeroDivisionError):
                    continue
    iterateOverSide(calls, nextCalls)
    iterateOverSide(puts, nextPuts)
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