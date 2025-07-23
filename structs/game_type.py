import enum
from dataclasses import dataclass
from enum import Enum

from . import figure


@dataclass
class GameTypeValue:
	symbol: str
	lang_key: str
	figure_types: list[figure.Type]
	figure_count: int

class GameType(Enum):
	Square = GameTypeValue('■', 'square', figure.squares, 4)
	Line = GameTypeValue('/', 'line', figure.lines, 3)
	Cross = GameTypeValue('⨉', 'cross', figure.crosses, 3)
	T = GameTypeValue('T', 'letter_t', figure.ts, 3)
	all = enum.nonmember(list[GameTypeValue]())
GameType.all = [type.value for type in GameType]
