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
from bpy.props import BoolProperty
from math import pi, sin, cos
from primitive.primitive import (Draw_Primitive,
	Primitive_Curve_Class, Primitive_Public_Class)
from bsmax.actions import set_create_target



def get_compass_shape(radius):
	r = radius
	verts = [(0,r,0),(0.1*r,0.2*r,0),(0.3*r,0.3*r,0),(0.2*r,0.1*r,0),
			(r,0,0),(0.2*r,-0.1*r,0),(0.3*r,-0.3*r,0),(0.1*r,-0.2*r,0),
			(0,-1*r,0),(-0.1*r,-0.2*r,0),(-0.3*r,-0.3*r,0),(-0.2*r,-0.1*r,0),
			(-1.0*r,0,0),(-0.2*r,0.1*r,0),(-0.3*r,0.3*r,0),(-0.1*r,0.2*r,0)]
	shape = [(v,v,'FREE',v,'FREE') for v in verts]
	return [shape]



class Light(Primitive_Public_Class):
	def init(self):
		self.finishon = 2
		self.owner = None
		self.target = None

	def create(self, ctx, datatype):
		name = datatype.capitalize()
		newdata = bpy.data.lights.new(name=name, type=datatype)
		newlight = bpy.data.objects.new(name=name, object_data=newdata)
		ctx.collection.objects.link(newlight)
		ctx.view_layer.objects.active = newlight
		newlight.select_set(True)
		self.owner = newlight

	def abort(self):
		bpy.ops.object.delete({'selected_objects': [self.owner, self.target]})



class Compass(Primitive_Curve_Class):
	def __init__(self):
		self.classname = "Compass"
		self.finishon = 3
		self.owner = None
		self.data = None
		self.close = True

	def create(self, ctx):
		shapes = get_compass_shape(0)
		self.create_curve(ctx, shapes, self.classname)
		pd = self.data.primitivedata
		pd.classname = self.classname

	def update(self):
		pd = self.data.primitivedata
		shapes = get_compass_shape(pd.radius1)
		self.update_curve(shapes)

	def abort(self):
		bpy.ops.object.delete({'selected_objects': [self.owner]})



class Create_OT_PointLight(Draw_Primitive):
	bl_idname="create.pointlight"
	bl_label="Point Light"
	subclass = Light()
	use_single_click = True

	def create(self, ctx):
		self.subclass.create(ctx, 'POINT')
		self.subclass.owner.location = self.gride.location
		self.subclass.owner.rotation_euler = self.gride.rotation

	def update(self, ctx, clickcount, dimension):
		if self.drag:
			self.subclass.owner.location = dimension.end



class Create_OT_SpotLight(Draw_Primitive):
	bl_idname="create.spotlight"
	bl_label="Spot Light (Create)"
	subclass = Light()
	use_single_click = True
	subclass.finishon = 2

	def create(self, ctx):
		self.subclass.create(ctx, 'SPOT')
		self.subclass.owner.location = self.gride.location
		self.subclass.owner.rotation_euler = self.gride.rotation

	def update(self, ctx, clickcount, dimension):
		if clickcount == 1:
			if self.drag and self.subclass.target == None:
				self.subclass.target = set_create_target(self.subclass.owner, None)

			if self.subclass.target != None:
				self.subclass.target.location = dimension.end




class Create_OT_SunLight(Draw_Primitive):
	bl_idname="create.sunlight"
	bl_label="Sun Light"
	subclass = Compass()
	light = Light()
	use_single_click = True
	use_gride = True
	distance = 0
	context = None

	def create(self, ctx):
		self.subclass.finishon = 3
		self.context = ctx
		self.subclass.create(ctx)
		self.subclass.owner.location = self.gride.location
		self.light.create(ctx, "SUN")
		self.light.owner.location = self.gride.location
		self.light.target = self.subclass.owner
		self.params = self.subclass.owner.data.primitivedata
		set_create_target(self.light.owner, self.subclass.owner, distance=(0,0,0))
	
	def update(self, ctx, clickcount, dimension):
		if clickcount == 1:
			self.params.radius1 = dimension.radius
			self.subclass.update()

		if clickcount == 2:
			self.distance = dimension.height
			self.light.owner.location.z = self.distance
			if self.params.radius1 == 0:
				self.step = 4

		if clickcount == 3:
			if self.distance > 0:
				# TODO create a better way to caculate angle
				# store angle in prim data
				dx = abs(dimension.width)
				dy = abs(dimension.length)
				delta = dx if abs(dx) > abs(dy) else dy
				delta = delta if delta < self.distance else self.distance
				delta = delta if delta > -self.distance else -self.distance
				teta = (-pi/2)*(delta/self.distance)
				x = sin(teta) * self.distance
				z = cos(teta) * self.distance
				self.light.owner.location.x = self.light.target.location.x + x
				self.light.owner.location.z = self.light.target.location.z + z

	def finish(self):
		if self.params.radius1 == 0:
			for constraint in self.light.owner.constraints:
				self.light.owner.constraints.remove(constraint)
			bpy.ops.object.delete({'selected_objects': [self.subclass.owner]})



class Create_OT_AreaLight(Draw_Primitive):
	bl_idname="create.arealight"
	bl_label="Area Light"
	subclass = Light()
	free: BoolProperty(name="Free", default=False)

	def create(self, ctx):
		self.subclass.create(ctx, 'AREA')
		self.subclass.owner.location = self.gride.location
		self.subclass.owner.rotation_euler = self.gride.rotation
		self.subclass.finishon = 2 if self.free else 3

	def update(self, ctx, clickcount, dimension):
		if clickcount == 1:
			width = abs(dimension.width)
			length = abs(dimension.length)
			self.subclass.owner.data.size = max(width, length)
			if max(width, length) > 0:
				aspect = min(width, length) / max(width, length)
				if width > length:
					self.subclass.owner.scale = (1, aspect, 1)
				else:
					self.subclass.owner.scale = (aspect, 1, 1)
			self.subclass.owner.location = dimension.center

		if clickcount == 2 and not self.free:
			if self.subclass.target == None:
				self.subclass.target = set_create_target(self.subclass.owner, None)
			self.subclass.target.location = dimension.end




classes = [Create_OT_PointLight, Create_OT_SunLight,
			Create_OT_SpotLight, Create_OT_AreaLight]

def register_light():
	for c in classes:
		bpy.utils.register_class(c)

def unregister_light():
	for c in classes:
		bpy.utils.unregister_class(c)

if __name__ == "__main__":
	register_light()