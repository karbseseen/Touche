import time
import streamlit as st

import field
from structs.game import Type, Request, Game, Base as GameBase
from structs.user import User


@st.fragment(run_every=2)
def game_list(user: User):
	requests = [base for base in GameBase.by_user.values() if isinstance(base, Request)]
	requests.sort(key=lambda request: request.begin_time, reverse=True)

	st.header('Найти')
	col1, col2, col3 = st.columns(3)
	selected_request: Request | None = None
	for request in requests:
		col1.markdown(request.user.markdown_str(), unsafe_allow_html=True)
		col2.write(f'**{request.type.value.symbol}**')
		if col3.button('Погнали'):
			selected_request = request

	if selected_request:
		Game(selected_request, user.info)
		st.rerun()


def init_page(user: User):
	st.set_page_config('Новая игра', '⚔️', layout='wide')
	create_col, find_col = st.columns(2)

	with create_col.container(border=True):
		st.header('Создать')
		game_type = st.selectbox('Собираем:', Type.strings, None, placeholder='Хуи')
		if game_type:
			st.button('Найти жертву', icon='⚔️',
				on_click=lambda: Request(user.info, Type.from_str(game_type)))

	with find_col.container(border=True):
		game_list(user)


def waiting_page(user: User, request: Request):
	st.set_page_config('Ждемcc', '⏳', layout='centered')
	spinner_holder = st.empty()
	st.button('Я передумал', on_click=request.cancel)

	with spinner_holder:
		with st.spinner('Ждемcc', show_time=True):
			while True:
				time.sleep(2)
				base = GameBase.by_user.get(user.id)
				if isinstance(base, Request):
					base.refresh()
				else:
					st.rerun()


def game_page(user: User, game: Game):
	st.set_page_config('Touche', '🎲', layout='centered')
	st.button('cancel', on_click=game.cancel)

	value = field.touche_field(game.pressed, game.deck1.value)
	st.write(value)



def page(user: User):
	base = GameBase.by_user.get(user.id)


	if isinstance(base, Game):
		game_page(user, base)
	elif isinstance(base, Request):
		waiting_page(user, base)
	else:
		init_page(user)
