import streamlit as st

from structs.user import User
from user_ui import user_ui
from game_page import page as game_page


st.set_page_config(initial_sidebar_state='collapsed')

user = User.safe_create()


if user and user_ui(user):

	def reborn(): user.name = ''
	st.sidebar.button('Переродиться', on_click=reborn)

	#for debug; todo remove
	#if len(Game.all) == 0:
	#	Game.all[st.user.email] = Game(Request(st.user.email, st.user.email, Type.Cross))
#
	game_page(user)
