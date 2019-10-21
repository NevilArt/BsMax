import bpy
import rna_keymap_ui

KeyMaps = []

# public Keymaps added anyway
def public_keymaps():
	pass

# Create Keymaps
def navigation_3dsmax():
	kcfg = bpy.context.window_manager.keyconfigs.addon
	if kcfg:
		# 2D View --------------------------------------------------------------
		#km = kcfg.keymaps.new(name = 'View2D', space_type = 'EMPTY', region_type = 'WINDOW')
		#kmi = km.keymap_items.new("view2d.zoom", "MIDDLEMOUSE", "PRESS", ctrl = True, alt = True)
		#BsMax_KeyMaps.append((km, kmi))
		# 3D View --------------------------------------------------------------
		km = kcfg.keymaps.new(name = '3D View', space_type = 'VIEW_3D')
		kmi = km.keymap_items.new("view3d.move", "MIDDLEMOUSE", "PRESS")
		KeyMaps.append((km, kmi))
		kmi = km.keymap_items.new("view3d.rotate", "MIDDLEMOUSE", "PRESS", alt = True)
		KeyMaps.append((km, kmi))
		kmi = km.keymap_items.new("view3d.zoom", "MIDDLEMOUSE", "PRESS", ctrl = True, alt = True)
		KeyMaps.append((km, kmi))

def navigation_maya():
	kcfg = bpy.context.window_manager.keyconfigs.addon
	if kcfg:
		# 2D View --------------------------------------------------------------
		#km = kcfg.keymaps.new(name = 'View2D', space_type = 'EMPTY', region_type = 'WINDOW')
		#kmi = km.keymap_items.new("view2d.zoom", "MIDDLEMOUSE", "PRESS", ctrl = True, alt = True)
		#BsMax_KeyMaps.append((km, kmi))
		# 3D View --------------------------------------------------------------
		km = kcfg.keymaps.new(name = '3D View', space_type = 'VIEW_3D')
		kmi = km.keymap_items.new("view3d.move", "MIDDLEMOUSE", "PRESS", alt = True)
		KeyMaps.append((km, kmi))
		kmi = km.keymap_items.new("view3d.rotate", "LEFTMOUSE", "PRESS", alt = True)
		KeyMaps.append((km, kmi))
		kmi = km.keymap_items.new("view3d.zoom", "RIGHTMOUSE", "PRESS", alt = True)
		KeyMaps.append((km, kmi))

def navigation_modo():
	kcfg = bpy.context.window_manager.keyconfigs.addon
	if kcfg:
		# 2D View --------------------------------------------------------------
		#km = kcfg.keymaps.new(name = 'View2D', space_type = 'EMPTY', region_type = 'WINDOW')
		#kmi = km.keymap_items.new("view2d.zoom", "MIDDLEMOUSE", "PRESS", ctrl = True, alt = True)
		#BsMax_KeyMaps.append((km, kmi))
		# 3D View --------------------------------------------------------------
		km = kcfg.keymaps.new(name = '3D View', space_type = 'VIEW_3D')
		kmi = km.keymap_items.new("view3d.move", "MIDDLEMOUSE", "PRESS")
		KeyMaps.append((km, kmi))
		kmi = km.keymap_items.new("view3d.rotate", "LEFTMOUSE", "PRESS", alt = True)
		KeyMaps.append((km, kmi))
		#kmi = km.keymap_items.new("view3d.rotate", "MIDDLEMOUSE", "PRESS", alt = True)
		#KeyMaps.append((km, kmi)) # Orbit mode
		kmi = km.keymap_items.new("view3d.zoom", "LEFTMOUSE", "PRESS", ctrl = True, alt = True)
		KeyMaps.append((km, kmi))
		#https://www.youtube.com/watch?v=SDvv34owpV0
		#x.view.use_mouse_depth_navigate = True # enable: Auto Depth
		#x.view.use_zoom_to_mouse = True # enable: Zoom To Mouse Position
		#x.inputs.use_mouse_emulate_3_button = True # enable: Emulate 3 Button Mouse
		#x.inputs.view_rotate_method = ‘TRACKBALL’ # Orbit Style: Trackball
		#x.inputs.view_zoom_axis = ‘HORIZONTAL’ # Zoom Style: Horizontal
		#x.view.use_auto_perspective = True # enable: Auto Perspective (auto orthographic views)
		#x.system.use_region_overlap = True # enable: Region Overlap (makes Tool Shelf transparent)
		#bpy.ops.wm.save_userpref()

def navigation_softimage():
	kcfg = bpy.context.window_manager.keyconfigs.addon
	if kcfg:
		# 2D View --------------------------------------------------------------
		#km = kcfg.keymaps.new(name = 'View2D', space_type = 'EMPTY', region_type = 'WINDOW')
		#kmi = km.keymap_items.new("view2d.zoom", "MIDDLEMOUSE", "PRESS", ctrl = True, alt = True)
		#BsMax_KeyMaps.append((km, kmi))
		# 3D View --------------------------------------------------------------
		km = kcfg.keymaps.new(name = '3D View', space_type = 'VIEW_3D')
		kmi = km.keymap_items.new("view3d.move", "MIDDLEMOUSE", "PRESS", alt = True)
		KeyMaps.append((km, kmi))
		kmi = km.keymap_items.new("view3d.rotate", "LEFTMOUSE", "PRESS", alt = True)
		KeyMaps.append((km, kmi))
		kmi = km.keymap_items.new("view3d.zoom", "RIGHTMOUSE", "PRESS", alt = True)
		KeyMaps.append((km, kmi))

def navigation_cinema4d():
	kcfg = bpy.context.window_manager.keyconfigs.addon
	if kcfg:
		# 2D View --------------------------------------------------------------
		#km = kcfg.keymaps.new(name = 'View2D', space_type = 'EMPTY', region_type = 'WINDOW')
		#kmi = km.keymap_items.new("view2d.zoom", "MIDDLEMOUSE", "PRESS", ctrl = True, alt = True)
		#BsMax_KeyMaps.append((km, kmi))
		# 3D View --------------------------------------------------------------
		km = kcfg.keymaps.new(name = '3D View', space_type = 'VIEW_3D')
		kmi = km.keymap_items.new("view3d.move", "MIDDLEMOUSE", "PRESS", alt = True)
		KeyMaps.append((km, kmi))
		kmi = km.keymap_items.new("view3d.rotate", "LEFTMOUSE", "PRESS", alt = True)
		KeyMaps.append((km, kmi))
		kmi = km.keymap_items.new("view3d.zoom", "RIGHTMOUSE", "PRESS", alt = True)
		KeyMaps.append((km, kmi))

def create_navigation_keymaps(app):
	if app == '3DsMax':
		navigation_3dsmax()
	elif app == 'Maya':
		navigation_maya()
	elif app == 'Modo':
		navigation_modo()
	elif app == 'Softimage':
		navigation_softimage()
	elif app == 'Cinema4D':
		navigation_cinema4d()
	public_keymaps()

def remove_navigation_keymaps():
	for km, kmi in KeyMaps:
		km.keymap_items.remove(kmi)
	KeyMaps.clear()

def navigation_keys(register, pref):
	if register:
		remove_navigation_keymaps()
		create_navigation_keymaps(pref.navigation)
	else:
		remove_navigation_keymaps()

if __name__ == '__main__':
	navigation_keys(True)

__all__=["navigation_keys"]