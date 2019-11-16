import bpy
from bpy.types import Operator
from bpy.props import IntProperty
from mathutils import Vector
from bsmax.state import has_constraint,get_obj_class
from bsmax.actions import link_to, set_origen

def get_joystic_mode(width, length):
	if length < width / 2:
		return "h"
	if width < length / 2:
		return "v"
	return "j"

def get_joy_radius(width, length, orient):
	if orient == 'j': 
		return (width + length) / 15.0
	return (min(width, length) / 2)

def create_joystic(ctx, frame, mode):
	width = frame.data.primitivedata.width
	length = frame.data.primitivedata.length
	orient = get_joystic_mode(width, length)
	radius = get_joy_radius(width, length, orient)
	frame.data.primitivedata.chamfer1 = radius

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

	location = frame.location - Vector((x_offset,0, y_offset))
	set_origen(ctx, frame, location)

	bpy.ops.object.empty_add(type='CIRCLE', location=(0, 0, 0))
	joy = ctx.active_object
	joy.empty_display_size = radius
	joy.scale = frame.scale
	joy.parent = frame
	joy.rotation_quaternion = frame.rotation_quaternion
	joy.delta_rotation_euler = Vector(joy.delta_rotation_euler) + Vector((1.5708,0,0))
	#joy.rotation_euler = Vector(joy.rotation_euler) + Vector((1.5708,0,0))

	cons = joy.constraints.new('LIMIT_LOCATION')
	cons.use_transform_limit = True
	cons.owner_space = 'LOCAL'

	cons.use_min_x = True
	cons.use_max_x = True
	cons.use_min_y = True
	cons.use_max_y = True
	cons.use_min_z = True
	cons.use_max_z = True

	if orient in ['j','h']:
		cons.min_x = -(width / 2 - radius) + x_offset
		cons.max_x = width / 2 - radius + x_offset
	if orient in ['j','v']:
		cons.min_y = -(length / 2 - radius) + y_offset
		cons.max_y = length / 2 - radius + y_offset

class JoyStickCreator:
	mode = 0
	direction = 0

def get_arrow_panel(op, layout, mode):
	col = layout.column(align=True)
	row = col.row(align = True)
	row.operator(op,text="", icon="BLANK1").mode = 1
	row.operator(op,text="",icon="TRIA_UP").mode = 2
	row.operator(op,text="",icon="BLANK1").mode = 3
	row = col.row(align = True)
	row.operator(op,text="",icon="TRIA_LEFT").mode = 4
	row.operator(op,text="",icon='DOT').mode = 5
	row.operator(op,text="",icon="TRIA_RIGHT").mode = 6
	row = col.row(align = True)
	row.operator(op,text="",icon="BLANK1").mode = 7
	row.operator(op,text="",icon="TRIA_DOWN").mode = 8
	row.operator(op,text="",icon="BLANK1").mode = 9
	
	if mode == 1: text = "Up Left"
	elif mode == 2: text = "Up"
	elif mode == 3: text = "Up Right"
	elif mode == 4: text = "Left"
	elif mode == 5: text = "Center"
	elif mode == 6: text = "Right"
	elif mode == 7: text = "Down Left"
	elif mode == 8: text = "Down"
	elif mode == 9: text = "Down Right"
	else: text = ""
	col.label(text=text)


class BsMax_TO_JoyStickCreator(Operator):
	bl_idname = "bsmax.joystickcreator"
	bl_label = "Joystick Creator"
	bl_description = "Conver Selected Rectangle to Joystick"

	mode: IntProperty()
	orient = "j"

	@classmethod
	def poll(self, ctx):
		if ctx.area.type == 'VIEW_3D':
			if ctx.active_object != None:
				return get_obj_class(ctx.active_object) == "Rectangle"
		return False

	def draw(self, ctx):
		layout = self.layout
		op = "bsmax.joystickcreator"
		mode = JoyStickCreator.mode
		get_arrow_panel(op, layout, mode)

	def execute(self, ctx):
		frame = ctx.active_object
		create_joystic(ctx, frame, JoyStickCreator.mode)
		JoyStickCreator.mode = 0
		return {"FINISHED"}

	def invoke(self, ctx, event):
		if self.mode == 0:
			rec = ctx.active_object
			if get_obj_class(rec) == "Rectangle":
				width = rec.data.primitivedata.width
				length = rec.data.primitivedata.length
				self.orient = get_joystic_mode(width, length)
				wm = ctx.window_manager
				return wm.invoke_props_dialog(self, width=62)
		elif self.mode > 0:
			JoyStickCreator.mode = self.mode
		return {'CANCELLED'}

