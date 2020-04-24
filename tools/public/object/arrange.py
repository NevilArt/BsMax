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
from bsmax.math import get_distance,point_on_curve

class BsMax_OT_DistanceSort(Operator):
	bl_idname = "object.distancesort"
	bl_label = "Distance Sort"
	bl_description = "Sort Selected object in Line"

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
		self.report({'INFO'},"bpy.ops.object.distancesort()")
		return{"FINISHED"}

class BsMax_OT_PathSort(Operator):
	bl_idname = "object.pathsort"
	bl_label = "Path Sort"
	bl_description = "Sort Selected object on Active Curve"

	@classmethod
	def poll(self, ctx):
		if ctx.area.type == 'VIEW_3D':
			if ctx.active_object.type == 'CURVE' and len(ctx.selected_objects) > 1:
				return True
		return False

	def execute(self, ctx):
		objs = ctx.selected_objects.copy()
		path = ctx.active_object
		if path.type == 'CURVE':
			if len(objs) > 0 and path != None:
				if path in objs:
					objs.remove(path)
				count = len(objs)
				close = path.data.splines[0].use_cyclic_u
				for i in range(count):
					t= i/count if close else i/(count - 1)
					p= point_on_curve(path, 0, t)
					p.x *= path.scale.x**2
					p.y *= path.scale.y**2
					p.z *= path.scale.z**2
					location = p @ path.matrix_world.inverted() + path.location
					objs[i].location = location
		self.report({'INFO'},"bpy.ops.object.pathsort()")
		return{"FINISHED"}

def object_sort_menu(self, ctx):
	layout = self.layout
	layout.separator()
	layout.operator("object.distancesort")
	layout.operator("object.pathsort")

classes = [BsMax_OT_DistanceSort, BsMax_OT_PathSort]

def register_arrange():
	[bpy.utils.register_class(c) for c in classes]
	bpy.types.VIEW3D_MT_transform_object.append(object_sort_menu)

def unregister_arrange():
	bpy.types.VIEW3D_MT_transform_object.remove(object_sort_menu)
	[bpy.utils.unregister_class(c) for c in classes]