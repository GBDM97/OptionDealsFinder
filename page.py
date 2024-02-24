import time
import browser
import clearScript
import streamlit as st

browser.start()
with st.empty():
    while True:
        driver = browser.getDriver()
        if driver:
            st.write(driver.title)
        else:
            st.write('LOADING....')
        time.sleep(1)