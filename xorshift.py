import time


class XorShift:
	def __init__(self, seed = int(time.time() * 1000)):
		self.__value = abs(seed) & 0xffff_ffff_ffff_ffff

	def next(self):
		self.__value ^= self.__value << 13
		self.__value ^= self.__value >> 17
		self.__value ^= self.__value << 5
		return self.__value
