from dataclasses import dataclass
from typing import Callable

from structs.cell import UsedCell


@dataclass
class _Cell:
	x: int
	y: int

	@classmethod
	def from_index(cls, index: int):
		y, x = divmod(index, 12)
		return cls(x, y)

	@property
	def index(self): return self.x + self.y * 12

	def left	(self): return _Cell(self.x - 1, self.y) if self.x > 0 else None
	def top		(self): return _Cell(self.x, self.y - 1) if self.y > 0 else None
	def right	(self): return _Cell(self.x + 1, self.y) if self.x < 11 else None
	def bottom	(self): return _Cell(self.x, self.y + 1) if self.y < 11 else None

	def top_left	(self): return _Cell(self.x - 1, self.y - 1) if self.x > 0 and self.y > 0 else None
	def top_right	(self): return _Cell(self.x + 1, self.y - 1) if self.x < 11 and self.y > 0 else None
	def bottom_left	(self): return _Cell(self.x - 1, self.y + 1) if self.x > 0 and self.y < 11 else None
	def bottom_right(self): return _Cell(self.x + 1, self.y + 1) if self.x < 11 and self.y < 11 else None


class Possible:
	def __init__(self, cell_index: int, user_id: int, field: dict[int, UsedCell]):
		self.cell = _Cell.from_index(cell_index)
		self.user_id = user_id
		self.field = field

	def _is_valid(self, cell: _Cell | None):
		if not cell: return False
		used = self.field.get(cell.index)
		return bool(used) and used.user_id == self.user_id and not used.final


	def square(self):
		left_valid 			= self._is_valid(self.cell.left())
		top_left_valid		= self._is_valid(self.cell.top_left())
		top_valid 			= self._is_valid(self.cell.top())
		if left_valid and top_left_valid and top_valid:			yield self.cell.top_left().index

		top_right_valid		= self._is_valid(self.cell.top_right())
		right_valid			= self._is_valid(self.cell.right())
		if top_valid and top_right_valid and right_valid:		yield self.cell.top().index

		bottom_right_valid	= self._is_valid(self.cell.bottom_right())
		bottom_valid		= self._is_valid(self.cell.bottom())
		if right_valid and bottom_right_valid and bottom_valid:	yield self.cell.index

		bottom_left_valid	= self._is_valid(self.cell.bottom_left())
		if bottom_valid and bottom_left_valid and left_valid:	yield self.cell.left().index


	def line(self):
		Transform = Callable[[_Cell], _Cell]

		def ray(transform: Transform):
			cell = self.cell
			size = 0
			while True:
				next_cell = transform(cell)
				if not self._is_valid(next_cell): break
				cell = next_cell
				size += 1
			return cell, size

		def lines(backward: Transform, forward: Transform, type: int):
			type <<= 8
			cell ,back_size = ray(backward)
			_, front_size = ray(forward)
			size = back_size + 1 + front_size
			for _ in range(size - 4):
				yield cell.index | type
				cell = forward(cell)

		yield from lines(_Cell.left, _Cell.right, 0)
		yield from lines(_Cell.top, _Cell.bottom, 1)
		yield from lines(_Cell.top_left, _Cell.bottom_right, 2)
		yield from lines(_Cell.top_right, _Cell.bottom_left, 3)


	def cross(self):
		self_used = self.field.pop(self.cell.index, None)
		self.field[self.cell.index] = UsedCell(self.user_id, False)

		def straight_cross(cell: _Cell | None):
			if	self._is_valid(cell)			and \
				self._is_valid(cell.left())		and \
				self._is_valid(cell.top())		and \
				self._is_valid(cell.right())	and \
				self._is_valid(cell.bottom()):
					yield cell.index

		def diagonal_cross(cell: _Cell | None):
			if	self._is_valid(cell)				and \
				self._is_valid(cell.top_left())		and \
				self._is_valid(cell.top_right())	and \
				self._is_valid(cell.bottom_left())	and \
				self._is_valid(cell.bottom_right()):
					yield cell.index | 0x100

		yield from straight_cross(self.cell)
		yield from straight_cross(self.cell.left())
		yield from straight_cross(self.cell.top())
		yield from straight_cross(self.cell.right())
		yield from straight_cross(self.cell.bottom())
		yield from diagonal_cross(self.cell)
		yield from diagonal_cross(self.cell.top_left())
		yield from diagonal_cross(self.cell.top_right())
		yield from diagonal_cross(self.cell.bottom_left())
		yield from diagonal_cross(self.cell.bottom_right())

		if self_used: self.field[self.cell.index] = self_used
		else: self.field.pop(self.cell.index)


	def t(self):
		pass
