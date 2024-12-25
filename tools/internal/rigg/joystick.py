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
#2024/09/11

#TODO need to mode simplify and cleanup

import bpy

from bpy.types import Operator
from bpy.props import IntProperty, EnumProperty
from mathutils import Vector
from bpy.utils import register_class, unregister_class

from bsmax.state import get_obj_class

from bsmax.actions import (
	set_origen, set_as_active_object, catche_collection, move_to_collection
)


def get_joystic_class(obj):
	obj_class = get_obj_class(obj)
	if obj_class == 'Rectangle':
		width = obj.data.primitivedata.width
		length = obj.data.primitivedata.length

		if length < width / 2:
			return 'HORIZONTAL_SLIDER'

		if width < length / 2:
			return 'VERTICAL_SLIDER'

		return 'RECTANGLE_JOYSTICK'

	if obj_class == 'Circle':
		return 'CIRCLE_JOYSTICK'
	
	return ''


def get_handle_radius(obj, joy_type):
	width = obj.data.primitivedata.width
	length = obj.data.primitivedata.length
	radius = obj.data.primitivedata.radius1

	if joy_type == 'RECTANGLE_JOYSTICK': 
		return (width + length) / 15.0

	elif joy_type in {'VERTICAL_SLIDER', 'HORIZONTAL_SLIDER'}:
		return (min(width, length) / 2)

	elif joy_type == 'CIRCLE_JOYSTICK':
		return radius / 5


def create_rectangle_frame_Mesh(ctx, mode, rectangle):

	width = round(rectangle.data.primitivedata.width, 3)
	length = round(rectangle.data.primitivedata.length, 3)
	name = "Joystic_Frame_" + str(mode) + "_" + str(width) + "X" + str(length)

	if name in bpy.data.objects:
		bpy.ops.object.select_all(action='DESELECT')
		rectangle.select_set(True)
		bpy.ops.object.delete(confirm=False)
		return bpy.data.objects[name]
	
	rectangle.name = name

	# fix orient
	bpy.ops.transform.rotate(
		value=-1.5708,
		orient_axis='X',
		orient_type='LOCAL',
		orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)),
		orient_matrix_type='LOCAL',
		constraint_axis=(True, False, False)
	)

	# convert (curve) frame to mesh
	bpy.ops.object.mode_set(mode='OBJECT', toggle=False)
	bpy.ops.object.select_all(action='DESELECT')
	rectangle.select_set(state=True)
	bpy.ops.object.convert(target='MESH')
	collection = catche_collection(ctx, "Joystick_Meshes")
	move_to_collection(rectangle, collection)
	rectangle.location = [0, 0, 0]

	return rectangle


def catch_circilar_frame(ctx):
	""" Find or Create a mesh for joystic Frame bone
		args:
			ctx: bpy.context
		return:
			object
	"""
	name = 'Joystic_Circle_Mesh'
	if name in bpy.data.objects:
		return bpy.data.objects[name]

	# Create new one
	bpy.ops.mesh.primitive_circle_add(radius=1, location=(0,0,0), vertices=32)
	joy_mesh = ctx.active_object
	joy_mesh.name = name
	collection = catche_collection(ctx, "Joystick_Meshes")
	move_to_collection(joy_mesh, collection)

	return joy_mesh


def catche_joy_mesh(ctx):
	""" Find or Create a mesh for joystic handle bone
		args:
			ctx: bpy.context
		return:
			object
	"""
	name = 'Joystic_handle_Mesh'
	if name in bpy.data.objects:
		return bpy.data.objects[name]
	
	if ctx.mode != 'OBJECT':
		bpy.ops.object.mode_set(mode='OBJECT', toggle=False)
	
	# Create new one
	bpy.ops.mesh.primitive_circle_add(radius=1, location=(0,0,0), vertices=16)
	joy_mesh = ctx.active_object
	joy_mesh.name = name
	bpy.ops.object.mode_set(mode='EDIT', toggle=False)
	bpy.ops.mesh.select_all(action='SELECT')
	bpy.ops.mesh.edge_face_add()
	bpy.ops.object.mode_set(mode='OBJECT', toggle=False)
	collection = catche_collection(ctx, "Joystick_Meshes")
	move_to_collection(joy_mesh, collection)
	
	return joy_mesh


