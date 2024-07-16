import streamlit as st

st.title('Hello Streamlit')
st.write("Welcome to your Streamlit app!")

if st.button('Say hello'):
    st.write('Hello!')
