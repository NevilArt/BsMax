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
from math import pi
from mathutils import Vector

def is_active_object(ctx, types):
	""" Return True if active object is same as given object type """
	if ctx.area.type == 'VIEW_3D':
		if ctx.active_object:
			return ctx.active_object.type in types
	return False



def is_active_primitive(ctx):
	""" Return True if active object has primitive data """
	if ctx.active_object:
		if ctx.active_object.type in ['MESH','CURVE']:
			return ctx.active_object.data.primitivedata.classname != ""
	return False



def is_objects_selected(ctx):
	""" Return True if ther was any selected objects """
	if ctx.area.type == 'VIEW_3D':
		return ctx.selected_objects



def has_constraint(obj, constrainttype):
	""" Find that given object has asked constraint or not """
	for c in obj.constraints:
		if c.type == constrainttype:
			return True
	return False



def get_active_type(ctx):
	""" Return active objects type if exist """
	return ctx.active_object.type if ctx.active_object else None



def get_obj_class(obj):
	""" return primitive object type """
	if obj:
		if obj.type in ['MESH', 'CURVE']:
			return obj.data.primitivedata.classname
	return ""



def get_view_orientation(ctx):
	""" return = (str, str) (view_orientation, view_type) """
	r = lambda x: round(x, 2)

	orientation_dict = {
		(0, 0, 0):'TOP',
		(r(pi), 0, 0):'BOTTOM',
		(r(-pi/2), 0, 0):'FRONT',
		(r(pi/2), 0, r(-pi)):'BACK',
		(r(-pi/2), r(pi/2), 0):'LEFT',
		(r(-pi/2), r(-pi/2), 0):'RIGHT'}
	
	r3d = ctx.area.spaces.active.region_3d
	view_rot = r3d.view_matrix.to_euler()
	
	view_orientation = orientation_dict.get(tuple(map(r, view_rot)), 'USER')
	view_type = r3d.view_perspective
	
	return view_orientation, view_type



#TODO need to clear name and info
def get_rotation_of_view_orient(view_orient):
		if view_orient == 'TOP':
			return Vector((0, 0, 0))
		if view_orient == 'BOTTOM':
			return Vector((pi, 0, 0))
		if view_orient == 'FRONT':
			return Vector((pi/2, 0, 0))
		if view_orient == 'BACK':
			return Vector((-pi/2, pi, 0))
		if view_orient == 'LEFT':
			return Vector((pi/2, 0, -pi/2))
		if view_orient == 'RIGHT':
			return Vector((pi/2, 0, pi/2))
		return Vector((0, 0, 0))



def get_dimensions_avrage(obj, x, y, z):
	""" get object and return avrage of wanted side

		args:
			obj: Object
			x: Boolean count x side
			y: Boolean count y side
			z: Boolean count z side
		return:
			float avrage of vanted sides
	"""
	value, count = 0, 0
	if x:
		value += obj.dimensions.x
		count += 1
	if y:
		value += obj.dimensions.y
		count += 1
	if z:
		value += obj.dimensions.z
		count += 1
	return value/count


def has_key_in_frame(obj, frame: int):
	""" Check Object has keyframe on given frame

		args:
			obj: bpy.data.Object
			frame: int
		return:
			bool
	"""
	if obj and obj.animation_data and obj.animation_data.action:
		for fcurves in obj.animation_data.action.fcurves:
			return frame in (point.co.x for point in fcurves.keyframe_points)
	return False