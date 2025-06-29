import streamlit as st
import game


if not st.user.is_logged_in:
	st.set_page_config('Кто ты?', '🙎🏻‍♂️')
	st.subheader('Залогинься')
	if st.button("Через Google", icon=":material/login:", type='primary'):
		st.login()
else:
	game.page()

