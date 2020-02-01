import bpy
from mathutils import Vector
from bpy.props import EnumProperty
from primitive.primitive import CreatePrimitive
from bsmax.actions import delete_objects
from bsmax.math import get_offset_by_orient

class Metaball:
	def __init__(self):
		self.finishon = 3
		self.owner = None
	def reset(self):
		self.__init__()
	def create(self, ctx, metaball_type):
		bpy.ops.object.metaball_add(type=metaball_type)
		self.owner = ctx.active_object
	def update(self, ctx):
		pass
	def abort(self):
		delete_objects([self.owner])

class BsMax_OT_CreateMetaball(CreatePrimitive):
	bl_idname="bsmax.createmetaball"
	bl_label="Metaball (Create)"
	subclass = Metaball()

	metaball_type: EnumProperty(name='Type', default='BALL',
		items =[('BALL','Ball',''),
				('CAPSULE','Capsule',''),
				('PLANE','Plane',''),
				('ELLIPSOID','Ellipsoid',''),
				('CUBE','Cube','')])
	radius = 0
	location = Vector((0,0,0))

	def create(self, ctx, clickpoint):
		if self.metaball_type == 'BALL':
			self.subclass.finishon = 2
		elif self.metaball_type == 'ELLIPSOID':
			self.subclass.finishon = 3
		elif self.metaball_type == 'CUBE':
			self.subclass.finishon = 4
		self.subclass.create(ctx, self.metaball_type)
		owner = self.subclass.owner
		owner.location = clickpoint.view
		owner.rotation_euler = clickpoint.orient
		owner.data.elements[0].radius = 0
		owner.data.elements[0].size_x = 0
		owner.data.elements[0].size_y = 0
		owner.data.elements[0].size_z = 0

	def update(self, ctx, clickcount, dimantion):
		data = self.subclass.owner.data
		if self.metaball_type == 'BALL':
			if clickcount == 1:
				data.elements[0].radius = dimantion.radius
		elif self.metaball_type == 'CAPSULE':
			if clickcount == 1:
				data.elements[0].radius = dimantion.radius
				data.elements[0].size_x = 0
			elif clickcount == 2:
				radius = dimantion.radius_from_start_point - data.elements[0].radius
				data.elements[0].size_x = radius
		elif self.metaball_type == 'PLANE':
			if clickcount == 1:
				self.radius = dimantion.radius / 10
				data.elements[0].radius = self.radius
				data.elements[0].size_x = dimantion.width / 2
				data.elements[0].size_y = dimantion.length / 2
				self.subclass.owner.location = dimantion.center
			elif clickcount == 2:
				data.elements[0].radius = self.radius + dimantion.height_np
		elif self.metaball_type == 'ELLIPSOID':
			if clickcount == 1:
				data.elements[0].radius = 2
				data.elements[0].size_x = dimantion.width
				data.elements[0].size_y = dimantion.length
				self.radius = dimantion.radius / 2
				data.elements[0].size_z = self.radius
			elif clickcount == 2:
				data.elements[0].size_z = self.radius + dimantion.height_np
		elif self.metaball_type == 'CUBE':
			if clickcount == 1:
				data.elements[0].radius = 1
				data.elements[0].size_x = dimantion.width / 2
				data.elements[0].size_y = dimantion.length / 2
				data.elements[0].size_z = 0.1
				self.location = self.subclass.owner.location = dimantion.center
			elif clickcount == 2:
				height = dimantion.height / 2
				offset = get_offset_by_orient(Vector((0,0,height)), dimantion.view_name)
				data.elements[0].size_z = height
				self.subclass.owner.location = self.location + offset
			elif clickcount == 3:
				data.elements[0].radius = 0.01 + dimantion.radius
		#TODO adapt resolation by size
		#self.subclass.data.resolution = 1.33

	def finish(self):
		pass

def metaball_cls(register):
	c = BsMax_OT_CreateMetaball
	if register: bpy.utils.register_class(c)
	else: bpy.utils.unregister_class(c)

if __name__ == '__main__':
	metaball_cls(True)

__all__ = ["metaball_cls"]