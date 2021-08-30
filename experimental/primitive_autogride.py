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
from math import sin, cos, pi, asin, atan2
from random import triangular
from bsmax.curve import Spline,Bezier_point
from bsmax.math import point_on_vector
from bsmax.actions import delete_objects

#############################################################################
from mathutils import Vector, Matrix, geometry
from math import pi, acos, sin, cos
from bpy_extras.view3d_utils import region_2d_to_location_3d, region_2d_to_vector_3d, region_2d_to_origin_3d

class ClickPoint:
	view = Vector((0,0,0))
	local = Vector((0,0,0))
	vertical = Vector((0,0,0))
	screen = Vector((0,0,0))
	orient = Vector((0,0,0))
	view_name = ""

class Triangle:
	def __init__(self, p1, p2, p3, direction):
		self.p1 = p1
		self.p2 = p2
		self.p3 = p3
		self.rotate(direction)
	def rotate(self, direction):
		pass


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
	""" Get mouse screen position and context
		return ....	
	"""
	# primitive_setting = ctx.scene.primitive_setting
	surface_posion, surface_normal = (0,0,0), (0,0,0)

	# if primitive_setting.position or primitive_setting.normal:
	# 	pos, normal, _, _ = ray_cast(ctx, x, y)
	# 	if primitive_setting.position and pos:
	# 		surface_posion = pos
	# 	if primitive_setting.normal and normal:
	# 		surface_normal = normal


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
		cp.view = geometry.intersect_ray_tri(p[0],p[1],p[2],ray_end,ray_start,False)
		if cp.view == None:
			cp.view = Vector((0,0,0))
	else:
		cp.view = region_2d_to_location_3d(region, region_data, (x, y), (0, 0, 0))
		# cp.view = region_2d_to_location_3d(region, region_data, (x, y), surface_posion)
	
	cp.screen = region_2d_to_location_3d(region, region_data, (x, y), (0, 0, 0))
	# cp.screen = region_2d_to_location_3d(region, region_data, (x, y), surface_posion)
	
	cp.local = switch_axis_by_orient(view_orient, cp.view)
	cp.orient = Vector(get_rotation_from_orient(view_orient))
	
	if view_type == 'ORTHO' and view_orient == 'USER':
		pass
		# TODO in orthografic user view not work correctly
		# r3d = ctx.area.spaces.active.region_3d
		# view_rot = r3d.view_matrix.to_euler()

	cp.view_name = view_orient
	return cp


def visible_objects_and_duplis(ctx):
	""" Loop over (object, matrix) pairs (mesh only) """

	depsgraph = ctx.evaluated_depsgraph_get()
	for dup in depsgraph.object_instances:
		if dup.is_instance:  # Real dupli instance
			obj = dup.instance_object
			yield (obj, dup.matrix_world.copy())
		else:  # Usual object
			obj = dup.object
			yield (obj, obj.matrix_world.copy())



def obj_ray_cast(obj, matrix, ray_origin, ray_target):
	""" Wrapper for ray casting that moves the ray into object space """

	# get the ray relative to the object
	matrix_inv = matrix.inverted()
	ray_origin_obj = matrix_inv @ ray_origin
	ray_target_obj = matrix_inv @ ray_target
	ray_direction_obj = ray_target_obj - ray_origin_obj

	# cast the ray
	success, location, normal, face = obj.ray_cast(ray_origin_obj, ray_direction_obj)

	if success:
		return location, normal, face
	else:
		return None, None, None


