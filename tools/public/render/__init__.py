from .frames import *
from .proxy import *

def render_cls(register, pref):
	frames_cls(register)
	proxy_cls(register)

__all__ = ["render_cls"]