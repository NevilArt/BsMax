import bpy, rna_keymap_ui

KeyMaps = []

def create_cinema4d_keymaps():
	kcfg = bpy.context.window_manager.keyconfigs.addon
	if kcfg:
		print("add Cinema4D keymaps")
		# Window --------------------------------------
		#km = kcfg.keymaps.new(name ='Window', space_type ='EMPTY')
		#kmi = km.keymap_items.new("wm.search_menu", "X", "PRESS")
		#KeyMaps.append((km, kmi))
		
def remove_cinema4d_keymaps():
	for km, kmi in KeyMaps:
		km.keymap_items.remove(kmi)
	KeyMaps.clear()

def cinema4d_keys(register):
	if register:
		remove_cinema4d_keymaps()
		create_cinema4d_keymaps()
	else:
		remove_cinema4d_keymaps()

if __name__ == '__main__':
	cinema4d_keys(True)

__all__=["cinema4d_keys"]