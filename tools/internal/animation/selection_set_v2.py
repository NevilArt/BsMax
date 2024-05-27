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

from math import sqrt

from bpy.types import Operator, Panel, PropertyGroup
from bpy.props import (
	IntProperty, StringProperty,
	BoolProperty, PointerProperty, EnumProperty
)


buttonSheet = []



def get_command_by_index(index):
	commands = (
		("RESETTRANSFORM", "Reset All", "Reset Location, Rotation, Scale"),#0
		("RESETLOCATION", "Reset Location", "Reset Location"),#1
		("RESETROTATION", "Reset ROTATION", "Reset Rotation"),#2
		("RESETSCALE", "Reset Scale", "Reset Scale"),#3
		("RESETLR", "Reset Location/Rotation", "Reset Location and Rotation"),#4
		("INSERTKEYALL", "Insert Key All", "Insert key to Location, Rotation, Scale"),#5
		("INSERTKEYLOCATION", "Insert Key Location", "Insert key to Location"),#6
		("INSERTKEYROTATION", "Insert Key Rotation", "Insert key to Rotation"),#7
		("INSERTKEYSCALE", "Insert Key Scale", "Insert key to Scale"),#8
		("INSERTKEYLR", "Insert Key Location/Rotation", "Insert key to Location and Rotation"),#9
		("HIDE", "Hide", "Hide bones"),#10
		("UNHIDE", "Unhide", "Unhide bones"),#11
		("HIDE", "Hide", "Hide bones"),#12
		("NONE", "None", "DO nothing")
	)
	if index < len(commands):
		return commands[index]
	return None



def button_get_unique_id(self):
	tab = self.owner
	ids = [button.id for button in tab.buttons]

	if ids:
		maxId = max(ids)
		return maxId + 1

	return 0


#Button{
# 'name':'',
# 'id':0, 'column':0, row:0,
# 'icon':'', command:''
# }
def get_button_layout(tab, button, layout):
	# icon = button['icon']
	buttonOperator = layout.operator(
		'pose.selection_set',
		text=button['name'],
		# icon=icon
	).id = button['id']
	# buttonOperator.tab = tab['id']
	# buttonOperator.command = button['command']



def armature_selection_set_get_unique_id(self):
	ids = [self.tabs[key]['id'] for key in self.tabs.keys()]
	if ids:
		return max(ids) + 1
	return 0



def armature_selection_set_new_tab(self, ctx):
	sceneSelectionSet = ctx.scene.selection_set

	id = armature_selection_set_get_unique_id(self)
	tabName = sceneSelectionSet.tabName if sceneSelectionSet.tabName else "Tab"
	newTab = {}
	newTab['name'] = tabName
	newTab['id'] = id
	newTab['columns'] = sceneSelectionSet.columns
	newTab['rows'] = sceneSelectionSet.rows
	newTab['buttons'] = {}
	self.tabs[str(id)] = newTab

	return newTab



def armature_selection_set_get_active_tab(self, ctx):
	if self.tab in self.tabs:
		return self.tabs[self.tab]

	if self.tabs:
		key = list(self.tabs.keys())[0]
		self.tab = key
		return self.tabs[key]

	return self.new_tab(ctx)



def scene_selection_set_tab_name_update(self, ctx):
	objselectionSet = ctx.object.data.selection_set
	activeTab = objselectionSet.active_tab(ctx)
	activeTab = objselectionSet.tabs[objselectionSet.tab]
	activeTab['name'] = self.tabName



def scene_selection_set_columns_update(self, ctx):
	objselectionSet = ctx.object.data.selection_set
	activeTab = objselectionSet.active_tab(ctx)
	activeTab['columns'] = self.columns


def scene_selection_set_rows_update(self, ctx):
	objselectionSet = ctx.object.data.selection_set
	activeTab = objselectionSet.active_tab(ctx)
	activeTab['rows'] = self.rows



def tab_operator_execute(self, ctx):
	objselectionSet = ctx.object.data.selection_set

	if self.action == "ADD":
		objselectionSet.new_tab(ctx)
		return{'FINISHED'}

	elif self.action == "REMOVE":
		objselectionSet.remove_tab(ctx)
		return{'FINISHED'}

	return{'FINISHED'}



