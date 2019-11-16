import bpy
import rna_keymap_ui

KeyMaps=[]

# public Keymaps added anyway
def public_keymaps(kcfg):
	km=kcfg.keymaps.new(name='3D View',space_type='VIEW_3D')
	kmi=km.keymap_items.new("view3d.zoomincover","WHEELINMOUSE","PRESS")
	KeyMaps.append((km,kmi))
	kmi=km.keymap_items.new("view3d.zoomoutcover","WHEELOUTMOUSE","PRESS")
	KeyMaps.append((km,kmi))

# Create Keymaps
def navigation_Blender(kcfg):
	# 3D View --------------------------------------------------------------
	km=kcfg.keymaps.new(name='3D View',space_type='VIEW_3D')
	kmi=km.keymap_items.new("view3d.movecover","MIDDLEMOUSE","PRESS",shift=True)
	KeyMaps.append((km,kmi))
	kmi=km.keymap_items.new("view3d.rotatecover","MIDDLEMOUSE","PRESS")
	KeyMaps.append((km,kmi))
	kmi=km.keymap_items.new("view3d.zoomcover","MIDDLEMOUSE","PRESS",ctrl=True)
	KeyMaps.append((km,kmi))
	kmi=km.keymap_items.new("view3d.dollycover","MIDDLEMOUSE","PRESS",ctrl=True,shift=True)
	KeyMaps.append((km,kmi))

def navigation_3dsmax(kcfg):
	# 3D View --------------------------------------------------------------
	km=kcfg.keymaps.new(name='3D View',space_type='VIEW_3D')
	kmi=km.keymap_items.new("view3d.movecover","MIDDLEMOUSE","PRESS")
	KeyMaps.append((km,kmi))
	kmi=km.keymap_items.new("view3d.rotatecover","MIDDLEMOUSE","PRESS",alt=True)
	KeyMaps.append((km,kmi))
	kmi=km.keymap_items.new("view3d.zoomcover","MIDDLEMOUSE","PRESS",ctrl=True,alt=True)
	KeyMaps.append((km,kmi))

def navigation_maya(kcfg):
	# 3D View --------------------------------------------------------------
	km=kcfg.keymaps.new(name='3D View',space_type='VIEW_3D')
	kmi=km.keymap_items.new("view3d.movecover","MIDDLEMOUSE","PRESS",alt=True)
	KeyMaps.append((km,kmi))
	kmi=km.keymap_items.new("view3d.rotatecover","LEFTMOUSE","PRESS",alt=True)
	KeyMaps.append((km,kmi))
	kmi=km.keymap_items.new("view3d.zoomcover","RIGHTMOUSE","PRESS",alt=True)
	KeyMaps.append((km,kmi))

def navigation_modo(kcfg):
	# 3D View --------------------------------------------------------------
	km=kcfg.keymaps.new(name='3D View',space_type='VIEW_3D')
	kmi=km.keymap_items.new("view3d.rotatecover","LEFTMOUSE","PRESS",alt=True)
	KeyMaps.append((km,kmi))
	kmi=km.keymap_items.new("view3d.movecover","LEFTMOUSE","PRESS",shift=True)
	KeyMaps.append((km,kmi))
	kmi=km.keymap_items.new("view3d.zoomcover","LEFTMOUSE","PRESS",ctrl=True)
	KeyMaps.append((km,kmi))
	#kmi=km.keymap_items.new("view3d.rotate","MIDDLEMOUSE","PRESS",alt=True)
	#KeyMaps.append((km,kmi)) # Orbit mode
	#kmi=km.keymap_items.new("view3d.zoomcover","RIGHTMOUSE","PRESS",alt=True)
	#KeyMaps.append((km,kmi)) # 
	#https://www.youtube.com/watch?v=SDvv34owpV0
	#x.view.use_mouse_depth_navigate=True # enable: Auto Depth
	#x.view.use_zoom_to_mouse=True # enable: Zoom To Mouse Position
	#x.inputs.use_mouse_emulate_3_button=True # enable: Emulate 3 Button Mouse
	#x.inputs.view_rotate_method=‘TRACKBALL’ # Orbit Style: Trackball
	#x.inputs.view_zoom_axis=‘HORIZONTAL’ # Zoom Style: Horizontal
	#x.view.use_auto_perspective=True # enable: Auto Perspective (auto orthographic views)
	#x.system.use_region_overlap=True # enable: Region Overlap (makes Tool Shelf transparent)
	#bpy.ops.wm.save_userpref()

def navigation_softimage(kcfg):
	# 3D View --------------------------------------------------------------
	km=kcfg.keymaps.new(name='3D View',space_type='VIEW_3D')
	kmi=km.keymap_items.new("view3d.movecover","MIDDLEMOUSE","PRESS",alt=True)
	KeyMaps.append((km,kmi))
	kmi=km.keymap_items.new("view3d.rotatecover","LEFTMOUSE","PRESS",alt=True)
	KeyMaps.append((km,kmi))
	kmi=km.keymap_items.new("view3d.zoomcover","RIGHTMOUSE","PRESS",alt=True)
	KeyMaps.append((km,kmi))

def navigation_cinema4d(kcfg):
	# 3D View --------------------------------------------------------------
	km=kcfg.keymaps.new(name='3D View',space_type='VIEW_3D')
	kmi=km.keymap_items.new("view3d.movecover","MIDDLEMOUSE","PRESS",alt=True)
	KeyMaps.append((km,kmi))
	kmi=km.keymap_items.new("view3d.rotatecover","LEFTMOUSE","PRESS",alt=True)
	KeyMaps.append((km,kmi))
	kmi=km.keymap_items.new("view3d.zoomcover","RIGHTMOUSE","PRESS",alt=True)
	KeyMaps.append((km,kmi))

def create_navigation_keymaps(app):
	kcfg=bpy.context.window_manager.keyconfigs.addon
	if kcfg:
		if app == 'Blender':
			navigation_Blender(kcfg)
		elif app == '3DsMax':
			navigation_3dsmax(kcfg)
		elif app == 'Maya':
			navigation_maya(kcfg)
		elif app == 'Modo':
			navigation_modo(kcfg)
		elif app == 'Softimage':
			navigation_softimage(kcfg)
		elif app == 'Cinema4D':
			navigation_cinema4d(kcfg)
		public_keymaps(kcfg)

def remove_navigation_keymaps():
	for km,kmi in KeyMaps:
		km.keymap_items.remove(kmi)
	KeyMaps.clear()

def navigation_keys(register,pref):
	if register:
		remove_navigation_keymaps()
		create_navigation_keymaps(pref.navigation)
	else:
		remove_navigation_keymaps()

if __name__ == '__main__':
	navigation_keys(True)

__all__=["navigation_keys"]