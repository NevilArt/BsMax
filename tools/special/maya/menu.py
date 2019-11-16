import bpy
from bpy.types import Menu

def lattice_menu(self, ctx):
	layout = self.layout
	layout.separator()
	layout.operator("modifier.lattice2x2x2set",text='Lattice 2x2x2 (Set)',icon="OUTLINER_OB_LATTICE")
	layout.operator("modifier.lattice3x3x3set",text='Lattice 3x3x3 (Set)',icon="OUTLINER_OB_LATTICE")
	layout.operator("modifier.lattice4x4x4set",text='Lattice 4x4x4 (Set)',icon="OUTLINER_OB_LATTICE")

def menu_cls(register):
	if register:
		bpy.types.BSMAX_MT_latticecreatemenu.append(lattice_menu)
	else:
		bpy.types.BSMAX_MT_latticecreatemenu.remove(lattice_menu)

if __name__ == '__main__':
	menu_cls(True)

__all__ = ["menu_cls"]