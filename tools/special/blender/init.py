from .modifier import *
from .menu import *

def blender_cls(register, pref):
	modifier_cls(register)
	menu_cls(register)

__all__ = ["blender_cls"]