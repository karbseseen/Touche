import streamlit as st


st.subheader('Залогинься')
if st.button("Через Google", icon=":material/login:", type='primary'):
	st.login()
