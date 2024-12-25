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
# 2024/05/16

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
		cls.bounding_box.get_center()

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
	target = public_option.target
	location = cls.matrix_world.translation

	if target == 'MIN':
		location = cls.bounding_box.min.copy()

	elif target == 'CENTER':
		location = cls.bounding_box.center.copy()

	elif target == 'MAX':
		location = cls.bounding_box.max.copy()

	elif target == 'CURSOR':
		location = bpy.context.scene.cursor.location.copy()
	
	ret_matrix = cls.matrix_world.copy()
	ret_matrix.translation = location

	return ret_matrix


def get_subobject_matrix_as_target(cls):
	global public_option
	target = public_option.target
	location = cls.matrix_world.translation

	if target == 'MIN':
		location = cls.bounding_box.min.copy()

	elif target == 'CENTER':
		location = cls.bounding_box.center.copy()

	elif target == 'MAX':
		location = cls.bounding_box.max.copy()

	elif target == 'CURSOR':
		location = bpy.context.scene.cursor.location.copy()

	rotation = cls.rotation
	scale = cls.scale
	
	return matrix_from_elements(location, rotation, scale)


def combine_matrix(original , target):
	global public_option

	# seprate original transform matrix
	location = original.translation.copy()
	rotation = original.to_euler()
	scale = original.to_scale()

	# seprate target transform matrix
	trg_location = target.translation
	trg_rotation = target.to_euler()
	trg_scale = target.to_scale()

	if public_option.location.x:
		location.x = value_by_percent(
			location.x, trg_location.x, public_option.percent
		)

	if public_option.location.y:
		location.y = value_by_percent(
			location.y, trg_location.y, public_option.percent
		)

	if public_option.location.z:
		location.z = value_by_percent(
			location.z, trg_location.z, public_option.percent
		)
	
	if public_option.rotation.x:
		rotation.x = value_by_percent(
			rotation.x, trg_rotation.x, public_option.percent
		)

	if public_option.rotation.y:
		rotation.y = value_by_percent(
			rotation.y, trg_rotation.y, public_option.percent
		)

	if public_option.rotation.z:
		rotation.z = value_by_percent(
			rotation.z, trg_rotation.z, public_option.percent
		)
	
	if public_option.scale.x:
		scale.x = value_by_percent(
			scale.x, trg_scale.x, public_option.percent
		)

	if public_option.scale.y:
		scale.y = value_by_percent(
			scale.y, trg_scale.y, public_option.percent
		)

	if public_option.scale.z:
		scale.z = value_by_percent(
			scale.z, trg_scale.z, public_option.percent
		)

	return matrix_from_elements(location, rotation, scale)


def shift_matrix(cls, matrix):
	""" Get target matrix and shift by bounding box info """
	global public_option
	location = matrix.translation.copy()
	rotation = matrix.to_euler()
	scale = matrix.to_scale()

	if public_option.current == 'MIN':
		location += cls.location - cls.bounding_box.min

	elif public_option.current == 'CENTER':
		location += cls.location - cls.bounding_box.center

	elif public_option.current == 'MAX':
		location += cls.location - cls.bounding_box.max

	return matrix_from_elements(location, rotation, scale)


def set_object_matrix(cls, targte_matrix):
	targte_matrix = shift_matrix(cls, targte_matrix)
	cls.owner.matrix_world = combine_matrix(cls.matrix_world , targte_matrix)


def align_object_get_tartget(cls, obj, subobj):
	""" Get target object ans sub target info """
	cls.target = ObjectInfo(obj)
	if subobj:
		cls.subtarget = Subobject_info()
		cls.subtarget.set(cls.target.owner, subobj)
	else:
		cls.subtarget = None
		cls.use_subtarget = False


def align_object_get_objects(cls, objs):
	""" Collect objects will align """
	cls.objects.clear()
	for obj in objs:
		if obj != cls.target.owner:
			cls.objects.append(ObjectInfo(obj))


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


def load_state(cls):
	global public_option 
	cls.pos_x = public_option.location.x
	cls.pos_y = public_option.location.y
	cls.pos_z = public_option.location.z

	cls.current = public_option.current
	cls.target = public_option.target

	cls.rot_x = public_option.rotation.x
	cls.rot_y = public_option.rotation.y
	cls.rot_z = public_option.rotation.z

	cls.scl_x = public_option.scale.x
	cls.scl_y = public_option.scale.y
	cls.scl_z = public_option.scale.z

	cls.percent = public_option.percent
	cls.ready = True


class AlignObjectOption:
	def __init__(self):
		self.location = BoolVector()
		self.rotation = BoolVector()
		self.scale = BoolVector()
		self.current = 'PIVOT'
		self.target = 'PIVOT'
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
		align_object_get_tartget(self, target, subtarget)
		align_object_get_objects(self, objects)
	
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
	if not cls.ready:
		return

	global public_option
	public_option.location.set(cls.pos_x, cls.pos_y, cls.pos_z)
	public_option.rotation.set(cls.rot_x, cls.rot_y, cls.rot_z)
	public_option.scale.set(cls.scl_x, cls.scl_y, cls.scl_z)
	public_option.percent = cls.percent
	public_option.current = cls.current
	public_option.target = cls.target

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
	
	ready: BoolProperty(default=False) # type: ignore

	""" Props """
	pos_x: BoolProperty(update=update) # type: ignore
	pos_y: BoolProperty(update=update) # type: ignore
	pos_z: BoolProperty(update=update) # type: ignore

	current: EnumProperty(
		items= get_source_options, update=update,
		default=2
	) # type: ignore

	target: EnumProperty(
		items= get_target_options, update=update,
		default=2
	) # type: ignore

	target_type: EnumProperty(update=update, items=sub_target) # type: ignore

	rot_x: BoolProperty(update=update) # type: ignore
	rot_y: BoolProperty(update=update) # type: ignore
	rot_z: BoolProperty(update=update) # type: ignore
	
	scl_x: BoolProperty(update=update) # type: ignore
	scl_y: BoolProperty(update=update) # type: ignore
	scl_z: BoolProperty(update=update) # type: ignore
	
	percent: FloatProperty(
		name="Percent", update=update,
		soft_min=0, soft_max=1, default=1, step=0.1
	) # type: ignore

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
		load_state(self)

		if align_abject.subtarget:
			self.target_type = 'SUB'
			align_abject.use_subtarget = True

		update(self, None)
		return ctx.window_manager.invoke_props_dialog(self)


class Object_OT_Align_Selected_to_Active(Operator):
	bl_idname = 'object.align_selected_to_active'
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
	bl_idname = 'object.align_selected_to_target'
	bl_label = "Align Selected to Target"
	bl_options = {'REGISTER', 'UNDO'}

	@classmethod
	def poll(self, _):
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
	for cls in classes:
		register_class(cls)


def unregister_align_objects():
	for cls in classes:
		unregister_class(cls)


if __name__ == '__main__':
	register_align_objects()