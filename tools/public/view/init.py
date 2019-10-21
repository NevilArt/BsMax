from .droptool import *
from .filebrowser import *

def view_cls(register, pref):
	droptool_cls(register, pref)
	filebrowser_cls(register)

__all__ = ["view_cls"]