# Raycast function is from Oliver Weissbarth`s BookGen add-on #
# https://blenderartists.org/u/Oweissbarth #
# Thanks him for Greate add-on # 
def ray_cast(ctx, mouse_x, mouse_y):
	""" Shoots a ray from the cursor position into the scene and returns the closest intersection

	Args:
		mouse_x (float): x position of the cursor in pixels
		mouse_y (float): y position of the cursor in pixels

	Returns:
		(Vector, Vector, int, bpy.types.Object): A tuple containing the position, normal,
												 face id and object of the closest intersection
	"""
	region = ctx.region
	region_data = ctx.space_data.region_3d

	view_vector = region_2d_to_vector_3d(region, region_data, (mouse_x, mouse_y))
	ray_origin = region_2d_to_origin_3d(region, region_data, (mouse_x, mouse_y))

	ray_target = ray_origin + view_vector

	best_length_squared = -1.0
	closest_loc = None
	closest_normal = None
	closest_obj = None
	closest_face = None

	for obj, matrix in visible_objects_and_duplis(ctx):
		if obj.type == 'MESH':
			hit, normal, face = obj_ray_cast(obj, matrix, ray_origin, ray_target)
			if hit is not None:
				_, rot, _ = matrix.decompose()
				hit_world = matrix @ hit
				normal_world = rot.to_matrix() @ normal
				length_squared = (hit_world - ray_origin).length_squared
				if closest_loc is None or length_squared < best_length_squared:
					best_length_squared = length_squared
					closest_loc = hit_world
					closest_normal = normal_world
					closest_face = face
					closest_obj = obj

	return closest_loc, closest_normal, closest_face, closest_obj
#############################################################################

# from primitive.primitive import CreatePrimitive,PrimitiveGeometryClass
#########################################################################
import bpy, bmesh, bgl, gpu
from bpy.types import Operator
from mathutils import Vector
from math import sqrt
from gpu_extras.batch import batch_for_shader
from bsmax.state import is_object_mode
from bsmax.actions import link_to_scene, set_as_active_object
# from bsmax.mouse import get_click_point_info, ClickPoint
from bsmax.math import get_2_point_center


class AutoGride:
	""" Float gride for drawing a primitive	"""
	def __init__(self, location, normal):
		# self.start = start
		self.location = location
		# self.end = end
		self.normal = normal
		# self.direction = (end - start).normalized()
		# self.rotation_matrix = Matrix([self.direction, -self.direction.cross(normal), normal]).transposed()
		self.rotation_matrix = Matrix([self.normal, -self.normal.cross(normal), normal]).transposed()
		self.tringle = Triangle((0,0,0), (1,0,0), (0,1,0), (0,0,0))
		self.direction = Matrix.Translation(normal)

	def genarate_triangle(self):
		pass
	def get_graphic(self):
		pass


class Dimantion:
	""" Package of data needs for draw any primitive
	
	width, length, height
	
	radius, center, orient, direction
	
	view, local, view_name, height_np
	
	width_from_start_point
	
	length_from_start_point
	
	height_from_start_point
	
	radius_from_start_point
	"""
	width = 0
	length = 0
	height = 0
	radius = 0
	direction = Vector((0,0,0))
	center = Vector((0,0,0))
	orient = Vector((0,0,0))
	view = Vector((0,0,0))
	local = Vector((0, 0, 0))
	view_name = ""

	height_np = 0

	width_from_start_point = 0
	length_from_start_point = 0
	height_from_start_point = 0
	radius_from_start_point = 0

	def from_click_points(self, cpa, cpb, cpo):
		w = self.width = abs(cpa.local.x - cpb.local.x)
		l = self.length = abs(cpa.local.y - cpb.local.y)
		if cpo.view_name == 'TOP':
			height = cpb.screen.y - cpa.screen.y
		elif cpo.view_name == 'BOTTOM':
			height = cpa.screen.y - cpb.screen.y
		else:
			height = cpb.screen.z - cpa.screen.z
		self.height_np = height
		self.height = height if height > 0 else 0
		self.radius = sqrt(w * w + l * l)
		self.orient = cpa.orient
		self.center = get_2_point_center(cpa.view, cpb.view)
		self.view = cpb.view
		self.local = cpb.view
		wo = abs(cpo.local.x - cpb.local.x)
		lo = abs(cpo.local.y - cpb.local.y)
		self.radius_from_start_point = sqrt(wo * wo + lo * lo)
		self.view_name = cpo.view_name

