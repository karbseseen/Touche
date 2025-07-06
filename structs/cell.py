from dataclasses import dataclass


@dataclass
class UsedCell:
	user_id: int
	final: bool

@dataclass
class SelectCell:
	index: int
	user_id: int
	prev_id: int | None
	card_index: int
	card_value: int

@dataclass
class FinalCell:
	index: int