def get_expration(mode, joy):
	for c in joy.constraints:
		if c.type == 'LIMIT_LOCATION':
			const = c
	minx,maxx = str(const.min_x), str(const.max_x)
	miny,maxy = str(const.min_y), str(const.max_y)

	if mode == 1:
		return "varx/ "+minx+" * vary/ "+maxy
	elif mode == 2:
		return "var/ "+maxy
	elif mode == 3:
		return "varx/ "+maxx+" * vary/ "+maxx
	elif mode == 4:
		return "var/ "+minx
	elif mode == 6:
		return "var/ "+maxx
	elif mode == 7:
		return "varx/ "+minx+" *vary/ "+miny
	elif mode == 8:
		return "var/ "+miny
	elif mode == 9:
		return "varx/ "+maxx+" *vary/ "+miny
	else:
		return "0"

def add_var(driver, name, joy):
	var=driver.driver.variables.new()
	var.name=name
	var.type='TRANSFORMS'
	target=var.targets[0]
	target.id=joy
	target.transform_space='LOCAL_SPACE'
	return target

class BsMax_TO_JoyStickShapeKeyConnector(Operator):
	bl_idname = "bsmax.joystickshapekeyconnector"
	bl_label = "Joystick Connecotr (Shapekey)"
	bl_description = "Connect Joystick to Shapekey"
	mode: IntProperty()

	@classmethod
	def poll(self, ctx):
		if ctx.area.type == 'VIEW_3D':
			if len(ctx.selected_objects) == 2:
				return True
		return False

	def execute(self, ctx):
		shape, joy = None, None
		for obj in ctx.selected_objects:
			if obj.type == 'EMPTY' and has_constraint(obj,'LIMIT_LOCATION'):
				joy = obj
			if obj.active_shape_key_index > 0:
				shape = obj

		if joy != None and shape != None:
			mode=JoyStickCreator.direction
			if mode in [1,2,3,4,6,7,8,9]:
				index=shape.active_shape_key_index
				key_block=shape.data.shape_keys.key_blocks[index]
				#TODO delet older driver
				driver=key_block.driver_add("value")
				driver.driver.type='SCRIPTED'
				if mode in [2,4,6,8]:
					target = add_var(driver,'var',joy)
					if mode in [2,8]:
						target.transform_type='LOC_Y'
					else:
						target.transform_type='LOC_X'
				if mode in [1,3,7,9]:
					targetx = add_var(driver,'varx',joy)
					targetx.transform_type='LOC_X'
					targety = add_var(driver,'vary',joy)
					targety.transform_type='LOC_Y'

				driver.driver.expression=get_expration(mode, joy)

				if index < len(shape.data.shape_keys.key_blocks) - 1:
					shape.active_shape_key_index=index+1
		return {"FINISHED"}

	def draw(self, ctx):
		layout = self.layout
		op = "bsmax.joystickshapekeyconnector"
		mode = JoyStickCreator.direction
		get_arrow_panel(op, layout, mode)

	def invoke(self, ctx, event):
		if self.mode == 0:
			wm = ctx.window_manager
			return wm.invoke_props_dialog(self, width=62)
		else:
			JoyStickCreator.direction = self.mode
		return {'CANCELLED'}

def joystick_cls(register):
	classes = [BsMax_TO_JoyStickCreator, BsMax_TO_JoyStickShapeKeyConnector]
	if register: 
		[bpy.utils.register_class(c) for c in classes]
	else:
		[bpy.utils.unregister_class(c) for c in classes]

if __name__ == '__main__':
	joystick_cls(True)

__all__ = ["joystick_cls"]