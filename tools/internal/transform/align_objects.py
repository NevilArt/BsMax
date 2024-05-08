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
# 2024/05/05

import bpy

from bpy.props import EnumProperty, BoolProperty, FloatProperty
from mathutils import Vector, Euler
from bpy.types import Operator
from bpy.utils import register_class, unregister_class

from bsmax.operator import PickOperator
from bsmax.math import BoolVector, value_by_percent
from bsmax.bsmatrix import matrix_from_elements
from bsmax.bounding_box import BoundBox

# TODO replace
def scan_subobject(cls):
	if cls.type == 'ARMATURE':
		# Replace bone head a and tale as min and max
		head = cls.owner.matrix_world @ cls.bone.head
		tail = cls.owner.matrix_world @ cls.bone.tail
		cls.matrix_world = cls.owner.matrix_world.copy()
		cls.matrix_world.translation = head.copy()
		
		cls.location = Vector(head)
		cls.bounding_box.min = Vector(head)
		cls.bounding_box.max = Vector(tail)
		cls.center = cls.bounding_box.get_center()
		
		# Combine bone and armature rotation
		bone_rotation = cls.bone.matrix.to_euler()
		armature_rotation = cls.matrix_world.to_euler()
		rx = bone_rotation.x + armature_rotation.x
		ry = bone_rotation.y + armature_rotation.y
		rz = bone_rotation.z + armature_rotation.z
		cls.rotation = Euler((rx, ry, rz))
		
		# Combine bone and armature scale
		bone_scale = cls.bone.matrix.to_scale()
		armature_scale = cls.matrix_world.to_scale()
		cls.scale = bone_scale * armature_scale


def get_object_matrix_as_target(cls):
	global public_option
	target_mode = public_option.target_mode
	location = cls.matrix_world.translation

	if target_mode == 'MIN':
		location = cls.bounding_box.min.copy()

	elif target_mode == 'CENTER':
		location = cls.bounding_box.get_center()

	elif target_mode == 'MAX':
		location = cls.bounding_box.max.copy()

	elif target_mode == 'CURSOR':
		location = bpy.context.scene.cursor.location.copy()
	
	ret_matrix = cls.matrix_world.copy()
	ret_matrix.translation = location

	return ret_matrix


def get_subobject_matrix_as_target(cls):
	target_mode = public_option.target_mode
	location = cls.matrix_world.translation

	if target_mode == 'MIN':
		location = cls.bounding_box.min.copy()

	elif target_mode == 'CENTER':
		location = cls.bounding_box.get_center()

	elif target_mode == 'MAX':
		location = cls.bounding_box.max.copy()

	elif target_mode == 'CURSOR':
		location = bpy.context.scene.cursor.location.copy()

	rotation = cls.rotation
	scale = cls.scale
	
	return matrix_from_elements(location, rotation, scale)


def combine_matrix(original , target):
	option = public_option

	# seprate original transform matrix
	location = original.translation.copy()
	rotation = original.to_euler()
	scale = original.to_scale()

	# seprate target transform matrix
	trg_location = target.translation
	trg_rotation = target.to_euler()
	trg_scale = target.to_scale()

	if option.location.x:
		location.x = value_by_percent(
			location.x, trg_location.x, option.percent
		)

	if option.location.y:
		location.y = value_by_percent(
			location.y, trg_location.y, option.percent
		)

	if option.location.z:
		location.z = value_by_percent(
			location.z, trg_location.z, option.percent
		)
	
	if option.rotation.x:
		rotation.x = value_by_percent(
			rotation.x, trg_rotation.x, option.percent
		)

	if option.rotation.y:
		rotation.y = value_by_percent(
			rotation.y, trg_rotation.y, option.percent
		)

	if option.rotation.z:
		rotation.z = value_by_percent(
			rotation.z, trg_rotation.z, option.percent
		)
	
	if option.scale.x:
		scale.x = value_by_percent(scale.x, trg_scale.x, option.percent)

	if option.scale.y:
		scale.y = value_by_percent(scale.y, trg_scale.y, option.percent)

	if option.scale.z:
		scale.z = value_by_percent(scale.z, trg_scale.z, option.percent)

	return matrix_from_elements(location, rotation, scale)


def shift_matrix(cls, matrix):
	""" Get target matrix and shift by bounding box info """
	option = public_option
	location = matrix.translation.copy()
	rotation = matrix.to_euler()
	scale = matrix.to_scale()

	if option.current_mode == 'min':
		location += cls.location - cls.bounding_box.min

	elif option.current_mode == 'center':
		location += cls.location - cls.bounding_box.get_center()

	elif option.current_mode == 'max':
		location += cls.location - cls.bounding_box.max

	return matrix_from_elements(location, rotation, scale)


