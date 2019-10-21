import bpy
from bpy.props import StringProperty, BoolProperty
from bpy.types import Scene, Panel, Operator

class BsMax_OT_AttachMesh(Operator):
	bl_idname = "bsmax.attachmesh"
	bl_label = "Attach (Mesh)"
	#custom_property: PointerProperty(type = bpy.types.Object)
	def execute(self, ctx):
		print("Attach by eyedrop working on progress")
		return{"FINISHED"}

class BsMax_OT_AttachListMesh(Operator):
	bl_idname = "bsmax.attachlistmesh"
	bl_label = "Attach List (Mesh)"
	def execute(self, ctx):
		print("Attach by list working on progress")
		return{"FINISHED"}

class BsMax_OT_DetachMesh(Operator):
	bl_idname = "bsmax.detachmesh"
	bl_label = "Detach (Mesh)"

	name:StringProperty(name="Name")
	element:BoolProperty(default=False)
	clone:BoolProperty(default=False)

	@classmethod
	def poll(self, ctx):
		return ctx.area.type == 'VIEW_3D'

	def draw(self, ctx):
		layout = self.layout
		box = layout.box()
		row = box.column()
		row.prop(self,"name",text="Detach as:")
		row.prop(self,"element",text ="Detach To Element")
		row.prop(self,"clone",text="Detach as clone")

	def execute(self, ctx):
		if self.clone:
			bpy.ops.mesh.duplicate_move(MESH_OT_duplicate={"mode":1},
				TRANSFORM_OT_translate={"value":(0, 0, 0),
				"orient_type":'GLOBAL',
				"orient_matrix":((0, 0, 0), (0, 0, 0), (0, 0, 0)),
				"orient_matrix_type":'GLOBAL',
				"constraint_axis":(False, False, False),
				"mirror":False,
				"use_proportional_edit":False,
				"proportional_edit_falloff":'SMOOTH',
				"proportional_size":1,
				"use_proportional_connected":False,
				"use_proportional_projected":False,
				"snap":False,
				"snap_target":'CLOSEST',
				"snap_point":(0, 0, 0),
				"snap_align":False,
				"snap_normal":(0, 0, 0),
				"gpencil_strokes":False,
				"cursor_transform":False,
				"texture_space":False,
				"remove_on_cancel":False,
				"release_confirm":False,
				"use_accurate":False})
		if self.element:
			bpy.ops.mesh.split('INVOKE_DEFAULT')
		else:
			bpy.ops.mesh.separate(type = 'SELECTED')
		return{"FINISHED"}
	def invoke(self, ctx, event):
		if ctx.active_object != None:
			self.name = ctx.active_object.name
		wm = ctx.window_manager
		return wm.invoke_props_dialog(self)

def Attach_Cls():
	return [BsMax_OT_AttachMesh, BsMax_OT_AttachListMesh, BsMax_OT_DetachMesh]
__all__ = [ "Attach_Cls",
			"BsMax_OT_AttachMesh",
			"BsMax_OT_AttachListMesh",
			"BsMax_OT_DetachMesh" ]

if __name__ == '__main__':
	for Cls in Attach_Cls():
		bpy.utils.register_class(Cls)

def attach_cls(register):
	classes = [BsMax_OT_AttachMesh, BsMax_OT_AttachListMesh, BsMax_OT_DetachMesh]
	for c in classes:
		if register: bpy.utils.register_class(c)
		else: bpy.utils.unregister_class(c)
	return classes

if __name__ == '__main__':
	attach_cls(True)

__all__ = ["attach_cls"]