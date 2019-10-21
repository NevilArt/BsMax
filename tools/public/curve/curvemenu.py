import bpy
from bpy.types import Menu

def CreateMenu_CallBack(self, ctx):
	layout = self.layout
	layout.separator()
	layout.operator("curve.chamfer", text="Chamfer/Fillet").typein=True

def append_Create_Menu():
	bpy.types.VIEW3D_MT_edit_curve_ctrlpoints.append(CreateMenu_CallBack)

def Remove_Create_Menu():
	bpy.types.VIEW3D_MT_edit_curve_ctrlpoints.remove(CreateMenu_CallBack)  

def curvemenu_cls(register):
	if register:
		append_Create_Menu()
	else:
		Remove_Create_Menu()

if __name__ == '__main__':
	curvemenu_cls(True)

__all__ = ["curvemenu_cls"]