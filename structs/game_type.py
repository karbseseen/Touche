import enum
from dataclasses import dataclass
from enum import Enum

import lxml.etree as xml

from util.figure_svg import generate_figure_svg
from . import figure


@dataclass
class GameTypeValue:
	symbol: str
	lang_key: str
	figure_types: list[figure.Type]
	figure_count: int
	_has_diagonal: bool = True
	def __post_init__(self):
		self.svg = generate_figure_svg(self.figure_types[0], use_diagonal=self._has_diagonal)

class GameType(Enum):
	Square	= GameTypeValue('■', 'square',	figure.squares,	4, False)
	Line	= GameTypeValue('/', 'line',	figure.lines,	3)
	Cross	= GameTypeValue('⨉', 'cross',	figure.crosses,	3)
	T		= GameTypeValue('T', 'letter_t',figure.ts,		3)
	all = enum.nonmember(list[GameTypeValue]())
GameType.all = [type.value for type in GameType]
