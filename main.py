import streamlit as st

from game.page import page as game_page
from structs.user import User
from user_ui import user_ui


st.set_page_config(initial_sidebar_state='collapsed')

user = User.safe_create()


def _reborn():
	user.name = ''
	user.color = User.default_color

if user and user_ui(user):
	st.sidebar.button('Переродиться', on_click=_reborn)
	game_page(user)
