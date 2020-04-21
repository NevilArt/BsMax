from .alignobjects import *
from .mirror import *
from .transforms import *
from .transformtypein import *
from .zoomextended import *

def transform_cls(register, pref):
	alignobjects_cls(register)
	mirror_cls(register)
	transforms_cls(register)
	transformtypein_cls(register)
	zoomextended_cls(register)

__all__ = ["transform_cls"]