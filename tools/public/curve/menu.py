import bpy

def controlpoints_menu(self, ctx):
	layout = self.layout
	layout.separator()
	layout.operator("curve.mergebydistance",text="Merge by Distance (Under Construction)").typein=True
	layout.separator()
	layout.operator("curve.chamfer",text="Chamfer/Fillet").typein=True

def segments_menu(self, ctx):
	layout = self.layout
	layout.operator("curve.dividplus",text="Divid plus").typein=True
	layout.separator()
	layout.operator("curve.outline",text="Outline").typein=True
	layout.separator()
	layout.operator("curve.boolean",text="Boolean (Under Construction)").typein=True
	bu = layout.operator("curve.boolean",text="Boolean (Union) (Under Construction)")
	bu.typein = False
	bu.mode = 'UNION'
	bi = layout.operator("curve.boolean",text="Boolean (Intersection) (Under Construction)")
	bi.typein = False
	bi.mode = 'INTERSECTION'
	bd = layout.operator("curve.boolean",text="Boolean (Diffrence) (Under Construction)")
	bd.typein = False
	bd.mode = 'DIFFERENCE'
	bc = layout.operator("curve.boolean",text="Boolean (Cut) (Under Construction)")
	bc.typein = False
	bc.mode = 'CUT'
		
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