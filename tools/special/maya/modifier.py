import bpy
from bpy.types import Operator
from bsmax.actions import modifier_add
from bsmax.state import is_objects_selected

class BsMax_OT_Lattice_2x2x2_Set(Operator):
	bl_idname = "modifier.lattice2x2x2set"
	bl_label = "Lattice 2x2x2 (Set)"
	@classmethod
	def poll(self, ctx):
		return is_objects_selected(ctx)
	def execute(self, ctx):
		bpy.ops.bsmax.latticebox(res_u=2,res_v=2,res_w=2)
		return{"FINISHED"}

class BsMax_OT_Lattice_3x3x3_Set(Operator):
	bl_idname = "modifier.lattice3x3x3set"
	bl_label = "Lattice 3x3x3 (Set)"
	@classmethod
	def poll(self, ctx):
		return is_objects_selected(ctx)
	def execute(self, ctx):
		bpy.ops.bsmax.latticebox(res_u=3,res_v=3,res_w=3)
		return{"FINISHED"}

class BsMax_OT_Lattice_4x4x4_Set(Operator):
	bl_idname = "modifier.lattice4x4x4set"
	bl_label = "Lattice 4x4x4 (Set)"
	@classmethod
	def poll(self, ctx):
		return is_objects_selected(ctx)
	def execute(self, ctx):
		bpy.ops.bsmax.latticebox(res_u=4,res_v=4,res_w=4)
		return{"FINISHED"}

class BsMax_OT_RevolveAdd(Operator):
	bl_idname = "bsmax.revolveadd"
	bl_label = "Revolve (add)"
	bl_options = {'REGISTER','UNDO'}
	@classmethod
	def poll(self, ctx):
		return is_objects_selected()
	def execute(self, ctx):
		modifier_add(ctx,ctx.selected_objects,'SCREW')
		return {'FINISHED'}

def modifier_cls(register):
	classes = [BsMax_OT_Lattice_2x2x2_Set,
			BsMax_OT_Lattice_3x3x3_Set,
			BsMax_OT_Lattice_4x4x4_Set,
			BsMax_OT_RevolveAdd]
	for c in classes:
		if register: bpy.utils.register_class(c)
		else: bpy.utils.unregister_class(c)
	return classes

if __name__ == '__main__':
	modifier_cls(True)

__all__ = ["modifier_cls"]