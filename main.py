import streamlit as st
import pandas as pd
# main pipeline

st.title("wtf is this even")

# dataframe section
st.subheader("Dataframe")
df = pd.DataFrame({
    'Name': ['alice', 'bob', 'kim', 'kirk'],
    'Age': [23, 34, 22, 21],
    'Occupation': ['engineer', 'doctor', 'doge', 'chef']
})
st.dataframe(df)
# data editor section editable datarame
st.subheader("Data Editor")
editable_df = st.data_editor(df)
print(editable_df)
# static table
st.subheader("static table")
st.table(df)
