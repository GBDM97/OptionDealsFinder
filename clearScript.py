import optionCodes,dataProcess
import ast
import ws

def testPrices():
    with open('Data\\testPrices.json', 'r') as file:
        return ast.literal_eval(file.read().replace('null','None'))

def generateDataSet(driver) -> list[list[dict]]:
    asset_dataset = []
    final_dataset = []

    def save(readArray,writeDict):
        writeDict['buyPrice'] = readArray['arguments'][1]['bestBuyPrice']
        writeDict['sellPrice'] = readArray['arguments'][1]['bestSellPrice']
        asset_dataset.append(writeDict)

    def search(readArray,writeDict):
        for i in readArray:
            if i['arguments'][0] == writeDict['code']:
                save(readArray,writeDict)
                return True
        return False
            
    prices_index = 0
    prices = ws.queryPrices(driver)
    for i in optionCodes.get():
        asset_dataset = []
        for ii in i:
            if ii['code'] == prices[prices_index]['arguments'][0]:
                save(prices[prices_index],ii)
            elif 'strike' not in ii:
                if not search(prices[prices_index-50:prices_index+50],ii):
                    while ii['code'][:4] == prices[prices_index]['arguments'][0][:4]:
                        prices_index+=1
                    break
            else:
                if not search(prices[prices_index-50:prices_index+50],ii):
                    prices_index+=1
                    continue
            prices_index+=1
        if asset_dataset:
            final_dataset.append(asset_dataset)
    return final_dataset

def getLockOutput(driver):
    return dataProcess.getLockInfo(generateDataSet(driver))