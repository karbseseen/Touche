from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class FigureBase(ABC):
	width: int
	height: int

	@abstractmethod
	def contains(self, x: int, y: int) -> bool: pass