#############################################
# import numpy
 
# def Rx(theta):
# 	return numpy.matrix([[1,0,0],
# 		[0,cos(theta),-sin(theta)],
# 		[0,sin(theta),cos(theta)]])

# def Ry(theta):
# 	return numpy.matrix([[cos(theta),0,sin(theta)],
# 				[0,1,0], 
# 				[-sin(theta),0,cos(theta)]])
  
# def Rz(theta):
# 	return numpy.matrix([[ cos(theta),-sin(theta),0],
# 					[sin(theta),cos(theta),0],
# 					[0,0,1]])

#############################################
def rotate_vector_with_normal(to_rotate, normal):

	# const newVector: Vector3 = new Vector3().copy(toRotate);
	new_vector = to_rotate.copy()

	# // set up direction
	# let up = new Vector3(0, 1, 0)
	up = Vector((0, 1, 0))
	# let axis: Vector3;
	axis = Vector((0, 0, 0))
	# // we want the vector to point in the direction of the face normal
	# // determine an axis to rotate around
	# // cross will not work if vec == +up or -up, so there is a special case
	# if (normal.y == 1 or normal.y == -1)
	if normal[1] == 1 or normal[1] == -1:
		axis = Vector((1, 0, 0))
	else:
		axis =  Vector().cross(up, normal)

	# // determine the amount to rotate
	radians = acos(normal.dot(up))
	# quat = Quaternion().setFromAxisAngle(axis, radians)
	# new_vector.applyQuaternion(quat)

	return new_vector
##############################################
class vector3:
	def __init__(self):
		self.x = 0
		self.y = 0
		self.z = 0

""" Get Eular Rotation as Vector3 """
def rotaion_eular(matrix):
	"""
	*   Formula From 
	*   https://www.euclideanspace.com/maths/geometry/rotations/conversions/matrixToEuler/
	*   Need to test
	*     
	*   Coordinate System: right hand
	*   Positive angle: right hand
	*   Order of euler angles: heading first, then attitude, then bank
	*   matrix row column ordering:
	*   [m00 m01 m02] [1, 0, 0][0] Xv
	*   [m10 m11 m12] [0, 1, 0][0] Yv
	*   [m20 m21 m22] [0, 0, 1][0] Zv
	* 
	*   angle applied first     heading
	*   angle applied second    attitude
	*   angle applied last      bank
	* 
	*   For now only XYZ system
	"""


	eular = Vector((0,0,0))
	pi = 2 * asin(1.0)
	# Assuming the angles are in radians.
	if (matrix[1][0] > 0.998): # singularity at north pole
		eular[0] = atan2(matrix[0][2], matrix[2][2]) # heading
		eular[1] = pi / 2 # attitude
		eular[2] = 0 # bank
	elif (matrix[1][0] < -0.998): # singularity at south pole
		eular[0] = atan2(matrix[0][2], matrix[2][2]) # heading
		eular[1] = -pi / 2 # attitude
		eular[2] = 0 # bank
	else:
		eular[0] = atan2(-matrix[2][0], matrix[0][0]) # heading
		eular[1] = atan2(-matrix[1][2], matrix[1][1]) # bank
		eular[2] = asin(matrix[1][0]) # attitude
	
	return eular

##############################################


