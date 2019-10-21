import bpy
from primitive.primitive import PrimitiveGeometryClass, CreatePrimitive
from bsmax.actions import delete_objects

def cylindersurface(radius, height):

	bpy.context.object.data.splines[0].points[0].co[0] = 0
	bpy.context.object.data.splines[0].points[0].co[1] = -0.99
	bpy.context.object.data.splines[0].points[0].co[1] = -1
	bpy.context.object.data.splines[0].points[0].co[3] = 1.01
	bpy.context.object.data.splines[0].type = 'NURBS'
	bpy.context.object.data.splines[0].use_smooth = True

class Surface(PrimitiveGeometryClass):
	def __init__(self):
		self.classname = "Surface"
		self.finishon = 2
		self.owner = None
		self.data = None
	def reset(self):
		self.__init__()
	def create(self, ctx):
		pass
	def update(self):
		pass
	def abort(self):
		pass
		#delete_objects([self.owner])
		#self.reset()

class BsMax_OT_CreateSurface(CreatePrimitive):
	bl_idname="bsmax.createsurface"
	bl_label="Surface (Create)"
	subclass = Surface()

	def create(self, ctx, clickpoint):
		self.subclass.create(ctx)
			
	def update(self, clickcount, dimantion):
		pass

	def finish(self):
		pass

def surface_cls(register):
	c = BsMax_OT_CreateSurface
	if register: bpy.utils.register_class(c)
	else: bpy.utils.unregister_class(c)

if __name__ == '__main__':
	surface_cls(True)

__all__ = ["surface_cls"]