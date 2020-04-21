from .edit import *
from .menu import *

def uv_cls(register, pref):
	edit_cls(register)
	menu_cls(register)

__all__ = ["uv_cls"]