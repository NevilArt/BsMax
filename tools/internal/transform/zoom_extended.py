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
# 2024/06/04

import bpy
from mathutils import Matrix
from bpy.types import Operator
from bpy.utils import register_class, unregister_class


class View3d_OT_HomeView(Operator):
	bl_idname = 'view3d.homeview'
	bl_label = "Home View"
	bl_description = "Home View"
	bl_options = {'REGISTER', 'INTERNAL'}
	
	@classmethod
	def poll(self, ctx):
		return ctx.area.type == 'VIEW_3D'
	
	def execute(self, ctx):
		homeview = (
			(0.4100, 0.9120, -0.0133, 0),
			(-0.4017, 0.1936, 0.8950, -1.9045),
			(0.8188, -0.3617, 0.4458, -17.9866),
			(0, 0, 0, 1)
		)
		ctx.area.spaces.active.region_3d.view_matrix = Matrix(homeview)
		return{'FINISHED'}


class View3d_OT_Zoom_Extended(Operator):
	bl_idname = 'view3d.zoom_extended'
	bl_label = "Zoom Extended"
	bl_description = "Zoom Extended"
	bl_options = {'REGISTER', 'INTERNAL'}

	@classmethod
	def poll(self, ctx):
		return ctx.area.type == 'VIEW_3D'

	def execute(self, ctx):
		view3d = bpy.ops.view3d
		ops_obj = bpy.ops.object
		if ctx.mode == 'OBJECT':
			if not ctx.scene.objects:
				view3d.homeview('INVOKE_DEFAULT')

			elif not ctx.selected_objects:
				view3d.view_all(use_all_regions=False,center=False)

			else:
				view3d.view_selected(use_all_regions=False)

		elif ctx.mode == 'EDIT_ARMATURE':
			if not ctx.selected_bones:
				ops_obj.mode_set(mode='OBJECT')
				view3d.view_selected(use_all_regions=False)
				ops_obj.mode_set(mode='EDIT')

			else:
				view3d.view_selected(use_all_regions=False)

		else:
			view3d.view_selected(use_all_regions=False)

		return{'FINISHED'}


class Node_OT_Zoom_Extended(Operator):
	bl_idname = 'node.zoom_extended'
	bl_label = 'Zoom Extended'

	@classmethod
	def poll(self, ctx):
		return ctx.area.type == 'NODE_EDITOR'

	def execute(self, ctx):
		node = bpy.ops.node
		if ctx.selected_nodes:
			node.view_selected('INVOKE_DEFAULT')
		else:
			try:
				node.view_all('INVOKE_DEFAULT')
			except:
				pass

		return{'FINISHED'}


classes = {
	View3d_OT_HomeView,
	View3d_OT_Zoom_Extended,
	Node_OT_Zoom_Extended
}


def register_zoom_extended():
	for cls in classes:
		register_class(cls)


def unregister_zoom_extended():
	for cls in classes:
		unregister_class(cls)


if __name__ == '__main__':
	register_zoom_extended()