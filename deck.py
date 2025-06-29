from xorshift import XorShift


class Deck:
	total_cards = 53 #including Joker

	@staticmethod
	def __random_card(random: XorShift):
		return min(Deck.total_cards - 1, random.next() % (Deck.total_cards + 2))

	def __init__(self, random: XorShift):
		self.value = [Deck.__random_card(random) for _ in range(5)]
