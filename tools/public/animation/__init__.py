from .animationkey import *
from .frameupdate import *

def animation_cls(register, pref):
	animationkey_cls(register)
	frameupdate_cls(register)

__all__ = ["animation_cls"]