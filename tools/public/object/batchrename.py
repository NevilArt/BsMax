import bpy
from bpy.types import Operator
from bpy.props import BoolProperty,StringProperty,IntProperty,EnumProperty

def arrange_selected_items(active, selected):
	# bring the active object to first in array
	items = selected
	if active != None:
		if active in items:
			items.remove(active)
		items.insert(0, active)
	# if len(selected) == 0 and active != None:
	#     items.append(active)
	return items

def indexstr(count, index):
	length = len(str(index))
	string = ""
	if length < count:
		for i in range(length, count):
			string += "0"
	return (string + str(index))

def renameitems(self, ctx):
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
			NewName += indexstr(self.digit_length, Index)
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

def draw_ui(self, ctx):
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

def createdialog(self, ctx):
	self.set_name = self.items[0].name
	wm = ctx.window_manager
	return wm.invoke_props_dialog(self, width= 400)

class Objects_OT_BatchRename(Operator):
	bl_idname = "object.batchrename"
	bl_label  = "Batch Rename"

	use_set_name: BoolProperty(name="Set Name:",description="Set Name")
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
		draw_ui(self, ctx)

	def execute(self, ctx):
		renameitems(self, ctx)
		return {'FINISHED'}
	   
	def invoke(self, ctx, event):
		active = ctx.active_object
		selected = ctx.selected_objects
		self.items = arrange_selected_items(active, selected)

		if len(self.items) == 1:
			if ctx.active_object == None:
				ctx.view_layer.objects.active = self.items[0]
			bpy.ops.wm.call_panel(name = 'TOPBAR_PT_name', keep_open = False)
		elif len(self.items) > 1:
			return createdialog(self, ctx)
		return {'FINISHED'}

class Armature_OT_BatchRename(Operator):
	bl_idname = "armature.batchrename"
	bl_label  = "BatchRename"
	use_set_name: BoolProperty(name="Set Name:",description="Set Name")
	set_name: StringProperty(name="",description="Base Name")
	find_replace: BoolProperty(name="Find/Replace",description="Find/Replace")
	find: StringProperty(name="", description="Find this")
	replace: StringProperty(name= "", description="Replace with this")
	clean_digs: BoolProperty(name= "Clean Digits",description="Clean Digits")
	clean_first: IntProperty(name="From First",min=0,description="From First")
	clean_last: IntProperty(name="From Last",min=0,description="From End")
	prefixsuffix: BoolProperty(name="Prefix/Suffix",description="Prefix/Suffix")
	prefix: StringProperty(name="",description="Prefix")
	suffix: StringProperty(name="",description="Suffix")
	use_digits: BoolProperty(name="Add Number:",description="Add Number")
	from_no: IntProperty(name="Start",min=0,description="Start From number")
	increment: IntProperty(name="Increment",min=1,default=1,description="increment value")
	digit_length: IntProperty(name="Length",min=0,max=9,default=3,description="e.g NewName_####")
	items = []

	def draw(self, ctx):
		draw_ui(self, ctx)

	def execute(self, ctx):
		renameitems(self, ctx)
		return {'FINISHED'}
	   
	def invoke(self, ctx, event):
		active = ctx.active_bone
		selected = ctx.selected_bones
		self.items = arrange_selected_items(active, selected)

		if len(self.items) == 1:
			if ctx.active_bone == None:
				pass #TODO set self.items[0] as active bone
			bpy.ops.wm.call_panel(name = 'TOPBAR_PT_name', keep_open = False)
		elif len(self.items) > 1:
			return createdialog(self, ctx)
		return {'FINISHED'}