def create_armature(
		ctx, name, frame_mesh, joy_mesh, frame_radius, joy_radius):

	# Create armature 
	bpy.ops.object.armature_add(location=(0, 0, 0))
	joystick = ctx.active_object
	joystick.name = name
	
	bpy.ops.object.mode_set(mode='EDIT', toggle=False)
	joystick.data.edit_bones[0].name = 'Frame'
	
	if joy_mesh:
		bpy.ops.armature.select_all(action='SELECT')
		bpy.ops.armature.duplicate('INVOKE_DEFAULT')
		joystick.data.edit_bones[1].name = 'Joy'
		joystick.data.edit_bones['Joy'].parent = joystick.data.edit_bones['Frame']

	bpy.ops.object.mode_set(mode='OBJECT', toggle=False)

	joystick.location = frame_mesh.location
	joystick.data.bones['Frame'].use_deform = False
	joystick.pose.bones['Frame'].custom_shape = frame_mesh

	joystick.pose.bones['Frame'].custom_shape_scale_xyz = [
		frame_radius, frame_radius, 1
	]

	if joy_mesh:
		joystick.data.bones['Joy'].use_deform = False
		joystick.pose.bones['Joy'].custom_shape = joy_mesh

		joystick.pose.bones['Joy'].custom_shape_scale_xyz = [
			joy_radius, joy_radius, 1
		]

	set_as_active_object(ctx, joystick)

	return joystick


def match_transform(source, target):
	# Set Transform
	source.scale = target.scale
	source.rotation_euler.x = target.rotation_euler.x
	source.rotation_euler.y = target.rotation_euler.y
	source.rotation_euler.z = target.rotation_euler.z


def create_circle_joystick(ctx, circle, joy_type):
	global joystick_data
	matrix_world = circle.matrix_world.copy()
	frame_radius = circle.data.primitivedata.radius1
	joy_radius = get_handle_radius(circle, joy_type)

	name = circle.name

	bpy.ops.object.select_all(action='DESELECT')
	circle.select_set(True)
	bpy.ops.object.delete(confirm=False)

	circle = catch_circilar_frame(ctx)
	joy_mesh = catche_joy_mesh(ctx)

	joystick = create_armature(
		ctx, name, circle, joy_mesh, frame_radius, joy_radius
	)

	joystick.matrix_world = matrix_world
	
	match_transform(joystick, circle)

	# setup constraints
	bpy.ops.object.mode_set(mode='POSE', toggle=False)

	distance = frame_radius - joy_radius
	
	consl = joystick.pose.bones['Joy'].constraints.new('LIMIT_LOCATION')
	consl.use_transform_limit = True
	consl.owner_space = 'LOCAL'
	consl.use_min_x = consl.use_max_x = True
	consl.use_min_y = consl.use_max_y = True
	consl.use_min_z = consl.use_max_z = True
	consl.min_x, consl.max_x = -distance, distance
	consl.min_y, consl.max_y = -distance, distance

	consd = joystick.pose.bones['Joy'].constraints.new('LIMIT_DISTANCE')
	consd.target = joystick
	consd.subtarget = "Frame"
	consd.target_space = 'LOCAL'
	consd.owner_space = 'LOCAL'
	consd.distance = distance
	consd.use_transform_limit = True
	consd.target_space = 'LOCAL_WITH_PARENT'
	consd.owner_space = 'LOCAL_WITH_PARENT'

	bpy.ops.object.mode_set(mode='OBJECT', toggle=False)


def create_rectangle_joystick(ctx, rectangle, joy_type):
	global joystick_data
	mode = joystick_data.mode
	matrix_world = rectangle.matrix_world.copy()
	width = rectangle.data.primitivedata.width
	length = rectangle.data.primitivedata.length
	radius = get_handle_radius(rectangle, joy_type)
	rectangle.data.primitivedata.chamfer1 = radius

	if mode in [1,4,7]:
		x_offset = width / 2 - radius

	elif mode in [3,6,9]:
		x_offset = -(width / 2 - radius)

	else:
		x_offset = 0

	if mode in [1,2,3]:
		y_offset = -(length / 2 - radius)

	elif mode in [7,8,9]:
		y_offset = length / 2 - radius

	else:
		y_offset = 0
	
	location = matrix_world.translation - Vector((x_offset,0, y_offset))
	set_origen(ctx, rectangle, location)
	name = rectangle.name
	rectangle = create_rectangle_frame_Mesh(ctx, mode, rectangle)
	joy_mesh = None if mode == 10 else catche_joy_mesh(ctx)
	joystick = create_armature(ctx, name, rectangle, joy_mesh, 1, radius)

	joystick.matrix_world = matrix_world
	joystick.location = location
	match_transform(joystick, rectangle)

	# do not continue if mode is frame only
	if mode == 10:
		return

	# setup constraints
	bpy.ops.object.mode_set(mode='POSE', toggle=False)
	
	cons = joystick.pose.bones['Joy'].constraints.new('LIMIT_LOCATION')
	cons.use_transform_limit = True
	cons.owner_space = 'LOCAL'

	cons.use_min_x = cons.use_max_x = True
	cons.use_min_y = cons.use_max_y = True
	cons.use_min_z = cons.use_max_z = True

	if joy_type in ['RECTANGLE_JOYSTICK','HORIZONTAL_SLIDER']:
		cons.min_x = -(width / 2 - radius) + x_offset
		cons.max_x = width / 2 - radius + x_offset

	if joy_type in ['RECTANGLE_JOYSTICK','VERTICAL_SLIDER']:
		cons.min_y = -(length / 2 - radius) + y_offset
		cons.max_y = length / 2 - radius + y_offset
	
	bpy.ops.object.mode_set(mode='OBJECT', toggle=False)