def selection_set_operator_bone_select(self, ctx):
	print(">> Do selection or command")



def selection_set_operator_bone_autohide(ctx, hide):
	print(">> Utohide")




def selection_set_operator_set(self, ctx):
	print(">> DO SET")
	objSelectionSet = ctx.object.data.selection_set
	bones = ctx.object.pose.bones
	activeButton = objSelectionSet.get_active_button(ctx)
	id = activeButton['id']
	print(">> ID >>",id)

	for bone in bones:
		if bone.bone.select:
			print(bone.name)
			# bone.selection_groups
		else:
			pass



def selection_set_operator_execute(self, ctx):
	mode = ctx.scene.selection_set.mode
	hide = ctx.scene.selection_set.autohide

	if mode == 'SELECT':
		selection_set_operator_bone_select(self, ctx)
		selection_set_operator_bone_autohide(ctx, hide)

	elif mode == 'SET':
		selection_set_operator_set(self, ctx)

	elif mode == 'EDIT':
		objSelectionSet = ctx.object.data.selection_set
		sceneSelectionSet = ctx.scene.selection_set
		sceneSelectionSet.activeRow = self.row
		sceneSelectionSet.activeColamn = self.column
		button = objSelectionSet.get_active_button(ctx)
		if button:
			sceneSelectionSet.buttonName = button['name']
		else:
			sceneSelectionSet.buttonName = ""

	return{'FINISHED'}



def armature_selection_set_tab_items(self, ctx):
	if ctx.object.type != "ARMATURE":
		return []

	items = []

	for key in self.tabs.keys():
		tab = self.tabs[key]
		items.append((str(tab['id']), tab['name'], ""))

	return items



def armature_selection_set_tab_update(self, ctx):
	sceneSelectionSet = ctx.scene.selection_set
	tab = self.active_tab(ctx)
	if tab:
		sceneSelectionSet.tabName =tab['name']
		sceneSelectionSet.columns = tab['columns']
		sceneSelectionSet.rows = tab['rows']
		sceneSelectionSet.activeRow = -1
		sceneSelectionSet.activeColamn = -1



def armature_selection_set_get_active_button(self, ctx):
	sceneSelectionSet = ctx.scene.selection_set
	activeRow = sceneSelectionSet.activeRow
	activeColamn = sceneSelectionSet.activeColamn
	tab = self.tabs[self.tab]
	buttonKey = str(activeColamn) + "." + str(activeRow)

	if buttonKey in tab['buttons']:
		return tab['buttons'][buttonKey]

	if not self.tab in self.tabs:
		return None

	for key in self.tabs[self.tab]['buttons'].keys():
		button = self.tabs[self.tab]['buttons'][key]
		if button['row'] == activeRow and button['column'] == activeColamn:
			return button

	return None



def get_unique_button_id(tab):
	ids = []
	for key in tab['buttons'].keys():
		button = tab['buttons'][key]
		ids.append(button['id'])
	if ids:
		return max(ids)+1
	return 0



def armature_selection_set_new_button(self, ctx):
	objSelectionSet = ctx.object.data.selection_set
	sceneSelectionSet = ctx.scene.selection_set
	activeColamn = sceneSelectionSet.activeColamn
	activeRow = sceneSelectionSet.activeRow
	dicName = str(activeColamn) + "." + str(activeRow)
	tab = objSelectionSet.active_tab(ctx)
	newButton = tab['buttons'][dicName] = {}
	newButton['name'] = sceneSelectionSet.buttonName
	print(">>--->>", get_unique_button_id(tab))
	newButton['id'] = 0#get_unique_button_id(tab)
	newButton['column'] = activeColamn
	newButton['row'] = activeRow
	newButton['icon'] = None
	newButton['command'] = ''



def armature_selection_set_get_button_sheet(self, ctx):
	if not self.tabs:
		self.new_tab(ctx)

	if not self.tab in self.tabs:
		return []

	tab = self.tabs[self.tab]
	buttonSheet = []
	# Create an empty sheet
	for _ in range(tab['rows']):
		rowButtons = []
		for _ in range(tab['columns']):
			rowButtons.append(None)
		buttonSheet.append(rowButtons)

	# add button in places
	for key in tab['buttons'].keys():
		btn = tab['buttons'][key]
		row = btn['row'] if 'row' in btn else 0
		column = btn['column'] if 'column' in btn else 0

		if row >= len(buttonSheet):
			continue
		if column >= len(buttonSheet[row]):
			continue
		
		buttonSheet[btn['row']][btn['column']] = btn

	return buttonSheet



