from dataclasses import dataclass

import lxml.etree as xml
from lxml.etree import Element

from util.FigureBase import FigureBase


_line_width = 0.08
_line_color = "#555"
_dot_radius = 0.33
_period = 2.5


@dataclass
class _Coord:
	x: int
	y: int

class _Frame:
	def __init__(self):
		self.coords: list[_Coord] = []
		self.min_x = 0
		self.min_y = 0
		self.max_x = 0
		self.max_y = 0
	def append(self, coord: _Coord):
		if len(self.coords) > 0:
			self.min_x, self.max_x = min(self.min_x, coord.x), max(self.max_x, coord.x)
			self.min_y, self.max_y = min(self.min_y, coord.y), max(self.max_y, coord.y)
		else:
			self.min_x = self.max_x = coord.x
			self.min_y = self.max_y = coord.y
		self.coords.append(coord)
	def center(self, max_dx: int, max_dy: int):
		x_diff = (max_dx - self.max_x - self.min_x) // 2
		y_diff = (max_dy - self.max_y - self.min_y) // 2
		for coord in self.coords:
			coord.x += x_diff
			coord.y += y_diff

class _Frames:
	def __init__(self):
		self.value: list[_Frame] = []
		self.max_dx = 0
		self.max_dy = 0
	def append(self, frame: _Frame):
		self.max_dx = max(self.max_dx, frame.max_x - frame.min_x)
		self.max_dy = max(self.max_dy, frame.max_y - frame.min_y)
		self.value.append(frame)
	def center(self):
		for frame in self.value:
			frame.center(self.max_dx, self.max_dy)

def _get_frames(input: FigureBase, count: int, use_diagonal: bool):
	frames = _Frames()

	if count < 1: return frames
	first = _Frame()
	for y in range(input.height):
		for x in range(input.width):
			if input.contains(x, y):
				first.append(_Coord(x, y))
	frames.append(first)

	if use_diagonal:
		if count < 2: return frames
		rotated45 = _Frame()
		for orig in first.coords:
			rotated45.append(_Coord(orig.x - orig.y, orig.x + orig.y))
		frames.append(rotated45)

	step = len(frames.value)
	for _ in range(step, count):
		frame = _Frame()
		for orig in frames.value[-step].coords:
			frame.append(_Coord(-orig.y, orig.x))
		frames.append(frame)

	frames.center()
	return frames


def _gen_line(root: xml.Element, x1: int|float, y1: int|float, x2: int|float, y2: int|float):
	line = xml.SubElement(root, 'line', x1=str(x1), y1=str(y1), x2=str(x2), y2=str(y2), stroke=_line_color)
	line.attrib['stroke-width'] = str(_line_width)
	line.attrib['stroke-linecap'] = 'round'

def _gen_dot(root: xml.Element, frames: _Frames, dot_index: int):
	x_values = [ str(frame.coords[dot_index].x + 0.5) for frame in frames.value ]
	y_values = [ str(frame.coords[dot_index].y + 0.5) for frame in frames.value ]

	key_splines = ';'.join(['.75 0 0.25 1'] * len(frames.value))

	circle = xml.SubElement(root, 'circle', r=str(_dot_radius))
	xml.SubElement(
		circle,
		'animate',
		attributeName='cx',
		values=';'.join(x_values) + ';' + x_values[0],
		dur=f'{_period * len(frames.value)}s',
		repeatCount='indefinite',
		calcMode='spline',
		keySplines=key_splines,
	)
	xml.SubElement(
		circle,
		'animate',
		attributeName='cy',
		values=';'.join(y_values) + ';' + y_values[0],
		dur=f'{_period * len(frames.value)}s',
		repeatCount='indefinite',
		calcMode='spline',
		keySplines=key_splines,
	)

def generate_figure_svg(input: FigureBase, frame_num: int|None = None, use_diagonal: bool = True) -> str:
	if frame_num is None:
		frame_num = 8 if use_diagonal else 4
	frames	= _get_frames(input, frame_num, use_diagonal)
	width	= frames.max_dx + 1
	height	= frames.max_dy + 1

	root = xml.Element("svg", viewBox=f"0 0 {width} {height}", xmlns="http://www.w3.org/2000/svg")

	for x in range(1, width):
		_gen_line(root, x, _line_width/2, x, height-_line_width/2)
	for y in range(1, height):
		_gen_line(root, _line_width/2, y, width-_line_width/2, y)

	for dot_index in range(len(frames.value[0].coords)):
		_gen_dot(root, frames, dot_index)

	return xml.tostring(root, encoding='unicode', pretty_print=True)

