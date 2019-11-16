from .modifier import *
from .menu import *

def maya_cls(register, pref):
	modifier_cls(register)
	menu_cls(register)

__all__ = ["maya_cls"]