class CreatePrimitive(Operator):
	""" Get click points and calculate dimantion for create a primitive object """
	bl_options = {'REGISTER','UNDO'}
	subclass = None
	params = None
	step = 0
	
	state = False
	drag = False
	forcefinish = False
	shift = False
	ctrl = False
	alt = False

	usedkeys = ['LEFTMOUSE', 'RIGHTMOUSE', 'ESC', 'MOUSEMOVE']
	cancelkeys = ['RIGHTMOUSE', 'ESC']
	requestkey = []

	start, end = Vector((0,0,0)), Vector((0,0,0))
	cpoint_a = ClickPoint()
	cpoint_b = ClickPoint()
	
	mpos = Vector((0, 0, 0))

	start_point = None
	end_point = None
	start_normal = None
	end_normal = None

	gride = None

	@classmethod
	def poll(self, ctx):
		return is_object_mode(ctx)
	
	def is_drawed_enough(self):
		return abs(self.start.x - self.end.x) + abs(self.start.y - self.end.y) > 8
	
	def get_shift_state(self, ctx, event):
		if event.type in {'LEFT_SHIFT', 'RIGHT_SHIFT'}:
			if event.value == 'PRESS':
				self.shift = True
			if event.value == 'RELEASE':
				self.shift = False


	
	def modal(self, ctx, event):
		ctx.area.tag_redraw()

		self.get_shift_state(ctx, event)
	
		# ignore if subclass not defined
		if self.subclass == None:
			return {'CANCELLED'}
		# free the non used keys
		elif not event.type in self.usedkeys: 
			return {'PASS_THROUGH'}
		else:
			dimantion = Dimantion()
			# get mouse position from screen in pixel
			x, y = event.mouse_region_x, event.mouse_region_y
			
			self.mpos = Vector((x, y, 0))
			self.cpoint_b = get_click_point_info(x, y, ctx)
			
			if event.type == 'LEFTMOUSE':
				###############################################################
				if self.start_point is None:
					self.start_point, self.start_normal, _, _ = ray_cast(ctx, x, y)
					ctx.workspace.status_text_set("Drag the mouse on a surface")
					return {'RUNNING_MODAL'}
				###############################################################
				if self.step == 0:
					self.step = 1
					self.cpoint_o = self.cpoint_a = self.cpoint_b
					self.create(ctx, self.cpoint_a)
					self.start = Vector((x,y,0))
					if ctx.space_data.local_view:
						self.subclass.owner.local_view_set(ctx.space_data, True)
					####################################################################################################
					# if self.gride == None:
					# 	location, normal, _, _ = ray_cast(ctx, x, y)
					# 	print("Normal", normal)
						# if location:
							# self.gride = AutoGride(location, normal)
							# print(location, normal)
							# rotation = self.gride.rotation_matrix
							# print(rotation)
							# matt = Matrix.Translation(normal)
							# d = rotaion_eular(matt)
							# print("direction: ", matt, d.x, d.y, d.z, normal)
							# bpy.ops.object.empty_add(type='ARROWS', align='WORLD', location=location, rotation=direction, scale=(1, 1, 1))
						# else:
						# 	self.gride = AutoGride(self.cpoint_o.view, self.cpoint_o.view, Vector((0,0,1)))
						# rotation = self.gride.rotation_matrix
						# bpy.ops.object.empty_add(type='ARROWS', align='WORLD', location=location, rotation=rotation, scale=(1, 1, 1))


					###################################################################################################
				if event.value == 'PRESS':
					self.state = True
				if event.value =='RELEASE':
					self.state = self.drag = False
					self.step += 1
					self.cpoint_a = self.cpoint_b
					self.end = Vector((x,y,0))

			if event.type in self.requestkey:
				self.event(event.type, event.value)
				dimantion.from_click_points(self.cpoint_a, self.cpoint_b, self.cpoint_o)	
				self.update(ctx, self.step, dimantion)

			if event.type == 'MOUSEMOVE':
				if self.state:
					self.drag = True
				if self.step > 0:
					dimantion.from_click_points(self.cpoint_a, self.cpoint_b, self.cpoint_o)
					self.update(ctx, self.step, dimantion)
					#################################################
					self.end_point, self.end_normal, _, _ = ray_cast(ctx, x, y)
					#################################################
				if self.subclass.finishon > 0:
					if self.step >= self.subclass.finishon:
						self.step = 0
						""" Delete object if was very tiny """
						if not self.is_drawed_enough():
							self.subclass.abort()
						else:
							##############################################
							location = self.start_point
							normal = (self.start_normal + self.end_normal) / 2
							direction = (self.end_point - self.start_point).normalized()
							rotation_matrix = Matrix([direction, -direction.cross(normal), normal]).transposed()
							d = rotaion_eular(rotation_matrix)
							print(rotation_matrix, d)
							# bpy.ops.object.empty_add(type='ARROWS', align='WORLD', location=location, rotation=d, scale=(1, 1, 1))
							##############################################
							self.finish()
							bpy.ops.ed.undo_push()
						self.subclass.reset()

			if event.type in self.cancelkeys or self.forcefinish:
				self.forcefinish = False
				###########################################
				# RemoveCursurOveride(self.drawhandler)
				###########################################
				if self.step > 0:
					self.subclass.abort()
				self.subclass.reset()
				return {'CANCELLED'}

		return {'RUNNING_MODAL'}

	def invoke(self, ctx, event):
		############################################
		# self.drawhandler = AddCursurOveride(self)
		ctx.window_manager.modal_handler_add(self)
		return {'RUNNING_MODAL'}