def set_object_matrix(cls, targte_matrix):
	targte_matrix = shift_matrix(cls, targte_matrix)
	cls.owner.matrix_world = combine_matrix(cls.matrix_world , targte_matrix)


def align_objects_ui_draw(cls):
	layout = cls.layout
	box = layout.box()

	row = box.row()
	row.prop(cls, 'pos_x', text='X Position')
	row.prop(cls, 'pos_y', text='Y Position')
	row.prop(cls, 'pos_z', text='Z Position')

	col = box.column()
	row = col.row()
	box = row.box()

	col = box.column()
	col.label(text='Current Object')
	col.prop(cls, 'current', expand=True)

	box = row.box()
	col = box.column()
	col.label(text='Target Object')
	col.prop(cls, 'target', expand=True)

	if align_abject.subtarget:
		col.prop(cls, 'target_type', text='')

	box = layout.box()
	row = box.row()
	row.prop(cls, 'rot_x', text='X Rotation')
	row.prop(cls, 'rot_y', text='Y Rotation')
	row.prop(cls, 'rot_z', text='Z Rotation')

	box = layout.box()
	row = box.row()
	row.prop(cls, 'scl_x', text='X Scale')
	row.prop(cls, 'scl_y', text='Y Scale')
	row.prop(cls, 'scl_z', text='Z Scale')

	layout.prop(cls, 'percent')


class AlignObjectOption:
	def __init__(self):
		self.location = BoolVector()
		self.rotation = BoolVector()
		self.scale = BoolVector()
		self.current_mode = 'PIVOT'
		self.target_mode = 'PIVOT'
		self.percent = 1.0

public_option = AlignObjectOption()


class Subobject_info:
	def __init__(self):
		self.owner = None
		self.type = ''
		self.bone = None
		self.index = 0 # Spline or Vertex Index

		self.matrix_world = matrix_from_elements(
			Vector((0, 0, 0)), Vector((0, 0, 0)), Vector((1, 1, 1))
		)
		
		self.location = Vector((0, 0, 0))
		self.rotation = Euler((0, 0, 0))
		self.scale = Vector((0, 0, 0))
		self.bounding_box = BoundBox(None)
		self.center = Vector((0, 0, 0))

	def set(self, owner, sub):
		self.owner = owner
		self.type = owner.type
		if self.type == 'ARMATURE':
			self.bone = sub

		elif self.type in {'CURVE', 'MESH'}:
			self.index = sub

		scan_subobject(self)

	def scan(self):
		scan_subobject(self)


class ObjectInfo:
	def __init__(self, obj):
		self.owner = obj
		self.matrix_world = obj.matrix_world.copy()
		self.location = obj.matrix_world.to_translation()
		self.rotation = obj.matrix_world.to_euler()
		self.scale = obj.matrix_world.to_scale()
		self.bounding_box = BoundBox(obj)
		self.center = self.bounding_box.center

	def reset(self):
		self.owner.matrix_world = self.matrix_world
	
	def set_matrix(self, targte_matrix):
		set_object_matrix(self, targte_matrix)


class AlignObject:
	def __init__(self):
		self.objects = []
		self.subobjects = []
		self.index = 0
		self.target = None
		self.subtarget = None
		self.use_subtarget = False

	def set(self, objects, target, subtarget):
		""" Take given info in row, set up the object """
		self.get_tartget(target, subtarget)
		self.get_objects(objects)
	
	def get_tartget(self, obj, subobj):
		""" Get target object ans sub target info """
		self.target = ObjectInfo(obj)
		if subobj:
			self.subtarget = Subobject_info()
			self.subtarget.set(self.target.owner, subobj)
		else:
			self.subtarget = None
			self.use_subtarget = False
	
	def get_objects(self, objs):
		""" Collect objects will align """
		self.objects.clear()
		for obj in objs:
			if obj != self.target.owner:
				self.objects.append(ObjectInfo(obj))
	
	def reset(self):
		""" Reset all objects world matrix """
		for obj in self.objects:
			obj.reset()
	
	def set_matrix(self):
		""" align objects to given matrix """
		for obj in self.objects:
			obj.reset()
			if self.use_subtarget:
				obj.set_matrix(get_subobject_matrix_as_target(self.subtarget))
			else:
				obj.set_matrix(get_object_matrix_as_target(self.target))

align_abject = AlignObject()


