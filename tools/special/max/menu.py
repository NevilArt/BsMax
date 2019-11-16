import bpy
from bpy.types import Menu

def ffd_menu(self, ctx):
	layout = self.layout
	layout.separator()
	layout.operator("modifier.ffd2x2x2set",text='FFD 2x2x2 (Set)',icon="OUTLINER_OB_LATTICE")
	layout.operator("modifier.ffd3x3x3set",text='FFD 3x3x3 (Set)',icon="OUTLINER_OB_LATTICE")
	layout.operator("modifier.ffd4x4x4set",text='FFD 4x4x4 (Set)',icon="OUTLINER_OB_LATTICE")

def menu_cls(register):
	if register:
		bpy.types.BSMAX_MT_latticecreatemenu.append(ffd_menu)
	else:
		bpy.types.BSMAX_MT_latticecreatemenu.remove(ffd_menu)

if __name__ == '__main__':
	menu_cls(True)

__all__ = ["menu_cls"]