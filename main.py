import streamlit as st
import game
from game import Game, Request, Type

if not st.user.is_logged_in:
	st.set_page_config('Кто ты?', '🙎🏻‍♂️')
	st.subheader('Залогинься')
	if st.button("Через Google", icon=":material/login:", type='primary'):
		st.login()
else:
	if len(Game.all) == 0:
		Game.all[st.user.email] = Game(Request(st.user.email, st.user.email, Type.Cross))
	game.page()

