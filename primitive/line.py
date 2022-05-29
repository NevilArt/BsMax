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

import re
import bpy
from bpy.types import Operator
from mathutils import Vector
from bsmax.math import get_axis_constraint
from primitive.primitive import Primitive_Curve_Class, Draw_Primitive
from bsmax.actions import delete_objects
from bpy_extras.view3d_utils import location_3d_to_region_2d

# global variable
close_line = False



class knot:
	def __init__(self, pos, invec, outvec, mode):
		self.pos = pos
		self.invec = invec
		self.outvec = outvec
		self.mode = mode



def get_line_shape(knots):
	shape = []
	for k in knots:
		shape.append((k.pos, k.invec, k.mode, k.outvec, k.mode))
	return [shape]



class Line(Primitive_Curve_Class):
	def __init__(self):
		self.classname = "Line"
		self.finishon = 0 # infinit
		self.owner = None
		self.data = None
		self.close = False
		self.knots = []
		self.lastknot = []
		self.ctx = None

	def reset(self):
		self.__init__()

	def create(self, ctx):
		global close_line
		close_line = False
		self.ctx = ctx
		shapes = get_line_shape([])
		self.create_curve(ctx,shapes,self.classname)

	def update(self):
		shapes = get_line_shape(self.knots + self.lastknot)
		self.update_curve(shapes)

	def abort(self):
		if len(self.knots) < 2:
			delete_objects([self.owner])
		else:
			self.lastknot = []
			self.knots.pop()
			self.update()
			bpy.ops.object.origin_set(type='ORIGIN_CENTER_OF_VOLUME', center='MEDIAN')
	
	def finish(self):
		pass



class Curve_OT_CloseLine(Operator):
	bl_idname = "curve.closeline"
	bl_label = "Close Line?"
	bl_options = {'REGISTER', 'INTERNAL'}
	
	def execute(self, ctx):
		global close_line
		close_line = True
		return {'FINISHED'}
	
	def cancel(self, ctx):
		global close_line
		close_line = False
	
	def invoke(self, ctx, event):
		return ctx.window_manager.invoke_confirm(self, event)

def check_for_close(self, ctx):
	if len(self.subclass.knots) > 2:
		region_3d = ctx.space_data.region_3d
		p0 = location_3d_to_region_2d(ctx.region,region_3d,self.subclass.knots[0].pos)
		pl = location_3d_to_region_2d(ctx.region,region_3d,self.subclass.lastknot[0].pos)
		if abs(p0.x-pl.x) < 10 and abs(p0.y-pl.y) < 10:
			bpy.ops.curve.closeline('INVOKE_DEFAULT')



class Create_OT_Line(Draw_Primitive):
	bl_idname = "create.line"
	bl_label = "Line"
	subclass = Line()
	use_gride = False
	lastclick = 1

	def create(self, ctx):
		global close_line
		self.used_keys += ['LEFT_SHIFT', 'RIGHT_SHIFT', 'BACK_SPACE']
		self.request_key = ['BACK_SPACE']
		self.subclass.close = close_line = False
		self.subclass.create(ctx)
		self.params = self.subclass.owner.data.primitivedata
		location = self.gride.location
		newknot = knot(location, location, location, "VECTOR")
		self.subclass.knots.append(newknot)

	def update(self, ctx, clickcount, dimension):
		global close_line
		dim = self.point_current.location.copy()
		
		if self.shift:
			index = -1 if len(self.subclass.knots) < 2 else -2
			lastpoint = self.subclass.knots[index].pos
			dim = get_axis_constraint(lastpoint, dim)

		if self.drag:
			pos = self.subclass.knots[-1].pos
			outvec = dim
			invec = Vector((0,0,0))
			invec.x = pos.x - (outvec.x - pos.x)
			invec.y = pos.y - (outvec.y - pos.y)
			invec.z = pos.z - (outvec.z - pos.z)
			newknot = knot(pos, invec, outvec, 'ALIGNED')
		else:
			newknot = knot(dim, dim, dim, "VECTOR")

		if clickcount != self.lastclick:
			self.subclass.knots.append(newknot)
			self.lastclick = clickcount
			check_for_close(self, ctx)
		
		if close_line:
			self.subclass.close = True
			self.forcefinish = True
			self.subclass.knots.pop()
			self.step = -1 #force to finish not kill
		else:
			self.subclass.knots[-1] = newknot
			self.subclass.lastknot = [knot(dim, dim, dim, "VECTOR")]

	def check_event(self, key, action):
		if key == 'BACK_SPACE':
			if action == 'RELEASE':
				if len(self.subclass.knots) > 2:
					self.subclass.knots.pop()
					self.changed = True

	def finish(self):
		self.subclass.reset()



classes = [Create_OT_Line, Curve_OT_CloseLine]

def register_line():
	for c in classes:
		bpy.utils.register_class(c)

def unregister_line():
	for c in classes:
		bpy.utils.unregister_class(c)

if __name__ == "__main__":
	register_line()