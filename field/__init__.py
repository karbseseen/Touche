from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any, Callable

import streamlit as st
import streamlit.components.v1 as components
from streamlit_theme import st_theme

from structs.game import Game


@dataclass
class Event:
	cell_index: int
	cell_value: int
	card_index: int


_component = components.declare_component(
	'touche_field',
	path=str((Path(__file__).parent / 'frontend').absolute())
)


def _get_values():
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

	values = Path('field/field.csv').read_text().replace('\n', ',').split(',')
	return [parse(value) for value in values]


class Field:
	_values = _get_values()
	@classmethod
	@property
	def values(cls): return cls._values

	@classmethod
	def component(cls,
		user_id: int,
		game: Game,
		callback: Callable[[Event], None],
	):
		def on_change():
			map: dict[str, Any] = st.session_state.get('touche-field')
			if not isinstance(map, dict): return
			cell_index: int = map.get('cell_index')
			card_index: int = map.get('card_index')
			if not isinstance(cell_index, int) or not isinstance(card_index, int): return
			callback(Event(cell_index, cls._values[cell_index], card_index))

		player = game.get_player(user_id)
		theme = st_theme()
		return _component(
			key='touche-field',
			on_change=on_change,

			field_data=cls._values,
			used_cells={ index: cell.to_dict() for index, cell in game.cell_by_index.items() },
			user_color={ player.info.id: player.info.color for player in game.players },
			history_size=len(game.cell_history),
			cards=player.deck.data,
			clickable=user_id == game.lead.info.id and not player.figures.is_invalid and game.winner is None,
			is_dark=theme['base'] == 'dark' if theme else False,
			counter=game.counter,
		)
