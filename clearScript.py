import json
import optionCodes,dataProcess
import ast
import ws

def testPrices():
    with open('Data\\testPrices.json', 'r') as file:
        return ast.literal_eval(file.read().replace('null','None'))

def exportTesPrices(l):
    with open("Data\\testPrices.json", "w") as file:
        json.dump(l, file, indent=2)

async def generateDataSet(driver,weekly) -> list[list[dict]]:
    asset_dataset = []
    final_dataset = []

    def save(readArray,writeDict):
        writeDict['buyPrice'] = readArray['arguments'][1]['bestBuyPrice']
        writeDict['sellPrice'] = readArray['arguments'][1]['bestSellPrice']
        writeDict['time'] = readArray['arguments'][1]['sendingTime']
        asset_dataset.append(writeDict)

    def search(readArray,writeDict):
        for i,v in enumerate(readArray):
            if v['arguments'][0] == writeDict['code']:
                save(readArray[i],writeDict)
                return True
        return False
            
    prices_index = 0
    currentOptions = optionCodes.importWeeklyFiltered() if weekly else optionCodes.importFiltered()
    prices = await ws.queryPrices([ii['code'] for i in currentOptions for ii in i],driver)
    # exportTesPrices(prices)
    # prices = testPrices()
    for i in currentOptions:
        asset_dataset = []
        for ii in i:
            if ii['code'] == prices[prices_index]['arguments'][0]:
                if ((prices[prices_index]['arguments'][1]['bestBuyPrice'] == None 
                or prices[prices_index]['arguments'][1]['bestSellPrice'] == None) 
                and 'strike' not in ii): 
                    while ii['code'][:4] == prices[prices_index]['arguments'][0][:4]:
                        prices_index+=1
                    break
                save(prices[prices_index],ii)
            elif 'strike' not in ii:
                if not search(prices[prices_index-50:prices_index+50],ii):
                    while ii['code'][:4] == prices[prices_index]['arguments'][0][:4]:
                        prices_index+=1
                    break
            else:
                if not search(prices[prices_index-50:prices_index+50],ii):
                    continue
            prices_index+=1
        if asset_dataset:
            final_dataset.append(asset_dataset)
    return final_dataset

async def createLockOutput(driver, weekly):
    await optionCodes.updateOptionsList(driver,weekly)
    assetsInputData = await generateDataSet(driver,weekly)
    exportTesPrices(assetsInputData)
    return dataProcess.getLockInfo(assetsInputData, weekly)