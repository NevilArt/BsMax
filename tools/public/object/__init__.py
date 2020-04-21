from .arrange import *
from .batchrename import *
from .clonearrayobjects import *
from .freeze import *
from .lattice import *
from .pivotpoint import *

def object_cls(register, pref):
	arrange_cls(register)
	batchrename_cls(register)
	cloneobject_cls(register)
	lattice_cls(register)
	pivotpoint_cls(register)

__all__ = ["object_cls"]