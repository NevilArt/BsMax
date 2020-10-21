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

class Render_OT_Quick_Render(Operator):
	bl_idname = "render.quick_render"
	bl_label = "Quick Render"

	@classmethod
	def poll(self, ctx):
		return True

	def execute(self, ctx):
		r3d = ctx.area.spaces[0].region_3d
		if r3d.view_perspective == 'CAMERA':
			bpy.ops.render.render('INVOKE_DEFAULT')
		else:
			# trick is create a camera from view and delete after render 
			# but for unknown reason 
			view_matrix = ctx.area.spaces.active.region_3d.view_matrix
			bpy.ops.object.camera_add()
			ctx.scene.camera = bpy.data.objects[ctx.active_object.name]
			cam = ctx.active_object
			cam.matrix_world = view_matrix
			bpy.ops.render.render('INVOKE_DEFAULT')
			bpy.ops.object.delete({"selected_objects": cam})
			# bpy.ops.object.delete(use_global=False, confirm=False)
		return{"FINISHED"}

def register_quick_render():
	bpy.utils.register_class(Render_OT_Quick_Render)

def unregister_quick_render():
	bpy.utils.unregister_class(Render_OT_Quick_Render)

if __name__ == "__main__":
	register_quick_render()