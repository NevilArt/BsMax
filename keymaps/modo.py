import bpy, rna_keymap_ui

KeyMaps = []

def create_modo_keymaps():
	kcfg = bpy.context.window_manager.keyconfigs.addon
	if kcfg:
		print("add Modo keymaps")
		# Window ---------------------------------------------------------------
		#km = kcfg.keymaps.new(name ='Window', space_type ='EMPTY')
		#kmi = km.keymap_items.new("wm.search_menu", "X", "PRESS")
		#KeyMaps.append((km, kmi))
		
def remove_modo_keymaps():
	for km, kmi in KeyMaps:
		km.keymap_items.remove(kmi)
	KeyMaps.clear()

def modo_keys(register):
	if register:
		remove_modo_keymaps()
		create_modo_keymaps()
	else:
		remove_modo_keymaps()

if __name__ == '__main__':
	modo_keys(True)

__all__=["modo_keys"]