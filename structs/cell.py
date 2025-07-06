from dataclasses import dataclass


@dataclass
class UsedCell:
	user_id: int
	final: bool

@dataclass
class SelectCell:
	index: int
	user_id: int

@dataclass
class FinalCell:
	index: int
