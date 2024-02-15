def assetLockInfo(input_data:list[dict]) -> list[dict]:
    result = []
    optType = 'CALL'
    for data in input_data[1:]:
        all_lock_combinations = [
            (i['strike'],i['code']+"("+i['strike']+")",i['sellPrice'],ii['code']+"("+ii['strike']+")",ii['buyPrice'],
            (float(i['sellPrice'])-float(ii['buyPrice']))/(float(ii['strike'])-float(i['strike']))) 
            for i in data for ii in data if ii['code'] != i['code'] and float(ii['strike']) >= float(i['strike'])
        ] if optType == 'CALL' else [
            (ii['strike'],ii['code']+"("+ii['strike']+")",ii['sellPrice'],i['code']+"("+i['strike']+")",i['buyPrice'],
            (float(ii['sellPrice'])-float(i['buyPrice']))/(float(ii['strike'])-float(i['strike'])))
            for i in data for ii in data if ii['code'] != i['code'] and float(ii['strike']) >= float(i['strike'])
        ]
        result.append(list(sorted(all_lock_combinations, key=lambda x: x[0],reverse=False if optType == 'CALL' else True)))
        optType = 'PUT'
    return result

def getLockInfo(l:list[list[dict]]) -> list[dict]:
    outList = []
    for i in l:
        outList.append(assetLockInfo(i))
    return outList