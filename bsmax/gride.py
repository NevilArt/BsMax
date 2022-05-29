############################################################################
#	This program is free software: you can redistribute it and/or modify
#	it under the terms of the GNU General Public License as published by
#	the Free Software Foundation, either version 3 of the License, or
#	(at your option) any later version.
#
#	This program is distributed in the hope that it will be useful,
#	but WITHOUT ANY WARRANTY without even the implied warranty of
#	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#	GNU General Public License for more details.
#
#	You should have received a copy of the GNU General Public License
#	along with this program.  If not, see <https://www.gnu.org/licenses/>.
############################################################################

import bpy
import gpu

from bgl import glEnable, GL_BLEND, glDisable, glLineWidth
from gpu_extras.batch import batch_for_shader
from mathutils import Vector

from bsmax.bsmatrix import BsMatrix, transform_point_to_matrix



class Local_Gride:
	def __init__(self):
		self.size = 1
		self.segments = 1
		self.gride_color = (0.5, 0.5, 0.5, 1)
		self.border_color = (0.75, 0.75, 0.75, 1)
		self.cross_x_color = (0.75, 0, 0, 1)
		self.cross_y_color = (0, 0.75, 0, 1)
		self.gride = []
		self.border = []
		self.cross = []
		self.border_on = False
		self.cross_on = False
		self.matrix = BsMatrix()
		self.handler = None
	
	def set(self, size, segments, matrix=None):
		self.size = size
		self.segments = segments
		if matrix:
			self.matrix.from_matrix(matrix)
	
	def genarate_gride_lines(self):
		self.gride.clear()
		self.border.clear()
		self.cross.clear()

		step = self.size / self.segments
		start, end = -self.size / 2, self.size / 2
		for i in range(self.segments + 1):
			p = i * step + start
			# Genarate and transform grid line points
			points = [
						Vector((p, start, 0)),
						Vector((p, end, 0)),
						Vector((start, p, 0)),
						Vector((end, p, 0))
			]
			self.gride += transform_point_to_matrix(points, self.matrix)

		# genarate borde lines if asked
		if self.border_on:
			self.border = [
							Vector((start, start, 0)),
							Vector((end, start, 0)),
							Vector((end, end, 0)),
							Vector((start, end, 0)),
							Vector((start, start, 0))
			]
			self.border = transform_point_to_matrix(self.border, self.matrix)

		# genarate cross lines if asked
		if self.cross_on:
			self.cross = [
							# X axis line
							Vector((start, 0, 0)),
							Vector((end, 0, 0)),
							# Y axis line
							Vector((0, start, 0)),
							Vector((0, end, 0))
			]
			self.cross = transform_point_to_matrix(self.cross, self.matrix)

	def draw_shader(self, shader, coords, mode, color):
		batch = batch_for_shader(shader, mode, {'pos': coords})
		shader.bind()
		shader.uniform_float('color', color)
		batch.draw(shader)
	
	
	def draw(self):
		glEnable(GL_BLEND)
		glLineWidth(1)
		shader = gpu.shader.from_builtin('3D_UNIFORM_COLOR')

		# draw gride
		self.draw_shader(shader, self.gride, 'LINES', self.gride_color)
		
		# draw border
		if self.border:
			self.draw_shader(shader, self.border,
							'LINE_STRIP', self.border_color)

		# draw closs
		if self.cross:
			self.draw_shader(shader, self.cross[0:2],
							'LINES', self.cross_x_color)

			self.draw_shader(shader, self.cross[2:4],
							'LINES', self.cross_y_color)

		glDisable(GL_BLEND)

	def register(self, ctx):
		space = ctx.area.spaces.active
		self.handler = space.draw_handler_add(self.draw, (), 'WINDOW', 'POST_VIEW')

	def unregister(self):
		if self.handler:
			bpy.types.SpaceView3D.draw_handler_remove(self.handler, 'WINDOW')
		self.handler = None



# """ test """"
# class View3D_OT_Local_Gride(bpy.types.Operator):
# 	bl_idname = "view3d.local_gride"
# 	bl_label = "local gride"

# 	local_gride = Local_Gride()

# 	@classmethod
# 	def poll(self, ctx):
# 		return ctx.area.type == 'VIEW_3D'

# 	def execute(self, ctx):
# 		if ctx.object:
# 			matrix = ctx.object.matrix_world.copy()
# 			self.local_gride.set(1, 10, matrix)

# 		self.local_gride.border_on = True
# 		self.local_gride.cross_on = True

# 		self.local_gride.genarate_gride_lines()
# 		self.local_gride.register(ctx)

# 		return{"FINISHED"}


# if __name__ == "__main__":
# 	bpy.utils.register_class(View3D_OT_Local_Gride)