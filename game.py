import time
from enum import Enum
from pathlib import Path
import streamlit as st
from streamlit_theme import st_theme
import field
from deck import Deck
from xorshift import XorShift



class Type(Enum):
	Square = 'Квадраты'
	Line = 'Линии'
	Cross = 'Кресты'
	T = 'Букву Т'

	@staticmethod
	def from_str(value: str):
		for type in Type:
			if type.value == value:
				return type
		return None
Type.strings = [type.value for type in Type]

class Request:
	all = {}
	def __init__(self, from_user: str, to_user: str, type: Type):
		self.from_user = from_user
		self.to_user = to_user
		self.type = type
		Request.all[from_user] = self
		Request.all[to_user] = self
	def cancel(self):
		Request.all.pop(self.from_user, None)
		Request.all.pop(self.to_user, None)

class Game:
	all = {}
	def __init__(self, request: Request):
		self.player1 = request.from_user
		self.player2 = request.to_user
		self.type = request.type

		self.random = XorShift()
		self.deck1 = Deck(self.random)
		self.deck2 = Deck(self.random)

		self.pressed: list[int] = []

		request.cancel()
		Game.all[self.player1] = self
		Game.all[self.player2] = self
	def cancel(self):
		Game.all.pop(self.player1, None)
		Game.all.pop(self.player2, None)


def init_page():
	@st.fragment(run_every=1.5)
	def invite_check():
		if st.user.email in Request.all:
			st.rerun()
	invite_check()

	st.set_page_config('Новая игра', '⚔️')
	st.warning('''Как вас можно найти:\n
''' + st.user.email)
	user2 = st.text_input('Вызываю на дуэль игрока:', placeholder='Гриб Грибович')
	game_type = st.selectbox('Собираем:', Type.strings, None)
	if user2 and game_type and st.user.email != user2:
		st.button('Бросить вызов', 'start-game', icon='⚔️',
			  on_click=lambda: Request(st.user.email, user2, Type.from_str(game_type)))

def waiting_page(request: Request):
	st.set_page_config('Ждем', '⏳')
	st.text_input('Вызываю на дуэль игрока:', request.to_user, disabled=True)
	st.selectbox('Собираем:', Type.strings, list(Type).index(request.type), disabled=True)
	spinner_holder = st.empty()
	st.button('Я передумал', on_click=request.cancel)

	with spinner_holder:
		with st.spinner('Ждем игрока ' + request.to_user, show_time=True):
			for _ in range(20):
				time.sleep(1.5)
				if st.user.email not in Request.all or st.user.email in Game.all:
					st.rerun()
			request.cancel()
			st.rerun()

def request_page(request: Request):
	@st.fragment(run_every=1.5)
	def still_available_check():
		if st.user.email not in Request.all:
			st.rerun()
	still_available_check()

	st.set_page_config('Вам бросили вызов', '⚔️')
	st.subheader(request.from_user + ' вызывает вас на дуэль в Touche!')
	st.text('Будем собирать ' + request.type.value)

	col1, col2, _ = st.columns([1,1,1.5])
	col1.button('Принять вызов', icon='⚔️', on_click=lambda: Game(request))
	col2.button('Послать его', icon='🚽', on_click=request.cancel)

def game_page(game: Game):
	st.set_page_config('Touche', '🎲')
	#st.button('cancel', on_click=game.cancel)

	value = field.touche_field()
	st.text(type(value))


def page():
	st.sidebar.button('Выйти (в окно)', on_click=st.logout)

	st.write(Request.all)
	st.write(Game.all)

	game_page(Game(Request(st.user.email, st.user.email, Type.T)))
	return

	request: Request = Request.all.get(st.user.email)
	game: Game = Game.all.get(st.user.email)
	if game:
		game_page(game)
	elif request and request.from_user == st.user.email:
		waiting_page(request)
	elif request and request.to_user == st.user.email:
		request_page(request)
	else:
		init_page()
