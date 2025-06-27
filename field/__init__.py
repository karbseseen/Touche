from pathlib import Path
from typing import Optional

import streamlit.components.v1 as components
import streamlit as st


frontend_dir = (Path(__file__).parent / 'frontend').absolute()
_component_func = components.declare_component("cookiecutter", path=str(frontend_dir))

def cookiecutter(key: Optional[str] = None):
	st.text(frontend_dir)
	return  _component_func(default=666, key=key)
