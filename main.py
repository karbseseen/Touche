import streamlit as st


#if not st.user.is_logged_in:
#	pages = [st.Page('auth.py', title='Кто ты?', icon='🙎🏻‍♂️')]
#else:
pages = [
	st.Page('game.py', title='Touche', icon='🎲'),
	st.Page('settings.py', title='Настройки', icon='⚙️')
]
st.sidebar.button('Выйти (в окно)', on_click=st.logout)

st.navigation(pages).run()
