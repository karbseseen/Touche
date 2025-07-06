import random


class Deck:
	total_cards = 53 #including Joker
	Joker = 52
	FreeSpace = 53

	@classmethod
	def _random_card(cls):
		return min(cls.total_cards - 1, random.randrange(cls.total_cards + 2))

	def __init__(self):
		self.data = [self._random_card() for _ in range(5)]

	def __getitem__(self, index: int):
		return self.data[index] & 0xff

	def __setitem__(self, index: int, value: int):
		counter = (self.data[index] & 0xff00) + 0x100
		self.data[index] = value | counter

	def play_card(self, index: int):
		self[index] = self._random_card()
