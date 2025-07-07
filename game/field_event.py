import field
from structs.cell import SelectCell, FinalCell, UsedCell
from structs.deck import Deck
from structs.game import Game


def callback(user_id: int, game: Game, event: field.Event):
	if game.ended: return
	game.counter += 1
	used_cell = game.cell_by_index.get(event.cell_index)

	if event.card_index == 5:
		if used_cell and used_cell.user_id == user_id and not used_cell.final:
			game.cell_by_index[event.cell_index].final = True
			game.cell_history.append(FinalCell(event.cell_index))

			game.final_count[game.lead_index] += 1
			if game.final_count[game.lead_index] == game.type.value.final_count:
				game.winner_index = 0 if game.players[0].id == user_id else 1

	elif user_id == game.lead.id:
		deck = game.user_deck(user_id)

		if event.card_index == -1:
			for index in range(5):
				if deck[index] == event.cell_value:
					event.card_index = index
		if event.card_index not in range(5): return
		card_value = deck[event.card_index]

		def basic_valid(): return event.cell_value == card_value and not used_cell
		def free_valid(): return event.cell_value == Deck.FreeSpace and not used_cell
		def joker_valid(): return card_value == Deck.Joker and	\
			(not used_cell or (used_cell.user_id != user_id and not used_cell.final))

		if basic_valid() or free_valid() or joker_valid():
			prev_used = game.cell_by_index.get(event.cell_index)
			prev_id = prev_used.user_id if prev_used else None

			game.cell_by_index[event.cell_index] = UsedCell(user_id, False)
			game.cell_history.append(SelectCell(event.cell_index, user_id, prev_id, event.card_index, card_value))
			game.lead_index = 1 - game.lead_index
			deck.play_card(event.card_index)


def undo(game: Game):
	game.counter += 1
	last_move = game.cell_history.pop()
	if isinstance(last_move, SelectCell):
		if last_move.prev_id:
			game.cell_by_index[last_move.index].user_id = last_move.prev_id
		else:
			game.cell_by_index.pop(last_move.index)
		game.user_deck(last_move.user_id)[last_move.card_index] = last_move.card_value
	elif isinstance(last_move, FinalCell):
		game.cell_by_index[last_move.index].final = False
