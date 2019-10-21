#from .blender.init import *
from .quad.init import *
# from .marking.init import *

current = None

def menu_cls(register, pref):
	global current

	# Unregister older #
	if register and current != None:
		if current == "QuadMenu_st_andkey":
			quad_cls(False, pref, False)
		elif current == "QuadMenu_st_nokey":
			quad_cls(False, pref, False)
		elif current == "Marking_Menu":
			# markmenu_cls(False, pref)
			pass

	# if pref.floatmenus == "Blender":
	#  	blender_cls(register, pref)

	if pref.floatmenus == "QuadMenu_st_nokey":
		quad_cls(register, pref, False)

	elif pref.floatmenus == "QuadMenu_st_andkey":
		quad_cls(register, pref, True)

	elif pref.floatmenus == "Marking_Menu":
		#markmenu_cls(register, pref)
		pass

	current = pref.floatmenus

__all__ = ["menu_cls"]