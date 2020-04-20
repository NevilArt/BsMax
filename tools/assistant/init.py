from .animation import animation_cls
from .rigg import rigg_cls
from .render import render_cls

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
			elif current == "Render":
				render_cls(False, pref)
			elif current == "Rigg":
				rigg_cls(False, pref)

		# register new #
		if pref.assistpack == "Animate":
			animation_cls(register, pref)
	
		if pref.assistpack == "Render":
			render_cls(register, pref)

		if pref.assistpack == "Rigg":
			rigg_cls(register, pref)
		
		current = pref.assistpack

__all__ = ["assistant_cls"]