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
from mathutils import Vector
from primitive.primitive import CreatePrimitive
from bsmax.actions import delete_objects
from bsmax.math import get_offset_by_orient

class LightProbe:
	def __init__(self):
		self.finishon = 2
		self.owner = None
		self.data = None
	def reset(self):
		self.__init__()
	def abort(self):
		delete_objects([self.owner])

class Create_OT_Light_Probe_Grid(CreatePrimitive):
	bl_idname="create.light_probe_grid"
	bl_label="Irradiance Volume"
	subclass = LightProbe()
	width,length,height,distance = 0,0,0,0
	location = Vector((0,0,0))

	def create(self, ctx, clickpoint):
		self.subclass.finishon = 4
		bpy.ops.object.lightprobe_add(type='GRID', location=clickpoint.view)
		self.subclass.owner = ctx.active_object
		self.subclass.owner.scale = (0,0,0)
		self.subclass.owner.rotation_euler = clickpoint.orient
	def update(self, ctx, clickcount, dimantion):
		if clickcount == 1:
			self.width = dimantion.width / 2
			self.length = dimantion.length / 2
			self.location = self.subclass.owner.location = dimantion.center
		if clickcount == 2:
			self.height = dimantion.height / 2
			offset = get_offset_by_orient(Vector((0,0,dimantion.height / 2)), dimantion.view_name)
			self.subclass.owner.location = self.location + offset
		if clickcount == 3:
			scale = 1 / max(self.width, self.length, self.height)
			self.distance = dimantion.height * scale
		if clickcount > 0:
			self.subclass.owner.scale = (self.width, self.length, self.height)
			self.subclass.owner.data.influence_distance = self.distance
	def finish(self):
		self.width,self.length,self.height,self.distance = 0,0,0,0

class Create_OT_Light_Probe_Planer(CreatePrimitive):
	bl_idname="create.light_probe_planer"
	bl_label="Reflection Plane"
	subclass = LightProbe()
	width,length,distance = 0,0,0

	def create(self, ctx, clickpoint):
		self.subclass.finishon = 3
		bpy.ops.object.lightprobe_add(type='PLANAR', location=clickpoint.view)
		self.subclass.owner = ctx.active_object
		self.subclass.owner.scale = (0,0,0)
		self.subclass.owner.rotation_euler = clickpoint.orient
	def update(self, ctx, clickcount, dimantion):
		if clickcount == 1:
			self.width = dimantion.width
			self.length = dimantion.length
		if clickcount == 2:
			self.distance = dimantion.height
		if clickcount > 0:
			self.subclass.owner.scale = (self.width, self.length, 1)
			self.subclass.owner.data.influence_distance = self.distance
	def finish(self):
		pass

class Create_OT_Light_Probe_Cubemap(CreatePrimitive):
	bl_idname = "create.light_probe_cubemap"
	bl_label = "Reflection Cubemap"
	subclass = LightProbe()

	def create(self, ctx, clickpoint):
		bpy.ops.object.lightprobe_add(type='CUBEMAP', location=clickpoint.view)
		self.subclass.owner = ctx.active_object
		self.subclass.owner.scale = (0,0,0)
		self.subclass.owner.rotation_euler = clickpoint.orient
	def update(self, ctx, clickcount, dimantion):
		if clickcount == 1:
			self.subclass.owner.data.influence_distance = dimantion.radius
			self.subclass.owner.scale = (1,1,1)
	def finish(self):
		pass

classes = [Create_OT_Light_Probe_Grid,
			Create_OT_Light_Probe_Planer,
			Create_OT_Light_Probe_Cubemap]

def register_lightprobe():
	[bpy.utils.register_class(c) for c in classes]

def unregister_lightprobe():
	[bpy.utils.unregister_class(c) for c in classes]