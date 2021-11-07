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
from mathutils import Vector
from bpy.types import Operator
from bsmax.operator import PickOperator

# Original Code by Ozzkar
# Edit by Nevil

class Align_object_Data_Class:
	def __init__(self):
		""" Location """
		self.pos_x = True
		self.pos_y = True
		self.pos_z = True
		""" Mode """
		self.c_min = False
		self.t_min = False
		self.c_center = False
		self.t_center = False
		self.c_pivot = True
		self.t_pivot = True
		self.c_max = False
		self.t_max = False
		self.c_cursor = False
		self.t_cursor = False
		""" Rotation """
		self.rot_x = False
		self.rot_y = False
		self.rot_z = False
		""" Scale """
		self.scl_x = False
		self.scl_y = False
		self.scl_z = False
		""" Action """
		self.target = None
		self.subtarget = ''
		""" UI Operation """
		self.t_state = ''
		self.c_state = ''
		""" Original Transforms """
		self.objects = []
		self.pos_curs = Vector((0,0,0))
		self.rot_curs = Vector((0,0,0))
		self.pos_list = []
		self.rot_list = []
		self.scl_list = []
		""" Target Transform """
		self.targ_pos = Vector((0,0,0))
		self.targ_rot = Vector((0,0,0))
		self.targ_scl = Vector((0,0,0))
		""" Subtarget Transform """
		self.subtarg_pos = Vector((0,0,0))
		self.subtarg_rot = Vector((0,0,0))
		self.subtarg_scl = Vector((0,0,0))
	
	def reset(self):
		""" Original Transforms """
		self.objects = []
		self.pos_curs = Vector((0,0,0))
		self.rot_curs = Vector((0,0,0))
		self.pos_list = []
		self.rot_list = []
		self.scl_list = []
		""" Target Transform """
		self.targ_pos = Vector((0,0,0))
		self.targ_rot = Vector((0,0,0))
		self.targ_scl = Vector((0,0,0))
		""" Subtarget Transform """
		self.subtarg_pos = Vector((0,0,0))
		self.subtarg_rot = Vector((0,0,0))
		self.subtarg_scl = Vector((0,0,0))
		""" Action """
		self.target = None
		self.subtarget = ''

	def value_by_percent(self, orig, targ, percent):
		return (targ - orig) * percent + orig
	
	def get_pos_data(self, obj):
		""" Get Targte Object and return Min, Center, Location, Max """
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
		
		""" get min/max/center/pivot data """
		if len(cld) == 0 or obj.type not in {'MESH', 'CURVE', 'SURFACE', 'FONT', 'ARMATURE'}:
			location = obj.matrix_world.to_translation()
			return location.copy(), location.copy(), location.copy(), location.copy()
		
		p_min, p_max = cld[0].copy(), cld[0].copy()
		for v in cld:
			if p_min.x > v.x:
				p_min.x = v.x
			if p_min.y > v.y:
				p_min.y = v.y
			if p_min.z > v.z:
				p_min.z = v.z
			if p_max.x < v.x:
				p_max.x = v.x
			if p_max.y < v.y:
				p_max.y = v.y
			if p_max.z < v.z:
				p_max.z = v.z
		
		""" Min, Center, Location, Max """
		pivot = obj.matrix_world.to_translation()
		return [p_min, (p_min+p_max)/2, pivot, p_max]
	
	def store_original_transforms(self, cls, ctx):
		self.pos_curs = ctx.scene.cursor.location.copy()
		self.rot_curs = ctx.scene.cursor.rotation_euler.copy()
		for obj in self.objects:
			self.pos_list.append(self.get_pos_data(obj))
			self.rot_list.append(obj.rotation_euler.copy())
			self.scl_list.append(obj.scale.copy())
	
	def get_target_transform(self, cls, ctx):
		obj = ctx.active_object
		self.targ_pos = self.get_pos_data(obj)
		self.targ_rot = obj.rotation_euler
		self.targ_scl = obj.scale
	
	def get_subtarget_transform(self, cls, ctx):
		if self.subtarget != '':
			cls.target_type = 'BONE'
			bone = self.target.data.bones.active
			h = self.target.matrix_world @ bone.head_local
			t = self.target.matrix_world @ bone.tail_local
			p_min = Vector(h)
			p_mid = Vector((h + t) / 2)
			p_piv = Vector(h)
			p_max = Vector(t)
			self.subtarg_pos = [p_min, p_mid, p_piv, p_max]
			self.subtarg_rot = bone.matrix_local.to_euler()
			self.subtarg_scl = bone.matrix_local.to_scale()
	
	def reset_objects_transform(self, cls, ctx):
		ctx.scene.cursor.location = self.pos_curs
		ctx.scene.cursor.rotation_euler = self.rot_curs
		for i, obj in enumerate(self.objects):
			""" Position """
			obj.location.x = self.pos_list[i][2].x
			obj.location.y = self.pos_list[i][2].y
			obj.location.z = self.pos_list[i][2].z
			""" Rotation """
			obj.rotation_euler.x = self.rot_list[i].x
			obj.rotation_euler.y = self.rot_list[i].y
			obj.rotation_euler.z = self.rot_list[i].z
			""" Scale """
			obj.scale.x = self.scl_list[i].x
			obj.scale.y = self.scl_list[i].y
			obj.scale.z = self.scl_list[i].z
	
	def set_objects_transform(self, cls, ctx):
		""" set modes """
		c_index, t_index = 0, 0

		if cls.c_center:
			c_index = 1
		elif cls.c_pivot:
			c_index = 2
		elif cls.c_max:
			c_index = 3
		
		if cls.t_center:
			t_index = 1
		elif cls.t_pivot:
			t_index = 2
		elif cls.t_max:
			t_index = 3

		""" pass if cursor to cursor """
		if cls.c_cursor and cls.t_cursor:
			return

		""" set 3D cursor """
		if cls.c_cursor:
			""" Position """
			cursor = ctx.scene.cursor
			if cls.pos_x:
				cursor.location[0] = self.targ_pos[t_index].x
			if cls.pos_y:
				cursor.location[1] = self.targ_pos[t_index].y
			if cls.pos_z:
				cursor.location[2] = self.targ_pos[t_index].z
			""" rotation """
			if cls.rot_x:
				cursor.rotation_euler.x = self.targ_rot.x
			if cls.rot_y:
				cursor.rotation_euler.y = self.targ_rot.y
			if cls.rot_z:
				cursor.rotation_euler.z = self.targ_rot.z
			return

		if cls.t_cursor:
			scp = ctx.scene.cursor.location.copy()
			for i, obj in enumerate(self.objects):
				""" Position """
				pos_list = self.pos_list
				if cls.pos_x:
					obj.location.x = scp.x + (pos_list[i][2].x - pos_list[i][c_index].x)
				if cls.pos_y:
					obj.location.y = scp.y + (pos_list[i][2].y - pos_list[i][c_index].y)
				if cls.pos_z:
					obj.location.z = scp.z + (pos_list[i][2].z - pos_list[i][c_index].z)
				""" Rotation """
				if cls.rot_x:
					obj.rotation_euler.x = self.rot_curs[0]
				if cls.rot_y:
					obj.rotation_euler.y = self.rot_curs[1]
				if cls.rot_z:
					obj.rotation_euler.z = self.rot_curs[2]
			return

		""" set selection """
		t_pos = self.targ_pos[t_index] if cls.target_type == 'ARM' else self.subtarg_pos[t_index]
		t_rot = self.targ_rot if cls.target_type == 'ARM' else self.subtarg_rot
		t_scl = self.targ_scl if cls.target_type == 'ARM' else self.subtarg_scl
		for i, obj in enumerate(self.objects):
			""" position """
			pos_list = self.pos_list
			if cls.pos_x:
				obj.location.x = self.value_by_percent(self.pos_list[i][2].x,
					t_pos.x + (pos_list[i][2].x - pos_list[i][c_index].x), cls.percent)
			if cls.pos_y:
				obj.location.y = self.value_by_percent(self.pos_list[i][2].y,
					t_pos.y + (pos_list[i][2].y - pos_list[i][c_index].y), cls.percent)
			if cls.pos_z:
				obj.location.z = self.value_by_percent(self.pos_list[i][2].z,
					t_pos.z + (pos_list[i][2].z - pos_list[i][c_index].z), cls.percent)
			
			""" rotation """
			if cls.rot_x:
				obj.rotation_euler.x = self.value_by_percent(obj.rotation_euler.x, t_rot.x, cls.percent)
			if cls.rot_y:
				obj.rotation_euler.y = self.value_by_percent(obj.rotation_euler.y, t_rot.y, cls.percent)
			if cls.rot_z:
				obj.rotation_euler.z = self.value_by_percent(obj.rotation_euler.z, t_rot.z, cls.percent)
			
			""" scale """
			if cls.scl_x:
				obj.scale.x = self.value_by_percent(obj.scale.x, t_scl.x, cls.percent)
			if cls.scl_y:
				obj.scale.y = self.value_by_percent(obj.scale.y, t_scl.y, cls.percent)
			if cls.scl_z:
				obj.scale.z = self.value_by_percent(obj.scale.z, t_scl.z, cls.percent)

