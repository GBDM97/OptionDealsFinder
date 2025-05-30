import browser
import clearScript
import asyncio
import priceMonitoring
import json
import ws

weekly = True

browser.start('https://portal.clear.com.br/login')
driver = browser.getDriver()

def exportLockOutput(l):
    with open('ReactApp\\optiondealsfinder\\src\\data\\lockOutput.json', "w") as file:
        json.dump(l, file, indent=2)

def exportWeeklyLockOutput(l):
    with open('Data\\weeklyLockOutput.json', "w") as file:
        json.dump(l, file, indent=2)

async def update():
    loop = asyncio.get_event_loop()
    while not await loop.run_in_executor(None, input, '\n Ready to update.\n\n'):
        await asyncio.sleep(10)
        ws.clearSnapshots(driver)
        await clearScript.createLockOutput(driver,weekly)
        priceMonitoring.subscribeList(driver)

async def main():
    input('Verify permission.')
    priceMonitoring.subscribeList(driver)
    driver.execute_script('await Notification.requestPermission();')
    input('Start?')
    await asyncio.gather(
        priceMonitoring.start(driver),
        update()
    )

asyncio.run(main())