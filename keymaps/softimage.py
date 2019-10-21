import bpy, rna_keymap_ui

KeyMaps = []

def create_softimage_keymaps():
	kcfg = bpy.context.window_manager.keyconfigs.addon
	if kcfg:
		print("add Softimage keymaps")
		# Window ---------------------------------------------------------------
		#km = kcfg.keymaps.new(name ='Window', space_type ='EMPTY')
		#kmi = km.keymap_items.new("wm.search_menu", "X", "PRESS")
		#KeyMaps.append((km, kmi))
		
def remove_softimage_keymaps():
	for km, kmi in KeyMaps:
		km.keymap_items.remove(kmi)
	KeyMaps.clear()

def softimage_keys(register):
	if register:
		remove_softimage_keymaps()
		create_softimage_keymaps()
	else:
		remove_softimage_keymaps()

if __name__ == '__main__':
	softimage_keys(True)

__all__=["softimage_keys"]