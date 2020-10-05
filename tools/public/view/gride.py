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
import bpy, gpu, bgl
from gpu_extras.batch import batch_for_shader

class View3D_Gride:
	def __init__(self):
		self.count = 10
		self.size = 0.1
		self.draw_handler = None
		self.vertices = []
		self.colors = []
		self.color_x = (0.0, 0.2, 0.0, 1.0)
		self.color_y = (0.2, 0.0, 0.0, 1.0)
		self.color_g = (0.5, 0.5, 0.5, 0.5)
		self.shader = gpu.shader.from_builtin('3D_SMOOTH_COLOR') # 3D_UNIFORM_COLOR
		self.enabled = False
		self.create()
		self.batch = batch_for_shader(self.shader, 'LINES', {"pos": self.vertices, "color": self.colors})
	
	def create(self):
		e = self.count*self.size
		s = -e
		for x in range(-self.count,self.count+1):
			px = x*self.size
			self.vertices.append((px,s,0))
			self.vertices.append((px,e,0))
			if px == 0 :
				self.colors.append(self.color_x)
				self.colors.append(self.color_x)
			else:
				self.colors.append(self.color_g)
				self.colors.append(self.color_g)
		for y in range(-self.count,self.count+1):
			py = y*self.size
			self.vertices.append((s,py,0))
			self.vertices.append((e,py,0))
			if py == 0:
				self.colors.append(self.color_y)
				self.colors.append(self.color_y)
			else:
				self.colors.append(self.color_g)
				self.colors.append(self.color_g)
	
	def draw(self):
		bgl.glEnable(bgl.GL_BLEND)
		bgl.glLineWidth(1)
		self.shader.bind()
		self.batch.draw(self.shader)
		# bgl.glDisable(bgl.GL_BLEND)
	
	def register(self):
		self.draw_handler = bpy.types.SpaceView3D.draw_handler_add(self.draw, (), 'WINDOW', 'POST_VIEW')
		self.enabled =  True

	def unregister(self):
		if self.draw_handler != None:
			bpy.types.SpaceView3D.draw_handler_remove(self.draw_handler,'WINDOW')
			self.draw_handler = None
			self.enabled =  False
	
class View3D_OT_Show_Hide_Gride(bpy.types.Operator):
	bl_idname = "view3d.show_hide_gride"
	bl_label = "Show Hide Gride"

	view_gride = View3D_Gride()
	state = 0

	@classmethod
	def poll(self, ctx):
		return ctx.area.type == 'VIEW_3D'

	def blender_gride(self, ctx, state):
		overlay = ctx.space_data.overlay
		overlay.show_floor = state
		overlay.show_axis_x = state
		overlay.show_axis_y = state
		overlay.show_axis_z = False
	
	def max_gride(self, ctx, stata):
		if stata:
			self.view_gride.register()
		else:
			self.view_gride.unregister()

	def execute(self, ctx):
		bg,mg = ctx.space_data.overlay.show_floor, self.view_gride.enabled
		if bg and not mg:
			self.blender_gride(ctx, False)
			self.max_gride(ctx, True)

		elif not bg and mg:
			self.blender_gride(ctx, False)
			self.max_gride(ctx, False)

		else:
			self.blender_gride(ctx, True)
			self.max_gride(ctx, False)

		self.report({'INFO'},'bpy.ops.view3d.show_hide_gride()')
		return{"FINISHED"}

def register_gride():
	bpy.utils.register_class(View3D_OT_Show_Hide_Gride)

def unregister_gride():
	bpy.utils.unregister_class(View3D_OT_Show_Hide_Gride)

if __name__ == "__main__":
	register_gride()