def update(cls, _):
	global public_option
	public_option.location.set(cls.pos_x, cls.pos_y, cls.pos_z)
	public_option.rotation.set(cls.rot_x, cls.rot_y, cls.rot_z)
	public_option.scale.set(cls.scl_x, cls.scl_y, cls.scl_z)
	public_option.percent = cls.percent
	public_option.current_mode = cls.current
	public_option.target_mode = cls.target

	if align_abject:
		align_abject.set_matrix()
		align_abject.use_subtarget = cls.target_type == 'SUB'


class Object_OT_Align_Objects(Operator):
	bl_idname = "object.align_objects"
	bl_label = "Align Object"
	bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

	def sub_target(self, _):
		if not align_abject.subtarget:
			return [('OBJECT', 'Object', '')]

		if align_abject.subtarget.type == 'ARMATURE':
			return [('OBJECT', 'Armature', ''), ('SUB', 'Bone', '')]

		elif align_abject.subtarget.type == 'CURVE':
			return [('OBJECT', 'Object', ''), ('SUB', 'Spline', '')]

		elif align_abject.subtarget.type == 'MESH':
			return [('OBJECT', 'Object', ''), ('SUB', 'Vertex', '')]

		return [('OBJECT', 'Object', '')]

	def get_source_options(self, _):
		return [
			('MIN', "Minimum", ""),
			('CENTER', "Center", ""),
			('PIVOT', "Pivot", ""),
			('MAX', "Maximum", ""),
			('CURSOR', "Cursor", "")
		]

	def get_target_options(self, _):
		if self.target_type == 'SUB':
			return  [
				('MIN', "Head", ""),
				('CENTER', "Center", ""),
				('PIVOT', "Pivot", ""),
				('MAX', "Tail", ""),
				('CURSOR', "Cursor", "")
			]

		return [
			('MIN', "Minimum", ""),
			('CENTER', "Center", ""),
			('PIVOT', "Pivot", ""),
			('MAX', "Maximum", ""),
			('CURSOR', "Cursor", "")
		]

	""" Props """
	pos_x: BoolProperty(update=update)
	pos_y: BoolProperty(update=update)
	pos_z: BoolProperty(update=update)

	current: EnumProperty(items= get_source_options, update=update)
	target: EnumProperty(items= get_target_options, update=update)
	target_type: EnumProperty(update=update, items=sub_target)

	rot_x: BoolProperty(update=update)
	rot_y: BoolProperty(update=update)
	rot_z: BoolProperty(update=update)
	
	scl_x: BoolProperty(update=update)
	scl_y: BoolProperty(update=update)
	scl_z: BoolProperty(update=update)
	
	percent: FloatProperty(
		name="Percent", update=update,
		soft_min=0, soft_max=1, default=1, step=0.1
	)

	@classmethod
	def poll(self, ctx):
		return ctx.mode == 'OBJECT'
	
	def draw(self, _):
		align_objects_ui_draw(self)
		
	def execute(self, _):
		return {'FINISHED'}

	def cancel(self, _):
		align_abject.reset()
	
	def invoke(self, ctx, _):
		if align_abject.subtarget:
			self.target_type = 'SUB'
			align_abject.use_subtarget = True
		update(self, None)
		return ctx.window_manager.invoke_props_dialog(self)


class Object_OT_Align_Selected_to_Active(Operator):
	bl_idname = "object.align_selected_to_active"
	bl_label = "Align Selected to Active object"
	bl_options = {'REGISTER', 'UNDO'}

	@classmethod
	def poll(self, ctx):
		return ctx.mode == 'OBJECT'

	def execute(self, ctx):
		objects = ctx.selected_objects
		target = ctx.active_object
		subtarget = None
		align_abject.set(objects, target, subtarget)
		bpy.ops.object.align_objects('INVOKE_DEFAULT')
		return {'FINISHED'}


class Object_OT_Align_Selected_to_Target(PickOperator):
	bl_idname = "object.align_selected_to_target"
	bl_label = "Align Selected to Target"
	bl_options = {'REGISTER', 'UNDO'}

	@classmethod
	def poll(self, ctx):
		return True

	def picked(self, ctx, source, subsource, target, subtarget):
		align_abject.set(source, target, subtarget)
		bpy.ops.object.align_objects('INVOKE_DEFAULT')


classes = {
	Object_OT_Align_Objects,
	Object_OT_Align_Selected_to_Active,
	Object_OT_Align_Selected_to_Target
}


def register_align_objects():
	for c in classes:
		register_class(c)


def unregister_align_objects():
	for c in classes:
		unregister_class(c)


if __name__ == "__main__":
	register_align_objects()