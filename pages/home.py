import streamlit as st


if not st.experimental_user.is_logged_in:
    st.title("Please login to access the home page.")
    

if st.experimental_user.is_logged_in:    
    st.title("Home page")
