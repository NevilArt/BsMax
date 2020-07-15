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
from bsmax.graphic import register_line,unregister_line

# TARGET WELD
# Original Coded from Stromberg90 updated by Nevil
# https://github.com/Stromberg90/Scripts/tree/master/Blender

def SelectVert(ctx, event, started):
	coord = event.mouse_region_x, event.mouse_region_y
	if started:
		result = bpy.ops.view3d.select(extend=True,location=coord)
	else:
		result = bpy.ops.view3d.select(extend=False,location=coord)
	if result == {'PASS_THROUGH'}:
		bpy.ops.mesh.select_all(action='DESELECT')

class Mesh_OT_Target_Weld(bpy.types.Operator):
	bl_idname = "mesh.target_weld"
	bl_label = "Target Weld"
	bl_options = {'REGISTER','UNDO'}
	start, end, handle = None, None, None
	drag, picked = False, False

	def modal(self, ctx, event):
		ctx.area.tag_redraw()
		if event.type in {'MIDDLEMOUSE','WHEELUPMOUSE','WHEELDOWNMOUSE'}:
			return {'PASS_THROUGH'}

		elif event.type == 'MOUSEMOVE':
			if self.start != None:
				self.end = event.mouse_region_x, event.mouse_region_y

		elif event.type == 'LEFTMOUSE':
			if event.value == 'PRESS':
				if self.start == None:
					self.start = event.mouse_region_x, event.mouse_region_y
					coord = event.mouse_region_x, event.mouse_region_y
					bpy.ops.view3d.select(extend=False, location=coord)

			if event.value =='RELEASE':
				self.end = event.mouse_region_x, event.mouse_region_y

				if self.start != None:
					coord = event.mouse_region_x, event.mouse_region_y
					bpy.ops.view3d.select(extend=True,location=coord)

				SelectVert(ctx, event, self.start != None)
				if ctx.object.data.total_vert_sel == 2:
					self.start = self.end = None
					bpy.ops.mesh.merge(type='LAST')
					bpy.ops.mesh.select_all(action='DESELECT')

			return {'RUNNING_MODAL'}
		elif event.type in {'RIGHTMOUSE','ESC'}:
			unregister_line(self.handle)
			return {'CANCELLED'}

		return {'RUNNING_MODAL'}

	def execute(self,ctx):
		self.report({'INFO'},'bpy.ops.mesh.target_weld()')
		return{"FINISHED"}

	def invoke(self, ctx, event):
		if ctx.space_data.type == 'VIEW_3D':
			self.handle = register_line(ctx, self, '2d', (1, 0.5, 0.5, 1))
			ctx.window_manager.modal_handler_add(self)
			return {'RUNNING_MODAL'}
		return {'CANCELLED'}

def register_weld():
	bpy.utils.register_class(Mesh_OT_Target_Weld)

def unregister_weld():
	bpy.utils.unregister_class(Mesh_OT_Target_Weld)

if __name__ == "__main__":
	register_weld()