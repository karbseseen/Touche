from __future__ import annotations

import random
from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
from time import time

from .deck import Deck
from .user import UserInfo


class Base(ABC):
	by_user: dict[int, Base] = {}
	_last_cleared = 0

	@classmethod
	def clear_old(cls):
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
		self.lives_until = 0
		self.refresh()
		for id in self.ids:
			self.by_user[id] = self

	def refresh(self):
		self.lives_until = int(time()) + self.life_time

	def cancel(self):
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
		self.deck1 = Deck()
		self.deck2 = Deck()
		self.pressed: list[int] = []
		if random.choice([True, False]):
			self.player1, self.player2 = self.player2, self.player1
		super().__init__()
	@property
	def ids(self): return [self.player1.id, self.player2.id]
	@property
	def life_time(self): return 60 * 60 * 24
