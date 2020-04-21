from .blender.init import *
from .max.init import *
from .maya.init import *

current = None

def special_cls(register, pref):
	global current

	if pref.toolpack != current:
		# Unregister older #
		if register and current != None:
			if current == "Blender":
				blender_cls(False, pref)
			elif current == "3DsMax":
				max_cls(False, pref)
			elif current == "Maya":
				maya_cls(False, pref)

		# register new #
		if pref.toolpack == "Blender":
			blender_cls(register, pref)

		if pref.toolpack == "3DsMax":
			max_cls(register, pref)

		if pref.toolpack == "Maya":
			maya_cls(register, pref)

	current = pref.toolpack

__all__ = ["special_cls"]