import bpy

def controlpoints_menu(self, ctx):
	layout = self.layout
	layout.separator()
	layout.operator("curve.chamfer", text="Chamfer/Fillet").typein=True

def segments_menu(self, ctx):
	layout = self.layout
	layout.separator()
	layout.operator("curve.outline", text="Outline").typein=True
	layout.separator()
	layout.operator("curve.boolean", text="Boolean (Union)").operation = 'UNION'
	layout.operator("curve.boolean", text="Boolean (Intersection)").operation = 'INTERSECTION'
	layout.operator("curve.boolean", text="Boolean (Diffrence)").operation = 'DIFFERENCE'
		
def menu_cls(register):
	if register: 
		bpy.types.VIEW3D_MT_edit_curve_ctrlpoints.append(controlpoints_menu)
		bpy.types.VIEW3D_MT_edit_curve_segments.append(segments_menu)
	else:
		bpy.types.VIEW3D_MT_edit_curve_ctrlpoints.remove(controlpoints_menu)
		bpy.types.VIEW3D_MT_edit_curve_segments.remove(segments_menu)

if __name__ == '__main__':
	menu_cls(True)

__all__ = ["menu_cls"]