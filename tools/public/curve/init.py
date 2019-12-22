from .chamfer import *
from .outline import *
from .boolean import *
from .divid import *
from .menu import *
#from .panel import *
#from .split import *
from .weld import *

def curve_cls(register, pref):
	chamfer_cls(register)
	outline_cls(register)
	boolean_cls(register)
	divid_cls(register)
	menu_cls(register)
	#panel_cls(register)
	#split_cls(register)
	weld_cls(register)

__all__ = ["curve_cls"]