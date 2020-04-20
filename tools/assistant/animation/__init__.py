from .parent import *
from .menu import *


def animation_cls(register, pref):
	parent_cls(register)
	menu_cls(register)

__all__ = ["animation_cls"]