def rename_active_button(self, ctx):
	objSelectionSet = ctx.object.data.selection_set
	sceneSelectionSet = ctx.scene.selection_set
	activeColamn = sceneSelectionSet.activeColamn
	activeRow = sceneSelectionSet.activeRow
	dicName = str(activeColamn) + "." + str(activeRow)

	tab = objSelectionSet.active_tab(ctx)
	if not dicName in tab['buttons']:
		armature_selection_set_new_button(objSelectionSet, ctx)
	
	button = tab['buttons'][dicName]
	button['name'] = sceneSelectionSet.buttonName



globalIconSheet = []
def armature_ot_selectionset_get_icons():
	""" create icon sheet once and return the same sheet
		args:
			None
		
		return:
			aray in array of Icon names

			[[name, name],[name, name],..]
	"""
	global globalIconSheet
	if globalIconSheet:
		return globalIconSheet
	
	prop = bpy.types.UILayout.bl_rna.functions["prop"]
	iconKeys = prop.parameters['icon'].enum_items.keys()

	globalIconSheet.clear()
	globalIconSheet.append([])
	for key in iconKeys:
		lastRow = globalIconSheet[-1]
		if len(lastRow) >= 38:
			globalIconSheet.append([])
		lastRow.append(key)

	return globalIconSheet



activeArmatureName = ""
def scene_selection_set_armature_update(ctx):
	global activeArmatureName

	if not ctx.object:
		return
	
	if activeArmatureName == ctx.object.name:
		return
	
	activeArmatureName = ctx.object.name
	objSelectionSet = ctx.object.data.selection_set
	tab = objSelectionSet.active_tab(ctx)
	#TODO
	# print(">>", tab['name'], tab['columns'], tab['rows'])
	# self.tabName = tab['name']
	# self.columns = tab['columns']
	# self.rows = tab['rows']

	# self.buttonName = ""
	# self.activeRow = 0
	# self.activeColamn = 0


def armature_ot_selectionset_icon_draw(self, ctx):
	iconSheet = armature_ot_selectionset_get_icons()
	layout = self.layout
	for sheetRow in iconSheet:
		row = layout.row()
		for icon in sheetRow:
			row.operator(
				'pose.selection_set_icon',
				text=""
				# icon=icon
			).icon=icon



def armature_ot_selectionset_command_draw(self, ctx):
	pass



def armature_ot_selectionset_icon_execute(self, ctx):
	objSelectionSet = ctx.object.data.selection_set
	button = objSelectionSet.get_active_button(ctx)
	if button:
		button['icon'] = self.icon
	return {'FINISHED'}



def armature_ot_selectionset_invoke(self, ctx, event):
	""" Read ctrl, shift alt state """
	self.ctrl = event.ctrl
	self.shift = event.shift
	self.alt = event.alt
	return self.execute(ctx)



