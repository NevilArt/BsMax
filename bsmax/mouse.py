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

import bpy, mathutils
from mathutils import Vector, Matrix
from math import pi
from bpy_extras.view3d_utils import region_2d_to_location_3d

class ClickPoint:
	view = Vector((0,0,0))
	local = Vector((0,0,0))
	vertical = Vector((0,0,0))
	screen = Vector((0,0,0))
	orient = Vector((0,0,0))
	view_name = ""

def get_view_orientation(ctx):
	r = lambda x: round(x, 2)
	orientation_dict = {(0,0,0):'TOP', (r(pi),0,0):'BOTTOM',
				(r(-pi/2),0,0):'FRONT', (r(pi/2),0,r(-pi)):'BACK',
				(r(-pi/2),r(pi/2),0):'LEFT', (r(-pi/2),r(-pi/2),0):'RIGHT'}
	r3d = ctx.area.spaces.active.region_3d
	view_rot = r3d.view_matrix.to_euler()
	view_orientation = orientation_dict.get(tuple(map(r, view_rot)),'USER')
	view_type = r3d.view_perspective
	return view_orientation, view_type

def get_triface_from_orient(orient):
	if orient in {'FRONT','BACK'}:
		return ((0,0,0),(1,0,0),(0,0,1))
	elif orient in {'LEFT','RIGHT'}:
		return ((0,0,0),(0,1,0),(0,0,1))
	else:
		return ((0,0,0),(0,1,0),(1,0,0))

def switch_axis_by_orient(orient, point):
	x, y, z = point
	if orient in ['FRONT','BACK']:
		return Vector((x,z,y))
	elif orient in ['LEFT','RIGHT']:
		return Vector((y,z,x))
	# elif orient in ['TOP','BOTTOM']:
	# 	return Vector((x,y,z))
	else:
		return Vector((x,y,z))

def get_rotation_from_orient(orient):
	r = pi/2
	if orient == 'FRONT': 
		return (r,0,0)
	elif orient == 'BACK':
		return (-r,0,0)
	elif orient == 'LEFT':
		return (r,0,-r)
	elif orient == 'RIGHT':
		return (r,0,r)
	elif orient == 'TOP':
		return (0,0,0)
	elif orient == 'BOTTOM':
		return (r*2,0,0)
	else:
		return (0,0,0)

def get_click_point_info(x, y, ctx):
	cp = ClickPoint()
	view_orient, view_type = get_view_orientation(ctx)
	region = ctx.region
	region_data = ctx.space_data.region_3d
	if view_type in ['PERSP', 'CAMERA']:
		view_matrix = region_data.view_matrix.inverted()
		ray_start = view_matrix.to_translation()
		ray_depth = view_matrix @ Vector((0,0,-100000))#TODO from view
		ray_end = region_2d_to_location_3d(region,region_data, (x, y), ray_depth)
		p = get_triface_from_orient(view_orient)
		cp.view = mathutils.geometry.intersect_ray_tri(p[0],p[1],p[2],ray_end,ray_start,False)
		if cp.view == None:
			cp.view = Vector((0,0,0))
	else:
		cp.view = region_2d_to_location_3d(region, region_data, (x, y), (0, 0, 0))
	cp.screen = region_2d_to_location_3d(region, region_data, (x, y), (0, 0, 0))
	cp.local = switch_axis_by_orient(view_orient, cp.view)
	cp.orient = Vector(get_rotation_from_orient(view_orient))
	if view_type == 'ORTHO' and view_orient == 'USER':
		pass
		# TODO in orthografic user view not work correctly
		# r3d = ctx.area.spaces.active.region_3d
		# view_rot = r3d.view_matrix.to_euler()
	cp.view_name = view_orient
	return cp