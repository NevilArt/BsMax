from .animation.init import *
from .armature.init import *
from .camera.init import *
from .curve.init import *
from .font.init import *
from .ligth.init import *
from .mesh.init import *
from .object.init import *
from .render.init import *
from .select.init import *
from .transform.init import *
from .uv.init import *
from .view.init import *

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