class Sequences_OT_BatchRename(Operator):
	bl_idname = "sequencer.batchrename"
	bl_label  = "BatchRename"

	use_set_name: BoolProperty(name="Set Name:",description="Set Name")
	set_name: StringProperty(name="",description="Base Name")
	find_replace: BoolProperty(name="Find / Replace",description="Find / Replace")
	find: StringProperty(name="",description="Find this")
	replace: StringProperty(name="", description="Replace with this")
	clean_digs: BoolProperty(name="Clean Digits",description="Clean Digits")
	clean_first: IntProperty(name="From First",min=0,description="From First")
	clean_last: IntProperty(name="From Last",min=0,description="From End")
	prefixsuffix: BoolProperty(name="Prefix / Suffix",description="Prefix / Suffix")
	prefix: StringProperty(name="",description="Prefix")
	suffix: StringProperty(name="",description="Suffix")
	use_digits: BoolProperty(name="Add Number:",description="Add Number")
	from_no: IntProperty(name="Start",min=0,description="Start From number")
	increment: IntProperty(name="Increment",min=1,default=1,description="increment value")
	digit_length: IntProperty(name="Length",min=0,max=9,default=3,description="e.g NewName_####")
	items = []

	def draw(self, ctx):
		draw_ui(self, ctx)

	def execute(self, ctx):
		renameitems(self, ctx)
		return {'FINISHED'}
	   
	def invoke(self, ctx, event):
		active = None # Get active sequence
		selected = ctx.selected_sequences
		self.items = arrange_selected_items(active, selected)

		if len(self.items) == 1:
			return createdialog(self, ctx)
			# if active == None:
			#     pass # Set selected item as active Item
			# bpy.ops.wm.call_panel(name = 'TOPBAR_PT_name', keep_open = False)
		elif len(self.items) > 1:
			return createdialog(self, ctx)
		return {'FINISHED'}

class Node_OT_BatchRename(Operator):
	bl_idname = "node.batchrename"
	bl_label  = "Batch Rename"

	use_set_name: BoolProperty(name="",description="Set Name")
	set_type: EnumProperty(name='',description='',default='SetName',
			items =[('SetName','SetName',''),('SetLabel','SetLabel','')])
	set_name: StringProperty(name="",description="Base Name")
	find_replace: BoolProperty(name="Find / Replace",description="Find / Replace")
	find: StringProperty(name="",description="Find this")
	replace: StringProperty(name="",description="Replace with this")
	clean_digs: BoolProperty(name="Clean Digits",description="Clean Digits")
	clean_first: IntProperty(name="From First",min=0,description="From First")
	clean_last: IntProperty(name="From Last",min=0,description="From End")
	prefixsuffix: BoolProperty(name="Prefix / Suffix",description="Prefix / Suffix")
	prefix: StringProperty(name="",description="Prefix")
	suffix: StringProperty(name="",description="Suffix")
	use_digits: BoolProperty(name="Add Number:",description="Add Number")
	from_no: IntProperty(name="Start",min=0,description="Start From number")
	increment: IntProperty(name="Increment",min=1,default=1,description="increment value")
	digit_length: IntProperty(name="Length",min=0,max=9,default=3,description="e.g NewName_####")
	items = []

	def draw(self, ctx):
		draw_ui(self, ctx)

	def execute(self, ctx):
		renameitems(self, ctx)
		return {'FINISHED'}
	   
	def invoke(self, ctx, event):
		active = ctx.active_node
		selected = ctx.selected_nodes
		self.items = arrange_selected_items(active, selected)

		if len(self.items) == 1:
			return createdialog(self, ctx)
			# if active == None:
			#     pass # Set selected item as active
			# bpy.ops.wm.call_panel(name = 'TOPBAR_PT_name', keep_open = False)

		elif len(self.items) > 1:
			return createdialog(self, ctx)
		return {'FINISHED'}

def batchrename_cls(register):
	classes = [Objects_OT_BatchRename, Armature_OT_BatchRename,
			Sequences_OT_BatchRename, Node_OT_BatchRename]

	if register:
		[bpy.utils.register_class(c) for c in classes]
	else:
		[bpy.utils.unregister_class(c) for c in classes]

if __name__ == '__main__':
	batchrename_cls(True)

__all__ = ["batchrename_cls"]