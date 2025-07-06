import streamlit as st

from field import Field
from field_callback import field_callback
from structs.game import Type, Request, Game, Base as GameBase
from structs.user import User


def init_page(user: User):

	base_version = GameBase.dict_version
	@st.fragment(run_every=2)
	def check_updates():
		if GameBase.dict_version != base_version:
			st.rerun()
	check_updates()

	st.set_page_config('Новая игра', '⚔️', layout='wide')
	create_col, find_col = st.columns(2)

	with create_col.container(border=True):
		st.header('Создать')
		game_type = st.selectbox('Собираем:', Type.strings, None, placeholder='Хуи')
		if game_type:
			st.button('Найти жертву', icon='⚔️',
				on_click=lambda: Request(user.info, Type.from_str(game_type)))

	with find_col.container(border=True):
		requests = [base for base in GameBase.by_user.values() if isinstance(base, Request)]
		requests.sort(key=lambda request: request.begin_time, reverse=True)

		st.header('Найти')
		col1, col2, col3 = st.columns(3)
		for request in requests:
			col1.markdown(request.user.markdown_str(), unsafe_allow_html=True)
			col2.write(f'**{request.type.value.symbol}**')
			col3.button('Погнали', on_click=lambda: Game(request, user.info))


def waiting_page(user: User, request: Request):

	@st.fragment(run_every=2)
	def check_updates():
		base = GameBase.by_user.get(user.id)
		if isinstance(base, Request):
			base.refresh()
		else:
			st.rerun()
	check_updates()

	st.set_page_config('Ищем соперника', '⏳')
	st.header('Ищем соперника...')

	url = 'https://lottie.host/embed/4d476f8d-4494-4e16-937f-96fd2e859ba4/tp9IqZ9iEj.lottie'
	div_style = 'width: 100%; text-align: center;'
	embed_style = 'width: 65%; aspect-ratio : 1 / 1;'
	st.markdown(f'<div style="{div_style}"><embed src="{url}" style="{embed_style}"></div>', unsafe_allow_html=True)

	st.button('Я передумал', on_click=request.cancel)


def game_page(user: User, game: Game):

	counter = game.counter
	@st.fragment(run_every=2)
	def check_updates():
		if counter != game.counter:
			st.rerun()
	check_updates()

	st.set_page_config('Touche', '🎲')

	st.markdown(
		'<span style="font-size:1.5rem">Ходит </span>' + game.lead.markdown_str(1.5),
		unsafe_allow_html=True,
	)
	Field.component(
		user.id,
		game,
		lambda event: field_callback(user.id, game, event),
	)
	st.button('cancel', on_click=game.cancel)



def page(user: User):
	base = GameBase.by_user.get(user.id)

	if isinstance(base, Game):
		game_page(user, base)
	elif isinstance(base, Request):
		waiting_page(user, base)
	else:
		init_page(user)
