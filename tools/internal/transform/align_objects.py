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
from bpy.props import EnumProperty, BoolProperty, FloatProperty
from mathutils import Vector, Euler
from bpy.types import Operator

from bsmax.operator import PickOperator
from bsmax.math import value_by_percent, matrix_from_elements

# TODO Apply button
# TODO Align along the path (combine with arrange on curve)
# TODO Align to vertex or Face + Normal by pic index


class BoolVector:
	def __init__(self):
		self.x = False
		self.y = False
		self.z = False
	def set(self, x, y, z):
		self.x = x
		self.y = y
		self.z = z



class Align_Object_Option:
	def __init__(self):
		self.location = BoolVector()
		self.rotation = BoolVector()
		self.scale = BoolVector()
		self.current_mode = 'pivot'
		self.target_mode = 'pivot'
		self.percent = 1.0
public_option = Align_Object_Option()



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
		location.x = value_by_percent(location.x, trg_location.x, option.percent)
	if option.location.y:
		location.y = value_by_percent(location.y, trg_location.y, option.percent)
	if option.location.z:
		location.z = value_by_percent(location.z, trg_location.z, option.percent)
	
	if option.rotation.x:
		rotation.x = value_by_percent(rotation.x, trg_rotation.x, option.percent)
	if option.rotation.y:
		rotation.y = value_by_percent(rotation.y, trg_rotation.y, option.percent)
	if option.rotation.z:
		rotation.z = value_by_percent(rotation.z, trg_rotation.z, option.percent)
	
	if option.scale.x:
		scale.x = value_by_percent(scale.x, trg_scale.x, option.percent)
	if option.scale.y:
		scale.y = value_by_percent(scale.y, trg_scale.y, option.percent)
	if option.scale.z:
		scale.z = value_by_percent(scale.z, trg_scale.z, option.percent)
	
	return matrix_from_elements(location, rotation, scale)



class Bounding_Box:
	def __init__(self, obj):
		self.min = Vector((0,0,0))
		self.max = Vector((0,0,0))
		if obj:
			self.get_bounding_box(obj)

	def get_bounding_box(self, obj):
		cld = []
		data = obj.data
		if obj.type == 'MESH':
			cld = [obj.matrix_world @ vert.co for vert in data.vertices]
		elif obj.type == 'CURVE':
			for spn in data.splines:
				cld += [obj.matrix_world @ pts.co for pts in spn.bezier_points]
		elif obj.type == 'SURFACE':
			for spn in data.splines:
				cld += [obj.matrix_world @ pts.co for pts in spn.points]
		elif obj.type == 'FONT':
			for spn in data.splines:
				cld += [obj.matrix_world @ pts.co for pts in spn.bezier_points]
		elif obj.type == 'ARMATURE':
			for bone in data.bones:
				cld.append(obj.matrix_world @ bone.head_local)
				if len(bone.children) == 0:
					cld.append(obj.matrix_world @ bone.tail_local)
		
		""" get min/max """
		if len(cld) == 0 or obj.type not in {'MESH', 'CURVE', 'SURFACE', 'FONT', 'ARMATURE'}:
			location = obj.matrix_world.to_translation()
			self.min_x = self.max_x = location.x
			self.min_y = self.max_y = location.y
			self.min_z = self.max_z = location.z
		
		else:
			self.min = cld[0].copy()
			self.max = cld[0].copy()
			for v in cld:
				if self.min.x > v.x:
					self.min.x = v.x
				if self.min.y > v.y:
					self.min.y = v.y
				if self.min.z > v.z:
					self.min.z = v.z
				if self.max.x < v.x:
					self.max.x = v.x
				if self.max.y < v.y:
					self.max.y = v.y
				if self.max.z < v.z:
					self.max.z = v.z
	
	def get_center(self):
		x = (self.min.x + self.max.x) / 2
		y = (self.min.y + self.max.y) / 2
		z = (self.min.z + self.max.z) / 2
		return Vector((x, y, z))



