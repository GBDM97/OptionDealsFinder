import ast
import json
import os
from dotenv import load_dotenv
import urllib

load_dotenv()

def sendMessage(m,driver):
    driver.execute_script('temp1.send(JSON.stringify('+m+')+\'\x1E\');')

async def getSnapshots(driver):
    return ast.literal_eval(str(driver.execute_script('return snapshots')).replace('null','None'))

async def getUpdates(driver):
    return ast.literal_eval(str(driver.execute_script('return updates')).replace('null','None'))
    
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

def sendTwilioMessage(driver,opt:str):
    url = os.getenv('TW_URL')
    auth = os.getenv('TW_AUTH_TOKEN')
    sid = os.getenv('TW_SID')
    number = os.getenv('MOBILE_NUMBER')
    js_code = f"""
        var xhr = new XMLHttpRequest();
        xhr.open('POST', '{url}', true);
        xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
        xhr.setRequestHeader('Authorization', 'Basic {auth}');
        var data = 'To=whatsapp:{number}&From=whatsapp:14155238886&ContentSid={sid}&ContentVariables={urllib.parse.quote(json.dumps({"1": opt}))};
        xhr.send(data);
        xhr.onload = function () {{
            if (xhr.status >= 200 && xhr.status < 300) {{
                console.log('Success:', xhr.status, xhr.responseText);
            }} else {{
                console.error('Request failed with status:', xhr.status, xhr.responseText);
            }}
        }};
    """
    print(js_code)
    driver.execute_script(js_code)


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

