from .cameras import *
from .targetcamera import *

def camera_cls(register, pref):
	cameras_cls(register)
	targetcamera_cls(register)

__all__ = ["camera_cls"]