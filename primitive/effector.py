import bpy
from bpy.props import EnumProperty
from primitive.primitive import CreatePrimitive
from bsmax.actions import delete_objects

class Effector:
	def __init__(self):
		self.finishon = 2
		self.owner = None
	def reset(self):
		self.__init__()
	def abort(self):
		delete_objects([self.owner])

class BsMax_OT_CreateEffector(CreatePrimitive):
	bl_idname="bsmax.createeffector"
	bl_label="Effector (Create)"
	subclass = Effector()

	effector_type: EnumProperty(name='Type',default='FORCE',
		items =[('FORCE','Force',''),('WIND','Wind',''),
				('VORTEX','Vortex',''),('MAGNET','Magnet',''),
				('HARMONIC','Harmonic',''),('CHARGE','Charge',''),
				('LENNARDJ','Lennardj',''),('TEXTURE','Texture',''),
				('GUIDE','Guide',''),('BOID','Boid',''),('TURBULENCE','Turbulence',''),
				('DRAG','Drag',''),('SMOKE','Smoke','')])

	def create(self, ctx, clickpoint):
		bpy.ops.object.effector_add(type=self.effector_type,radius=1,
									location=clickpoint.view)
		self.subclass.owner = ctx.active_object
		self.subclass.owner.rotation_euler = clickpoint.orient
	def update(self, ctx, clickcount, dimantion):
		if clickcount == 1:
			self.subclass.owner.empty_display_size = dimantion.radius
	def finish(self):
		pass

def effector_cls(register):
	c = BsMax_OT_CreateEffector
	if register: bpy.utils.register_class(c)
	else: bpy.utils.unregister_class(c)

if __name__ == '__main__':
	effector_cls(True)

__all__ = ["effector_cls"]