class Joystick_Creator_Data:
	def __init__(self):
		# pass value from an operator to silent run
		self.mode = 0

joystick_data = Joystick_Creator_Data()


def get_arrow_panel(op, self):
	global joystick_data
	mode = joystick_data.mode
	layout = self.layout
	col = layout.column(align=True)
	row = col.row(align=True)

	if self.type == 'RECTANGLE_JOYSTICK':
		row.operator(op, text='', icon='BLANK1').mode = 1

	if self.type in {'RECTANGLE_JOYSTICK', 'VERTICAL_SLIDER'}:
		row.operator(op, text='', icon='TRIA_UP').mode = 2

	if self.type == 'RECTANGLE_JOYSTICK':
		row.operator(op, text='', icon='BLANK1').mode = 3

	row = col.row(align = True)

	if self.type in {'RECTANGLE_JOYSTICK', 'HORIZONTAL_SLIDER'}:
		row.operator(op, text='', icon='TRIA_LEFT').mode = 4

	row.operator(op, text='', icon='DOT').mode = 5

	if self.type in {'RECTANGLE_JOYSTICK', 'HORIZONTAL_SLIDER'}:
		row.operator(op, text='', icon='TRIA_RIGHT').mode = 6

	row = col.row(align = True)

	if self.type == 'RECTANGLE_JOYSTICK':
		row.operator(op, text='', icon='BLANK1').mode = 7

	if self.type in {'RECTANGLE_JOYSTICK', 'VERTICAL_SLIDER'}:
		row.operator(op, text='', icon='TRIA_DOWN').mode = 8

	if self.type == 'RECTANGLE_JOYSTICK':
		row.operator(op, text='', icon='BLANK1').mode = 9

	col = layout.column()
	col.operator(op, text='', icon='MESH_PLANE').mode = 10
	
	if mode == 1:
		text = 'Up Left'
	elif mode == 2:
		text = 'Up'
	elif mode == 3:
		text = 'Up Right'
	elif mode == 4:
		text = 'Left'
	elif mode == 5:
		text = 'Center'
	elif mode == 6:
		text = 'Right'
	elif mode == 7:
		text = 'Down Left'
	elif mode == 8:
		text = 'Down'
	elif mode == 9:
		text = 'Down Right'
	elif mode == 10:
		text = 'Frame Only'
	else:
		text = ''

	col.label(text=text)


class Rigg_TO_Joystick_Creator(Operator):
	bl_idname = 'rigg.joystick_creator'
	bl_label = "Joystick Creator"
	bl_description = "Convert Selected Rectangle or Circle to Joystick"
	bl_options = {'REGISTER', 'UNDO'}

	mode: IntProperty() # type: ignore
	type = ''

	@classmethod
	def poll(self, ctx):
		if ctx.area.type == 'VIEW_3D':
			return get_obj_class(ctx.object) in {'Rectangle', 'Circle'}
		return False

	def draw(self, ctx):
		get_arrow_panel('rigg.joystick_creator', self)

	def execute(self, ctx):
		global joystick_data
		create_rectangle_joystick(ctx, ctx.object, self.type)
		joystick_data.mode = 0
		return {'FINISHED'}

	def invoke(self, ctx, event):
		if self.mode == 0:
			self.type = get_joystic_class(ctx.object)
			if self.type == 'CIRCLE_JOYSTICK':
				create_circle_joystick(ctx, ctx.object, self.type)

			elif self.type in {'HORIZONTAL_SLIDER',
								'VERTICAL_SLIDER',
								'RECTANGLE_JOYSTICK'}:
				return ctx.window_manager.invoke_props_dialog(self, width=62)

			else:
				return {'CANCELLED'}

		elif self.mode > 0:
			global joystick_data
			joystick_data.mode = self.mode

		return {'CANCELLED'}


