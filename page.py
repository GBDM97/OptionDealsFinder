import time
import browser
import clearScript
import pandas as pd
import streamlit as st

browser.start()

def colorFn(v):
    if v.name == 'Buy':
        return ['color: deepSkyBlue'] * len(v)
    if v.name == 'Sell':
        return ['color: red'] * len(v)

with st.empty():
    while True:
        driver = browser.getDriver()
        if driver:
            input("input")
            df = pd.DataFrame(clearScript.getLockOutput(driver),
                               columns=['Profit Level','Buy','Buy Price', 'Sell', 'Sell Price', 
                                        'Multiplication', 'Percentage To Max. Profit'])
            df = df.style.apply(colorFn, subset=(slice(None),['Buy','Sell'])
            ).applymap(lambda x: 'color: lime' if float(x) >= 5 else None, subset=(slice(None),['Multiplication'])).applymap(
                 lambda x: 'color: lime' if float(x) <= 4 else None, subset=(slice(None),['Percentage To Max. Profit']))
            st.dataframe(df, hide_index=True, width=1100, height=500)
        else:
            st.write('LOADING....')

        time.sleep(1)