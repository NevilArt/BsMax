from .attach import *
from .coordinate import *
from .dragclone import *
from .floateditor import *
from .hold import *
from .modifier import *
from .navigation import *
#from .objectproperties import *
from .snap import *
from .subobjectlevel import *
from .viewport import *
from .viewportbg import *

def max_cls(register, pref):
	attach_cls(register)
	coordinate_cls(register)
	dragclone_cls(register)
	floateditor_cls(register)
	hold_cls(register)
	modifier_cls(register)
	navigation_cls(register)
	#objectproperties_cls(register)
	snap_cls(register)
	subobjectlevel_cls(register)
	viewport_cls(register)
	viewportbg_cls(register)

__all__ = ["max_cls"]