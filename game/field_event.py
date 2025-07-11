import field
from structs import figure
from structs.cell import SelectCell, UsedCell, UsedType, FinalFigure
from structs.deck import Deck
from structs.game import Game


def callback(user_id: int, game: Game, event: field.Event):
	if game.winner: return
	game.counter += 1
	used_cell = game.cell_by_index.get(event.cell_index)

	player = game.get_player(user_id)

	if event.card_index == 5:
		if used_cell and used_cell.user_id == user_id and used_cell.type == UsedType.Normal:
			game.cell_by_index[event.cell_index].type = UsedType.SemiFinal
			figure_result = player.figures.add_cell(event.cell_index)
			if isinstance(figure_result, figure.SuccessResult):
				for cell_index in figure_result.cell_indices:
					game.cell_by_index[cell_index].type = UsedType.Final
				game.cell_history.append(FinalFigure(figure_result.cell_indices, user_id))
				player.final_figure_count += 1

	elif user_id == game.lead.info.id:
		if event.card_index == -1:
			for index in range(5):
				if player.deck[index] == event.cell_value:
					event.card_index = index
		if event.card_index not in range(5): return
		card_value = player.deck[event.card_index]

		def basic_valid(): return event.cell_value == card_value and not used_cell
		def free_valid(): return event.cell_value == Deck.FreeSpace and not used_cell
		def joker_valid(): return card_value == Deck.Joker and	\
			(not used_cell or (used_cell.user_id != user_id and used_cell.type == UsedType.Normal))

		if basic_valid() or free_valid() or joker_valid():
			prev_used = game.cell_by_index.get(event.cell_index)
			prev_id = prev_used.user_id if prev_used else None

			game.cell_by_index[event.cell_index] = UsedCell(user_id, UsedType.Normal)
			game.cell_history.append(SelectCell(event.cell_index, user_id, prev_id, event.card_index, card_value))
			game.lead_index = 1 - game.lead_index
			player.deck.play_card(event.card_index)


_SemiFigure = 0
def _move_to_undo_index(user_id: int, game: Game):
	if not game.cell_history: return None
	if not game.get_player(user_id).figures.is_empty: return _SemiFigure
	if game.cell_history[-1].user_id == user_id: return -1
	for index, move in enumerate(reversed(game.cell_history)):
		if move.user_id == user_id:
			return -1 - index if isinstance(move, FinalFigure) else None
	return None

def can_undo(user_id: int, game: Game):
	return _move_to_undo_index(user_id, game) is not None

def undo(user_id: int, game: Game):
	game.counter += 1
	player = game.get_player(user_id)
	move_index = _move_to_undo_index(user_id, game)

	if move_index == _SemiFigure:
		cell_index = player.figures.pop_cell()
		game.cell_by_index[cell_index].type = UsedType.Normal
		return

	move = game.cell_history.pop(move_index)
	if isinstance(move, SelectCell):
		if move.prev_id:
			game.cell_by_index[move.index].user_id = move.prev_id
		else:
			game.cell_by_index.pop(move.index)
		player.deck[move.card_index] = move.card_value
	elif isinstance(move, FinalFigure):
		for cell_index in move.indices[:-1]:
			game.cell_by_index[cell_index].type = UsedType.SemiFinal
			player.figures.add_cell(cell_index)
		game.cell_by_index[move.indices[-1]].type = UsedType.Normal
		player.final_figure_count -= 1
