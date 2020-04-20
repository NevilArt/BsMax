from .lightlister import *
from .menu import *

def render_cls(register, pref):
	lightlister_cls(register)
	menu_cls(register)

__all__ = ["render_cls"]