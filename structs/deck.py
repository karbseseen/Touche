from __future__ import annotations
import random


class Source:
	def __init__(self, joker_num = 6):
		self.joker_num = joker_num
		self.remaining_cards: list[int] = []

	def random_card(self):
		if len(self.remaining_cards) == 0:
			self.remaining_cards = [i for i in range(Deck.total_cards - 1)] * 2 + [Deck.Joker] * self.joker_num
		index = random.randrange(len(self.remaining_cards))
		result = self.remaining_cards[index]
		last = self.remaining_cards.pop()
		if index != len(self.remaining_cards):
			self.remaining_cards[index] = last
		return result


class Deck:
	total_cards = 53 #including Joker
	Joker = 52
	FreeSpace = 53

	def __init__(self, source: Source):
		self.source = source
		self.data = [source.random_card() for _ in range(5)]

	def __getitem__(self, index: int):
		return self.data[index] & 0xff

	def __setitem__(self, index: int, value: int):
		counter = (self.data[index] & 0xff00) + 0x100
		self.data[index] = value | counter

	def play_card(self, index: int):
		self[index] = self.source.random_card()