aod = Align_object_Data_Class()

def update(cls, ctx):
	aod.reset_objects_transform(cls, ctx)
	aod.set_objects_transform(cls, ctx)

def c_update(self, ctx, check):
	""" just try to mimic the radio buttons """
	if check == 'min' and self.c_min:
		self.c_center = self.c_pivot = self.c_max = self.c_cursor = False
		update(self, ctx)
	elif check == 'center' and self.c_center:
		self.c_min = self.c_pivot = self.c_max = self.c_cursor = False
		update(self, ctx)
	elif check == 'pivot' and self.c_pivot:
		self.c_min = self.c_center = self.c_max = self.c_cursor = False
		update(self, ctx)
	elif check == 'max' and self.c_max:
		self.c_min = self.c_center = self.c_pivot = self.c_cursor = False
		update(self, ctx)
	elif check == 'cursor' and self.c_cursor:
		self.c_min = self.c_center = self.c_pivot = self.c_max = False
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
	""" just try to mimic the radio buttons """
	if check == 'min' and self.t_min:
		self.t_center = self.t_pivot = self.t_max = self.t_cursor = False
		update(self, ctx)
	elif check == 'center' and self.t_center:
		self.t_min = self.t_pivot = self.t_max = self.t_cursor = False
		update(self, ctx)
	elif check == 'pivot' and self.t_pivot:
		self.t_min = self.t_center = self.t_max = self.t_cursor = False
		update(self, ctx)
	elif check == 'max' and self.t_max:
		self.t_min = self.t_center = self.t_pivot = self.t_cursor = False
		update(self, ctx)
	elif check == 'cursor' and self.t_cursor:
		self.t_min = self.t_center = self.t_pivot = self.t_max = False
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

