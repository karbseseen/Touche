import streamlit as st

from structs.game import Base as GameBase, Game, Request, Type
from structs.user import User
from user_ui import user_ui
from game_page import page as game_page


st.set_page_config(initial_sidebar_state='collapsed', layout='centered')

user = User.safe_create()


if user and user_ui(user):

	def reborn(): user.name = ''
	st.sidebar.button('Переродиться', on_click=reborn)

	#for debug; todo remove
	#if len(GameBase.by_user) == 0:
	#	GameBase.by_user[user.id] = Game(Request(user.info, Type.Cross), user.info)

	game_page(user)
