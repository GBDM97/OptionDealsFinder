import ast
import requests
import json

currentList = [
  "ABEV3",
  "AESB3",
  "ALOS3",
  "ALPA4",
  "ALUP11",
  "ARZZ3",
  "ASAI3",
  "B3SA3",
  "BBAS3",
  "BBDC3",
  "BBDC4",
  "BBSE3",
  "BEEF3",
  "BHIA3",
  "BOVA11",
  "BOVV11",
  "BPAC11",
  "BPAN4",
  "BRAP4",
  "BRFS3",
  "BRKM5",
  "CASH3",
  "CCRO3",
  "CIEL3",
  "CMIG4",
  "CMIN3",
  "COGN3",
  "CPFE3",
  "CPLE6",
  "CRFB3",
  "CSAN3",
  "CSNA3",
  "CXSE3",
  "CYRE3",
  "DXCO3",
  "ECOR3",
  "EGIE3",
  "ELET3",
  "ELET6",
  "EMBR3",
  "ENEV3",
  "ENGI11",
  "EQTL3",
  "EZTC3",
  "FLRY3",
  "GFSA3",
  "GGBR4",
  "GOAU4",
  "HAPV3",
  "HYPE3",
  "IBOV11",
  "IGTI11",
  "IRBR3",
  "ITSA4",
  "ITUB3",
  "ITUB4",
  "IVVB11",
  "JBSS3",
  "JHSF3",
  "KLBN11",
  "LEVE3",
  "LREN3",
  "LWSA3",
  "MEAL3",
  "MGLU3",
  "MRFG3",
  "MRVE3",
  "MULT3",
  "NEOE3",
  "NTCO3",
  "PCAR3",
  "PETR3",
  "PETR4",
  "PETZ3",
  "POSI3",
  "PRIO3",
  "RADL3",
  "RAIL3",
  "RAIZ4",
  "RDOR3",
  "RENT3",
  "RRRP3",
  "SANB11",
  "SAPR11",
  "SBSP3",
  "SLCE3",
  "SMAL11",
  "SMTO3",
  "SOMA3",
  "SUZB3",
  "TAEE11",
  "USIM5",
  "VALE3",
  "WEGE3"
]
testList = ['ABEV3','AESB3']

def assetOptionsToList(asset: str,currentCode: str) -> list:
    response = requests.get('https://opcoes.net.br/opcoes/bovespa/'+asset+'/json?skip=0&load=8&colsAndUnderlyingInfo=true').json()
    index = 0
    for i,v in enumerate(response['data']['expirations']):
        optCode = v['calls'][0][0]
        if len(optCode) <= 4 and optCode[0]==currentCode:
            index = i
            break 
    calls = response['data']['expirations'][index]['calls']
    puts = response['data']['expirations'][index]['puts']
    calls+=puts
    return calls


def get():
    with open('Data\\testOptionsList.json', 'r') as file:
        return ast.literal_eval(file.read())

def write(callCode):
    outArray = []
    for i in currentList:
        assetArr = []
        assetArr.append({'code':i})
        l = assetOptionsToList(i,callCode)
        for ii in l:
            d = {"code":i[:4]+ii[0],"strike":ii[3]}
            assetArr.append(d)
        outArray.append(assetArr)
    with open('currentOptionsList.json', 'w') as file:
        file.write(json.dumps(outArray))