class Rigg_TO_Joystick_Shapekey_Connector(Operator):
	""" Select Armature contain Joystick and Mesh contain
		Shape keys and run this operator
	"""
	bl_idname = 'rigg.joystick_shapekey_connector'
	bl_label = "Joystick Connecotr"
	bl_description = "Connect Joystick to Shapekey"
	bl_options = {'REGISTER', 'UNDO'}

	@classmethod
	def poll(self, ctx):
		if ctx.area.type == 'VIEW_3D':
			if ctx.mode == 'OBJECT':
				if len(ctx.selected_objects) == 2:
					o = ctx.selected_objects
					if o[0].type == 'ARMATURE' and o[1].type == 'MESH':
						return True
					if o[0].type == 'MESH' and o[1].type == 'ARMATURE':
						return True
		return False
	
	def coolect_joys(self, ctx):
		active_obj = ctx.active_object
		armatuar = active_obj if active_obj.type == 'ARMATURE' else None

		if armatuar:
			joys = []
			for b in armatuar.pose.bones:
				for c in b.constraints:
					is_joystick = False
					if c.type == 'LIMIT_LOCATION':
						is_joystick = c.use_min_x and c.use_max_x and \
							c.use_min_y and c.use_max_y and \
							c.use_min_z and c.use_max_z and \
							c.use_transform_limit and \
							c.owner_space == 'LOCAL' and c.influence == 1 and \
							c.max_z == 0 and c.min_z == 0

					if is_joystick:
						joys.append(b.name)

			return [(j, j, '') for j in joys]
		else:
			return [('None', 'None', '')]

	joystick: EnumProperty(items=coolect_joys) # type: ignore
	
	items = []
	def collect_shapekeys(self, ctx):
		shell = None
		for obj in ctx.selected_objects:
			if obj.type in {'MESH', 'CURVE'}:
				shell = obj
		items = [('None', '', '')]

		if shell != None:
			names = [
				n.name for n in shell.data.shape_keys.key_blocks
					if n.name != 'Basis'
			]
			
			items += [(n, n, '') for n in names]

		return items

	up: EnumProperty(items=collect_shapekeys) # type: ignore
	upright: EnumProperty(items=collect_shapekeys) # type: ignore
	right: EnumProperty(items=collect_shapekeys) # type: ignore
	downright: EnumProperty(items=collect_shapekeys) # type: ignore
	down: EnumProperty(items=collect_shapekeys) # type: ignore
	downleft: EnumProperty(items=collect_shapekeys) # type: ignore
	left: EnumProperty(items=collect_shapekeys) # type: ignore
	upleft: EnumProperty(items=collect_shapekeys) # type: ignore

	def get_expration(self, direction, joy):
		# rectangular joystic
		for c in joy.constraints:
			if c.type == 'LIMIT_LOCATION':
				const = c
				break	
		minx, maxx = str(const.min_x), str(const.max_x)
		miny, maxy = str(const.min_y), str(const.max_y)

		# circular joystic
		if minx == 0 and maxx == 0 and miny == 0 and maxy == 0:
			for c in joy.constraints:
				if c.type == 'LIMIT_DISTANCE':
					const = c
					break
			minx, maxx = -const.distance, const.distance
			miny, maxy = -const.distance, const.distance


		if direction == 1: # up left #
			return '(min(0,varx)/' + minx + ')*(max(0,vary)/' + maxy + ')'

		elif direction == 2: # up #
			return 'var/' + maxy

		elif direction == 3: # up right #
			return '(max(0,varx)/' + maxx + ')*(max(0,vary)/' + maxy + ')'

		elif direction == 4: # left #
			return 'var/' + minx

		elif direction == 6: # right #
			return 'var/' + maxx

		elif direction == 7: # down left #
			return '(min(0,varx)/' + minx + ')*(min(0,vary)/' + miny + ')'

		elif direction == 8: # down #
			return 'var/' + miny

		elif direction == 9: # down right #
			return '(max(0,varx)/' + maxx + ')*(min(0,vary)/' + miny + ')'

		else:
			return '0'

	def add_var(self, driver, name, armatuar, joy):
		var = driver.driver.variables.new()
		var.name = name
		var.type = 'TRANSFORMS'
		var.targets[0].id = armatuar
		var.targets[0].bone_target = joy.name
		var.targets[0].transform_space = 'LOCAL_SPACE'
		return var.targets[0]
	
	def set_driver(self, armatuar, joy, direction, shell, shape_key):
		key_block = shell.data.shape_keys.key_blocks[shape_key]
		key_block.driver_remove('value')
		driver = key_block.driver_add('value')
		driver.driver.type = 'SCRIPTED'
		if direction in [2,4,6,8]:
			target = self.add_var(driver, 'var', armatuar, joy)
			if direction in [2,8]:
				target.transform_type = 'LOC_Y'
			else:
				target.transform_type = 'LOC_X'
		if direction in [1,3,7,9]:
			targetx = self.add_var(driver, 'varx', armatuar, joy)
			targetx.transform_type = 'LOC_X'
			targety = self.add_var(driver, 'vary', armatuar, joy)
			targety.transform_type = 'LOC_Y'
		driver.driver.expression = self.get_expration(direction, joy)
	
	def execute(self, ctx):
		armatuar,shell = None, None
		for obj in ctx.selected_objects:
			if obj.type == 'ARMATURE':
				armatuar = obj
			elif obj.type in {'MESH', 'CURVE'}:
				shell = obj
		if armatuar != None and shell != None:
			joy = armatuar.pose.bones[self.joystick]

			if self.up != 'None':
				self.set_driver(armatuar, joy, 2, shell, self.up)
			if self.upright != 'None':
				self.set_driver(armatuar, joy, 3, shell, self.upright)
			if self.right != 'None':
				self.set_driver(armatuar, joy, 6, shell, self.right)
			if self.downright != 'None':
				self.set_driver(armatuar, joy, 9, shell, self.downright)
			if self.down != 'None':
				self.set_driver(armatuar, joy, 8, shell, self.down)
			if self.downleft != 'None':
				self.set_driver(armatuar, joy, 7, shell, self.downleft)
			if self.left != 'None':
				self.set_driver(armatuar, joy, 4, shell, self.left)
			if self.upleft != 'None':
				self.set_driver(armatuar, joy, 1, shell, self.upleft)
			
			bpy.ops.object.mode_set(mode='OBJECT', toggle=False)
		return {'FINISHED'}

	def draw(self, ctx):
		layout = self.layout
		box = layout.box()
		box.label(text='Select Joystick')
		box.prop(self, 'joystick')
		box = layout.box()
		box.label(text='Direction')
		col = box.column(align=True)
		row = col.row(align=True)
		row.prop(self, 'upleft', text='')
		row.prop(self, 'up', text='')
		row.prop(self, 'upright', text='')
		row = col.row(align=True)
		row.prop(self,'left',text='')
		row.label(text='')
		row.prop(self, 'right', text='')
		row = col.row(align = True)
		row.prop(self, 'downleft', text='')
		row.prop(self, 'down', text='')
		row.prop(self, 'downright', text='')
	
	def reset_enoms(self):
		# TODO check for has data or not
		try:
			self.up = 'None'
			self.upright = 'None'
			self.right = 'None'
			self.downright = 'None'
			self.down = 'None'
			self.downleft = 'None'
			self.left = 'None'
			self.upleft = 'None'
		except:
			pass

	def invoke(self, ctx, event):
		for obj in ctx.selected_objects:
			if obj.type == 'ARMATURE':
				armatuar = obj
			elif obj.type in {'MESH', 'CURVE'}:
				shell = obj
		if armatuar:
			set_as_active_object(ctx, armatuar)
		if shell:
			shell.select_set(state=True)
		self.reset_enoms()
		return ctx.window_manager.invoke_props_dialog(self, width=400)


def joystick_connectore_menu(self, ctx):
	layout = self.layout
	layout.separator()
	layout.operator('rigg.joystick_shapekey_connector')
	#TODO temprary location for this operator
	# layout.operator('modifier.copy_selected')


classes = {
	Rigg_TO_Joystick_Creator,
	Rigg_TO_Joystick_Shapekey_Connector
}


def register_joystic():
	for cls in classes:
		register_class(cls)
	bpy.types.VIEW3D_MT_make_links.append(joystick_connectore_menu)


def unregister_joystic():
	bpy.types.VIEW3D_MT_make_links.remove(joystick_connectore_menu)
	for cls in classes:
		unregister_class(cls)


if __name__ == '__main__':
	register_joystic()
