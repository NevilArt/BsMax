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
from bpy.props import IntProperty, EnumProperty
from mathutils import Vector
from bsmax.state import get_obj_class
from bsmax.actions import set_origen, set_as_active_object



def get_joystic_mode(width, length):
	if length < width / 2:
		return 'h'
	if width < length / 2:
		return 'v'
	return 'j'



def get_joy_radius(width, length, orient):
	if orient == 'j': 
		return (width + length) / 15.0
	return (min(width, length) / 2)



def create_joystic(ctx, rectangle, mode):
	width = rectangle.data.primitivedata.width
	length = rectangle.data.primitivedata.length
	orient = get_joystic_mode(width, length)
	radius = get_joy_radius(width, length, orient)
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
	
	location = rectangle.location - Vector((x_offset,0, y_offset))
	set_origen(ctx, rectangle, location)

	""" fix orient """
	bpy.ops.transform.rotate(
			value=-1.5708,
			orient_axis='X',
			orient_type='LOCAL',
			orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)),
			orient_matrix_type='LOCAL',
			constraint_axis=(True, False, False),
			mirror=True,
			use_proportional_edit=False,
			proportional_edit_falloff='SMOOTH',
			proportional_size=1,
			use_proportional_connected=False,
			use_proportional_projected=False,
			release_confirm=True
		)

	""" convert the frame to mesh """
	bpy.ops.object.mode_set(mode='OBJECT', toggle=False)
	bpy.ops.object.select_all(action='DESELECT')
	rectangle.data.resolution_u = 8
	rectangle.select_set(state=True)
	bpy.ops.object.convert(target='MESH')

	""" Creaye circle for joystic """
	bpy.ops.mesh.primitive_circle_add(radius=radius, vertices=16)
	circle = ctx.active_object
	bpy.ops.object.mode_set(mode='EDIT', toggle=False)
	bpy.ops.mesh.select_all(action='SELECT')
	bpy.ops.mesh.edge_face_add()
	bpy.ops.object.mode_set(mode='OBJECT', toggle=False)

	bpy.ops.object.armature_add(location=(0,0,0))
	joystick = ctx.active_object
	joystick.name = "Joystick"
	bpy.ops.object.mode_set(mode='EDIT', toggle=False)
	bpy.ops.armature.select_all(action='SELECT')
	bpy.ops.armature.duplicate('INVOKE_DEFAULT')
	bpy.ops.object.mode_set(mode='OBJECT', toggle=False)
	joystick.location = location
	frame = joystick.data.bones[0]
	joy = joystick.data.bones[1]
	frame.name, joy.name = 'Frame', 'Joy'
	
	""" disable for diformation """
	frame.use_deform = False
	joy.use_deform = False

	""" Set Transform """
	joystick.scale = rectangle.scale
	joystick.rotation_euler.x = rectangle.rotation_euler.x
	joystick.rotation_euler.y = rectangle.rotation_euler.y
	joystick.rotation_euler.z = rectangle.rotation_euler.z
	""" Set Parent """
	bpy.ops.object.mode_set(mode='EDIT', toggle=False)
	joystick.data.edit_bones['Joy'].parent = joystick.data.edit_bones['Frame']
	""" setup constraints """
	bpy.ops.object.mode_set(mode='POSE', toggle=False)
	frame = joystick.pose.bones['Frame']
	joy = joystick.pose.bones['Joy']
	
	cons = joy.constraints.new('LIMIT_LOCATION')
	cons.use_transform_limit = True
	cons.owner_space = 'LOCAL'

	cons.use_min_x = cons.use_max_x = True
	cons.use_min_y = cons.use_max_y = True
	cons.use_min_z = cons.use_max_z = True

	if orient in ['j','h']:
		cons.min_x = -(width / 2 - radius) + x_offset
		cons.max_x = width / 2 - radius + x_offset
	if orient in ['j','v']:
		cons.min_y = -(length / 2 - radius) + y_offset
		cons.max_y = length / 2 - radius + y_offset
	
	""" Setup Display """
	frame.custom_shape = rectangle
	joy.custom_shape = circle
	
	""" Clear Scene """
	bpy.ops.object.mode_set(mode='OBJECT', toggle=False)
	objs = [rectangle,circle]
	bpy.ops.object.delete({'selected_objects': objs})

	""" frame only mode delete joystick """
	if mode == 10:
		bpy.ops.object.editmode_toggle()
		bpy.ops.armature.delete()
		bpy.ops.object.editmode_toggle()



#TODO convert to defined class rather than class itself
class JoyStickCreator:
	mode = 0
	direction = 0



def get_arrow_panel(op, layout, mode, orient):
	col = layout.column(align=True)
	row = col.row(align=True)
	if orient == 'j':
		row.operator(op, text='', icon='BLANK1').mode = 1
	if orient in {'j', 'v'}:
		row.operator(op, text='', icon='TRIA_UP').mode = 2
	if orient == 'j':
		row.operator(op, text='', icon='BLANK1').mode = 3
	row = col.row(align = True)
	if orient in {'j', 'h'}:
		row.operator(op, text='', icon='TRIA_LEFT').mode = 4
	row.operator(op, text='', icon='DOT').mode = 5
	if orient in {'j', 'h'}:
		row.operator(op, text='', icon='TRIA_RIGHT').mode = 6
	row = col.row(align = True)
	if orient == 'j':
		row.operator(op, text='', icon='BLANK1').mode = 7
	if orient in {'j', 'v'}:
		row.operator(op, text='', icon='TRIA_DOWN').mode = 8
	if orient == 'j':
		row.operator(op, text='', icon='BLANK1').mode = 9
	col = layout.column()
	col.operator(op, text='', icon='MESH_PLANE').mode = 10
	
	if mode == 1: text = 'Up Left'
	elif mode == 2: text = 'Up'
	elif mode == 3: text = 'Up Right'
	elif mode == 4: text = 'Left'
	elif mode == 5: text = 'Center'
	elif mode == 6: text = 'Right'
	elif mode == 7: text = 'Down Left'
	elif mode == 8: text = 'Down'
	elif mode == 9: text = 'Down Right'
	elif mode == 10: text = 'Frame Only'
	else: text = ''
	col.label(text=text)




