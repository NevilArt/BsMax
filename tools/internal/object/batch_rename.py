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
# 2024/08/23

import bpy

from bpy.types import Operator
from bpy.props import BoolProperty, StringProperty, IntProperty, EnumProperty

from bsmax.math import get_index_str


def get_selected_collections(ctx):
	#TODO find a way to get lsit of selected collections
	return []


def arrange_selected_items(active, selected):
	# bring the active object to first in array
	items = selected
	if active:
		if active in items:
			items.remove(active)
		items.insert(0, active)
	# if selected and active:
	# 	items.append(active)
	return items


def rename_items(cls, ctx):
	index = cls.from_no
	new_names = []
	for item in cls.items:
		# Get Object Original Name #
		new_name = item.name

		# Set the Base name #
		if cls.use_set_name or len(cls.items) == 1:
			new_name = cls.set_name

		# Remove First characters #
		if cls.clean_digs:
			new_name = new_name[
				cls.clean_first : cls.clean_first + len(new_name)
			]

			new_name = new_name[1 : len(new_name) - cls.clean_last]

		# Add Prefix and sufix to the new name #
		if cls.prefixsuffix:
			new_name = cls.prefix + new_name
			new_name = new_name + cls.suffix

		# Add Digits to end of new name #
		if cls.use_digits:
			new_name += get_index_str(cls.digit_length, index)
			index += 1

		# Find and Replace #
		if cls.find_replace:
			new_name = new_name.replace(cls.find, cls.replace)

		# Trim Left and Right #
		new_name = new_name.strip()

		new_names.append(new_name)
	
	# Set random name to the object #
	for index, item in enumerate(cls.items):
		random_name = "__new_random_name_of__" + str(index)
		if ctx.area.type == 'NODE_EDITOR':
			if cls.set_type == 'SetLabel':
				item.label = random_name
		item.name = random_name

	# Set the new name to the object #
	for item in zip(cls.items, new_names):
		if ctx.area.type == 'NODE_EDITOR':
			if cls.set_type == 'SetLabel':
				item[0].label = item[1]
		item[0].name = item[1]


def multi_item_rename_draw(self, ctx):
	if len(self.items) == 1: # single object
		layout = self.layout
		layout.prop(self, "set_name")
		return

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


def multi_item_rename_invoke(self, ctx):
	active, selected, mode = None, [], ''

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
		active = ctx.active_sequence_strip
		selected = ctx.selected_editable_sequences

	elif mode == 'OUTLINER':
		active = ctx.collection
		selected = get_selected_collections(ctx)

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
		return ctx.window_manager.invoke_props_dialog(self, width=400)

	return {'FINISHED'}


class WM_OT_Multi_Item_Rename(Operator):
	bl_idname = "wm.multi_item_rename" 
	bl_label  = "Multi Item Rename"
	bl_options = {'REGISTER', 'UNDO'}

	force: EnumProperty(
		name="",
		items =[
			('AUTO', "Auto", ""),
			('OBJECT', "Object", "")
		],
		default='AUTO',
		description=""
	) # type: ignore

	use_set_name: BoolProperty(
		name="Set Name:", description="Set Name"
	) # type: ignore
	
	set_type: EnumProperty(
		name='',
		items =[
			('SetName', "SetName", ""),
			('SetLabel', "SetLabel", "")
		],
		default='SetName',
		description=''
	) # type: ignore

	set_name: StringProperty(name="", description="Base Name") # type: ignore
	find_replace: BoolProperty(
		name="Find/Replace", description="Find/Replace"
	) # type: ignore
	
	find: StringProperty(name="", description="Find this") # type: ignore
	replace: StringProperty(
		name="", description="Replace with this"
	) # type: ignore
	
	clean_digs: BoolProperty(
		name="Clean Digits", description="Clean Digits"
	) # type: ignore
	
	clean_first: IntProperty(
		name="From First", min=0, description="From First"
	) # type: ignore

	clean_last: IntProperty(
		name="From Last", min=0, description="From End"
	) # type: ignore
	
	prefixsuffix: BoolProperty(
		name="Prefix/Suffix", description="Prefix/Suffix"
	) # type: ignore
	
	prefix: StringProperty(name="", description="Prefix") # type: ignore
	suffix: StringProperty(name="", description="Suffix") # type: ignore
	use_digits: BoolProperty(
		name="Add Number:", description="Add Number"
	) # type: ignore
	
	from_no: IntProperty(
		name="Start", min=0, description="Start From number"
	) # type: ignore
	
	increment: IntProperty(
		name="Increment", min=1, default=1, description="increment value"
	)  # type: ignore
	
	digit_length: IntProperty(
		name="Length", min=0, max=9, default= 3,
		description= "e.g NewName_####"
	) # type: ignore
	
	items = []

	def draw(self, ctx):
		multi_item_rename_draw(self, ctx)

	def execute(self, ctx):
		rename_items(self, ctx)
		return {'FINISHED'}
	   
	def invoke(self, ctx, _):
		return multi_item_rename_invoke(self, ctx)


def register_batchrename():
	bpy.utils.register_class(WM_OT_Multi_Item_Rename)


def unregister_batchrename():
	bpy.utils.unregister_class(WM_OT_Multi_Item_Rename)


if __name__ == '__main__':
	register_batchrename()