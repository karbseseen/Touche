from pathlib import Path
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

values = __get_values()


__func = components.declare_component(
	'touche_field',
	path=str((Path(__file__).parent / 'frontend').absolute())
)

def touche_field():
	return __func(
		values=values,
		deck=[0,1,30,52,52],
		is_dark=st_theme()['base'] == 'dark',
		default=666,
	)
