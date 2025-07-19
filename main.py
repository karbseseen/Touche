import streamlit as st

from game.page import page as game_page
from structs.user import User
from user_ui import user_ui


st.set_page_config(initial_sidebar_state='collapsed')

user = User.safe_create()

if user and user_ui(user):
	game_page(user)
