from .animation.init import *
#from .model.init import *
from .rigg.init import *

current = None

def assistant_cls(register, pref):
	global current
	
	if pref.assistpack != current:
		# Unregister older #
		if register and current != None:
			if current == "Animate":
				animation_cls(False, pref)
			elif current == "Model":
				pass
			elif current == "Rigg":
				rigg_cls(False, pref)

		# register new #
		if pref.assistpack == "Animate":
			animation_cls(register, pref)

		if pref.assistpack == "Model":
			#model_cls(register, pref)
			pass

		if pref.assistpack == "Rigg":
			rigg_cls(register, pref)
		
		current = pref.assistpack

__all__ = ["assistant_cls"]