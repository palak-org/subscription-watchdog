import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import streamlit as st
from main import run_project   # your main function

st.title("Subscription Watchdog")

statement = st.text_area(
    "Paste your subscription statement:"
)



if st.button("Analyze"):

    result = run_project(statement)

    st.write("DEBUG RESULT:")
    st.write(result)