class Subobject_info:
	def __init__(self):
		self.owner = None
		self.type = ''
		self.bone = None
		self.index = 0 # Spline or Vertex Index

		self.matrix_world = matrix_from_elements(Vector((0,0,0)),Vector((0,0,0)),Vector((1,1,1)))
		self.location = Vector((0,0,0))
		self.rotation = Euler((0,0,0))
		self.scale = Vector((0,0,0))
		self.bounding_box = Bounding_Box(None)
		self.center = Vector((0,0,0))

	def set(self, owner, sub):
		self.owner = owner
		self.type = owner.type
		if self.type == 'ARMATURE':
			self.bone = sub
		if self.type in {'CURVE', 'MESH'}:
			self.index = sub
		self.scan()

	def scan(self):
		if self.type == 'ARMATURE':
			# Replace bone head a and tale as min and max
			head = self.owner.matrix_world @ self.bone.head
			tail = self.owner.matrix_world @ self.bone.tail
			self.matrix_world = self.owner.matrix_world.copy()
			self.matrix_world.translation = head.copy()
			
			self.location = Vector(head)
			self.bounding_box.min = Vector(head)
			self.bounding_box.max = Vector(tail)
			self.center = self.bounding_box.get_center()
			
			# Combine bone and armature rotation
			bone_rotation = self.bone.matrix.to_euler()
			armature_rotation = self.matrix_world.to_euler()
			rx = bone_rotation.x + armature_rotation.x
			ry = bone_rotation.y + armature_rotation.y
			rz = bone_rotation.z + armature_rotation.z
			self.rotation = Euler((rx, ry, rz))
			
			# Combine bone and armature scale
			bone_scale = self.bone.matrix.to_scale()
			armature_scale = self.matrix_world.to_scale()
			self.scale = bone_scale * armature_scale
	
	def get_matrix_as_target(self):
		option = public_option
		location = self.matrix_world.translation

		if option.target_mode == 'min':
			location = self.bounding_box.min.copy()
		elif option.target_mode == 'center':
			location = self.bounding_box.get_center()
		elif option.target_mode == 'max':
			location = self.bounding_box.max.copy()
		elif option.target_mode == 'cursor':
			location = bpy.context.scene.cursor.location.copy()

		rotation = self.rotation
		scale = self.scale
		
		return matrix_from_elements(location, rotation, scale)



class Object_info:
	def __init__(self, obj):
		self.owner = obj
		self.matrix_world = obj.matrix_world.copy()
		self.location = obj.matrix_world.to_translation()
		self.rotation = obj.matrix_world.to_euler()
		self.scale = obj.matrix_world.to_scale()
		self.bounding_box = Bounding_Box(obj)
		self.center = self.bounding_box.get_center()

	def reset(self):
		self.owner.matrix_world = self.matrix_world
	
	def shift_matrix(self, matrix):
		""" Get target matrix and shift by bounding box info """
		option = public_option
		location = matrix.translation.copy()
		rotation = matrix.to_euler()
		scale = matrix.to_scale()

		if option.current_mode == 'min':
			location += self.location - self.bounding_box.min
		elif option.current_mode == 'center':
			location += self.location - self.bounding_box.get_center()
		elif option.current_mode == 'max':
			location += self.location - self.bounding_box.max

		return matrix_from_elements(location, rotation, scale)
	
	def set_matrix(self, targte_matrix):
		targte_matrix = self.shift_matrix(targte_matrix)
		self.owner.matrix_world = combine_matrix(self.matrix_world , targte_matrix)
	
	def get_matrix_as_target(self):
		option = public_option
		location = self.matrix_world.translation

		if option.target_mode == 'min':
			location = self.bounding_box.min.copy()
		elif option.target_mode == 'center':
			location = self.bounding_box.get_center()
		elif option.target_mode == 'max':
			location = self.bounding_box.max.copy()
		elif option.target_mode == 'cursor':
			location = bpy.context.scene.cursor.location.copy()
		
		ret_matrix = self.matrix_world.copy()
		ret_matrix.translation = location
		return ret_matrix



class Align_Object:
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
		self.target = Object_info(obj)
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
				self.objects.append(Object_info(obj))
	
	def reset(self):
		""" Reset all objects world matrix """
		for obj in self.objects:
			obj.reset()
	
	def set_matrix(self):
		""" align objects to given matrix """
		for obj in self.objects:
			obj.reset()
			if self.use_subtarget:
				obj.set_matrix(self.subtarget.get_matrix_as_target())
			else:
				obj.set_matrix(self.target.get_matrix_as_target())

align_abject = Align_Object()



def update(self, ctx):
	if self.ready:
		public_option.location.set(self.pos_x, self.pos_y, self.pos_z)
		public_option.rotation.set(self.rot_x, self.rot_y, self.rot_z)
		public_option.scale.set(self.scl_x, self.scl_y, self.scl_z)
		public_option.percent = self.percent

		if align_abject:
			align_abject.set_matrix()
			align_abject.use_subtarget = self.target_type == 'SUB'


