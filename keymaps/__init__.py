from .max import *
from .blender import *
from .cinema4d import *
from .maya import *
from .modo import *
from .softimage import *

from .navigation import navigation_keys
from .public import public_keys

def keymaps_keys(register, pref):
	# load applications key maps #
	if pref.keymaps == '3DsMax':
		max_keys(register)
	elif pref.keymaps == 'Blender':
		blender_keys(register)
	elif pref.keymaps == 'Cinema4D':
		cinema4d_keys(register)
	elif pref.keymaps == 'Maya':
		maya_keys(register)
	elif pref.keymaps == 'Modo':
		modo_keys(register)
	elif pref.keymaps == 'Softimage':
		softimage_keys(register)


__all__ = ["keymaps_keys", "navigation_keys", "public_keys"]