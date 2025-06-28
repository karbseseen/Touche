from pathlib import Path
import streamlit as st
from streamlit_theme import st_theme
import field



# Main page content
st.markdown("# Main page 🎈")
st.sidebar.markdown("# Main page 🎈")

cell_values = Path('field.csv').read_text() 	\
	.replace('\n', ',')			\
	.replace(' ', '\n')			\
	.split(',')
value = field.touche_field(cell_values, st_theme()['base'] == 'dark')
st.text(value)



#st.markdown("""
#<style>
#.stHorizontalBlock {
#	gap: 1rem !important;
#}
#.stVerticalBlock {
#	gap: 0rem !important;
#}
#button[kind="secondary"] {
#    height: 60px !important;
#    width: 60px !important;
#    line-height: 1 !important;
#    padding: 0rem !important;
#}
#</style>
#""", unsafe_allow_html=True)
#
#fields = pandas.read_csv('field.csv', header=None)
#columns = st.columns(12, gap='small')
#
#counter = 0
#for (_, p_column), st_column in zip(fields.items(), columns):
#	for value in p_column:
#		st_column.button(value if isinstance(value, str) else ' ', key=f'{counter}')
#		counter += 1





#fields = pandas.read_csv('field.csv', header=None)
#for _, row in fields.iterrows():
#	sac.buttons([value if isinstance(value, str) else '' for value in row], gap=0)

#fields = pandas.read_csv('field.csv', header=None)
#grid = ste_grid(12, vertical_align='center')
#counter = 0
#for _, row in fields.iterrows():
#	for value in row:
#		if isinstance(value, str):
#			grid.button(value, str(counter))
#			counter += 1
#		else:
#			grid.empty()

