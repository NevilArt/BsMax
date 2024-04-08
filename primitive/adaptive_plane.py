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

import bpy
from primitive.primitive import Primitive_Geometry_Class, Draw_Primitive



def get_plane_mesh(width, length):
	# Create vertexes
	w, l = width * 0.5, length * 0.5
	verts = [(-w, -l, 0), (-w, l, 0),
		(w, -l, 0), (w, l, 0)]
	# create faces
	faces = [(0, 1, 2, 3)]
	return verts, [], faces



def get_camera_info():
	# get active camera
	camera = bpy.context.scene.camera
	if not camera:
		return None
	render = bpy.context.scene.render

	aspect_ratio = render.resolution_x / render.resolution_y
	angle = camera.data.angle
	clip_start = camera.data.clip_start
	clip_end = camera.data.clip_end
	euler_angels = camera.matrix_world.to_euler()
	location = camera.matrix_world.to_translation()

	# create view cage
	# create view surface



def get_adaptive_plane_mesh(width, length, camera, min, max, steps):

	if not camera:
		return get_plane_mesh(width, length)

	verts, faces = [], []

	# Create Bound
	min_x, max_x = -width/2, width/2
	min_y, max_y = -length/2, length/2

	return verts, [], faces



class Adaptive_Plane(Primitive_Geometry_Class):
	def __init__(self):
		self.classname = "Adaptive_Plane"
		self.finishon = 2
		self.drawing = True

	def create(self, ctx):
		mesh = get_plane_mesh(0, 0)
		self.create_mesh(ctx, mesh, self.classname)
		pd = self.data.primitivedata
		pd.classname = self.classname

	def update(self):
		pd = self.data.primitivedata
		if self.drawing:
			mesh = get_plane_mesh(pd.width, pd.length)
		else:
			mesh = get_adaptive_plane_mesh(pd.width, pd.length, pd.thickness, pd.bias)
		self.update_mesh(mesh)


class Create_OT_Adaptive_Plane(Draw_Primitive):
	bl_idname = "create.adaptive_plane"
	bl_label = "Camera Plane"
	subclass = Adaptive_Plane()
	use_gride = True

	def create(self, ctx):
		self.subclass.create(ctx)
		self.params = self.subclass.owner.data.primitivedata
		self.subclass.owner.location = self.gride.location
		self.subclass.owner.rotation_euler = self.gride.rotation

	def update(self, ctx, clickcount, dimension):
		if clickcount == 1:
			if self.ctrl:
				self.params.width = dimension.radius
				self.params.length = dimension.radius
			else:
				self.params.width = abs(dimension.width)
				self.params.length = abs(dimension.length)
				self.subclass.owner.location = dimension.center
		if clickcount > 0:
			self.subclass.update()



def register_adaptive_plane():
	bpy.utils.register_class(Create_OT_Adaptive_Plane)

def unregister_adaptive_plane():
	bpy.utils.unregister_class(Create_OT_Adaptive_Plane)

if __name__ == '__main__':
	register_adaptive_plane()