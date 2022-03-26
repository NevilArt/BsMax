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


blender_version = None
def version():
	""" Return Version as Integer e.g 2.83 as 283 """
	global blender_version
	# return same value if already calculated
	if blender_version:
		return blender_version

	# this value not changns and one time calculate is enough
	v = bpy.app.version
	if v[1] < 10:
		blender_version = v[0]*100 + v[1]*10
	blender_version = v[0]*100 + v[1]

	return blender_version



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
		return len(ctx.selected_objects) > 0



def is_object_mode(ctx):
	""" in all possible condition return True if is not Edit mode """
	if ctx.area.type == 'VIEW_3D':
		if len(ctx.scene.objects) > 0:
			if ctx.object:
				return ctx.object.mode == 'OBJECT'
			return True
		return True
	return False



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
	if obj.type in ['MESH', 'CURVE']:
		return obj.data.primitivedata.classname
	return ""