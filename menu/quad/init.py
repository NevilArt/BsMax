from .quadmenu import *
from .keymap_std import *

def quad_cls(register, pref, keymap):
	quadmenu_cls(register)
	keymap_std_keys(register and keymap, pref)

__all__ = ["quad_cls"]