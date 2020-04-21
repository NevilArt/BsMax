from .animation import *
from .armature import *
from .camera import *
from .curve import *
from .font import *
from .ligth import *
from .mesh import *
from .object import *
from .render import *
from .select import *
from .transform import *
from .uv import *
from .view import *

registered = False

def public_cls(register, pref):
	global registered

	# register and unregister just once #
	if registered != register:
		animation_cls(register, pref)
		armature_cls(register, pref)
		camera_cls(register, pref)
		curve_cls(register, pref)
		font_cls(register, pref)
		ligth_cls(register, pref)
		mesh_cls(register, pref)
		object_cls(register, pref)
		render_cls(register, pref)
		select_cls(register, pref)
		transform_cls(register, pref)
		uv_cls(register, pref)
		view_cls(register, pref)

	registered = register

__all__ = ["public_cls"]