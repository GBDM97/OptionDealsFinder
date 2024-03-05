import ast
import requests
import json
import ws

underlyingAssets = ["ABEV3","AESB3","ALOS3","ALPA4","ALUP11","ARZZ3","ASAI3","B3SA3","BBAS3","BBDC3","BBDC4","BBSE3","BEEF3","BHIA3","BOVA11","BOVV11","BPAC11","BPAN4","BRAP4","BRFS3","BRKM5","CASH3","CCRO3","CIEL3","CMIG4","CMIN3","COGN3","CPFE3","CPLE6","CRFB3","CSAN3","CSNA3","CXSE3","CYRE3","DXCO3","ECOR3","EGIE3","ELET3","ELET6","EMBR3","ENEV3","ENGI11","EQTL3","EZTC3","FLRY3","GFSA3","GGBR4","GOAU4","HAPV3","HYPE3","IBOV11","IGTI11","IRBR3","ITSA4","ITUB3","ITUB4","IVVB11","JBSS3","JHSF3","KLBN11","LEVE3","LREN3","LWSA3","MEAL3","MGLU3","MRFG3","MRVE3","MULT3","NEOE3","NTCO3","PCAR3","PETR3","PETR4","PETZ3","POSI3","PRIO3","RADL3","RAIL3","RAIZ4","RDOR3","RENT3","RRRP3","SANB11","SAPR11","SBSP3","SLCE3","SMAL11","SMTO3","SOMA3","SUZB3","TAEE11","USIM5","VALE3","WEGE3"]
testList = ['ABEV3','AESB3']

def getAllOptionsAPI(assets: str,currentCallCode: str) -> list:
    output = []
    for a in assets:
        print(a)
        response = requests.get('https://opcoes.net.br/opcoes/bovespa/'+a+'/json?skip=0&load=8&colsAndUnderlyingInfo=true').json()
        index = 0
        for i,v in enumerate(response['data']['expirations']):
            optCode = v['calls'][0][0]
            if len(optCode) <= 4 and optCode[0]==currentCallCode:
                index = i
                break 
        calls = response['data']['expirations'][index]['calls']
        puts = response['data']['expirations'][index]['puts']
        calls+=puts
        outAssetList = [{'code':a}]
        outAssetList.extend(map(lambda x: {"code":a[:4]+x[0],"strike":x[3]},calls))
        output.append(outAssetList)
    return output
    
def importCurrent():
    with open('Data\\currentOptionsList.json', 'r') as file:
        return ast.literal_eval(file.read())

def importPrices():
    with open('Data\\testPrices.json', 'r') as file:
        return ast.literal_eval(file.read().replace('null','None'))

def importFiltered():
    with open('Data\\filteredOptionsList.json', 'r') as file:
        return ast.literal_eval(file.read())

def exportCurrentOptionsList(l):
    with open('Data\\currentOptionsList.json', "w") as file:
        json.dump(l, file, indent=2)

def exportFilteredOptions(l):
    with open('Data\\filteredOptionsList.json', "w") as file:
        json.dump(l, file, indent=2)

def exportTestPrices(l):
    with open('Data\\testPrices.json', "w") as file:
        json.dump(l, file, indent=1)

async def updateOptionsList(driver):
    percentage = 5
    assetsPrices = await ws.queryPrices(underlyingAssets,driver)
    driver.execute_script('messages=[]')
    # assetsPrices = getPrices()
    # assetsOptions = getAllOptionsAPI(underlyingAssets, 'C')
    assetsOptions = importCurrent()
    for i,v in enumerate(assetsPrices):
        b = v['arguments'][1]['bestBuyPrice']
        b = b if b is not None else 0
        s = v['arguments'][1]['bestSellPrice']
        s = s if s is not None else 0
        price = (b+s)/2
        if price == 0:
            assetsPrices[i]=None
            assetsOptions[i]=None
            continue
        priceRange = [price-price*(percentage/100),price+price*(percentage/100)]
        for ii,vv in enumerate(assetsOptions[i][1:]):
            if vv['strike'] < priceRange[0] or vv['strike'] > priceRange[1]:
                assetsOptions[i][ii+1]=None
        assetsOptions[i] = list(filter(None,assetsOptions[i]))
    assetsOptions = list(filter(lambda x: x is not None and len(x) != 1, assetsOptions))
    exportFilteredOptions(assetsOptions)