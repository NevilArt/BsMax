
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
import gpu

from bgl import glEnable, GL_BLEND, glDisable, glLineWidth
from gpu_extras.batch import batch_for_shader
from bpy_extras.view3d_utils import location_3d_to_region_2d
from bpy.app import version



def get_uniform_color(mode="2D"):
	if version < (3, 6, 0):
		if mode == "2D":
			return "2D_UNIFORM_COLOR"
		else:
			return "3D_UNIFORM_COLOR"
	return "UNIFORM_COLOR"



def get_screen_pos(ctx,coord):
	region = ctx.region
	rv3d = ctx.space_data.region_3d
	return location_3d_to_region_2d(region, rv3d, coord, default=None)



def draw_line(self, mode, color):
	glEnable(GL_BLEND)
	coords = [self.start, self.end]
	shader = gpu.shader.from_builtin(mode)
	batch = batch_for_shader(shader, 'LINE_STRIP', {'pos': coords})
	shader.bind()
	shader.uniform_float('color', color)
	batch.draw(shader)
	glDisable(GL_BLEND)



def register_line(ctx, self, mode, color):
	""" owner most have to 'start' and 'end' point values """
	""" self.start self.end """
	space = ctx.area.spaces.active
	if mode == '2d':
		return space.draw_handler_add(
				draw_line,
				tuple([self, get_uniform_color(mode="2D"), color]),
				'WINDOW',
				'POST_PIXEL'
			)
	
	if mode == '3d':
		return space.draw_handler_add(
			draw_line,
			tuple([self, get_uniform_color(mode="3D"), color]),
			'WINDOW',
			'POST_VIEW'
		)



def unregister_line(handle):
	if handle:
		bpy.types.SpaceView3D.draw_handler_remove(handle, 'WINDOW')



class Rubber_Band:
	def __init__(self):
		self.start = (0, 0, 0)
		self.end = (0, 0, 0)
		self.segment = 10
		self.size = 2
		self.draw_handler = None
		self.vertices = []
		self.colors = []
		self.color_a = (0.0, 0.5, 0.5, 1.0)
		self.color_b = (0.2, 0.0, 0.0, 1.0)
		self.shader = gpu.shader.from_builtin(get_uniform_color(mode="2D"))
		
	def create(self, sx, sy, ex, ey):
		self.vertices.clear()
		self.colors.clear()
		self.vertices.append((sx, sy))
		self.vertices.append((ex, ey))
		self.colors.append(self.color_a)
		self.colors.append(self.color_b)
	
	def draw_rubber(self):
		glEnable(GL_BLEND)
		glLineWidth(self.size)

		if len(self.vertices) == 2:
			coords = [self.vertices[0], self.vertices[1]]
			batch = batch_for_shader(self.shader, 'LINE_STRIP', {"pos": coords})

			self.shader.bind()
			self.shader.uniform_float("color", self.color_a)
			
			batch.draw(self.shader)
			glDisable(GL_BLEND)
	
	def register(self):
		SpaceView3D = bpy.types.SpaceView3D
		self.draw_handler = SpaceView3D.draw_handler_add(self.draw_rubber, (),
														'WINDOW', 'POST_PIXEL')
	
	def unregister(self):
		if self.draw_handler:
			bpy.types.SpaceView3D.draw_handler_remove(self.draw_handler, 'WINDOW')
		self.draw_handler = None