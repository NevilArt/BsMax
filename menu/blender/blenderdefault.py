import bpy
from bpy.types import Operator

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

def blenderdefault_cls(register):
	c = BsMax_OT_BlenderDefaultMenueCall
	if register: bpy.utils.register_class(c)
	else: bpy.utils.unregister_class(c)

if __name__ == '__main__':
	blenderdefault_cls(True)

__all__ = ["blenderdefault_cls"]

# VIEW3D_PT_gpencil_draw_context_menu
# VIEW3D_PT_gpencil_sculpt_context_menu
# VIEW3D_PT_paint_texture_context_menu
# VIEW3D_PT_paint_vertex_context_menu
# VIEW3D_PT_paint_weight_context_menu
# VIEW3D_PT_sculpt_context_menu

# DOPESHEET_MT_context_menu
# DOPESHEET_MT_channel_context_menu

# TEXT_MT_toolbox
# CLIP_MT_tracking_context_menu



