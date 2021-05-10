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
from bpy.types import Operator, Panel, PropertyGroup
from bpy.props import IntProperty, StringProperty, BoolProperty, PointerProperty, EnumProperty



class Armature_Selection_Set:
	def __init__(self):
		self.armature = None
		self.button_names = []
	
	def get_names_from_armature(self, armature):
		""" calculate once if armature changes """
		if self.armature != armature:
			""" fill name list if less than buttons count """
			buttons_count = armature.data.selection_set.columns * armature.data.selection_set.rows
			names = armature.data.selection_set.names.split(':')
			if len(names) == 1:
				if names[0] == '':
					names = []
			if len(names) < buttons_count:
				for i in range(len(names), buttons_count):
					names.append(str(i))
			self.button_names = names
			self.armature = armature

	def get_name_by_index(self, armature, index):
		self.get_names_from_armature(armature)
		if index < len(self.button_names):
			return self.button_names[index]
		else:
			return ' '

	def set_names_to_armature(self, armature, new_name, index):
		self.get_names_from_armature(armature)
		names = self.button_names
		if index < len(names):
			names[index] = new_name
		name_str = ''
		for name in names:
			name_str += name + ':'
		armature.data.selection_set.names = name_str

arm_sel_set = Armature_Selection_Set()



def rename_selection_set(self, ctx):
	""" Filter the new name """
	new_name = ''
	selection_set = ctx.scene.selection_set
	
	for v in selection_set.name:
		if v != ':':
			new_name += v
	
	if new_name == '':
		new_name = ' '
	
	if selection_set.name != new_name:
		selection_set.name = new_name
		
	""" Put new name on names list """
	arm_sel_set.set_names_to_armature(ctx.active_object, new_name, selection_set.active)



class Selection_Set_Scene(PropertyGroup):
	mode: EnumProperty(name='Mode',default='SELECT',
		items =[('SELECT','Select',''), ('SET','Set',''),('RENAME','Rename',''), ('EDIT','Edit','')])
	multi: BoolProperty(name='Multi Selection', default=False)
	name: StringProperty(name="", update=rename_selection_set)
	active: IntProperty(name="", default=0)



class Selection_Set_Armature(PropertyGroup):
	columns: IntProperty(name='columns', min=1, max=100, default=3)
	rows: IntProperty(name='row', min=1, max=100, default=10)
	names: StringProperty(name='')



class ARMATURE_OT_Selection_Set(Operator):
	bl_idname = 'pose.selection_set'
	bl_label = 'Selection set'
	# bl_description = ''
	bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

	index: IntProperty(name='index')

	def get_groups(self, bone):
		return bone.selection_groups.split(',')
	
	def set_groups(self, bone, groups):
		string = ''
		for s in groups:
			string += s + ','
		bone.selection_groups = string
	
	def add(self, bone, index):
		groups = self.get_groups(bone)
		if not index in groups:
			groups.append(index)
		self.set_groups(bone, groups)
	
	def remove(self, bone, index):
		groups = self.get_groups(bone)
		if index in groups:
			groups.remove(index)
			self.set_groups(bone, groups)

	def execute(self, ctx):
		mode = ctx.scene.selection_set.mode
		bones = ctx.active_object.pose.bones
		index = str(self.index)
		if mode == 'SELECT':
			for bone in bones:
				if index in self.get_groups(bone):
					bone.bone.select = True
				else:
					if not ctx.scene.selection_set.multi:
						bone.bone.select = False
		elif mode == 'SET':
			for bone in bones:
				if bone.bone.select:
					self.add(bone, index)
				else:
					self.remove(bone, index)
		elif ctx.scene.selection_set.mode == 'RENAME':
			ctx.scene.selection_set.active = self.index
			""" Get Old Name """
			name = arm_sel_set.get_name_by_index(ctx.active_object, ctx.scene.selection_set.active)
			ctx.scene.selection_set.name = name
		return{'FINISHED'}



class Armature_OP_Selection_Set(Panel):
	bl_space_type = 'VIEW_3D'
	bl_region_type = 'UI'
	bl_label = 'Selection (Pose Bone)'
	bl_idname = 'VIEW3D_PT_selection_set'
	bl_category = 'Tool'

	@classmethod
	def poll(self, ctx):
		if ctx.active_object != None:
			if ctx.active_object.type == 'ARMATURE':
				return ctx.mode == 'POSE'
		return False
	
	def draw(self, ctx):
		layout = self.layout

		obj_selection_set = ctx.active_object.data.selection_set
		scene_selection_set = ctx.scene.selection_set
		
		""" Controll """
		box = layout.box()
		row = box.row()
		row.prop(scene_selection_set, 'multi',icon='ADD', text='')
		row.prop(scene_selection_set, 'mode')
		if scene_selection_set.mode == 'EDIT':
			row.prop(obj_selection_set, 'columns', text='Col:')
			row.prop(obj_selection_set, 'rows', text='Row:')
		
		""" Buttons """
		box = layout.box()
		for j in range(obj_selection_set.rows):
			row = box.row()
			for i in range(obj_selection_set.columns):
				index = j*obj_selection_set.columns + i
				if scene_selection_set.mode == 'RENAME' and scene_selection_set.active == index:
					row.prop(scene_selection_set, 'name')
				else:
					if scene_selection_set.mode == 'EDIT':
						name = str(index)
					else:
						name = arm_sel_set.get_name_by_index(ctx.active_object, index)
					row.operator('pose.selection_set', text=name).index=index



classes = [ARMATURE_OT_Selection_Set,
	Armature_OP_Selection_Set,
	Selection_Set_Scene,
	Selection_Set_Armature]

def register_selection_set():
	[bpy.utils.register_class(c) for c in classes]
	bpy.types.Scene.selection_set = PointerProperty(type=Selection_Set_Scene)
	bpy.types.Armature.selection_set = PointerProperty(type=Selection_Set_Armature)
	bpy.types.PoseBone.selection_groups = StringProperty(name='Selection Groups', default='')

def unregister_selection_set():
	[bpy.utils.unregister_class(c) for c in classes]
	del bpy.types.Scene.selection_set
	del bpy.types.Armature.selection_set
	del bpy.types.PoseBone.selection_groups

if __name__ == "__main__":
	register_selection_set()