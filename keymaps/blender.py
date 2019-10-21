import bpy
import rna_keymap_ui

KeyMaps = []

# Create Keymaps
def create_blender_keymaps():
	kcfg = bpy.context.window_manager.keyconfigs.addon
	if kcfg:
		# Object Non-modal --------------------------------------------------------------------
		km = kcfg.keymaps.new(name='Object Non-modal', space_type='EMPTY', region_type='WINDOW')

		kmi = km.keymap_items.new("bsmax.mode_set", 'F9', "PRESS")
		KeyMaps.append((km, kmi))

		# 3D View --------------------------------------------------------------
		km = kcfg.keymaps.new(name='3D View', space_type='VIEW_3D', region_type='WINDOW')
		#kmi = km.keymap_items.new("bsmax.renameobjects", "F2", "PRESS")
		#KeyMaps.append((km, kmi))
		kmi = km.keymap_items.new("object.batchrename", "F2", "PRESS")
		KeyMaps.append((km, kmi))
		kmi = km.keymap_items.new("wm.call_menu", "A", "PRESS", ctrl=True, shift=True)
		kmi.properties.name = "BsMax_MT_Create"
		KeyMaps.append((km, kmi))

		# Armature -------------------------------------------------------------
		km = kcfg.keymaps.new(name='Armature', space_type='EMPTY', region_type='WINDOW')
		kmi = km.keymap_items.new("armature.batchrename", "F2", "PRESS")
		KeyMaps.append((km, kmi))

		# Node Editor -----------------------------------------------------------------
		km = kcfg.keymaps.new(name="Node Editor", space_type="NODE_EDITOR", region_type='WINDOW')
		kmi = km.keymap_items.new("node.batchrename", "F2", "PRESS")
		KeyMaps.append((km, kmi))

		# SEQUENCE_EDITOR--------------------------------------------------------------------
		km = kcfg.keymaps.new(name='Sequencer', space_type='SEQUENCE_EDITOR', region_type='WINDOW')
		kmi = km.keymap_items.new("sequencer.batchrename", "F2", "PRESS")
		KeyMaps.append((km, kmi))

def remove_blender_keymaps():
	for km, kmi in KeyMaps:
		km.keymap_items.remove(kmi)
	KeyMaps.clear()

def blender_keys(register):
	if register:
		remove_blender_keymaps()
		create_blender_keymaps()
	else:
		remove_blender_keymaps()

if __name__ == '__main__':
	blender_keys(True)

__all__=["blender_keys"]