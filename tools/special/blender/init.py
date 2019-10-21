from .modifier import modifier_cls

def blender_cls(register, pref):
	modifier_cls(register)

__all__ = ["blender_cls"]