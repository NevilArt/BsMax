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
from bpy_extras.view3d_utils import region_2d_to_location_3d,location_3d_to_region_2d

# def obj_ray_cast(obj, matrix):
# 	"""Wrapper for ray casting that moves the ray into object space"""
# 	# get the ray relative to the object
# 	matrix_inv = matrix.inverted()
# 	ray_origin_obj = matrix_inv * ray_origin
# 	ray_target_obj = matrix_inv * ray_target
# 	# cast the ray
# 	hit, normal, face_index = obj.ray_cast(ray_origin_obj, ray_target_obj)
# 	if face_index != -1:
# 		return hit, normal, face_index
# 	else:
# 		return None, None, None

def view_pan(ctx,x,y):
	# region = ctx.region
	# region_data = ctx.space_data.region_3d
	# depth = view_matrix @ Vector((0,0,-100000))
	# r = region_2d_to_location_3d(region,region_data, (x,y), depth)
	# p = location_3d_to_region_2d(region,region_data,(self.subclass.knots[0].pos))
	# #bpy.ops.view3d.move('INVOKE_DEFAULT')

	# # get the context arguments
	# scene = ctx.scene
	# region = ctx.region
	# rv3d = ctx.region_data
	# coord = 100, 100

	# # get the ray from the viewport and mouse
	# view_vector = view3d_utils.region_2d_to_vector_3d(region, rv3d, coord)
	# ray_origin = view3d_utils.region_2d_to_origin_3d(region, rv3d, coord)

	# if rv3d.view_perspective == 'ORTHO':
	# 	# move ortho origin back
	# 	ray_origin = ray_origin - (view_vector * (ray_max / 2.0))
	
	# ray_target = ray_origin + (view_vector * ray_max)

	# # cast the ray
	# hit, normal, face_index = obj.ray_cast(ray_origin_obj, ray_target_obj)
	print("Pan")
	pass

def view_orbit(ctx,x,y):
	#bpy.ops.view3d.rotate('INVOKE_DEFAULT')
	print("Orbit")
	pass

def view_dolly(ctx,x,y):
	#bpy.ops.view3d.dolly('INVOKE_DEFAULT')
	print("dolly")
	pass

def view_zoom(ctx,x,y):
	val = ctx.space_data.lens + y
	val = 250 if val > 250 else val
	val = 1 if val < 1 else val
	ctx.space_data.lens = val

class View2D_OT_3DsMax_Navigation(bpy.types.Operator):
	bl_idname = "view3d.max_navigation"
	bl_label = "3DsMax Navigation"
	alt = False
	ctrl = False
	shift = False
	mmb = False
	x,y = 0,0

	@classmethod
	def poll(self, ctx):
		return ctx.area.type == 'VIEW_3D'

	def modal(self,ctx,event):
		print(event.type)
		if not event.type in ['MIDDLEMOUSE','MOUSEMOVE','LEFT_CTRL','RIGHT_CTRL',
							'LEFT_ALT','RIGHT_ALT','LEFT_SHIFT','RIGHT_SHIFT',]:
			return {'PASS_THROUGH'}

		if event.type == 'MIDDLEMOUSE':
			if event.value in {'PRESS','CLICK_DRAG'}:
				self.mmb = True
			elif event.value == 'RELEASE':
				self.mmb = False

		if event.type in {'LEFT_ALT','RIGHT_ALT'}:
			if event.value in {'PRESS','CLICK_DRAG'}:
				self.alt = True
			elif event.value == 'RELEASE':
				self.alt = False

		if event.type in {'LEFT_CTRL','RIGHT_CTRL'}:
			if event.value in {'PRESS','CLICK_DRAG'}:
				self.ctrl = True
			elif event.value == 'RELEASE':
				self.ctrl = False

		if event.type in {'LEFT_SHIFT','RIGHT_SHIFT'}:
			if event.value in {'PRESS','CLICK_DRAG'}:
				self.ctrl = True
			elif event.value == 'RELEASE':
				self.ctrl = False

		x,y = event.mouse_region_x,event.mouse_region_y
		dx,dy = x-self.x, y-self.y
		self.x,self.y = x,y

		mmb,alt,ctrl,shift = self.mmb,self.alt,self.ctrl,self.shift

		if mmb and not alt and not ctrl and not shift:
			view_pan(ctx,dx,dy)
		if mmb and alt and not ctrl and not shift:
			view_orbit(ctx,dx,dy)
		if mmb and alt and ctrl and not shift:
			view_dolly(ctx,dx,dy)
		if mmb and not alt and ctrl and shift:
			view_zoom(ctx,dx,dy)

		if not self.mmb:
			return {'CANCELLED'}
		return {'RUNNING_MODAL'}

	def invoke(self,ctx,event):
		self.x,self.y = event.mouse_region_x,event.mouse_region_y
		self.mmb = True
		ctx.window_manager.modal_handler_add(self)
		return {'RUNNING_MODAL'}

def register_navigation():
	bpy.utils.register_class(View2D_OT_3DsMax_Navigation)

def unregister_navigation():
	bpy.utils.unregister_class(View2D_OT_3DsMax_Navigation)