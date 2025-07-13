from dataclasses import dataclass
from enum import Enum

from . import figure


@dataclass
class GameTypeValue:
	symbol: str
	text: str
	figure_types: list[figure.Type]
	figure_count: int

class GameType(Enum):
	Square = GameTypeValue('■', 'Квадраты', figure.squares, 4)
	Line = GameTypeValue('/', 'Линии', figure.lines, 3)
	Cross = GameTypeValue('⨉', 'Кресты', figure.crosses, 3)
	T = GameTypeValue('T', 'Букву Т', figure.ts, 3)

	@classmethod
	def from_str(cls, value: str):
		for type in cls:
			if type.value.text == value:
				return type
		return None
