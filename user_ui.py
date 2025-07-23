import streamlit as st

from structs.lang import Langs
from structs.user import User


def user_ui(user: User):

	def update_name(name: str | None = None):
		if not name:
			name = st.session_state['user_name']
		if name:
			user.name = name

	def update_color():
		color = st.session_state['user_color']
		if color:
			user.color = color

	def update_lang():
		lang = st.session_state['user_lang']
		if lang:
			user.lang = lang

	def reborn():
		user.name = ''
		user.color = User.default_color


	def lang_select():
		st.selectbox(
			key='user_lang',
			label='-',
			label_visibility='hidden',
			options=Langs.all.values(),
			index=user.lang.index,
			format_func=lambda strings: strings['_name'],
			on_change=update_lang,
		)


	if not user.name:
		col,_ = st.columns([1,2])
		with col: lang_select()
		st.header(user.lang['who_are_you'])
		user_name = st.text_input(user.lang['whats_your_name'], max_chars=32, placeholder=user.lang['name_placeholder'])
		if user_name:
			st.button('Сохранить', on_click=lambda: update_name(user_name))
	else:
		col1, col2 = st.sidebar.columns([3,1])
		col1.text_input(
			user.lang['whats_your_name'],
			user.name,
			max_chars=32,
			placeholder=user.lang['name_placeholder'],
			key='user_name',
			on_change=update_name,
		)
		col2.color_picker(
			'color',
			user.color,
			label_visibility='hidden',
			key='user_color',
			on_change=update_color,
		)
		st.sidebar.markdown(user.lang['confirm_name'] + user.info.markdown_str(2), unsafe_allow_html=True)
		st.sidebar.markdown('##')
		st.sidebar.button(user.lang['reborn'], on_click=reborn)
		with st.sidebar: lang_select()

	return bool(user.name)
