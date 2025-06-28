from pathlib import Path
from typing import Optional

import streamlit.components.v1 as components


frontend_dir = (Path(__file__).parent / 'frontend').absolute()
_component_func = components.declare_component('touche_field', path=str(frontend_dir))

def touche_field(values: list[str], is_dark: bool):
	return _component_func(values=values, is_dark=is_dark, default=666)