def armature_op_selectionset_draw(self, ctx):
	layout = self.layout

	scene_selection_set_armature_update(ctx)

	sceneSelectionSet = ctx.scene.selection_set
	objSelectionSet = ctx.object.data.selection_set
	mode = sceneSelectionSet.mode
	buttonSheet = objSelectionSet.get_button_sheet(ctx)
	tab = objSelectionSet.active_tab(ctx)
	activeRow = sceneSelectionSet.activeRow
	activeColamn = sceneSelectionSet.activeColamn

	""" Controll """
	box = layout.box()
	row = box.row()

	hideIcon = 'HIDE_ON' if sceneSelectionSet.autohide else 'HIDE_OFF'
	row.prop(sceneSelectionSet, 'autohide',icon=hideIcon, text='')
	row.prop(sceneSelectionSet, 'mode')

	row.operator(
		'wm.url_open', 	icon='HELP'
	).url= "https://github.com/NevilArt/BsMax/wiki/Animation-SelectionSet"

	if mode == 'EDIT':
		ptss = 'pose.transfer_selection_set'
		row.operator(ptss, text='', icon='COPYDOWN').action = 'COPY'
		row.operator(ptss, text='', icon='PASTEDOWN').action = 'PASTE'

		row = box.row()
		row.prop(sceneSelectionSet, 'columns', text='Columns:')
		row.prop(sceneSelectionSet, 'rows', text='Rows:')
		row = box.row()
		row.prop(sceneSelectionSet, 'tabName')

		row.operator('pose.selection_set_tab',
			text='', icon='ADD'
		).action="ADD"

		row.operator('pose.selection_set_tab',
			text='', icon='REMOVE'
		).action="REMOVE"

		# row = box.row()
		# row.operator('pose.selection_set_icon',
		# 	text="Icon",
		# 	icon="ADD"
		# )

		# row.operator('pose.selection_set_command',
		# 	text="Command",
		# )

	# Drawe Tabs
	box = layout.box()
	row = box.row()
	if mode == 'EDIT':
		pass

	else:
		row.label(text=ctx.object.name)

	row = box.row()
	row.prop(objSelectionSet, 'tab', expand=True)

	# Draw Buttons
	#	[][][][]
	#	[][][][]
	#	[][][][]

	box = layout.box()

	if mode in {'SET', 'SELECT'}:
		for line in buttonSheet:
			row = box.row()
			for button in line:
				if button:
					get_button_layout(tab, button, row)
					#button.get_layout(row)
				else:
					row.label(text='') # Hiden button
	
	elif mode == 'EDIT':
		for rowIndex, line in enumerate(buttonSheet):
			row = box.row()
			for columnIndex, button in enumerate(line):
				if rowIndex == activeRow and columnIndex == activeColamn:
					row.prop(
						sceneSelectionSet, 'buttonName'
					)

				else:
					name = button['name'] if button else ""
					operator = row.operator(
						'pose.selection_set',
						text=name
					)
					operator.row = rowIndex
					operator.column = columnIndex



class PoseBoneSelectionSet(PropertyGroup):
	tabs = {}

	def is_in_list(self, tabId, buttonId):
		if tabId in self.tabs:
			return buttonId in self.tabs[tabId]
		return False
	
	def append(self, tabId, buttonId):
		if tabId in self.tabs:
			if not buttonId in self.tabs[tabId]:
				self.tabs[tabId].append(buttonId)
				return
		self.tabs[tabId] = [buttonId]
	
	def remove_tab(self, tabId):
		if tabId in self.tabs:
			del self.tabs[tabId]
	
	def remove_button(self, tabId, buttonId):
		if tabId in self.tabs:
			if buttonId in self.tabs[tabId]:
				self.tabs[tabId].remove(buttonId)



# selection set curent sata in scene and no have saving data
class SceneSelectionSet(PropertyGroup):
	# Evru time shown
	mode: EnumProperty(
		name='Mode',
		default='SELECT',
		items =[
			('SELECT', 'Select', 'Select group of bones'),
			('SET', 'Set', 'Set Selection groups'),
			('EDIT', 'Edit', 'Edit buttons layout')
		]
	) # type: ignore

	# Shown on select mode
	autohide: BoolProperty(name='Auto hide Non selected', default=False) # type: ignore
	unselect: BoolProperty(name='Remove From Selection', default=False) # type: ignore

	# shown on Edit mode
	buttonName: StringProperty(
		name="",
		update=rename_active_button
	) # type: ignore

	tabName: StringProperty(
		name="",
		update=scene_selection_set_tab_name_update
	) # type: ignore
	
	columns: IntProperty(
		name='columns', min=1, max=30, default=3,
		update=scene_selection_set_columns_update
	) # type: ignore
	
	rows: IntProperty(
		name='rows', min=1, max=30, default=10,
		update=scene_selection_set_rows_update
	) # type: ignore

	activeRow: IntProperty(name="", default=0) # type: ignore
	activeColamn: IntProperty(name="", default=0) # type: ignore



class ArmatureSelectionSet(PropertyGroup):
	# current tab data for UI draw
	tab: EnumProperty(
		name='Tab',
		items=armature_selection_set_tab_items,
		update=armature_selection_set_tab_update
	) # type: ignore
	# main data for save in file
	tabs = {}

	def new_tab(self, ctx):
		return armature_selection_set_new_tab(self, ctx)
	
	def active_tab(self, ctx):
		return armature_selection_set_get_active_tab(self, ctx)
	
	def new_button(self, ctx):
		armature_selection_set_new_button(self, ctx)
	
	def remove_tab(self, ctx):
		pass

	def get_active_button(self, ctx):
		return armature_selection_set_get_active_button(self, ctx)
	
	def get_button_sheet(self, ctx):
		return armature_selection_set_get_button_sheet(self, ctx)



