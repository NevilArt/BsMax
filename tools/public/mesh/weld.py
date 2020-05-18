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

import bpy, bgl, gpu
from gpu_extras.batch import batch_for_shader

# TARGET WELD
# Original Coded from Stromberg90 updated by Nevil
# https://github.com/Stromberg90/Scripts/tree/master/Blender

def draw_callback_px(self):
	if self.srt_vert != None:
		bgl.glEnable(bgl.GL_BLEND)
		coords = [self.srt_vert, self.end_vert]
		shader = gpu.shader.from_builtin('2D_UNIFORM_COLOR')
		batch = batch_for_shader(shader, 'LINE_STRIP', {"pos": coords})
		shader.bind()
		shader.uniform_float("color", (1, 0.5, 0.5, 1))
		batch.draw(shader)
	bgl.glDisable(bgl.GL_BLEND)


def SelectVert(ctx, event, started):
	coord = event.mouse_region_x, event.mouse_region_y
	if started:
		result = bpy.ops.view3d.select(extend=True,location=coord)
	else:
		result = bpy.ops.view3d.select(extend=False,location=coord)
	if result == {'PASS_THROUGH'}:
		bpy.ops.mesh.select_all(action='DESELECT')


class BsMax_OT_TargetWeldToggle(bpy.types.Operator):
	bl_idname = "bsmax.targetweld"
	bl_label = "Target Weld"
	bl_options = {'REGISTER', 'UNDO'}
	srt_vert = end_vert = None
	_handle = None
	drag = False
	picked = False

	def modal(self, ctx, event):
		ctx.area.tag_redraw()
		if event.type in {'MIDDLEMOUSE','WHEELUPMOUSE','WHEELDOWNMOUSE'}:
			return {'PASS_THROUGH'}

		elif event.type == 'MOUSEMOVE':
			if self.srt_vert != None:
				self.end_vert = event.mouse_region_x, event.mouse_region_y

		elif event.type == 'LEFTMOUSE':
			if event.value == 'PRESS':
				if self.srt_vert == None:
					self.srt_vert = event.mouse_region_x, event.mouse_region_y
					coord = event.mouse_region_x, event.mouse_region_y
					bpy.ops.view3d.select(extend = False, location = coord)

			if event.value =='RELEASE':
				self.end_vert = event.mouse_region_x, event.mouse_region_y

				if self.srt_vert != None:
					coord = event.mouse_region_x, event.mouse_region_y
					bpy.ops.view3d.select(extend=True,location=coord)

				SelectVert(ctx, event, self.srt_vert != None)
				if ctx.object.data.total_vert_sel == 2:
					self.srt_vert = self.end_vert = None
					bpy.ops.mesh.merge(type='LAST')
					bpy.ops.mesh.select_all(action='DESELECT')

			return {'RUNNING_MODAL'}
		elif event.type in {'RIGHTMOUSE','ESC'}:
			bpy.types.SpaceView3D.draw_handler_remove(self._handle,'WINDOW')
			return {'CANCELLED'}

		return {'RUNNING_MODAL'}

	def invoke(self, ctx, event):
		if ctx.space_data.type == 'VIEW_3D':
			sv3d = bpy.types.SpaceView3D
			self._handle = sv3d.draw_handler_add(draw_callback_px, tuple([self]),
													'WINDOW','POST_PIXEL')
			ctx.window_manager.modal_handler_add(self)
			return {'RUNNING_MODAL'}
		return {'CANCELLED'}

def register_weld():
	bpy.utils.register_class(BsMax_OT_TargetWeldToggle)

def unregister_weld():
	bpy.utils.unregister_class(BsMax_OT_TargetWeldToggle)