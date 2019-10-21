import bpy, rna_keymap_ui

KeyMaps = []

def create_public_keymaps():
	kcfg = bpy.context.window_manager.keyconfigs.addon
	if kcfg:
		# 3D View --------------------------------------------------------------
		km = kcfg.keymaps.new(name='3D View',space_type='VIEW_3D')

		kmi = km.keymap_items.new("bsmax.droptool", "RIGHTMOUSE", "PRESS")
		KeyMaps.append((km, kmi))

		# Object Mode -------------------------------------------------------------------------
		km = kcfg.keymaps.new(name='Object Mode',space_type='EMPTY',region_type='WINDOW')

		kmi = km.keymap_items.new("bsmax.droptool", "RIGHTMOUSE", "PRESS")
		KeyMaps.append((km, kmi))
		
		# Mesh -----------------------------------------------------------------
		km = kcfg.keymaps.new(name='Mesh',space_type='EMPTY')

		kmi = km.keymap_items.new("bsmax.droptool", "RIGHTMOUSE", "PRESS")
		KeyMaps.append((km, kmi))

		# Curve ----------------------------------------------------------------
		km = kcfg.keymaps.new(name='Curve',space_type='EMPTY')

		kmi = km.keymap_items.new("bsmax.droptool", "RIGHTMOUSE", "PRESS")
		KeyMaps.append((km, kmi))

		# Armature -------------------------------------------------------------
		km = kcfg.keymaps.new(name='Armature',space_type='EMPTY')

		kmi = km.keymap_items.new("bsmax.droptool", "RIGHTMOUSE", "PRESS")
		KeyMaps.append((km, kmi))

		# Metaball -------------------------------------------------------------
		km = kcfg.keymaps.new(name='Metaball',space_type='EMPTY')

		kmi = km.keymap_items.new("bsmax.droptool", "RIGHTMOUSE", "PRESS")
		KeyMaps.append((km, kmi))

		# Lattice --------------------------------------------------------------
		km = kcfg.keymaps.new(name='Lattice',space_type='EMPTY')

		kmi = km.keymap_items.new("bsmax.droptool", "RIGHTMOUSE", "PRESS")
		KeyMaps.append((km, kmi))

		# Pose -----------------------------------------------------------------
		km = kcfg.keymaps.new(name='Pose',space_type='EMPTY')

		kmi = km.keymap_items.new("bsmax.droptool", "RIGHTMOUSE", "PRESS")
		KeyMaps.append((km, kmi))

def remove_public_keymaps():
	for km,kmi in KeyMaps:
		km.keymap_items.remove(kmi)
	KeyMaps.clear()

def public_keys(register, pref):
	if register:
		remove_public_keymaps()
		create_public_keymaps()
	else:
		remove_public_keymaps()

if __name__ == '__main__':
	max_keys(True)

__all__=["max_keys"]