from .joystick import *

def rigg_cls(register, pref):
	classes = joystick_cls(register)
	return classes

__all__ = ["rigg_cls"]