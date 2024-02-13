import requests

currentList = ['ABEV3', 'ABCB4', 'AERI3', 'AESB3', 'AGRO3', 'ALOS3', 'ALPA4', 'ALUP11', 'AMBP3', 'ANIM3', 'ARZZ3', 'ASAI3', 'AURE3', 'AZUL4', 'B3SA3', 'BBAS3', 'BBDC3', 'BBDC4', 'BBSE3', 'BEEF3', 'BHIA3', 'BLAU3', 'BMOB3', 'BOVA11', 'BOVV11', 'BPAC11', 'BPAN4', 'BRAP4', 'BRFS3', 'BRKM5', 'BRSR6', 'CASH3', 'CCRO3', 'CEAB3', 'CIEL3', 'CMIG4', 'CMIN3', 'COGN3', 'CPFE3', 'CPLE6', 'CRFB3', 'CSAN3', 'CSMG3', 'CSNA3', 'CVCB3', 'CXSE3', 'CYRE3', 'DXCO3', 'ECOR3', 'EGIE3', 'ELET3', 'ELET6', 'EMBR3', 'ENAT3', 'ENEV3', 'ENGI11', 'EQTL3', 'EVEN3', 'EZTC3', 'FLRY3', 'GFSA3', 'GGBR4', 'GGPS3', 'GOAU4', 'GRND3', 'GUAR3', 'HAPV3', 'HBOR3', 'HBSA3', 'HYPE3', 'IBOV11', 'IGTI11', 'IRBR3', 'ITSA4', 'ITUB3', 'ITUB4', 'IVVB11', 'JBSS3', 'JHSF3', 'KEPL3', 'KLBN11', 'LEVE3', 'LJQQ3', 'LREN3', 'LWSA3', 'MEAL3', 'MGLU3', 'MILS3', 'MRFG3', 'MRVE3', 'MULT3', 'MYPK3', 'NEOE3', 'NTCO3', 'PCAR3', 'PETR3', 'PETR4', 'PETZ3', 'POSI3', 'PRIO3', 'QUAL3', 'RADL3', 'RAIL3', 'RAIZ4', 'RANI3', 'RAPT4', 'RDOR3', 'RENT3', 'ROMI3', 'RRRP3', 'SANB11', 'SAPR11', 'SBFG3', 'SBSP3', 'SEER3', 'SIMH3', 'SLCE3', 'SMAL11', 'SMFT3', 'SMTO3', 'SOMA3', 'STBP3', 'SUZB3', 'TAEE11', 'TEND3', 'TIMS3', 'TOTS3', 'TRPL4', 'UGPA3', 'USIM5', 'VALE3', 'VBBR3', 'VIVA3', 'VIVT3', 'WEGE3', 'WIZC3', 'XPBR31', 'YDUQ3']
testList = ['AERI3']

def assetOptionsToList(asset):
    response = requests.get('https://opcoes.net.br/opcoes/bovespa/'+asset+'/json?skip=0&load=8&colsAndUnderlyingInfo=true').json()
    calls = response['data']['expirations'][0]['calls']
    puts = response['data']['expirations'][0]['puts']
    with open('currentOptionsList.txt', 'w') as file:
        file.write(asset+'\n')
        [file.write(asset[:4] + i[0] + '\n') for i in calls]
        [file.write(asset[:4] + i[0] + '\n')for i in puts]

def get():
    with open('currentOptionsList.txt', 'r') as file:
        return [i.replace('\n','') for i in file]

def write():
    [assetOptionsToList(i) for i in testList]

# print(get())
# write()
    