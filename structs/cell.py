from dataclasses import dataclass
from enum import Enum, auto


class UsedType(Enum):
	Normal = 'n'
	SemiFinal = 'sf'
	Final = 'f'

@dataclass
class UsedCell:
	user_id: int
	type: UsedType
	def to_dict(self):
		return { 'user_id': self.user_id, 'type': self.type.value }

@dataclass
class SelectCell:
	index: int
	user_id: int
	prev_id: int | None
	card_index: int
	card_value: int

@dataclass
class FinalFigure:
	indices: list[int]
	user_id: int