class PrimitiveGeometryClass:
	def create_mesh(self, ctx, meshdata, classname):
		verts,edges,faces, = meshdata
		newmesh = bpy.data.meshes.new(classname)
		newmesh.from_pydata(verts,edges,faces)
		newmesh.update(calc_edges=True)
		self.owner = bpy.data.objects.new(classname,newmesh)
		link_to_scene(ctx, self.owner)
		set_as_active_object(ctx,self.owner)
		self.data = self.owner.data
		self.data.use_auto_smooth = True

	def update_mesh(self, meshdata):
		if self.data != None and bpy.context.mode == 'OBJECT':
			verts,edges,faces, = meshdata
			""" Genarate New Data """
			# ver = bpy.app.version
			# if ver[0] == 2 and ver[1] == 80:
			if True:
				""" old method for V2.80 """
				orgmesh = bpy.data.meshes[self.data.name]
				tmpmesh = bpy.data.meshes.new("_NewTempMesh_")
				tmpmesh.from_pydata(verts, edges, faces)
				bm = bmesh.new()
				bm.from_mesh(tmpmesh)
				bm.to_mesh(orgmesh.id_data)
				bm.free()
				bpy.data.meshes.remove(tmpmesh)
				for f in self.data.polygons:
					f.use_smooth = True
			else:
				""" new method for V2.81 and above """
				self.data.clear_geometry()
				self.data.from_pydata(verts, edges, faces)
				""" Note this method is faster but clear the keyframes too """
				""" I had to skip this part till I find a solution for this """

class PrimitiveCurveClass:
	def __init__(self):
		self.close = False
	def create_curve(self, ctx, shapes, classname):
		# Create Spline
		newcurve = bpy.data.curves.new(classname, type='CURVE')
		newcurve.dimensions = '3D'
		curve_from_shapes(newcurve, shapes, self.close)
		# Create object and link to collection
		self.owner = bpy.data.objects.new(classname, newcurve)
		link_to_scene(ctx, self.owner)
		set_as_active_object(ctx, self.owner)
		self.data = self.owner.data
	def update_curve(self, shapes):
		if self.data != None and bpy.context.mode == 'OBJECT':
			curve = bpy.data.curves[self.data.name]
			curve_from_shapes(curve, shapes, self.close)

# Create Curve from Splines in the shape Data
def curve_from_shapes(curve, shapes, close):
	""" put BsMax primitive Shape Date in to Blender Curve Data """
	curve.splines.clear()
	for shape in shapes:
		count = len(shape)
		newspline = curve.splines.new('BEZIER')
		newspline.bezier_points.add(count - 1)
		for i in range(count):
			bez = newspline.bezier_points[i]
			bez.co, bez.handle_left, bez.handle_left_type, bez.handle_right, bez.handle_right_type = shape[i]
		newspline.use_cyclic_u = close

