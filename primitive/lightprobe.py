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
# 2024/04/20

import bpy

from mathutils import Vector
from bpy.utils import register_class, unregister_class

from primitive.primitive import Draw_Primitive, Primitive_Public_Class
from bsmax.bsmatrix import transform_point_to_matrix


class LightProbe(Primitive_Public_Class):
	def init(self):
		self.finishon = 2
		self.owner = None
		self.data = None


class Create_OT_Light_Probe_Grid(Draw_Primitive):
	bl_idname='create.light_probe_grid'
	bl_label="Irradiance Volume"
	subclass = LightProbe()
	width, length, height, distance = 0, 0, 0, 0
	location = Vector((0, 0, 0))

	def create(self, ctx):
		self.subclass.finishon = 4
		bpy.ops.object.lightprobe_add(
			type='GRID', location=self.gride.location
		)
		
		self.subclass.owner = ctx.active_object
		self.subclass.owner.scale = (0, 0, 0)
		self.subclass.owner.rotation_euler = self.gride.rotation

	def update(self, ctx, clickcount, dimension):
		if clickcount == 1:
			self.width = dimension.width / 2
			self.length = dimension.length / 2
			self.location = self.subclass.owner.location = dimension.center

		if clickcount == 2:
			self.height = dimension.height / 2

			# height correction
			offset = Vector((self.width, self.length, self.height))
			location = transform_point_to_matrix(offset, self.gride.gride_matrix)
			self.subclass.owner.location = location

		if clickcount == 3:
			scale = 1 / max(abs(self.width), abs(self.length), self.height)
			self.distance = dimension.height * scale

		if clickcount > 0:
			self.subclass.owner.scale = (abs(self.width), abs(self.length),
										self.height)
			self.subclass.owner.data.influence_distance = self.distance

	def finish(self):
		self.width, self.length, self.height, self.distance = 0, 0, 0, 0


class Create_OT_Light_Probe_Planer(Draw_Primitive):
	bl_idname='create.light_probe_planer'
	bl_label="Reflection Plane"
	subclass = LightProbe()
	width, length, distance = 0, 0, 0

	def create(self, ctx):
		self.subclass.finishon = 3
		bpy.ops.object.lightprobe_add(type='PLANAR', location=self.gride.location)
		self.subclass.owner = ctx.active_object
		self.subclass.owner.scale = (0, 0, 0)
		self.subclass.owner.rotation_euler = self.gride.rotation

	def update(self, ctx, clickcount, dimension):
		if clickcount == 1:
			self.width = abs(dimension.width)
			self.length = abs(dimension.length)

		if clickcount == 2:
			self.distance = dimension.height

		if clickcount > 0:
			self.subclass.owner.scale = (self.width, self.length, 1)
			self.subclass.owner.data.influence_distance = self.distance


class Create_OT_Light_Probe_Cubemap(Draw_Primitive):
	bl_idname = 'create.light_probe_cubemap'
	bl_label = "Reflection Cubemap"
	subclass = LightProbe()

	def create(self, ctx):
		bpy.ops.object.lightprobe_add(type='CUBEMAP', location=self.gride.location)
		self.subclass.owner = ctx.active_object
		self.subclass.owner.scale = (0, 0, 0)
		self.subclass.owner.rotation_euler = self.gride.rotation

	def update(self, ctx, clickcount, dimension):
		if clickcount == 1:
			self.subclass.owner.data.influence_distance = dimension.radius
			self.subclass.owner.scale = (1, 1, 1)


classes = {
	Create_OT_Light_Probe_Grid,
	Create_OT_Light_Probe_Planer,
	Create_OT_Light_Probe_Cubemap
}


def register_lightprobe():
	for c in classes:
		register_class(c)


def unregister_lightprobe():
	for c in classes:
		unregister_class(c)


if __name__ == '__main__':
	register_lightprobe()