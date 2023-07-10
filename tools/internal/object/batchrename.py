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
from bpy.props import BoolProperty, StringProperty, IntProperty, EnumProperty

from bsmax.math import get_index_str



def get_active_collection(ctx):
	active_layer_name = ctx.view_layer.active_layer_collection.name
	if active_layer_name == "Master Collection":
		collection = ctx.scene.collection
	else:
		collection = bpy.data.collections[active_layer_name]
	return collection



def arrange_selected_items(active, selected):
	# bring the active object to first in array
	items = selected
	if active != None:
		if active in items:
			items.remove(active)
		items.insert(0, active)
	# if len(selected) == 0 and active != None:
	# 	items.append(active)
	return items



class WM_OT_Multi_Item_Rename(Operator):
	bl_idname = "wm.multi_item_rename" 
	bl_label  = "Multi Item Rename"
	bl_options = {'REGISTER', 'UNDO'}

	force: EnumProperty(name='',description='',default='AUTO',
			items =[('AUTO','Auto',''),('OBJECT','Object','')])

	use_set_name: BoolProperty(name="Set Name:",description="Set Name")
	set_type: EnumProperty(name='',description='',default='SetName',
			items =[('SetName','SetName',''),('SetLabel','SetLabel','')])
	set_name: StringProperty(name="",description="Base Name")
	find_replace: BoolProperty(name="Find/Replace",description="Find/Replace")
	find: StringProperty(name="",description="Find this")
	replace: StringProperty(name="",description="Replace with this")
	clean_digs: BoolProperty(name="Clean Digits",description="Clean Digits")
	clean_first: IntProperty(name="From First",min=0,description="From First")
	clean_last: IntProperty(name="From Last",min=0,description="From End")
	prefixsuffix: BoolProperty(name="Prefix/Suffix",description="Prefix/Suffix")
	prefix: StringProperty(name="",description="Prefix")
	suffix: StringProperty(name="",description="Suffix")
	use_digits: BoolProperty(name="Add Number:",description="Add Number")
	from_no: IntProperty(name="Start",min=0,description="Start From number")
	increment: IntProperty(name="Increment",min=1,default=1,description="increment value")
	digit_length: IntProperty(name="Length",min=0,max=9,default= 3,description= "e.g NewName_####")
	items = []

	def draw(self, ctx):
		if len(self.items) > 1:
			box = self.layout.box()
			if ctx.area.type == 'NODE_EDITOR':
				row = box.row(align = True)
				row.prop(self, "use_set_name")
				spl = row.split(factor = 0.6, align = False)
				row = spl.row(align = False)
				row.prop(self, "set_type")
				spl = row.split(factor = 2.0, align = False)
				row = spl.row(align = False)
				row.prop(self, "set_name")
			else:
				row = box.row(align = True)
				row.prop(self, "use_set_name")
				spl = row.split(factor = 2.0, align = False)
				row = spl.row(align = True)
				row.prop(self, "set_name")
			row = box.row(align = True)
			row.prop(self, "find_replace")
			row.prop(self, "find")
			row.prop(self, "replace")
			row = box.row(align = True)
			row.prop(self, "clean_digs")
			row.prop(self, "clean_first")
			row.prop(self, "clean_last")
			row = box.row(align = True)
			row.prop(self, "prefixsuffix")
			row.prop(self, "prefix")
			row.prop(self, "suffix")
			row = box.row(align = True)
			row.prop(self, "use_digits")
			spl = row.split()
			row = spl.row(align = True)
			row.alignment = 'RIGHT'
			row.prop(self, "from_no")
			row.prop(self, "increment")
			row.prop(self, "digit_length")
		else:
			layout = self.layout
			layout.prop(self, "set_name")
	
	def rename_items(self, ctx):
		Index = self.from_no
		for item in self.items:
			# Get Object Original Name #
			NewName = item.name
			# Set the Base name #
			if self.use_set_name or len(self.items) == 1:
				NewName = self.set_name
			# Remove First characters #
			if self.clean_digs:
				NewName = NewName[self.clean_first : self.clean_first + len(NewName)]
				NewName = NewName[1 : len(NewName) - self.clean_last]
			# Add Prefix and sufix to the new name #
			if self.prefixsuffix:
				NewName = self.prefix + NewName
				NewName = NewName + self.suffix
			# Add Digits to end of new name #
			if self.use_digits:
				NewName += get_index_str(self.digit_length, Index)
				Index += 1
			# Find and Replace #
			if self.find_replace:
				NewName = NewName.replace(self.find, self.replace)
			# Trim Left and Right #
			NewName = NewName.strip()
			# Set the new name to the object #
			if ctx.area.type == 'NODE_EDITOR':
				if self.set_type == 'SetLabel':
					item.label = NewName
				else:
					item.name = NewName    
			else:
				item.name = NewName

	def execute(self, ctx):
		self.rename_items(ctx)
		self.report({'OPERATOR'},'bpy.ops.wm.multi_item_rename()')
		return {'FINISHED'}
	   
	def invoke(self, ctx, event):
		active, selected, mode = None,[],''
		if ctx.area.type == 'VIEW_3D':
			if ctx.mode in {'OBJECT','EDIT_ARMATURE','POSE'}:
				mode = ctx.mode
		elif ctx.area.type in {'NODE_EDITOR','SEQUENCE_EDITOR','OUTLINER'}:
			mode = ctx.area.type
		
		if self.force == 'OBJECT':
			mode == 'OBJECT'

		if mode == 'OBJECT':
			active = ctx.active_object
			selected = ctx.selected_objects
		elif mode == 'EDIT_ARMATURE':
			active = ctx.active_bone
			selected = ctx.selected_bones
		elif mode == 'POSE':
			active = ctx.active_bone
			selected = ctx.selected_pose_bones
		elif mode == 'NODE_EDITOR':
			active = ctx.active_node
			selected = ctx.selected_nodes
		elif mode == 'SEQUENCE_EDITOR':
			active = None #ctx.active_sequences
			selected = ctx.selected_sequences
		elif mode == 'OUTLINER':
			active = get_active_collection(ctx)
			# selected = get selected collection

		self.items = arrange_selected_items(active, selected)

		if len(self.items) == 1:
			if mode == 'OBJECT':
				if ctx.active_object == None:
					ctx.view_layer.objects.active = self.items[0]
			elif mode == 'POSE':
				if ctx.active_bone == None:
					ctx.object.data.bones.active = self.items[0]

			bpy.ops.wm.call_panel(name='TOPBAR_PT_name', keep_open=False)
		
		elif len(self.items) > 1:
			self.set_name = self.items[0].name
			return ctx.window_manager.invoke_props_dialog(self, width= 400)

		return {'FINISHED'}



def register_batchrename():
	bpy.utils.register_class(WM_OT_Multi_Item_Rename)



def unregister_batchrename():
	bpy.utils.unregister_class(WM_OT_Multi_Item_Rename)



if __name__ == "__main__":
	register_batchrename()