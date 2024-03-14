import re

def assetLockInfo(input_data:list[dict]) -> list[dict]:
    callCodes = ['A','B','C','D','E','F','G','H','I','J','K','L']
    all_lock_combinations = []
    stockPrice = (input_data[0]['buyPrice']+input_data[0]['sellPrice'])/2
    data = input_data[1:]
    def verifyOptType(s):
        return any(map(lambda x: x == (re.search("[a-zA-Z]+",s[::-1]).group(0)[0]),callCodes))
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
                        all_lock_combinations.append([i['strike'],i['code']+"("+str(i['strike'])+")",i['sellPrice'],
                        ii['code']+"("+str(ii['strike'])+")",ii['buyPrice'],round(i['sellPrice']-ii['buyPrice']),
                        (strikeDiff-(i['sellPrice']-ii['buyPrice']))/(i['sellPrice']-ii['buyPrice']),
                        round(((ii['strike']-stockPrice)/stockPrice)*100,3)])
                    if not itype and not iitype and i['strike'] < stockPrice and ii['strike'] < stockPrice:
                        all_lock_combinations.append([ii['strike'],ii['code']+"("+str(ii['strike'])+")",ii['sellPrice'],
                        i['code']+"("+str(i['strike'])+")",i['buyPrice'],round(ii['sellPrice']-i['buyPrice'],2),
                        (strikeDiff-(ii['sellPrice']-i['buyPrice']))/(ii['sellPrice']-i['buyPrice']),
                        round(((stockPrice-i['strike'])/stockPrice)*100,3)])
            except (TypeError, ZeroDivisionError):
                continue
    return list(sorted(all_lock_combinations, key=lambda x: x[0],reverse=False))

def getLockInfo(l:list[list[dict]]) -> list[dict]:
    outList = []
    for i in l:
        outList.extend(assetLockInfo(i))
    return outList