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
# 2024/04/04

import bpy

from mathutils import Vector
from bpy.props import EnumProperty

from primitive.primitive import Draw_Primitive, Primitive_Public_Class


class Metaball(Primitive_Public_Class):
	def init(self):
		self.finishon = 3
		self.owner = None

	def create(self, ctx, metaball_type):
		bpy.ops.object.metaball_add(type=metaball_type)
		self.owner = ctx.active_object


class Create_OT_Metaball(Draw_Primitive):
	bl_idname="create.metaball"
	bl_label="Metaball"
	subclass = Metaball()

	metaball_type: EnumProperty(
		name='Type',
		items =[
			('BALL','Ball',''),
			('CAPSULE','Capsule',''),
			('PLANE','Plane',''),
			('ELLIPSOID','Ellipsoid',''),
			('CUBE','Cube','')
		],
		default='BALL'
	)

	radius = 0
	location = Vector((0,0,0))

	def create(self, ctx):
		if self.metaball_type == 'BALL':
			self.subclass.finishon = 2
		elif self.metaball_type == 'ELLIPSOID':
			self.subclass.finishon = 3
		elif self.metaball_type == 'CUBE':
			self.subclass.finishon = 4

		self.subclass.create(ctx, self.metaball_type)
		
		self.subclass.owner.location = self.gride.location
		self.subclass.owner.rotation_euler = self.gride.rotation
		
		owner = self.subclass.owner
		owner.data.elements[0].radius = 0
		owner.data.elements[0].size_x = 0
		owner.data.elements[0].size_y = 0
		owner.data.elements[0].size_z = 0

	def update(self, ctx, clickcount, dimension):
		data = self.subclass.owner.data
		if self.metaball_type == 'BALL':
			if clickcount == 1:
				data.elements[0].radius = dimension.radius

		elif self.metaball_type == 'CAPSULE':
			if clickcount == 1:
				data.elements[0].radius = dimension.radius
				data.elements[0].size_x = 0
			elif clickcount == 2:
				radius = dimension.distance - data.elements[0].radius
				data.elements[0].size_x = radius

		elif self.metaball_type == 'PLANE':
			if clickcount == 1:
				self.radius = dimension.radius / 10
				data.elements[0].radius = self.radius
				data.elements[0].size_x = abs(dimension.width) / 2
				data.elements[0].size_y = abs(dimension.length) / 2
				self.subclass.owner.location = dimension.center
			elif clickcount == 2:
				data.elements[0].radius = self.radius #+ dimension.height_np

		elif self.metaball_type == 'ELLIPSOID':
			if clickcount == 1:
				data.elements[0].radius = 2
				data.elements[0].size_x = abs(dimension.width)
				data.elements[0].size_y = abs(dimension.length)
				self.radius = dimension.radius / 2
				data.elements[0].size_z = self.radius
			elif clickcount == 2:
				data.elements[0].size_z = self.radius #+ dimension.height_np

		elif self.metaball_type == 'CUBE':
			if clickcount == 1:
				data.elements[0].radius = 1
				data.elements[0].size_x = abs(dimension.width) / 2
				data.elements[0].size_y = abs(dimension.length) / 2
				data.elements[0].size_z = 0.1
				self.location = self.subclass.owner.location = dimension.center

			elif clickcount == 2:
				height = dimension.height / 2
				data.elements[0].size_z = height
				self.subclass.owner.location = self.location #+ offset

			elif clickcount == 3:
				data.elements[0].radius = 0.01 + dimension.radius
		#TODO adapt resolation by size
		#self.subclass.data.resolution = 1.33


def register_metaball():
	bpy.utils.register_class(Create_OT_Metaball)


def unregister_metaball():
	bpy.utils.unregister_class(Create_OT_Metaball)


if __name__ == '__main__':
	register_metaball()