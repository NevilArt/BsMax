import bpy, rna_keymap_ui

KeyMaps = []

def create_view3d_quads(km, navigation):
	kmi = km.keymap_items.new("bsmax.view3dquadmenue", "V", "PRESS")
	kmi.properties.menu = 'viewport'
	kmi.properties.space = 'View3D'
	KeyMaps.append((km, kmi))

	kmi = km.keymap_items.new("bsmax.view3dquadmenue", "RIGHTMOUSE", "PRESS")
	kmi.properties.menu = 'default'
	kmi.properties.space = 'View3D'
	KeyMaps.append((km, kmi))

	# ignore alt + RMB if maya navigation was selected
	if navigation != 'Maya':
		kmi = km.keymap_items.new("bsmax.view3dquadmenue", "RIGHTMOUSE", "PRESS", alt = True)
		kmi.properties.menu = 'coordinate'
		kmi.properties.space = 'View3D'
		KeyMaps.append((km, kmi))

	kmi = km.keymap_items.new("bsmax.view3dquadmenue", "RIGHTMOUSE", "PRESS", ctrl = True)
	kmi.properties.menu = 'create'
	kmi.properties.space = 'View3D'
	KeyMaps.append((km, kmi))
	kmi = km.keymap_items.new("bsmax.view3dquadmenue", "RIGHTMOUSE", "PRESS", shift = True)
	kmi.properties.menu = 'snap'
	kmi.properties.space = 'View3D'
	KeyMaps.append((km, kmi))
	kmi = km.keymap_items.new("bsmax.view3dquadmenue", "RIGHTMOUSE", "PRESS", alt = True, ctrl = True)
	kmi.properties.menu = 'render'
	kmi.properties.space = 'View3D'
	KeyMaps.append((km, kmi))
	kmi = km.keymap_items.new("bsmax.view3dquadmenue", "RIGHTMOUSE", "PRESS", alt = True, shift = True)
	kmi.properties.menu = 'fx'
	kmi.properties.space = 'View3D'
	KeyMaps.append((km, kmi))
	kmi = km.keymap_items.new("bsmax.view3dquadmenue", "RIGHTMOUSE", "PRESS", ctrl = True, shift = True)
	kmi.properties.menu = 'Selection'
	kmi.properties.space = 'View3D'
	KeyMaps.append((km, kmi))
	kmi = km.keymap_items.new("bsmax.view3dquadmenue", "RIGHTMOUSE", "PRESS", alt = True, ctrl = True, shift = True)
	kmi.properties.menu = 'custom'
	kmi.properties.space = 'View3D'
	KeyMaps.append((km, kmi))

# Create Keymaps
def create_standard_quadmenue(navigation):
	kcfg = bpy.context.window_manager.keyconfigs.addon
	if kcfg:
		# Window ---------------------------------------------------------------
		#km = kcfg.keymaps.new(name='Window',space_type='EMPTY')
		# 2D View --------------------------------------------------------------
		#km = kcfg.keymaps.new(name='View2D',space_type='EMPTY',region_type='WINDOW')
		# 3D View --------------------------------------------------------------
		km = kcfg.keymaps.new(name='3D View',space_type='VIEW_3D')
		create_view3d_quads(km, navigation)
		# Object Mode -------------------------------------------------------------------------
		km = kcfg.keymaps.new(name='Object Mode',space_type='EMPTY',region_type='WINDOW')
		create_view3d_quads(km, navigation)
		# Mesh -----------------------------------------------------------------
		km = kcfg.keymaps.new(name='Mesh',space_type='EMPTY')
		create_view3d_quads(km, navigation)
		# Curve ----------------------------------------------------------------
		km = kcfg.keymaps.new(name='Curve',space_type='EMPTY')
		create_view3d_quads(km, navigation)
		# Armature -------------------------------------------------------------
		km = kcfg.keymaps.new(name='Armature',space_type='EMPTY')
		create_view3d_quads(km, navigation)
		# Pose -----------------------------------------------------------------
		km = kcfg.keymaps.new(name='Pose',space_type='EMPTY')
		create_view3d_quads(km, navigation)

def remove_standard_quadmenue():
	for km, kmi in KeyMaps:
		km.keymap_items.remove(kmi)
	KeyMaps.clear()

def keymap_std_keys(register, pref):
	if register:
		remove_standard_quadmenue()
		create_standard_quadmenue(pref.navigation)
	else:
		remove_standard_quadmenue()

__all__=["keymap_std_keys"]