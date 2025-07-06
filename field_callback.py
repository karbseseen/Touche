import field
from structs.cell import SelectCell, FinalCell, UsedCell
from structs.deck import Deck
from structs.game import Game


def field_callback(user_id: int, game: Game, event: field.Event):
	game.counter += 1
	used_cell = game.cell_by_index.get(event.cell_index)

	if event.card_index == 5:
		if used_cell and used_cell.user_id == user_id and not used_cell.final:
			game.cell_by_index[event.cell_index].final = True
			game.cell_history.append(FinalCell(event.cell_index))
	elif user_id == game.lead.id:
		deck = game.user_deck(user_id)

		if event.card_index == -1:
			for index in range(5):
				if deck[index] == event.cell_value:
					event.card_index = index
		if event.card_index not in range(5): return
		card_value = deck[event.card_index]

		def joker_valid(): return card_value == Deck.Joker and	\
			(not used_cell or (used_cell.user_id != user_id and not used_cell.final))
		def free_valid(): return event.cell_value == Deck.FreeSpace and not used_cell
		def basic_valid(): return event.cell_value == card_value and not used_cell

		if joker_valid() or free_valid() or basic_valid():
			game.cell_by_index[event.cell_index] = UsedCell(user_id, False)
			game.cell_history.append(SelectCell(event.cell_index, user_id))
			deck.play_card(event.card_index)
