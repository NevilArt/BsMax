import bpy
from bpy.types import Operator
from bsmax.state import get_pref

class BsMax_OT_BlenderDefaultMenueCall(Operator):
	bl_idname = "bsmax.blenderdefaultmenucall"
	bl_label = "Call Blender Menu"
	
	def execute(self, ctx):
		mode = ctx.mode
		if mode == 'OBJECT':
			mt = "VIEW3D_MT_object_context_menu"	
		elif mode == 'EDIT_MESH':
			mt = "VIEW3D_MT_edit_mesh_context_menu"
		elif mode == 'EDIT_CURVE':
			mt = "VIEW3D_MT_edit_curve_context_menu"
		elif mode == 'EDIT_METABALL':
			mt = "VIEW3D_MT_edit_metaball_context_menu"
		elif mode == 'EDIT_ARMATURE':
			mt = "VIEW3D_MT_armature_context_menu"
		elif mode == 'EDIT_LATTICE':
		   mt = "VIEW3D_MT_edit_lattice_context_menu"
		elif mode == 'EDIT_TEXT':
			mt = "VIEW3D_MT_edit_text_context_menu"
		elif mode == 'POSE':
			mt = "VIEW3D_MT_pose_context_menu"
		elif mode == 'GPENCIL_EDIT':
		   mt = "VIEW3D_MT_gpencil_edit_context_menu"
		elif mode == 'PARTICLE':
		   mt = "VIEW3D_MT_particle_context_menu"
		bpy.ops.wm.call_menu(name = mt)
		return{"FINISHED"}

class BsMax_OT_DropTool(Operator):
	bl_idname = "bsmax.droptool"
	bl_label = "Drop Tool"

	def drop_tool(self, ctx):
		tools = ctx.workspace.tools
		tool = tools.from_space_view3d_mode(ctx.mode, create=False).idname
		leagals = ( "builtin.select",
					"builtin.select_box",
					"builtin.select_circle",
					"builtin.select_lasso",
					"builtin.cursor",
					"builtin.move",
					"builtin.rotate",
					"builtin.scale",
					"builtin.scale_cage" )
		if not tool in leagals:
			bpy.ops.wm.tool_set_by_id(name='builtin.move')
			return True
		return False

	def call_menu(self, ctx):
		pref = get_pref(ctx)
		if pref.floatmenus == "QuadMenu_st_andkey":
			bpy.ops.bsmax.view3dquadmenue('INVOKE_DEFAULT',menu='default',space='View3D')
		else:
			bpy.ops.bsmax.blenderdefaultmenucall('INVOKE_DEFAULT')

	def execute(self, ctx):
		if not self.drop_tool(ctx):
			self.call_menu(ctx)
		return{"FINISHED"}

	# def modal(self, ctx, event):
	# 	if not self.drop_tool(ctx):
	# 		return {'PASS_THROUGH'}
	# 	return {'CANCELLED'}

	# def invoke(self, ctx, event):
	# 	ctx.window_manager.modal_handler_add(self)
	# 	return {'RUNNING_MODAL'}

def droptool_cls(register, pref):
	classes = [BsMax_OT_BlenderDefaultMenueCall, BsMax_OT_DropTool]
	if register:
		[bpy.utils.register_class(c) for c in classes]
	else:
		[bpy.utils.unregister_class(c) for c in classes]

if __name__ == '__main__':
	droptool_cls(True)

__all__ = ["droptool_cls"]