def ClearPrimitiveData(obj):
	if obj != None:
		obj.primitivedata.classname = ""

# Overide mouse pointer
def GetCursurMesh(size, x, y):
	shape =((0.4, 0.0), (0.6, 0.0), (0.6, 0.4),
			(1.0, 0.4), (1.0, 0.6), (0.6, 0.6),
			(0.6, 1.0), (0.4, 1.0), (0.4, 0.6),
			(0.0, 0.6), (0.0, 0.4), (0.4, 0.4))
	verts = []
	offset_x = x - size / 2
	offset_y = y - size / 2
	for i in range(len(shape)):
		xpos = shape[i][0] * size + offset_x
		ypos = shape[i][1] * size + offset_y
		verts.append((xpos, ypos))
	faces =((0, 1, 11), (1, 2, 11),
			(2, 3, 5), (3, 4, 5),
			(5, 6, 7), (7, 8, 5),
			(8, 9, 11), (11, 9, 10))
	return verts, faces

def DrawCursurOveride(self):
	pass
	# bgl.glEnable(bgl.GL_BLEND)
	# shader = gpu.shader.from_builtin('2D_UNIFORM_COLOR')
	# v,f = GetCursurMesh(20,self.mpos.x, self.mpos.y)
	# batch = batch_for_shader(shader,'TRIS',{"pos":v},indices=f)
	# shader.bind()
	# shader.uniform_float("color",(0.8,0.8,0.8,0.6))
	# batch.draw(shader)
	# bgl.glDisable(bgl.GL_BLEND)

def AddCursurOveride(self):
	SV3D = bpy.types.SpaceView3D
	handle = SV3D.draw_handler_add(DrawCursurOveride, tuple([self]), 
						'WINDOW', 'POST_PIXEL')
	return handle

def RemoveCursurOveride(handle):
	bpy.types.SpaceView3D.draw_handler_remove(handle, 'WINDOW')

def is_true_class(ctx, classname):
	if ctx.active_object != None:
		if classname == ctx.active_object.primitivedata.classname:
			return True
	return False

#########################################################################


