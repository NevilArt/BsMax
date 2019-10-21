import bpy
from time import sleep

def start_up(mode):
	sleep(0.1)	
	if mode == '3DsMax':
		try:
			bpy.context.space_data.overlay.show_cursor = False
			bpy.context.space_data.overlay.show_annotation = False
		except:
			pass

__all__ = ["start_up"]