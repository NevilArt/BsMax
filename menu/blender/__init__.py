from .blenderdefault import *

def blender_cls(register, pref):
	blenderdefault_cls(register)

__all__ = ["blender_cls"]