import bpy
from bpy.types import Operator
from mathutils import Vector, Matrix
from bsmax.math import get_distance

class BsMax_OT_DistanceSort(Operator):
	bl_idname = "bsmax.distancesort"
	bl_label = "Distance Sort"

	def execute(self, ctx):
		objs,md = ctx.selected_objects, 0
		if len(objs) > 2:
			A,B = objs[1],objs[2]
			for i in range(len(objs)):
				for j in range(i,len(objs)):
					if get_distance (objs[i],objs[j]) > md:
						md = get_distance(objs[i],objs[j])
						A,B= objs[i],objs[j]
			dis,Sobj = [],[]
			for o in objs:
				dis.append(get_distance(A,o))
			dis.sort()
			for i in range(len(dis)):
				for j in range(len(objs)):
					if get_distance(A,objs[j]) == dis[i]:
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
		return{"FINISHED"}

class BsMax_OT_PathSort(Operator):
	bl_idname = "bsmax.pathsort"
	bl_label = "Path Sort"
	def execute(self, ctx):
		# this tool not complet yet I had to learn more to do this ;)
		objs = ctx.selected_objects
		#if len(objs) > 0:
		#    obj = pickObject message:"Now Get a Shap Object" filter:shapeFilt
		#if obj != undefined do undo on
		#   Local pos = point pos:[0,0,0] 
		#   Pos.pos.controller = Path_Constraint()
		#   Pos.pos.controller.follow = on
		#   Pos.pos.controller.path = obj
		#   for i = 1 to S.count do
		#       Pos.pos.controller.percent = (100.0 / (S.count - 1)) * (i - 1)
		#       S[i].transform = Pos.transform
		#   Delete Pos
		print("Path sort")

def arrange_cls(register):
	classes = [BsMax_OT_DistanceSort, BsMax_OT_PathSort]
	for c in classes:
		if register: bpy.utils.register_class(c)
		else: bpy.utils.unregister_class(c)

if __name__ == '__main__':
	arrange_cls(True)

__all__ = ["arrange_cls"]