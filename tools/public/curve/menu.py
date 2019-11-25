import bpy

def curve_menu(self, ctx):
	layout = self.layout
	layout.separator()
	layout.operator("curve.chamfer", text="Chamfer/Fillet").typein=True
	layout.operator("curve.outlinecurve", text="Outline").typein=True
		
def menu_cls(register):
	if register: 
		bpy.types.VIEW3D_MT_edit_curve_ctrlpoints.append(curve_menu)
	else:
		bpy.types.VIEW3D_MT_edit_curve_ctrlpoints.remove(curve_menu)

if __name__ == '__main__':
	menu_cls(True)

__all__ = ["menu_cls"]