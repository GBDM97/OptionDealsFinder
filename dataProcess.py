import re

def assetLockInfo(input_data:list[dict]) -> list[dict]:
    callCodes = ['A','B','C','D','E','F','G','H','I','J','K','L']
    all_lock_combinations = []
    stockPrice = (input_data[0]['buyPrice']+input_data[0]['sellPrice'])/2
    data = input_data[1:]
    def verifyOptType(s):
        return any(map(lambda x: x == (re.search("[a-zA-Z]+",s).group(0)[-1]),callCodes))
    for ii in data: 
        for i in data:
            try:
                strikeDiff = ii['strike']-i['strike']
                if (ii['code'] != i['code'] and ii['strike'] >= i['strike'] 
                and i['buyPrice'] >= 0.1 and i['buyPrice'] <= 0.5 
                and ii['buyPrice'] >= 0.1 and ii['buyPrice'] <= 0.5
                and i['sellPrice'] >= 0.1 and i['sellPrice'] <= 0.5 
                and ii['sellPrice'] >= 0.1 and ii['sellPrice'] <= 0.5
                and strikeDiff >= 0.25):
                    itype = verifyOptType(i['code'])
                    iitype = verifyOptType(ii['code'])
                    if itype and iitype and i['strike'] > stockPrice and ii['strike'] > stockPrice:
                        all_lock_combinations.append([i['strike'],i['code']+"("+str(i['strike'])+")",i['sellPrice'],
                        ii['code']+"("+str(ii['strike'])+")",ii['buyPrice'],
                        strikeDiff,
                        round(((ii['strike']-stockPrice)/stockPrice)*100,3)])
                    if not itype and not iitype and i['strike'] < stockPrice and ii['strike'] < stockPrice:
                        all_lock_combinations.append([ii['strike'],ii['code']+"("+str(ii['strike'])+")",ii['sellPrice'],
                        i['code']+"("+str(i['strike'])+")",i['buyPrice'],
                        strikeDiff,
                        round(((stockPrice-i['strike'])/stockPrice)*100,3)])
            except (TypeError, ZeroDivisionError):
                continue
    return list(sorted(all_lock_combinations, key=lambda x: x[0],reverse=False))

def getLockInfo(l:list[list[dict]]) -> list[dict]:
    outList = []
    for i in l:
        outList.extend(assetLockInfo(i))
    return outList