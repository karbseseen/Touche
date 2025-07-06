from __future__ import annotations

import random
from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
from time import time

from .cell import UsedCell, SelectCell, FinalCell
from .deck import Deck, DeckList
from .user import UserInfo


class Base(ABC):
	by_user: dict[int, Base] = {}
	_dict_version = 0
	_last_cleared = 0

	@classmethod
	@property
	def dict_version(cls): return cls._dict_version

	@classmethod
	def _clear_old(cls):
		now = time()
		if cls._last_cleared + 60 < now:
			cls.by_user = { id: base for id, base in cls.by_user.items() if base.lives_until > now }

	@property
	@abstractmethod
	def life_time(self) -> int: pass

	@property
	@abstractmethod
	def ids(self) -> list[int]: pass

	def __init__(self):
		Base._dict_version += 1
		Base._clear_old()
		self.lives_until = 0
		self.refresh()
		for id in self.ids:
			self.by_user[id] = self

	def refresh(self):
		self.lives_until = int(time()) + self.life_time

	def cancel(self):
		Base._dict_version += 1
		for id in self.ids:
			self.by_user.pop(id, None)


@dataclass
class TypeValue:
	symbol: str
	text: str

class Type(Enum):
	Square = TypeValue('■', 'Квадраты')
	Line = TypeValue('/', 'Линии')
	Cross = TypeValue('⨉', 'Кресты')
	T = TypeValue('T', 'Букву Т')

	_ignore_ = ['strings']
	strings: list[str] = []

	@classmethod
	def from_str(cls, value: str):
		for type in cls:
			if type.value.text == value:
				return type
		return None
Type.strings = [type.value.text for type in Type]


class Request(Base):
	def __init__(self, user: UserInfo, type: Type):
		self.user = user
		self.type = type
		super().__init__()
		self.begin_time = self.lives_until - self.life_time
	@property
	def ids(self): return [self.user.id]
	@property
	def life_time(self): return 20


class Game(Base):
	def __init__(self, request: Request, player2: UserInfo):
		self.type = request.type
		self.player1 = request.user
		self.player2 = player2
		self.deck1 = Deck.create()
		self.deck2 = Deck.create()
		self.cell_by_index: dict[int, UsedCell] = {}
		self.cell_history: list[SelectCell | FinalCell] = []
		self.invalid_cell = -1
		self.counter = 0
		if random.choice([True, False]):
			self.player1, self.player2 = self.player2, self.player1
		super().__init__()

	def user_deck(self, user_id: int):
		if user_id == self.player1.id: return self.deck1
		if user_id == self.player2.id: return self.deck2
		raise ValueError(f'User with id {user_id} does not belong to this game')

	@property
	def lead(self): return self.player2 if self.counter & 1 else self.player1
	@property
	def ids(self): return [self.player1.id, self.player2.id]
	@property
	def life_time(self): return 60 * 60 * 24
