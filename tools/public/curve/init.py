from .chamfer import *
from .outline import *
from .menu import *
#from .panel import *
#from .split import *

def curve_cls(register, pref):
	chamfer_cls(register)
	outline_cls(register)
	menu_cls(register)
	#panel_cls(register)
	#split_cls(register)

__all__ = ["curve_cls"]