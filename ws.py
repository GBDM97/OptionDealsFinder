import ast

def sendMessage(m,driver):
    driver.execute_script('temp1.send(JSON.stringify('+m+')+\'\x1E\');')

async def getSnapshots(driver):
    return driver.execute_script('return snapshots')

async def getUpdates(driver):
    return driver.execute_script('return updates')

def quoteSnapshot(a,driver):
    sendMessage('{"arguments":["'+a+'"],"target":"SubscribeQuote","type":1}',driver)
    sendMessage('{"arguments":["'+a+'"],"target":"UnsubscribeQuote","type":1}',driver)

def subscribeQuote(a,driver):
    sendMessage('{"arguments":["'+a+'"],"target":"SubscribeQuote","type":1}',driver)

def unsubscribeQuote(a,driver):
    sendMessage('{"arguments":["'+a+'"],"target":"UnsubscribeQuote","type":1}',driver)

def clearSnapshots(driver):
    driver.execute_script('snapshots=[]')

def clearUpdates(driver):
    driver.execute_script('updates=[]')

async def queryPrices(list, driver):
    last = ''
    for index,asset in enumerate(list):
        quoteSnapshot(asset,driver)
        print('Snap= '+asset)
        index += 1
        if (index == 2000 or index == 3000 or
        index == 4000 or index == 5000 or index == 6000 or
        index == 7000 or index == 8000):
            input('WS')
        last = asset
    ret = await getSnapshots(driver)
    while not ret or ret[-1]['arguments'][0] != last:
        ret = await getSnapshots(driver)
    return ast.literal_eval(str(ret).replace('null','None'))

