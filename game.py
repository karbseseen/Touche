import streamlit as st
import streamlit.components.v1 as components
import streamlit_antd_components as sac
import st_aggrid
from streamlit_extras.grid import grid as ste_grid
from streamlit_extras.great_tables import great_tables
from great_tables import GT
import pandas

import field


# Main page content
st.markdown("# Main page 🎈")
st.sidebar.markdown("# Main page 🎈")

value = field.cookiecutter()
st.text(value)



st.markdown("""
<style>
.stHorizontalBlock {
	gap: 1rem !important;
}
.stVerticalBlock {
	gap: 0rem !important;
}
button[kind="secondary"] {
    height: 60px !important;
    width: 60px !important;
    line-height: 1 !important;
    padding: 0rem !important;
}
</style>
""", unsafe_allow_html=True)

fields = pandas.read_csv('field.csv', header=None)
columns = st.columns(12, gap='small')

counter = 0
for (_, p_column), st_column in zip(fields.items(), columns):
	for value in p_column:
		st_column.button(value if isinstance(value, str) else ' ', key=f'{counter}')
		counter += 1

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

