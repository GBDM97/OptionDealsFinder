import re
from datetime import datetime

callCodes = ['A','B','C','D','E','F','G','H','I','J','K','L']
def verifyOptType(s):
        return any(map(lambda x: x == (re.search("[a-zA-Z]+",s[::-1]).group(0)[0]),callCodes))

def assetLockInfo(input_data:list[dict]) -> list[dict]:
    all_lock_combinations = []
    stockPrice = (input_data[0]['buyPrice']+input_data[0]['sellPrice'])/2
    data = input_data[1:]
    for ii in data: 
        for i in data:
            try:
                strikeDiff = ii['strike']-i['strike']
                if (ii['code'] != i['code'] and ii['strike'] >= i['strike'] 
                and i['buyPrice'] >= 0.1 and i['buyPrice'] <= 0.5 
                and ii['buyPrice'] >= 0.1 and ii['buyPrice'] <= 0.5
                and i['sellPrice'] >= 0.1 and i['sellPrice'] <= 0.5 
                and ii['sellPrice'] >= 0.1 and ii['sellPrice'] <= 0.5
                and strikeDiff > 0):
                    itype = verifyOptType(i['code'])
                    iitype = verifyOptType(ii['code'])
                    if itype and iitype and i['strike'] > stockPrice and ii['strike'] > stockPrice:
                        all_lock_combinations.append([
                        i['time'] if datetime.fromisoformat(i['time']) < datetime.fromisoformat(ii['time'])
                        else ii['time'], i['strike'],i['code']+"("+str(i['strike'])+")",i['sellPrice'],
                        ii['code']+"("+str(ii['strike'])+")",ii['buyPrice'],
                        (strikeDiff-(i['sellPrice']-ii['buyPrice']))/(i['sellPrice']-ii['buyPrice']),
                        round(((ii['strike']-stockPrice)/stockPrice)*100,3), stockPrice])
                    if not itype and not iitype and i['strike'] < stockPrice and ii['strike'] < stockPrice:
                        all_lock_combinations.append([
                        i['time'] if datetime.fromisoformat(i['time']) < datetime.fromisoformat(ii['time']) 
                        else ii['time'], ii['strike'],ii['code']+"("+str(ii['strike'])+")",ii['sellPrice'],
                        i['code']+"("+str(i['strike'])+")",i['buyPrice'],
                        (strikeDiff-(ii['sellPrice']-i['buyPrice']))/(ii['sellPrice']-i['buyPrice']),
                        round(((stockPrice-i['strike'])/stockPrice)*100,3), stockPrice])
            except (TypeError, ZeroDivisionError):
                continue
    return list(sorted(all_lock_combinations, key=lambda x: x[0],reverse=False))

def assetWeeklyLockInfo(input_data):
    all_lock_combinations = []
    data = input_data[1:]
    curr_call_code = data[0]['code'][4]
    curr_put_code
    curr_week_code = data[0]['code'][-2:] if len(data[0]['code']) > 8 else 'W3'
    next_week_code
    for i in data:
        if i['code'][4] != curr_call_code:
            curr_put_code = i['code'][4]
            break
    for i in data:
        if i['code'][4] != curr_week_code or curr_week_code == 'W3':
            next_week_code = i['code'][4] if curr_week_code != 'W3' else 'W4'
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
            if i['code'][4] == curr_call_code:
                nextCalls.append(i)
            if i['code'][4] == curr_put_code:
                nextPuts.append(i)
    def iterateOverSide(side, nextWeekSide):
        for i in side:
            for ii in nextWeekSide:
                try:
                    priceDiff = ii['sellPrice']-i['buyPrice']
                    if priceDiff < 0.1 and priceDiff > 0:
                        all_lock_combinations.append([i['time'] if datetime.fromisoformat(i['time']) < datetime.fromisoformat(ii['time']) 
                        else ii['time'],i['code'],i['buyPrice'],ii['code'],ii['sellPrice'],priceDiff])
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
            return val[-1] 
        outList.sort(key=sortLast)
    return outList