############# Create tepot for test normal direction ##############
def get_path(part):
	body_path = Spline(None)
	points = []
	if part == 'body':
		points = (((0,0,0),(0,0,0),(0.358946,0,0.00480962)),
			((0.774773,0,-0.000830472),(0.75,0,0.075),(0.791808,0,0.150003)),
			((0.978876,0,0.20208),(1,0,0.45),(1.02112,0,0.69792)),
			((0.805268,0,1.06392),(0.750701,0,1.2012),(0.695276,0,1.29381)),
			((0.676157,0,1.2304),(0.7,0,1.2),(0.7,0,1.2)))
	elif part == 'lid':
		points = (((0,0,1.575),(0,0,1.575),(0.400656,0,1.56443)),
			((0.00236605,0,1.43537),(0.1,0,1.35),(0.211611,0,1.27556)),
			((0.657876,0,1.26831),(0.65,0,1.2),(0.65,0,1.2)))
	elif part == 'spout_a':
		points = (((0.85,0,0.7125),(0.85,0,0.7125),(1.30583,0,0.724497)),
			((1.15645,0,1.0605),(1.35,0,1.2),(1.39425,0,1.23295)),
			((1.45212,0,1.24122),(1.4,0,1.2),(1.4,0,1.2)))
	elif part == 'spout_b':
		points = (((0.848828,0,0.3),(0.848828,0,0.3),(1.5298,0,0.39321)),
			((1.22074,0,1.03193),(1.65,0,1.2),(1.70914,0,1.22046)),
			((1.78246,0,1.27581),(1.6,0,1.2),(1.6,0,1.2)))
	elif part == 'spout_s':
		points = (((0,0.2475,0),(0,0.2475,0),(0,0.24786,0)),
			((0,0.0876482,0),(0,0.09375,0),(0,0.0926101,0)),
			((0,0.0610992,0),(0,0.05625,0),(0,0.05625,0)))
	elif part == 'handle_a':
		points = (((-0.75,0,1.125),(-0.75,0,1.125),(-0.999939,0,1.12514)),
			((-1.51932,0,1.16786),(-1.5,0,0.9),(-1.47991,0,0.621563)),
			((-1.2955,0,0.456572),(-0.95,0,0.3),(-0.95,0,0.3)))
	elif part == 'handle_b':
		points = (((-0.8,0,1.0125),(-0.8,0,1.0125),(-1.01763,0,0.999294)),
			((-1.34732,0,1.04424),(-1.35,0,0.9),(-1.35272,0,0.753523)),
			((-1.19108,0,0.528823),(-1,0,0.45),(-1,0,0.45)))
	elif part == 'handle_s':
		points = (((0,0.112449,0),(0,0.112449,0),(0,0.112449,0)),
			((0,0.112449,0),(0,0.112449,0),(0,0.112449,0)),
			((0,0.112449,0),(0,0.112449,0),(0,0.112449,0)))
	for p in points:
		newbp = Bezier_point(None)
		newbp.handle_left = Vector((p[0]))
		newbp.co = Vector((p[1]))
		newbp.handle_right = Vector((p[2]))
		body_path.bezier_points.append(newbp)
	return body_path

def get_ring(point1, point2, scale):
	ring = Spline(None)
	d = Vector((0,scale*1.25,0))
	p1 = Bezier_point(None)
	p2 = Bezier_point(None)
	p1.handle_left = point1+d
	p1.co = point1
	p1.handle_right = point1-d
	ring.bezier_points.append(p1)
	p2.handle_left = point2-d
	p2.co = point2
	p2.handle_right = point2+d
	ring.bezier_points.append(p2)
	ring.use_cyclic_u = True
	return ring

def get_verts_body(spline,ssegs,scale):
	verts = []
	for index in range(len(spline.bezier_points)):
		a,b,c,d = spline.get_segment(index)
		for j in range(ssegs):
			t = (1/ssegs)*j
			newvert = point_on_vector(a,b,c,d,t)
			verts.append(newvert*scale)
	return verts

def get_verts_pipe(spline,ssegs,scale):
	verts = []
	if spline.use_cyclic_u:
		for index in range(len(spline.bezier_points)):
			a,b,c,d = spline.get_segment(index)
			for j in range(ssegs):
				t = (1/ssegs)*j
				newvert = point_on_vector(a,b,c,d,t)
				verts.append(newvert*scale)
	else:
		for index in range(len(spline.bezier_points)-1):
			a,b,c,d = spline.get_segment(index)
			for j in range(ssegs):
				t = (1/ssegs)*j
				newvert = point_on_vector(a,b,c,d,t)
				verts.append(newvert*scale)
			if index == len(spline.bezier_points)-2:
				verts.append(d*scale)
	return verts

