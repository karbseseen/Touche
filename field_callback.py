import field
from field import UsedCell
from structs.cell import SelectCell
from structs.deck import Deck, DeckList
from structs.game import Game


def field_callback(user_id: int, game: Game, event: field.Event):
	if user_id != game.lead.id: return

	deck = game.user_deck(user_id)

	if not isinstance(event.card_index, int):
		try:
			event.card_index = deck.index(event.cell_value)
			event.card_value = event.cell_value
		except ValueError:
			pass

	event_valid = (
		event.cell_value == event.card_value	or
		event.card_value == Deck.Joker			or
		event.cell_value == Deck.FreeSpace
	)
	used_cell = game.cell_by_index.get(event.cell_index)
	used_final = isinstance(used_cell, UsedCell) and used_cell.final

	if event_valid and not used_final:
		game.cell_by_index[event.cell_index] = UsedCell(user_id, False)
		game.cell_history.append(SelectCell(event.cell_index, user_id))
		game.invalid_cell = -1
		game.counter += 1
		deck[event.card_index] = Deck.random_card(game.counter)
		return
	else:
		game.invalid_cell = event.cell_index
