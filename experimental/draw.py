############################################################################
#	This program is free software: you can redistribute it and/or modify
#	it under the terms of the GNU General Public License as published by
#	the Free Software Foundation,either version 3 of the License,or
#	(at your option) any later version.
#
#	This program is distributed in the hope that it will be useful,
#	but WITHOUT ANY WARRANTY; without even the implied warranty of
#	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#	GNU General Public License for more details.
#
#	You should have received a copy of the GNU General Public License
#	along with this program.  If not,see <https://www.gnu.org/licenses/>.
############################################################################
# 2024/03/16

import bpy
import gpu

from mathutils import Vector

from bpy.types import Operator
from gpu_extras.batch import batch_for_shader
from bpy_extras.view3d_utils import location_3d_to_region_2d
from bpy.app import version


def get_uniform_color(mode="2D"):
	if version < (3, 6, 0):
		if mode == "2D":
			return "2D_UNIFORM_COLOR"
		return "3D_UNIFORM_COLOR"
	return "UNIFORM_COLOR"


def create_gizmo(sx, sy, sz, ex, ey, ez):
	# Box
	vertices = (
		Vector((sx, sy, sz)), Vector((ex, sy, sz)),
		Vector((ex, sy, sz)), Vector((ex, ey, sz)),
		Vector((ex, ey, sz)), Vector((sx, ey, sz)),
		Vector((sx, ey, sz)), Vector((sx, sy, sz)),
		Vector((sx, sy, sz)), Vector((sx, sy, ez)),
		Vector((ex, sy, sz)), Vector((ex, sy, ez)),
		Vector((ex, ey, sz)), Vector((ex, ey, ez)),
		Vector((sx, ey, sz)), Vector((sx, ey, ez)),
		Vector((sx, sy, ez)), Vector((ex, sy, ez)),
		Vector((ex, sy, ez)), Vector((ex, ey, ez)),
		Vector((ex, ey, ez)), Vector((sx, ey, ez)),
		Vector((sx, ey, ez)), Vector((sx, sy, ez)) 
	)
	# Sphere
	# Cylinder
	return vertices


class Gizmo:
	def __init__(self):
		self.start = Vector((0, 0, 0))
		self.end = Vector((0, 0, 0))
		self.segment = 10
		self.size = 2
		self.draw_handler = None
		self.vertices = []
		self.color = (1, 1, 0, 1)
		self.shader = gpu.shader.from_builtin("UNIFORM_COLOR")

	def draw_gizmo(self):
		sx, sy, sz = self.start
		ex, ey, ez = self.end
		coords = create_gizmo(sx, sy, sz, ex, ey, ez)
		batch = batch_for_shader(self.shader, 'LINES', {'pos': coords})
		self.shader.bind()
		self.shader.uniform_float('color', self.color)
		batch.draw(self.shader)
	
	def register(self):
		SpaceView3D = bpy.types.SpaceView3D
		self.draw_handler = SpaceView3D.draw_handler_add(
			self.draw_gizmo, (), 'WINDOW', 'POST_VIEW'
		)
	
	def unregister(self):
		if self.draw_handler:
			bpy.types.SpaceView3D.draw_handler_remove(self.draw_handler, 'WINDOW')
		self.draw_handler = None


class Draw3DObject(Operator):
    bl_options = {'REGISTER','UNDO'}


class Drow_OT_Box(Draw3DObject):
	bl_idname = "test.draw"
	bl_label = "Draw Test"
	bl_options = {'REGISTER', 'UNDO'}

	start, end, handle = None, None, None
	drag, picked = False, False
	
	gizmo = Gizmo()

	@classmethod
	def poll(self, ctx):
		return ctx.area.type == 'VIEW_3D'
	
	def modal(self, ctx, event):
		ctx.area.tag_redraw()
		if not event.type in {'LEFTMOUSE','RIGHTMOUSE', 'MOUSEMOVE','ESC'}:
			return {'PASS_THROUGH'}

		elif event.type == 'MOUSEMOVE':
			if self.start != None:
				self.end = event.mouse_region_x, event.mouse_region_y
			self.gizmo.draw_gizmo()

		elif event.type == 'LEFTMOUSE':
			if event.value == 'PRESS':
				if self.start == None:
					# self.start = event.mouse_region_x, event.mouse_region_y
					self.gizmo.start = Vector((50, 50, 50))
					self.gizmo.end = Vector((100, 100, 100))
					# print(">>>>> Created")


			if event.value =='RELEASE':
				self.end = event.mouse_region_x, event.mouse_region_y

		
		elif event.type in {'RIGHTMOUSE','ESC'}:
			self.gizmo.unregister()
			return {'CANCELLED'}

		return {'RUNNING_MODAL'}
	
	def execute(self,ctx):
		return{"FINISHED"}

	def invoke(self, ctx, event):
		self.gizmo.register()
		ctx.window_manager.modal_handler_add(self)
		return {'RUNNING_MODAL'}


def register_draw():
	bpy.utils.register_class(Drow_OT_Box)


def unregister_draw():
	bpy.utils.unregister_class(Drow_OT_Box)

if __name__ == "__main__":
	register_draw()