def get_teapot_mesh(radius,csegs,body,handle,spout,lid):
	verts,edges,faces = [],[],[]
	cs = csegs*4
	step = (pi*2)/cs

	def create_body(line,flip):
		f = len(verts) # First vertex of element

		""" Create vertexes """
		path = get_path(line)
		sides = get_verts_body(path,csegs,radius)
		l = len(sides)-1
		verts.append(sides[0])

		for i in range(1,l):
			x = sides[i].x
			for j in range(cs):
				d = j*step
				X = sin(d)*x 
				Y = cos(d)*x
				Z = sides[i].z
				verts.append([X,Y,Z])

		""" first triangle faces """
		for i in range(cs):
			newface = (f,f+i,f+i+1) if flip else (f+i+1,f+i,f)
			faces.append(newface)
		newface = (f,f+cs,f+1) if flip else (f+1,f+cs,f)
		faces.append(newface)
				
		faces.append((0,cs,1))
		""" faces """
		f += 1 # First vertex of element
		for i in range(l-2):
			for j in range(cs):
				a = f+j+(i*cs)
				if j < cs-1:
					b = a+1
					c = a+cs+1
					d = c-1
				else: 
					b = f+i*cs
					c = a+1
					d = a+cs
				newface = (d,c,b,a) if flip else (a,b,c,d)
				faces.append(newface)

	def create_pipe(line1, line2, line3,flip):
		f = len(verts)
		""" create vertexes """
		spline1 = get_path(line1)
		spline2 = get_path(line2)
		spline3 = get_path(line3)
		v1 = get_verts_pipe(spline1,csegs,radius)
		v2 = get_verts_pipe(spline2,csegs,radius)
		v3 = get_verts_pipe(spline3,csegs,radius)
		for p1,p2,p3 in zip(v1,v2,v3):
			ring = get_ring(p1,p2,p3.y)
			vert = get_verts_pipe(ring,csegs,1)
			for v in vert:
				verts.append(v)
		""" faces """
		ssegs = csegs*2
		for i in range(len(v1)-1):
			for j in range(ssegs):
				a = f+i*ssegs+j
				if j < ssegs-1:
					b = a+1
					c = a+ssegs+1
					d = c-1
				else:
					b = f+i*ssegs
					c = b+ssegs
					d = a+ssegs
				newface = (d,c,b,a) if flip else (a,b,c,d)
				faces.append(newface)
	if body:
		create_body('body',True)
	if lid:
		create_body('lid',False)
	if handle:
		create_pipe("handle_a","handle_b","handle_s",True)
	if spout:
		create_pipe("spout_a","spout_b","spout_s",False)

	return verts,edges,faces

class Teapot(PrimitiveGeometryClass):
	def __init__(self):
		self.classname = "Teapot"
		self.finishon = 2
		self.owner = None
		self.data = None
		""" Default Settings """
		self.auto_smooth_angle = 1.5708
	def reset(self):
		self.__init__()
	def create(self, ctx):
		mesh = get_teapot_mesh(0,4,True,True,True,True)
		self.create_mesh(ctx, mesh, self.classname)
		pd = self.data.primitivedata
		pd.classname = self.classname
		pd.csegs = 4
		pd.bool1,pd.bool2,pd.bool3,pd.bool4 = True,True,True,True
		""" Apply Default Settings """
		self.data.auto_smooth_angle = self.auto_smooth_angle
	def update(self):
		pd = self.data.primitivedata
		mesh = get_teapot_mesh(pd.radius1,pd.csegs,pd.bool1,pd.bool2,pd.bool3,pd.bool4)
		self.update_mesh(mesh)
	def abort(self):
		delete_objects([self.owner])

class Create_OT_Teapot_test(CreatePrimitive):
	bl_idname = "create.teapot_test"
	bl_label = "Teapot (Test)"
	subclass = Teapot()

	def create(self, ctx, clickpoint):
		self.subclass.create(ctx)
		self.params = self.subclass.owner.data.primitivedata
		self.subclass.owner.location = clickpoint.view
		self.subclass.owner.rotation_euler = clickpoint.orient
	def update(self, ctx, clickcount, dimantion):
		if clickcount == 1:
			self.params.radius1 = dimantion.radius
		if clickcount > 0:
			self.subclass.update()
	def finish(self):
		pass

def register_test_teapot():
	bpy.utils.register_class(Create_OT_Teapot_test)

def unregister_test_teapot():
	bpy.utils.unregister_class(Create_OT_Teapot_test)

if __name__ == '__main__':
    register_test_teapot()