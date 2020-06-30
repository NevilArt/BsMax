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
	def update(self, ctx):
		pass
	def abort(self):
		pass
		#delete_objects([self.owner])
		#self.reset()

class Create_OT_Surface(CreatePrimitive):
	bl_idname="create.surface"
	bl_label="Surface (Create)"
	subclass = Surface()

	def create(self, ctx, clickpoint):
		self.subclass.create(ctx)
			
	def update(self, ctx, clickcount, dimantion):
		pass

	def finish(self):
		pass

def register_surface():
	bpy.utils.register_class(Create_OT_Surface)
	
def unregister_surface():
	bpy.utils.unregister_class(Create_OT_Surface)