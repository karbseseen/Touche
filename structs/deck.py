import random


DeckList = list[int]

class Deck:
	total_cards = 53 #including Joker
	Joker = 52
	FreeSpace = 53

	@classmethod
	def random_card(cls, counter: int):
		return min(cls.total_cards - 1, random.randrange(cls.total_cards + 2)) | (counter << 8)

	@classmethod
	def create(cls) -> DeckList:
		return [cls.random_card(0) for _ in range(5)]
