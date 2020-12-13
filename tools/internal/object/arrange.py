############################################################################
#	This program is free software: you can redistribute it and/or modify
#	it under the terms of the GNU General Public License as published by
#	the Free Software Foundation, either version 3 of the License, or
#	(at your option) any later version.
#
#	This program is distributed in the hope that it will be useful,
#	but WITHOUT ANY WARRANTY; without even the implied warranty of
#	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#	GNU General Public License for more details.
#
#	You should have received a copy of the GNU General Public License
#	along with this program.  If not, see <https://www.gnu.org/licenses/>.
############################################################################

import bpy
from bpy.types import Operator
from bpy.props import FloatProperty
from bsmax.math import get_distance,point_on_curve
from bsmax.operator import PickOperator

class Object_OT_Distance_Sort(Operator):
	bl_idname = "object.distance_sort"
	bl_label = "Distance Sort"
	bl_description = "Sort Selected object in Line"
	bl_options = {'REGISTER', 'UNDO'}

	@classmethod
	def poll(self, ctx):
		if ctx.area.type == 'VIEW_3D':
			return len(ctx.selected_objects) > 2
		return False

	def execute(self, ctx):
		objs,md = ctx.selected_objects, 0
		if len(objs) > 2:
			A,B = objs[1],objs[2]
			for i in range(len(objs)):
				for j in range(i,len(objs)):
					if get_distance (objs[i].location,objs[j].location) > md:
						md = get_distance(objs[i].location,objs[j].location)
						A,B= objs[i],objs[j]
			dis,Sobj = [],[]
			for o in objs:
				dis.append(get_distance(A.location,o.location))
			dis.sort()
			for i in range(len(dis)):
				for j in range(len(objs)):
					if get_distance(A.location,objs[j].location) == dis[i]:
						Sobj.append(objs[j])
			for i in range(1,len(Sobj) - 1):
				Sobj[i].location = A.location+(((B.location - A.location)/(len(Sobj) - 1))*i)
			for i in range(1,len(Sobj) - 1):
				Sobj[i].scale = A.scale+(((B.scale - A.scale)/(len(Sobj) - 1))*i)
			XA,YA,ZA = A.rotation_euler
			XB,YB,ZB = B.rotation_euler

			# TODO probleam in linked objects place by global location
			for i in range(1,(len(Sobj) - 1)):
				Sobj[i].rotation_euler.x = XA+((XB - XA)/(len(Sobj) - 1))*i
			for i in range(1,(len(Sobj) - 1)):
				Sobj[i].rotation_euler.y = YA+((YB - YA)/(len(Sobj) - 1))*i
			for i in range(1,(len(Sobj) - 1)):
				Sobj[i].rotation_euler.z = ZA+((ZB - ZA)/(len(Sobj) - 1))*i
		self.report({'OPERATOR'},"bpy.ops.object.distance_sort()")
		return{"FINISHED"}



class Object_OT_Path_Sort_Apply(Operator):
	bl_idname = "object.path_sort_apply"
	bl_label = "Path Sort Apply"
	bl_options = {'REGISTER', 'INTERNAL','UNDO'}
	
	objs, path = [], None
	start: FloatProperty(name="Start:",min=0,max=1,step=0.01,precision=3,default=0.0)
	end: FloatProperty(name="End:",min=0,max=1,step=0.01,precision=3,default=1.0)

	def draw(self, ctx):
		layout = self.layout
		row = layout.row(align=True)
		row.prop(self,"start")
		row.prop(self,"end")
	
	def set_location(self, obj, path, time):
		p = point_on_curve(path, 0, time)
		p.x *= path.scale.x**2
		p.y *= path.scale.y**2
		p.z *= path.scale.z**2
		location = p @ path.matrix_world.inverted() + path.location
		obj.location = location
	
	def check(self, ctx):
		close = self.path.data.splines[0].use_cyclic_u
		count = len(self.objs)
		length = (self.end - self.start) / 1
		for i in range(count):
			t = i/count if close else i / (count - 1) if count > 1 else 0
			time = self.start + t * length
			self.set_location(self.objs[i], self.path, time)

	def execute(self,ctx):
		return {'FINISHED'}

	def invoke(self, ctx, event):
		self.objs = ctx.selected_objects
		self.path = ctx.active_object
		self.check(ctx)
		return ctx.window_manager.invoke_props_dialog(self)
	
class Object_OT_Path_Sort(PickOperator):
	bl_idname = "object.path_sort"
	bl_label = "Path Sort"
	bl_description = "Sort Selected object on a Curve"
	
	filters = ['CURVE']
	def picked(self, ctx, source, subsource, target, subtarget):
		ctx.view_layer.objects.active = target
		bpy.ops.object.path_sort_apply('INVOKE_DEFAULT')

def object_sort_menu(self, ctx):
	layout = self.layout
	layout.operator("object.align_selected_to_target", text='Align Objects (BsMax)')
	layout.separator()
	layout.operator("object.distance_sort")
	layout.operator("object.path_sort")

classes = [Object_OT_Distance_Sort, Object_OT_Path_Sort, Object_OT_Path_Sort_Apply]

def register_arrange():
	[bpy.utils.register_class(c) for c in classes]
	bpy.types.VIEW3D_MT_transform_object.append(object_sort_menu)

def unregister_arrange():
	bpy.types.VIEW3D_MT_transform_object.remove(object_sort_menu)
	[bpy.utils.unregister_class(c) for c in classes]

if __name__ == "__main__":
	register_arrange()