import streamlit as st


class Spinner:
	def __init__(self, text = 'In progress...', show_time=False):
		self._spinner = iter(self._start(text, show_time))
		next(self._spinner)

	def _start(self, text, show_time):
		with st.spinner(text, show_time=show_time):
			yield

	def end(self):
		next(self._spinner, None)
