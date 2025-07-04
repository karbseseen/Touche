from dataclasses import dataclass
import random


@dataclass
class _HistoryCard:
	value: int
	index: int


class Deck:
	total_cards = 53 #including Joker

	@classmethod
	def _random_card(cls):
		return min(cls.total_cards - 1, random.randrange(cls.total_cards + 2))

	def __init__(self):
		self._value = [self._random_card() for _ in range(5)]
		self._history: list[_HistoryCard] = []

	@property
	def value(self): return self._value

	@property
	def has_history(self): return len(self._history) > 0

	def play_card(self, index: int):
		self._history.append(_HistoryCard(self._value[index], index))
		self._value[index] = self._random_card()

	def unplay_card(self):
		last = self._history.pop()
		self._value[last.index] = last.value
