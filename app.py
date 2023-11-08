from io import StringIO

import streamlit as st
import pandas as pd

with st.sidebar:
    text = st.text_area("Text to analyze", "Enter some text here", height=250)
    deliminator = st.text_input("Deliminator", ",")

text_io = StringIO(text)

df = pd.read_csv(text_io, sep=deliminator)

st.dataframe(df)
