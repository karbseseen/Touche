from pathlib import Path
from random import random

import streamlit as st
import streamlit.components.v1 as components
from streamlit_theme import st_theme
from deck import Deck


def __get_values():
	suits = ['♥', '♦', '♣', '♠']
	numbers = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
	numbers = [num.ljust(2) for num in numbers]
	def parse(text: str):
		try:
			number = numbers.index(text[:2])
			suit = suits.index(text[-1])
			return number + suit * len(numbers)
		except ValueError:
			return 53 if text == 'free space' else -1

	values = Path('field.csv').read_text().replace('\n', ',').split(',')
	return [parse(value) for value in values]

__field_data = __get_values()


__func = components.declare_component(
	'touche_field',
	path=str((Path(__file__).parent / 'frontend').absolute())
)



def touche_field(pressed: list[int], deck: Deck):

	def callback():
		dict = st.session_state.get('touche-field')
		if not dict:
			return

	return __func(
		on_change=callback,
		key='touche-field',

		field_data=__field_data,
		pressed=pressed,
		deck=deck.value,
		can_press=True,
		is_dark=st_theme()['base'] == 'dark',
		dot_color=0,
	)
