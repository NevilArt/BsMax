import bpy

v3camera, v3empty, v3light = None, None, None

def store_original_theme():
	v3camera = bpy.context.preferences.themes[0].view_3d.camera
	v3empty = bpy.context.preferences.themes[0].view_3d.empty
	v3light = bpy.context.preferences.themes[0].view_3d.light

def restore_original_theme():
	if v3camera != None:
		bpy.context.preferences.themes[0].view_3d.camera = v3camera
	if v3empty !=  None:
		bpy.context.preferences.themes[0].view_3d.empty = v3empty
	if v3light != None:
		bpy.context.preferences.themes[0].view_3d.light = v3light

def set_3dsmax_theme():
	bpy.context.preferences.themes[0].view_3d.camera = (0.341,0.47,0.8)
	bpy.context.preferences.themes[0].view_3d.empty = (0.054,1,0.007)
	bpy.context.preferences.themes[0].view_3d.light = (1,0.898,0,1)

def set_custom_theme(mode):
	store_original_theme()
	if mode == '3DsMax':
		set_3dsmax_theme()

__all__ = ["restore_original_theme", "set_custom_theme"]