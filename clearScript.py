import optionCodes,dataProcess
import ast
import json
import ws

def testPrices():
    with open('Data\\testPrices.json', 'r') as file:
        return ast.literal_eval(file.read().replace('null','None'))

def generateDataSet(driver) -> list[list[dict]]:
    asset_dataset = []
    final_dataset = []
    prices_index = 0
    prices = testPrices()
    # prices = ws.queryPrices(driver)
    for ii in optionCodes.get():
        asset_dataset = []
        if prices_index >= 7000:
            print
        for i in ii:
            b = prices[prices_index]['arguments'][1]['bestBuyPrice'] 
            s = prices[prices_index]['arguments'][1]['bestSellPrice']
            new = {'code': i['code'], 'buyPrice': b if b!=None else '-','sellPrice': s if s!=None else '-'}
            if 'strike' in i:
                new['strike'] = i['strike']
            asset_dataset.append(new)
            prices_index += 1
        final_dataset.append(asset_dataset)
    return final_dataset

def getLockOutput(driver):
    return dataProcess.getLockInfo(generateDataSet(driver))