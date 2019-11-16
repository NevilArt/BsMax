from .chamfer import *
#from .panel import *
#from .split import *

def curve_cls(register, pref):
	chamfer_cls(register)
	#panel_cls(register)
	#split_cls(register)

__all__ = ["curve_cls"]