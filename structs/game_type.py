from dataclasses import dataclass
from enum import Enum

from . import figure


@dataclass
class GameTypeValue:
	symbol: str
	text: str
	figure_types: list[figure.Type]

class GameType(Enum):
	Square = GameTypeValue('■', 'Квадраты', figure.squares)
	Line = GameTypeValue('/', 'Линии', figure.lines)
	Cross = GameTypeValue('⨉', 'Кресты', figure.crosses)
	T = GameTypeValue('T', 'Букву Т', figure.ts)

	@classmethod
	def from_str(cls, value: str):
		for type in cls:
			if type.value.text == value:
				return type
		return None
