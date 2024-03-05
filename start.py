import browser
import clearScript
import asyncio
import json

browser.start()
driver = browser.getDriver()

def exportLockOutput(l):
    with open('Data\\lockOutput.json', "w") as file:
        json.dump(l, file, indent=2)

async def main():
    while not input("\n\nReady for update.\n\n"):
        driver.execute_script('messages=[]')
        lockOutput = await clearScript.createLockOutput(driver)
        exportLockOutput(lockOutput)

asyncio.run(main())