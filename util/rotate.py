from typing import TypeVar


T = TypeVar('T')

class Rotate90View:
	def __init__(self, array: list[T], width: int):
		self.src = array
		self.height = width
		self.width = len(array) // width
	def __getitem__(self, dst_xy: tuple[int, int]):
		dst_x, dst_y = dst_xy
		src_y = dst_x
		src_x = self.height - dst_y - 1
		return self.src[src_x + src_y * self.height]

def rotate90(array: list[T], width: int) -> tuple[list[T], int]:
	view = Rotate90View(array, width)
	rotated = [None] * (view.width * view.height)
	for x in range(view.width):
		for y in range(view.height):
			rotated[x + y * view.width] = view[x, y]
	return rotated, view.width