class ARMATURE_OT_SelectionSetTab(Operator):
	bl_idname = 'pose.selection_set_tab'
	bl_label = 'Selection set Tab'
	bl_description = ''
	bl_options = {'REGISTER', 'INTERNAL'}
	action: EnumProperty(
		name='Action',
		items=[
			('ADD', 'Add', 'Add as new Tab'),
			('REMOVE', 'Remove', 'Remove Current Tab')
		]
	) # type: ignore

	def execute(self, ctx):
		return tab_operator_execute(self, ctx)



class ARMATURE_OT_SelectionSetIcon(Operator):
	bl_idname = 'pose.selection_set_icon'
	bl_label = 'Selection Set Icon Picker'
	bl_description = ""
	bl_options = {'REGISTER', 'INTERNAL'}

	icon: StringProperty("") # type: ignore

	def draw(self, ctx):
		armature_ot_selectionset_icon_draw(self, ctx)

	def execute(self, ctx):
		return armature_ot_selectionset_icon_execute(self, ctx)

	def invoke(self, ctx, event):
		if self.icon:
			return self.execute(ctx)
		return ctx.window_manager.invoke_props_dialog(self, width=800)



class ARMATURE_OT_SelectionSetCommand(Operator):
	bl_idname = 'pose.selection_set_command'
	bl_label = 'Selection Set Command'
	bl_description = ""
	bl_options = {'REGISTER', 'INTERNAL'}

	def draw(self, ctx):
		armature_ot_selectionset_command_draw(self, ctx)

	def execute(self, ctx):
		return {'FINISHED'}

	def invoke(self, ctx, event):
		return ctx.window_manager.invoke_props_dialog(self, width=200)



class ARMATURE_OT_SelectionSet(Operator):
	bl_idname = 'pose.selection_set'
	bl_label = 'Selection set'
	bl_description = 'Select Bones by selection set ID'
	bl_options = {'REGISTER', 'INTERNAL'}

	name: StringProperty(name="Name") # type: ignore
	id: IntProperty(name='id') # type: ignore
	column: IntProperty(name='Column') # type: ignore
	row: IntProperty(name='Row') # type: ignore
	
	ctrl, shift, alt = False, False, False

	def execute(self, ctx):
		return selection_set_operator_execute(self, ctx)

	def invoke(self, ctx, event):
		return armature_ot_selectionset_invoke(self, ctx, event)



class Armature_OP_SelectionSet(Panel):
	bl_space_type = 'VIEW_3D'
	bl_region_type = 'UI'
	bl_label = 'Selection (Pose Bone)'
	bl_idname = 'VIEW3D_PT_selection_set'
	bl_category = 'Tool'

	@classmethod
	def poll(self, ctx):
		return ctx.mode == 'POSE'
	
	def draw(self, ctx):
		armature_op_selectionset_draw(self, ctx)



classes = (
	SceneSelectionSet,
	PoseBoneSelectionSet,
	ArmatureSelectionSet,
	Armature_OP_SelectionSet,
	ARMATURE_OT_SelectionSet,
	ARMATURE_OT_SelectionSetIcon,
	ARMATURE_OT_SelectionSetCommand,
	ARMATURE_OT_SelectionSetTab,
)



def register_selection_set():
	for c in classes:
		bpy.utils.register_class(c)
	
	types = bpy.types
	types.Scene.selection_set = PointerProperty(type=SceneSelectionSet)
	types.Armature.selection_set = PointerProperty(type=ArmatureSelectionSet)
	types.PoseBone.selection_groups = PointerProperty(type=PoseBoneSelectionSet)



def unregister_selection_set():
	for c in classes:
		bpy.utils.unregister_class(c)

	types = bpy.types
	del types.Scene.selection_set
	del types.Armature.selection_set
	del types.PoseBone.selection_groups



if __name__ == "__main__":
	register_selection_set()