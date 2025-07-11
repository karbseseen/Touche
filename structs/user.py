from __future__ import annotations

from datetime import datetime, timedelta
from time import time
from weakref import WeakValueDictionary
from streamlit_cookies_controller import CookieController


class Info:
	test = -1
	by_id: WeakValueDictionary[int, Info] = WeakValueDictionary()
	def __init__(self, id: int, name: str, color: str):
		self.id = id
		self.name = name
		self.color = color if color else User.default_color
		self.by_id[id] = self
	def markdown_str(self, size: float = 1.0):
		return f'<span style="color:{self.color}; font-size:{size}rem"> {self.name}</span>'


class User:
	_last_id = int(time() * 1000)
	default_color = '#023434'

	@classmethod
	def safe_create(cls):
		cookies = CookieController()
		return cls(cookies) if cookies.getAll() else None

	def __init__(self, cookies: CookieController):
		self._cookies = cookies

		self._id = self._cookies.get('user_id')
		if not isinstance(self._id, int):
			User._last_id += 1
			self._id = User._last_id
			self._cookies.set('user_id', self._id, expires=self._expires)

		self._info = Info.by_id.get(self._id)
		if not self._info:
			self._info = Info(self._id, self._cookies.get('user_name'), self._cookies.get('user_color'))

	@property
	def _expires(self): return datetime.now() + timedelta(365)

	@property
	def id(self): return self._id

	@property
	def info(self): return self._info

	@property
	def name(self): return self._info.name
	@name.setter
	def name(self, name: str | None):
		self._info.name = name
		self._cookies.set('user_name', name, expires=self._expires)

	@property
	def color(self): return self._info.color
	@color.setter
	def color(self, color: str):
		self._info.color = color
		self._cookies.set('user_color', color, expires=self._expires)