def c_update(self, ctx, check):
	if self.ready:
		""" just try to mimic the radio buttons """
		if check == 'min' and self.c_min:
			self.c_center = self.c_pivot = self.c_max = self.c_cursor = False
			public_option.current_mode = check
			update(self, ctx)
		elif check == 'center' and self.c_center:
			self.c_min = self.c_pivot = self.c_max = self.c_cursor = False
			public_option.current_mode = check
			update(self, ctx)
		elif check == 'pivot' and self.c_pivot:
			self.c_min = self.c_center = self.c_max = self.c_cursor = False
			public_option.current_mode = check
			update(self, ctx)
		elif check == 'max' and self.c_max:
			self.c_min = self.c_center = self.c_pivot = self.c_cursor = False
			public_option.current_mode = check
			update(self, ctx)
		elif check == 'cursor' and self.c_cursor:
			self.c_min = self.c_center = self.c_pivot = self.c_max = False
			public_option.current_mode = check
			update(self, ctx)

		if not self.c_min and not self.c_center and not self.c_pivot and not self.c_max and not self.c_cursor:
			if check == 'min': 
				self.c_min = True
			elif check == 'center':
				self.c_center = True
			elif check == 'pivot':
				self.c_pivot = True
			elif check == 'max':
				self.c_max = True
			elif check == 'cursor':
				self.c_cursor = True


def t_update(self, ctx, check):
	if self.ready:
		""" just try to mimic the radio buttons """
		if check == 'min' and self.t_min:
			self.t_center = self.t_pivot = self.t_max = self.t_cursor = False
			public_option.target_mode = check
			update(self, ctx)
		elif check == 'center' and self.t_center:
			self.t_min = self.t_pivot = self.t_max = self.t_cursor = False
			public_option.target_mode = check
			update(self, ctx)
		elif check == 'pivot' and self.t_pivot:
			self.t_min = self.t_center = self.t_max = self.t_cursor = False
			public_option.target_mode = check
			update(self, ctx)
		elif check == 'max' and self.t_max:
			self.t_min = self.t_center = self.t_pivot = self.t_cursor = False
			public_option.target_mode = check
			update(self, ctx)
		elif check == 'cursor' and self.t_cursor:
			self.t_min = self.t_center = self.t_pivot = self.t_max = False
			public_option.target_mode = check
			update(self, ctx)

		if not self.t_min and not self.t_center and not self.t_pivot and not self.t_max and not self.t_cursor:
			if check == 'min': 
				self.t_min = True
			elif check == 'center':
				self.t_center = True
			elif check == 'pivot':
				self.t_pivot = True
			elif check == 'max':
				self.t_max = True
			elif check == 'cursor':
				self.t_cursor = True



