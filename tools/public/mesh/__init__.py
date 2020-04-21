from .meshs import *
from .smartcreate import *
from .smartloop import *
from .smartring import *
from .weld import *

def mesh_cls(register, pref):
	meshs_cls(register)
	smartcreate_cls(register)
	smartloop_cls(register)
	smartring_cls(register)
	weld_cls(register)

__all__ = ["mesh_cls"]