############################################################################
#	This program is free software: you can redistribute it and/or modify
#	it under the terms of the GNU General Public License as published by
#	the Free Software Foundation, either version 3 of the License, or
#	(at your option) any later version.
#
#	This program is distributed in the hope that it will be useful,
#	but WITHOUT ANY WARRANTY; without even the implied warranty of
#	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#	GNU General Public License for more details.
#
#	You should have received a copy of the GNU General Public License
#	along with this program.  If not, see <https://www.gnu.org/licenses/>.
############################################################################

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



def register_blenderdefault():
	bpy.utils.register_class(BsMax_OT_BlenderDefaultMenueCall)



def unregister_blenderdefault():
	bpy.utils.unregister_class(BsMax_OT_BlenderDefaultMenueCall)