class Object_OT_Align_Objects(Operator):
	bl_idname = "object.align_objects"
	bl_label = "Align Object"
	bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

	def sub_target(self, ctx):
		if not align_abject.subtarget:
			return [('OBJECT', 'Object', '')]
		if align_abject.subtarget.type == 'ARMATURE':
			return [('OBJECT', 'Armature', ''), ('SUB', 'Bone', '')]
		elif align_abject.subtarget.type == 'CURVE':
			return [('OBJECT', 'Object', ''), ('SUB', 'Spline', '')]
		elif align_abject.subtarget.type == 'MESH':
			return [('OBJECT', 'Object', ''), ('SUB', 'Vertex', '')]
		return [('OBJECT', 'Object', '')]

	""" Props """
	pos_x: BoolProperty(update=update)
	pos_y: BoolProperty(update=update)
	pos_z: BoolProperty(update=update)

	c_min: BoolProperty(update=lambda self,ctx: c_update(self,ctx,'min'))
	t_min: BoolProperty(update=lambda self,ctx: t_update(self,ctx,'min'))

	c_center: BoolProperty(update=lambda self,ctx: c_update(self,ctx,'center'))
	t_center: BoolProperty(update=lambda self,ctx: t_update(self,ctx,'center'))

	c_pivot: BoolProperty(default=True, update=lambda self,ctx: c_update(self,ctx,'pivot'))
	t_pivot: BoolProperty(default=True, update=lambda self,ctx: t_update(self,ctx,'pivot'))
	
	c_max: BoolProperty(update=lambda self,ctx: c_update(self,ctx,'max'))
	t_max: BoolProperty(update=lambda self,ctx: t_update(self,ctx,'max'))

	c_cursor: BoolProperty(update=lambda self,ctx: c_update(self,ctx,'cursor'))
	t_cursor: BoolProperty(update=lambda self,ctx: t_update(self,ctx,'cursor'))

	target_type: EnumProperty(update=update, items=sub_target)

	rot_x: BoolProperty(update=update)
	rot_y: BoolProperty(update=update)
	rot_z: BoolProperty(update=update)
	
	scl_x: BoolProperty(update=update)
	scl_y: BoolProperty(update=update)
	scl_z: BoolProperty(update=update)
	
	percent: FloatProperty(name="Percent", update=update,
		soft_min=0, soft_max=1, default=1, step=0.1)

	ready: BoolProperty(default=False, description="freeze update till UI loaded")

	@classmethod
	def poll(self, ctx):
		return True
	
	def draw(self, ctx):
		layout = self.layout
		box = layout.box()
		row = box.row()
		row.prop(self,'pos_x',text='X Position')
		row.prop(self,'pos_y',text='Y Position')
		row.prop(self,'pos_z',text='Z Position')
		col = box.column()
		row = col.row()
		box = row.box()
		col = box.column()
		col.label(text='Current Object')
		col.prop(self, 'c_min', text='Minimum')
		col.prop(self, 'c_center', text='Center')
		col.prop(self, 'c_pivot', text='Pivot Point')
		col.prop(self, 'c_max', text='Maximum')
		col.prop(self, 'c_cursor', text='Cursor')
		box = row.box()
		col = box.column()
		col.label(text='Target Object')
		if self.target_type == 'OBJECT':
			col.prop(self, 't_min', text='Minimum')
			col.prop(self, 't_center', text='Center')
			col.prop(self, 't_pivot', text='Pivot Point')
			col.prop(self, 't_max', text='Maximum')
			col.prop(self, 't_cursor', text='Cursor')
		else:
			col.prop(self, 't_min', text='Head')
			col.prop(self, 't_center', text='Center')
			col.prop(self, 't_pivot', text='Pivot Point')
			col.prop(self, 't_max', text='Tail')
			col.prop(self, 't_cursor', text='Cursor')
			
		if align_abject.subtarget:
			col.prop(self, 'target_type', text='')
		box = layout.box()
		row = box.row()
		row.prop(self,'rot_x',text='X Rotation')
		row.prop(self,'rot_y',text='Y Rotation')
		row.prop(self,'rot_z',text='Z Rotation')
		box = layout.box()
		row = box.row()
		row.prop(self,'scl_x',text='X Scale')
		row.prop(self,'scl_y',text='Y Scale')
		row.prop(self,'scl_z',text='Z Scale')
		layout.prop(self, 'percent')
		
	def execute(self, ctx):
		return {'FINISHED'}

	def cancel(self, ctx):
		align_abject.reset()
	
	def load_state(self):
		self.ready = False
		option = public_option
		self.pos_x = option.location.x
		self.pos_y = option.location.y
		self.pos_z = option.location.z

		self.c_min = option.current_mode == 'min'
		self.t_min = option.target_mode == 'min'

		self.c_center = option.current_mode == 'center'
		self.t_center = option.target_mode == 'center'

		self.c_pivot = option.current_mode == 'pivot'
		self.t_pivot = option.target_mode == 'pivot'

		self.c_max = option.current_mode == 'max'
		self.t_max = option.current_mode == 'max'

		self.c_cursor = option.current_mode == 'cursor'
		self.t_cursor = option.target_mode == 'cursor'

		self.rot_x = option.rotation.x
		self.rot_y = option.rotation.y
		self.rot_z = option.rotation.z

		self.scl_x = option.scale.x
		self.scl_y = option.scale.y
		self.scl_z = option.scale.z

		# self.percent = option.percent
		self.ready = True

	def invoke(self, ctx, event):
		self.load_state()
		if align_abject.subtarget:
			self.target_type = 'SUB'
			align_abject.use_subtarget = True
		update(self, ctx)
		return ctx.window_manager.invoke_props_dialog(self)



class Object_OT_Align_Selected_to_Active(Operator):
	bl_idname = "object.align_selected_to_active"
	bl_label = "Align Selected to Active object"
	bl_options = {'REGISTER', 'UNDO'}

	@classmethod
	def poll(self, ctx):
		return True
		
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



classes = [Object_OT_Align_Objects,
	Object_OT_Align_Selected_to_Active,
	Object_OT_Align_Selected_to_Target]

def register_align_objects():
	for c in classes:
		bpy.utils.register_class(c)

def unregister_align_objects():
	for c in classes:
		bpy.utils.unregister_class(c)

if __name__ == "__main__":
	register_align_objects()