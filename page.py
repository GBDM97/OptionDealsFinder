import ast
import time
import pandas as pd
import streamlit as st

def colorFn(v):
    if v.name == 'Buy':
        return ['color: deepSkyBlue'] * len(v)
    if v.name == 'Sell':
        return ['color: red'] * len(v)

def importLockOutput():
    with open('Data\\lockOutput.json', 'r') as file:
        return ast.literal_eval(file.read())

with st.empty():
    while True:
        df = pd.DataFrame(importLockOutput(),
            columns=['Profit Level','Buy','Buy Price', 'Sell', 'Sell Price',
            'Multiplication', 'Percentage To Max. Profit'])
        df = df.style.apply(colorFn, subset=(slice(None),['Buy','Sell'])
        ).applymap(lambda x: 'color: lime' if float(x) <= 3 else None, 
                   subset=(slice(None),['Percentage To Max. Profit']))
        st.dataframe(df, hide_index=True, width=1100, height=500)
        time.sleep(1)
