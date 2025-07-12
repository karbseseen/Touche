from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Callable

from util.rotate import rotate90


class Type(ABC):
	def __init__(self, width: int, height: int, square: int | None = None):
		self.width = width
		self.height = height
		if isinstance(square, int):
			self.square = square
		else:
			self.square = 0
			for x in range(self.width):
				for y in range(self.height):
					if self.contains(x, y):
						self.square += 1

	@abstractmethod
	def contains(self, x: int, y: int) -> bool: pass

	def _bounded_ids(self, x0: int, y0: int, x1: int, y1: int):
		for x in range(x0, x1):
			for y in range(y0, y1):
				if self.contains(x, y):
					yield x, y

	def cell_figure_ids(self, cell_index: int):
		cell_y, cell_x = divmod(cell_index, 12)
		x0 = max(0, cell_x + self.width - 12)
		y0 = max(0, cell_y + self.height - 12)
		x1 = min(self.width, cell_x + 1)
		y1 = min(self.height, cell_y + 1)
		for x, y in self._bounded_ids(x0, y0, x1, y1):
			yield (cell_x - x) + (cell_y - y) * 12

	def check_figure_full(self, figure_id: int, cell_available: Callable[[int], bool]):
		for x, y in self._bounded_ids(0, 0, self.width, self.height):
			if not cell_available(figure_id + x + y * 12):
				return False
		return True

class RectType(Type):
	def __init__(self, width: int, height: int): super().__init__(width, height, width * height)
	def contains(self, x: int, y: int): return True

class CustomType(Type):
	def __init__(self, content: list[Any], width: int):
		self.content = content
		super().__init__(width, len(content) // width)
	def contains(self, x: int, y: int):
		return bool(self.content[x + y * self.width])
	def rotate(self):
		result = [self,self,self,self]
		for index in range(1, 4):
			prev = result[index - 1]
			content, width = rotate90(prev.content, prev.width)
			result[index] = CustomType(content, width)
		return result


@dataclass
class SuccessResult: cell_indices: list[int]

@dataclass
class _SemiFigure:
	id: int
	remaining: int
	def dec(self): return _SemiFigure(self.id, self.remaining - 1)
@dataclass
class _HistoryItem:
	cell_index: int
	figure_remaining: list[_SemiFigure]

class SemiFigure:
	def __init__(self, *types: Type):
		self.types = list(types)
		self._history: list[_HistoryItem] = []
	@property
	def cell_num(self): return len(self._history)
	@property
	def cell_indices(self): return [item.cell_index for item in self._history]
	@property
	def is_invalid(self): return len(self._history) and not len(self._history[-1].figure_remaining)

	def _possible_figures(self, cell_index: int):
		for type_index, type in enumerate(self.types):
			for figure_id in type.cell_figure_ids(cell_index):
				yield type, figure_id | type_index << 8

	def _figure_type(self, figure_id: int): return self.types[figure_id >> 8]

	def add_cell(self, cell_index: int):
		possible_figures = self._possible_figures(cell_index)
		if len(self._history):
			possible_set = set(figure_id for _, figure_id in possible_figures)
			figure_remaining = [f.dec() for f in self._history[-1].figure_remaining if f.id in possible_set]
		else:
			figure_remaining = [_SemiFigure(figure_id, type.square - 1) for type, figure_id in possible_figures]
			figure_remaining.sort(key=lambda figure: figure.remaining)
		self._history.append(_HistoryItem(cell_index, figure_remaining))

		if len(figure_remaining) != 0 and figure_remaining[0].remaining == 0:
			cell_indices = self.cell_indices
			self._history = []
			return SuccessResult(cell_indices)
		else:
			return None

	def pop_cell(self):
		return self._history.pop().cell_index

	def check_free_space(self, cell_index: int, is_cell_available: Callable[[int], bool]):
		for figure_type, figure_id in self._possible_figures(cell_index):
			if figure_type.check_figure_full(
				figure_id,
				lambda _cell_index: _cell_index == cell_index or is_cell_available(_cell_index),
			): return True
		return False
		

class Square(RectType):
	def __init__(self): super().__init__(2, 2)

class HorizontalLine(RectType):
	def __init__(self): super().__init__(5, 1)
class VerticalLine(RectType):
	def __init__(self): super().__init__(1, 5)
class DownDiagonalLine(Type):
	def __init__(self): super().__init__(5, 5)
	def contains(self, x: int, y: int): return x == y
	def _bounded_ids(self, x0: int, y0: int, x1: int, y1: int):
		for xy in range(max(x0, y0), min(x1, y1)):
			yield xy, xy
class UpDiagonalLine(Type):
	def __init__(self): super().__init__(5, 5)
	def contains(self, x: int, y: int): return x + y == 4
	def _bounded_ids(self, x0: int, y0: int, x1: int, y1: int):
		for x in range(max(x0, 5 - y1), min(x1, 5 - y0)):
			yield x, 4 - x

class StraightCross(Type):
	def __init__(self): super().__init__(3, 3)
	def contains(self, x: int, y: int): return (x + y) & 1 == 1 or x == 1 and y == 1
class DiagonalCross(Type):
	def __init__(self): super().__init__(3, 3)
	def contains(self, x: int, y: int): return (x + y) & 1 == 0

class StraightT(CustomType):
	_content = [
		1,1,1,
		0,1,0,
		0,1,0,
	]
	def __init__(self): super().__init__(self._content, 3)
class DiagonalT(CustomType):
	_content = [
		0,0,1,0,
		0,1,0,0,
		1,0,1,0,
		0,0,0,1,
	]
	def __init__(self): super().__init__(self._content, 4)


squares = [Square()]
lines = [HorizontalLine(), VerticalLine(), DownDiagonalLine(), UpDiagonalLine()]
crosses = [StraightCross(), DiagonalCross()]
ts = StraightT().rotate() + DiagonalT().rotate()
