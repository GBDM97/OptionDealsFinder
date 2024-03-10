import browser
import clearScript
import asyncio
import priceMonitoring
import json

browser.start()
driver = browser.getDriver()

def exportLockOutput(l):
    with open('Data\\lockOutput.json', "w") as file:
        json.dump(l, file, indent=2)

async def test():
    n = 0
    while True:
        print('loop running...'+str(n))
        await asyncio.sleep(2)
        n += 1

async def update():
    loop = asyncio.get_event_loop()
    while not await loop.run_in_executor(None, input, '\n Ready for Update.\n\n'):
        await asyncio.sleep(10)
        driver.execute_script('messages=[]')
        lockOutput = await clearScript.createLockOutput(driver)
        exportLockOutput(lockOutput)

async def main():
    input('Start?')
    await asyncio.gather(
        priceMonitoring.start(),
        update()
    )

asyncio.run(main())