import time
import browser
import clearScript
import pandas as pd
import streamlit as st
import asyncio

def colorFn(v):
    if v.name == 'Buy':
        return ['color: deepSkyBlue'] * len(v)
    if v.name == 'Sell':
        return ['color: red'] * len(v)
    
async def main():
    browser.start()
    updateStatus = False
    if input("Please configure env and set params:\n"): #anything other than blank will update optionsList
        updateStatus = True
    driver = browser.getDriver()
    try:
        lockOutput = await clearScript.getLockOutput(updateStatus,driver)
    except Exception as e:
        print(e)
    with st.empty():
        while True:
            if driver:
                df = pd.DataFrame(lockOutput,
                                columns=['Profit Level','Buy','Buy Price', 'Sell', 'Sell Price',
                                            'Strike Difference*100', 'Percentage To Max. Profit'])
                df = df.style.apply(colorFn, subset=(slice(None),['Buy','Sell'])
                ).applymap(lambda x: 'color: lime' if float(x) <= 4 else None, subset=(slice(None),['Percentage To Max. Profit']))
                st.dataframe(df, hide_index=True, width=1100, height=500)
            else:
                st.write('LOADING....')

            time.sleep(1)

asyncio.run(main())