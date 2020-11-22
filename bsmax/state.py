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

def is_active_object(ctx, types):
	if ctx.area.type == 'VIEW_3D':
		if ctx.active_object != None:
			if ctx.active_object.type in types:
				return True
	return False

def is_active_primitive(ctx):
	active_obj = ctx.active_object
	if active_obj != None:
		if active_obj.type in ['MESH','CURVE']:
			if active_obj.data.primitivedata.classname != "":
				return True
	return False

def is_objects_selected(ctx):
	if ctx.area.type == 'VIEW_3D':
		return len(ctx.selected_objects) > 0

def is_object_mode(ctx):
	if ctx.area.type == 'VIEW_3D':
		if len(ctx.scene.objects) > 0:
			if ctx.object != None:
				if ctx.object.mode == 'OBJECT':
					return True
			else:
				return True
		else:
			return True
	return False

def is_mode(ctx, mode):
	if ctx.area.type == 'VIEW_3D':
		if len(ctx.scene.objects) > 0:
			if ctx.object != None:
				if ctx.object.mode == mode: 
					return True
			else:
				return True
		else:
			return True
	return False

def has_constraint(obj, constrainttype):
	for c in obj.constraints:
		if c.type == constrainttype:
			return True
	return False

def get_active_type(ctx):
	return None if ctx.active_object == None else ctx.active_object.type

def get_obj_class(obj):
	if obj.type in ['MESH', 'CURVE']:
		return obj.data.primitivedata.classname
	return ""