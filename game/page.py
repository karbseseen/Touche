import streamlit as st
from streamlit_extras.let_it_rain import rain

from field import Field
from structs.game import Request, Game, Base as GameBase
from structs.game_type import GameType
from structs.user import User
from . import field_event


def _init_page(user: User):

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
		game_type = st.selectbox('Собираем:', [type.value.text for type in GameType], None, placeholder='Хуи')
		if game_type:
			st.button('Найти жертву', icon='⚔️',
				on_click=lambda: Request(user.info, GameType.from_str(game_type)))

	with find_col.container(border=True):
		requests = [base for base in GameBase.by_user.values() if isinstance(base, Request)]
		requests.sort(key=lambda request: request.begin_time, reverse=True)

		st.header('Найти')
		col1, col2, col3 = st.columns(3)
		for request in requests:
			col1.markdown(request.user.markdown_str(), unsafe_allow_html=True)
			col2.write(f'**{request.type.value.symbol}**')
			col3.button('Погнали', on_click=lambda: Game(request, user.info))


def _waiting_page(user: User, request: Request):

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


def _game_page(user: User, game: Game):

	counter = game.counter
	@st.fragment(run_every=1.5)
	def check_updates():
		if counter != game.counter:
			st.rerun()
	check_updates()

	st.set_page_config('Touche', '🎲')

	winner = game.winner
	if winner:
		is_winner = winner.info.id == user.id
		rain('🏆' if is_winner else '💩')
		st.header('Вы чемпион!' if is_winner else 'Вы продули :(')
	else:
		st.markdown(
			'<span style="font-size:2rem">Ходит </span>' + game.lead.info.markdown_str(2),
			unsafe_allow_html=True,
		)

	player = game.get_player(user.id)
	if player.figures.is_invalid:
		st.error('Поздравляю, вы собрали какую-то хрень. Вам остается только отменять ходы и пробовать заново.')

	Field.component(
		user.id,
		game,
		lambda event: field_event.callback(user.id, game, event),
	)

	if field_event.can_undo(user.id, game):
		st.button('Отмена хода', on_click=lambda: field_event.undo(user.id, game))
	st.button('Уйти', on_click=game.cancel)


def page(user: User):
	base = GameBase.by_user.get(user.id)

	if isinstance(base, Game):
		_game_page(user, base)
	elif isinstance(base, Request):
		_waiting_page(user, base)
	else:
		_init_page(user)
