#from . addon import *
from _thread import start_new_thread
from .default import start_up
from .theme import restore_original_theme, set_custom_theme

def startup_settings(app):
	start_new_thread(start_up,tuple([app]))
	set_custom_theme(app)

def restore_settings():
	restore_original_theme()

def	startup_cls(register, pref):
	if register:
		startup_settings(pref.keymaps)
	else:
		restore_settings()

__all__ = ["startup_cls"]