class Object_OT_Align_Selected_to_Active(Operator):
	bl_idname = "object.align_selected_to_active"
	bl_label = "Align Selected to Active object"

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

	target_type: EnumProperty(update=update, default='ARM', items=[('ARM',"Armature",''),('BONE','Bone','')])

	rot_x: BoolProperty(update=update)
	rot_y: BoolProperty(update=update)
	rot_z: BoolProperty(update=update)
	
	scl_x: BoolProperty(update=update)
	scl_y: BoolProperty(update=update)
	scl_z: BoolProperty(update=update)
	
	percent: FloatProperty(name="Percent", update=update, soft_min=0, soft_max=1, default=1, step=0.1)

	@classmethod
	def poll(self, ctx):
		return True
	
	def check(self, ctx):
		pass

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
		if self.target_type == 'BONE':
			col.prop(self, 't_min', text='Head')
			col.prop(self, 't_center', text='Center')
			col.prop(self, 't_pivot', text='Pivot Point')
			col.prop(self, 't_max', text='Tail')
			col.prop(self, 't_cursor', text='Cursor')
		else:
			col.prop(self, 't_min', text='Minimum')
			col.prop(self, 't_center', text='Center')
			col.prop(self, 't_pivot', text='Pivot Point')
			col.prop(self, 't_max', text='Maximum')
			col.prop(self, 't_cursor', text='Cursor')
		if aod.subtarget != '':
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
	
	def store(self):
		""" Location """
		aod.pos_x = self.pos_x
		aod.pos_y = self.pos_y
		aod.pos_z = self.pos_z
		""" Mode """
		aod.c_min = self.c_min
		aod.t_min = self.t_min 
		aod.c_center = self.c_center
		aod.t_center = self.t_center
		aod.c_pivot = self.c_pivot 
		aod.t_pivot = self.t_pivot 
		aod.c_max = self.c_max 
		aod.t_max = self.t_max 
		aod.c_cursor = self.c_cursor
		aod.t_cursor = self.t_cursor
		""" Rotation """
		aod.rot_x = self.rot_x
		aod.rot_y = self.rot_y
		aod.rot_z = self.rot_z
		""" Scale """
		aod.scl_x = self.scl_x
		aod.scl_y = self.scl_y
		aod.scl_z = self.scl_z
		""" reset for new round """
		aod.reset()
	
	def restore(self):
		""" Location """
		self.pos_x = aod.pos_x
		self.pos_y = aod.pos_y
		self.pos_z = aod.pos_z
		""" Mode """
		self.c_min = aod.c_min
		self.t_min = aod.t_min
		self.c_center = aod.c_center
		self.t_center = aod.t_center
		self.c_pivot = aod.c_pivot
		self.t_pivot = aod.t_pivot
		self.c_max = aod.c_max
		self.t_max = aod.t_max
		self.c_cursor = aod.c_cursor
		self.t_cursor = aod.t_cursor
		""" Rotation """
		self.rot_x = aod.rot_x
		self.rot_y = aod.rot_y
		self.rot_z = aod.rot_z
		""" Scale """
		self.scl_x = aod.scl_x
		self.scl_y = aod.scl_y
		self.scl_z = aod.scl_z
	
	def restore_selection(self, ctx):
		aod.target.select_set(False)
		ctx.view_layer.objects.active = None

	def execute(self, ctx):
		self.restore_selection(ctx)
		self.store()
		self.report({'OPERATOR'},'bpy.ops.object.align_selected_to_target()')
		return {'FINISHED'}

	def cancel(self, ctx):
		""" restore to origin """
		aod.reset_objects_transform(self, ctx)
		aod.target = None
		aod.subtarget = ''
		return None
		
	def invoke(self, ctx, event):
		self.restore()
		aod.objects = ctx.selected_objects
		aod.target = ctx.active_object
		aod.objects.remove(aod.target)
		aod.store_original_transforms(self, ctx)
		aod.get_target_transform(self, ctx)
		aod.get_subtarget_transform(self, ctx)
		aod.set_objects_transform(self, ctx)
		return ctx.window_manager.invoke_props_dialog(self)

class Object_OT_Align_Selected_to_Target(PickOperator):
	bl_idname = "object.align_selected_to_target"
	bl_label = "Align Selected to Target"
	bl_options = {'REGISTER', 'UNDO'}

	def picked(self, ctx, source, subsource, target, subtarget):
		target.select_set(True)
		ctx.view_layer.objects.active = target
		aod.subtarget = subtarget if subtarget else ''
		bpy.ops.object.align_selected_to_active('INVOKE_DEFAULT')

classes = [Object_OT_Align_Selected_to_Active, Object_OT_Align_Selected_to_Target]

def register_align_objects():
	for c in classes:
		bpy.utils.register_class(c)

def unregister_align_objects():
	for c in classes:
		bpy.utils.unregister_class(c)

if __name__ == "__main__":
	register_align_objects()