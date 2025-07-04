import streamlit as st
from structs.user import User


def user_ui(user: User):

	def _update_name(name: str | None = None):
		if not name:
			name = st.session_state['user_name']
		if name:
			user.name = name

	def _update_color():
		color = st.session_state['user_color']
		if color:
			user.color = color


	if not user.name:
		st.header('Ты кто такой?')
		user_name = st.text_input('Как вас зовут?', max_chars=32, placeholder='Гриб Картошкин')
		if user_name:
			st.button('Сохранить', on_click=lambda: _update_name(user_name))
	else:
		col1, col2 = st.sidebar.columns([3,1])
		col1.text_input(
			'Как вас зовут?',
			user.name,
			max_chars=32,
			placeholder='Гриб Картошкин',
			key='user_name',
			on_change=_update_name,
		)
		col2.color_picker(
			'color',
			user.color,
			label_visibility='hidden',
			key='user_color',
			on_change=_update_color,
		)

		st.sidebar.markdown('Ваше имя будет выглядеть так: ' + user.info.markdown_str(2), unsafe_allow_html=True)

	return bool(user.name)
