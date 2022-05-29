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

class Bone_Group:
	def __init__(self, name, groups):
		self.name = name
		self.groups = groups

class Armature_Selection_Set:
	def __init__(self):
		self.armature = None
		self.button_names = []
		self.clipboard_test_key = '"""__armature_selection_set_clipboard__"""'
		
		""" Orginal Data for Restore"""
		self.orig_coumns = 0
		self.orig_raws = 0
		self.orig_bones = []
	
	def get_names_from_armature(self, armature, reload=False):
		""" calculate once if armature changes """
		if self.armature != armature or reload:
			""" fill name list if less than buttons count """
			buttons_count = armature.data.selection_set.columns * armature.data.selection_set.rows
			names = armature.data.selection_set.names.split(':')
			
			""" Read for first time """
			if len(names) == 1:
				if names[0] == '':
					names = []
			
			""" Create name for new ganarated buttons """
			if len(names) < buttons_count:
				for i in range(len(names), buttons_count):
					names.append('')
			
			self.button_names = names
			self.armature = armature
	
	def store_armature_date(self, armature):
		self.orig_coumns = armature.data.selection_set.columns
		self.orig_raws = armature.data.selection_set.rows

		# print("---------------------------------")
		for bone in armature.pose.bones:
			name = bone.name
			# selection_groups = bone.selection_groups
			# print(name, selection_groups)
			new_bone = Bone_Group(name, [])
			self.orig_bones.append(new_bone)
		

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
	
	def copy_to_clipboard(self, ctx):
		if self.armature:
			""" Read data from armature """
			armature = ctx.active_object
			names = armature.data['selection_set']['names']
			columns = armature.data.selection_set.columns
			rows = armature.data.selection_set.rows
			
			""" Convert data to string """
			string = self.clipboard_test_key + '\n'
			string += '\n'
			string += 'import bpy\n'
			string += '\n'
			string += 'armature = bpy.context.active_object' + '\n'
			string += 'armature.data["selection_set"]["names"] = "' + names + '"\n'
			string += 'armature.data.selection_set.columns = ' + str(columns) + '\n'
			string += 'armature.data.selection_set.rows = ' + str(rows) + '\n'
			string += '\n'
			string += 'bone_groups = (\n' # Open array

			for bone in armature.pose.bones:
				name = bone.name
				selection_groups = bone.selection_groups
				string += '["' + name + '", "' + selection_groups + '"],\n'
			
			string += ')\n' # Close the array
			string += '\n'

			""" Check and aply selection data to new bonse is exist """
			string += 'for name, selection_groups in bone_groups:\n'
			string += '	for bone in armature.pose.bones:\n'
			string += '		if name == bone.name:\n'
			string += '			bone.selection_groups = selection_groups\n'
			string += '			break\n'
			string += '\n'
			string += 'bpy.context.scene.selection_set.mode = "EDIT"\n'

			""" Send data to clipboard """
			ctx.window_manager.clipboard = string
	
	def past_from_clipboard(self, ctx):
		if self.armature:
			string = ctx.window_manager.clipboard
			test = string.splitlines()
			if len(test) > 0:
				if test[0] == self.clipboard_test_key:
					exec(string)
					self.get_names_from_armature(self.armature, reload=True)

arm_sel_set = Armature_Selection_Set()



def rename_selection_set(self, ctx):

	# TODO temprary solution but works
	arm_sel_set.get_names_from_armature(ctx.active_object, reload=True)
	
	""" Filter the new name """
	new_name = ''
	selection_set = ctx.scene.selection_set
	
	for v in selection_set.name:
		if v != ':':
			new_name += v
	
	# TODO check before remove
	# this part is unnececery
	if new_name == '':
		new_name = ' '
	
	if selection_set.name != new_name:
		selection_set.name = new_name
		
	""" Put new name on names list """
	arm_sel_set.set_names_to_armature(ctx.active_object, new_name, selection_set.active)



class Selection_Set_Scene(PropertyGroup):
	mode: EnumProperty(name='Mode', default='SELECT',
		items =[
			('SELECT', 'Select', 'Select group of bones'),
			('SET', 'Set', 'Set Selection groups'),
			# ('RENAME', 'Rename', 'Rename buttons'),
			('EDIT', 'Edit', 'Edit buttons layout')])
	multi: BoolProperty(name='Multi Selection', default=False)
	unselect: BoolProperty(name='Remove From Selection', default=False)
	name: StringProperty(name="", update=rename_selection_set)
	active: IntProperty(name="", default=0)



class Selection_Set_Armature(PropertyGroup):
	columns: IntProperty(name='columns', min=1, max=100, default=3)
	rows: IntProperty(name='row', min=1, max=100, default=10)
	names: StringProperty(name='')



class ARMATURE_OT_Selection_Set_Transfer(Operator):
	bl_idname = 'pose.transfer_selection_set'
	bl_label = 'Transfer Selection set'
	# bl_description = ''
	bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}
	action: StringProperty()
	
	def execute(self, ctx):
		if self.action == 'COPY':
			arm_sel_set.copy_to_clipboard(ctx)
		else:
			arm_sel_set.past_from_clipboard(ctx)
		return{'FINISHED'}



