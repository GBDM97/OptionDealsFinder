import ast
import ws

def sendNotification(driver,i):
    driver.execute_script("new Notification("+i['code']+ "'BREAKOUT',{'body':"+i['alertPrice']+"})")
    inputList[inputList.index()]['notified'] = True

async def importList():
    with open('Data\\priceMonitoring.json', 'r') as file:
        return ast.literal_eval(file.read())

inputList = importList()

async def start(driver):
    [ws.subscribeQuote(i['code']) for i in inputList]
    while True:
        # updates = ws.getUpdates(driver)
        # ws.clearUpdates()
        updates = ws.getSnapshots(driver)
        ws.clearSnapshots()
        for i in updates:
            for ii in inputList:
                if ((i['reference'] == ">" and not 'notified' in i and
                     i['alertPrice'] > ii['arguments'][1]['lastPrice'])
                or  (i['reference'] == "<" and not 'notified' in i and
                     i['alertPrice'] < ii['arguments'][1]['lastPrice'])):
                    sendNotification(driver,i)
