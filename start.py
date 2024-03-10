import browser
import clearScript
import asyncio
import priceMonitoring
import json
import ws

browser.start()
driver = browser.getDriver()

def exportLockOutput(l):
    with open('Data\\lockOutput.json', "w") as file:
        json.dump(l, file, indent=2)

async def update():
    loop = asyncio.get_event_loop()
    while not await loop.run_in_executor(None, input, '\n Ready for Update.\n\n'):
        await asyncio.sleep(10)
        ws.clearSnapshots()
        lockOutput = await clearScript.createLockOutput(driver)
        exportLockOutput(lockOutput)
        [ws.subscribeQuote(i['code']) for i in priceMonitoring.importList()]


async def main():
    driver.execute_script('await Notification.requestPermission();')
    input('Start?')
    await asyncio.gather(
        priceMonitoring.start(driver),
        update()
    )

asyncio.run(main())