class ARMATURE_OT_Selection_Set_Dimension_Resize(Operator):
	bl_idname = 'pose.selection_set_dimension_resize'
	bl_label = 'Selection set Dimension Resize'
	# bl_description = ''
	bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}
	action: StringProperty()
	
	def execute(self, ctx):
		selection_set = ctx.active_object.data.selection_set

		if self.action == 'SUB_COL_LEFT':
			if selection_set.columns > 2:
				selection_set.columns -= 1
		
		elif self.action == 'ADD_COL_LEFT':
			selection_set.columns += 1
		
		elif self.action == 'ADD_COL_RIGHT':
			selection_set.columns += 1
		
		elif self.action == 'SYB_COL_RIGHT':
			if selection_set.columns > 2:
				selection_set.columns -= 1
		
		elif self.action == 'SUB_ROW_LEFT':
			if selection_set.rows > 2:
				selection_set.rows -= 1
		
		elif self.action == 'ADD_ROW_LEFT':
			selection_set.rows += 1
		
		elif self.action == 'ADD_ROW_RIGHT':
			selection_set.rows += 1
		
		elif self.action == 'SUB_ROW_RIGHT':
			if selection_set.rows > 2:
				selection_set.rows -= 1
		
		return{'FINISHED'}



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
			if not s in {'', ' '}:
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
		
		# elif ctx.scene.selection_set.mode == 'RENAME':
		elif ctx.scene.selection_set.mode == 'EDIT':
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
		# row.prop(scene_selection_set, 'unselect',icon='REMOVE', text='')
		row.prop(scene_selection_set, 'mode')
		
		if scene_selection_set.mode == 'EDIT':
			ptss = 'pose.transfer_selection_set'
			row.operator(ptss, text='', icon='COPYDOWN').action = 'COPY'
			row.operator(ptss, text='', icon='PASTEDOWN').action = 'PASTE'

			# pssdr = 'pose.selection_set_dimension_resize'
			# row_cr = box.row()
			# box_c = row_cr.box()
			# row_c = box_c.row()
			# row_c.operator(pssdr, text='', icon='REMOVE').action='SUB_COL_LEFT'
			# row_c.operator(pssdr, text='', icon='ADD').action='ADD_COL_LEFT'
			# row_c.label(text= 'C: ' + str(obj_selection_set.columns))
			# row_c.operator(pssdr, text='', icon='ADD').action='ADD_COL_RIGHT'
			# row_c.operator(pssdr, text='', icon='REMOVE').action='SYB_COL_RIGHT'

			# box_r = row_cr.box()
			# row_r = box_r.row()
			# row_r.operator(pssdr, text='', icon='REMOVE').action='SUB_ROW_LEFT'
			# row_r.operator(pssdr, text='', icon='ADD').action='ADD_ROW_LEFT'
			# row_r.label(text= 'R: ' +  str(obj_selection_set.rows))
			# row_r.operator(pssdr, text='', icon='ADD').action='ADD_ROW_RIGHT'
			# row_r.operator(pssdr, text='', icon='REMOVE').action='SUB_ROW_RIGHT'
			
			row = box.row()
			row.prop(obj_selection_set, 'columns', text='Columns:')
			row.prop(obj_selection_set, 'rows', text='Rows:')

			
		
		# Draw Buttons
		#	[][][][]
		#	[][][][]
		#	[][][][]

		box = layout.box()
		mode = scene_selection_set.mode
		active = scene_selection_set.active
		
		for r in range(obj_selection_set.rows):

			row = box.row()
			for c in range(obj_selection_set.columns):

				index = r * obj_selection_set.columns + c
				
				""" Draw Rename box for active slot """
				if mode == 'EDIT' and active == index:
					row.prop(scene_selection_set, 'name')
				else:
					name = arm_sel_set.get_name_by_index(ctx.active_object, index)
					
					if mode in {'SET', 'SELECT'} and name in {'', ' '}:
						row.label(text='') # Hiden button
					else:
						row.operator('pose.selection_set', text=name).index=index				



classes = [
	Selection_Set_Scene,
	Selection_Set_Armature,
	Armature_OP_Selection_Set,
	ARMATURE_OT_Selection_Set,
	ARMATURE_OT_Selection_Set_Transfer,
	ARMATURE_OT_Selection_Set_Dimension_Resize]

def register_selection_set():
	for c in classes:
		bpy.utils.register_class(c)
	bpy.types.Scene.selection_set = PointerProperty(type=Selection_Set_Scene)
	bpy.types.Armature.selection_set = PointerProperty(type=Selection_Set_Armature)
	bpy.types.PoseBone.selection_groups = StringProperty(name='Selection Groups', default='')

def unregister_selection_set():
	for c in classes:
		bpy.utils.unregister_class(c)
	del bpy.types.Scene.selection_set
	del bpy.types.Armature.selection_set
	del bpy.types.PoseBone.selection_groups

if __name__ == "__main__":
	# unregister_selection_set()
	register_selection_set()