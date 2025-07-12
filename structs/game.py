from __future__ import annotations

import random
from abc import ABC, abstractmethod
from time import time

from . import deck, figure, user
from .cell import UsedCell, SelectCell, FinalFigure
from .deck import Deck
from .game_type import GameType


class Player:
	def __init__(self, info: user.Info, deck_source: deck.Source, figure_types: list[figure.Type]):
		self.info = info
		self.opponent: Player = None
		self.deck = Deck(deck_source)
		self.figures = figure.SemiFigure(*figure_types)
		self.final_figure_count = 0


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


class Request(Base):
	def __init__(self, user: user.Info, type: GameType):
		self.user = user
		self.type = type
		super().__init__()
		self.begin_time = self.lives_until - self.life_time
	@property
	def ids(self): return [self.user.id]
	@property
	def life_time(self): return 20


class Game(Base):
	def __init__(self, request: Request, player2: user.Info):
		deck_source = deck.Source()
		self.players = [Player(info, deck_source, request.type.value.figure_types) for info in [request.user, player2]]
		self.players[0].opponent, self.players[1].opponent = self.players[1], self.players[0]

		self.lead: Player = random.choice(self.players)
		self.cell_by_index: dict[int, UsedCell] = {}
		self.cell_history: list[SelectCell | FinalFigure] = []
		self.updated_cell: int = 0
		self.counter = 0
		super().__init__()

	def get_player(self, user_id: int):
		if user_id == self.players[0].info.id: return self.players[0]
		if user_id == self.players[1].info.id: return self.players[1]
		raise ValueError(f'User with id {user_id} does not belong to this game')

	def cancel(self):
		super().cancel()
		self.counter += 1

	@property
	def winner(self):
		for player in self.players:
			if player.final_figure_count == 4:
				return player
		return None

	@property
	def ids(self): return [player.info.id for player in self.players]
	@property
	def life_time(self): return 60 * 60 * 24