class Rigg_TO_Joy_Stick_Creator(Operator):
	bl_idname = 'rigg.joy_stick_creator'
	bl_label = 'Joystick Creator'
	bl_description = 'Conver Selected Rectangle to Joystick'
	bl_options = {'REGISTER', 'UNDO'}

	mode: IntProperty()
	orient = 'j'

	@classmethod
	def poll(self, ctx):
		if ctx.area.type == 'VIEW_3D':
			if ctx.active_object != None:
				return get_obj_class(ctx.active_object) == 'Rectangle'
		return False

	def draw(self, ctx):
		layout = self.layout
		mode = JoyStickCreator.mode
		get_arrow_panel('rigg.joy_stick_creator', layout, mode, self.orient)

	def execute(self, ctx):
		frame = ctx.active_object
		create_joystic(ctx, frame, JoyStickCreator.mode)
		JoyStickCreator.mode = 0
		self.report({'OPERATOR'},'bpy.ops.rigg.joy_stick_creator()')
		return {'FINISHED'}

	def invoke(self, ctx, event):
		if self.mode == 0:
			rec = ctx.active_object
			if get_obj_class(rec) == 'Rectangle':
				width = rec.data.primitivedata.width
				length = rec.data.primitivedata.length
				self.orient = get_joystic_mode(width, length)
				wm = ctx.window_manager
				return wm.invoke_props_dialog(self, width=62)
		elif self.mode > 0:
			JoyStickCreator.mode = self.mode
		return {'CANCELLED'}




class Rigg_TO_Joystick_Shapekey_Connector(Operator):
	""" Select Armature contain Joystick and Mesh contain
		Shape keys and run this operator
	"""
	bl_idname = 'rigg.joystick_shapekey_connector'
	bl_label = 'Joystick Connecotr'
	bl_description = 'Connect Joystick to Shapekey'
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
		if armatuar != None:
			joys = []
			# TODO need to more secure method to detect joystics but for now it is ok
			for b in armatuar.pose.bones:
				for c in b.constraints:
					is_joystick = False
					if c.type == 'LIMIT_LOCATION':
						if c.use_min_x == True and c.use_max_x == True and \
							c.use_min_y == True and c.use_max_y == True and \
							c.use_min_z == True and c.use_max_z == True and \
							c.use_transform_limit == True and \
							c.owner_space == 'LOCAL' and c.influence == 1 and \
							c.max_z == 0 and c.min_z == 0:
							is_joystick = True
					if is_joystick:
						joys.append(b.name)
			return [(j,j,'') for j in joys]
		else:
			return [('None','None','')]
	joystick: EnumProperty(items=coolect_joys)
	
	items = []
	def collect_shapekeys(self, ctx):
		shell = None
		for obj in ctx.selected_objects:
			if obj.type in {'MESH', 'CURVE'}:
				shell = obj
		items = [('None', '', '')]
		if shell != None:
			names = [n.name for n in shell.data.shape_keys.key_blocks
												if n.name != 'Basis']
			items += [(n, n, '') for n in names]
		return items

	up: EnumProperty(items=collect_shapekeys)
	upright: EnumProperty(items=collect_shapekeys)
	right: EnumProperty(items=collect_shapekeys)
	downright: EnumProperty(items=collect_shapekeys)
	down: EnumProperty(items=collect_shapekeys)
	downleft: EnumProperty(items=collect_shapekeys)
	left: EnumProperty(items=collect_shapekeys)
	upleft: EnumProperty(items=collect_shapekeys)

	def get_expration(self, direction, joy):
		for c in joy.constraints:
			if c.type == 'LIMIT_LOCATION':
				const = c
		minx,maxx = str(const.min_x), str(const.max_x)
		miny,maxy = str(const.min_y), str(const.max_y)

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
		if armatuar != None:
			set_as_active_object(ctx, armatuar)
		if shell != None:
			shell.select_set(state=True)
		self.reset_enoms()
		return ctx.window_manager.invoke_props_dialog(self, width=400)




def joystick_connectore_menu(self, ctx):
	layout = self.layout
	layout.separator()
	layout.operator('rigg.joystick_shapekey_connector')
	#TODO temprary location for this operator
	# layout.operator('modifier.copy_selected')



classes = [Rigg_TO_Joy_Stick_Creator,
	Rigg_TO_Joystick_Shapekey_Connector]

def register_joystic():
	for c in classes:
		bpy.utils.register_class(c)
	bpy.types.VIEW3D_MT_make_links.append(joystick_connectore_menu)

def unregister_joystic():
	bpy.types.VIEW3D_MT_make_links.remove(joystick_connectore_menu)
	for c in classes:
		bpy.utils.unregister_class(c)

if __name__ == '__main__':
	register_joystic()
