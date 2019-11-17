from .eyetarget import *
from .joystick import *
from .menu import *

def rigg_cls(register, pref):
	eyetarget_cls(register)
	joystick_cls(register)
	menu_cls(register)

__all__ = ["rigg_cls"]