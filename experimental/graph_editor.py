############################################################################
#	This program is free software: you can redistribute it and/or modify
#	it under the terms of the GNU General Public License as published by
#	the Free Software Foundation,either version 3 of the License,or
#	(at your option) any later version.
#
#	This program is distributed in the hope that it will be useful,
#	but WITHOUT ANY WARRANTY; without even the implied warranty of
#	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#	GNU General Public License for more details.
#
#	You should have received a copy of the GNU General Public License
#	along with this program.  If not,see <https://www.gnu.org/licenses/>.
############################################################################
#
# If you want to contribute to the development of this add-on,
# there is a file with a list of features to be implemented.
# Feel free to email me at fede.parodi.blend@gmail.com


bl_info = {
	"name": "Relative Ease",
	"author": "Fede Parodi",
	"version": (1, 0, 3),
	"blender": (3, 5, 1),
	"location": "Graph Editor - Dope Sheet - Timeline - Sidebar",
	"description": "Tools for easing bezier f-curves using percentage-based values",
	"category": "Animation",
}

import bpy, math
from bpy.props import FloatProperty, IntProperty, FloatVectorProperty
from bpy.types import PropertyGroup, Operator, Panel

# Get data about a keyframe's context
def get_keyframe_context(keyframe_data):
	keyframe_context = []

	fcurve, keyframe = keyframe_data

	# Calculate differences between current keyframe and its handles
	left_handle_own_diff_x = keyframe.handle_left.x - keyframe.co.x
	left_handle_own_diff_y = keyframe.handle_left.y - keyframe.co.y
	right_handle_own_diff_x = keyframe.handle_right.x - keyframe.co.x
	right_handle_own_diff_y = keyframe.handle_right.y - keyframe.co.y

	# Define adjacent keyframes
	prev_key = None
	next_key = None
	for point in fcurve.keyframe_points:
		if point.co.x < keyframe.co.x and \
			(prev_key is None or point.co.x > prev_key.co.x):
			prev_key = point

		if point.co.x > keyframe.co.x and \
			(next_key is None or point.co.x < next_key.co.x):
			next_key = point

	# If it is lonely keyframe, asume a distance of 30 frames 
	# on each side and an influence of 33%
	if prev_key is None and next_key is None:
		prev_diff_x = 30
		prev_diff_y = 0
		prev_handle_diff_x = 20
		next_diff_x = 30
		next_diff_y = 0
		next_handle_diff_x = 20
	else:
		# Calculate differences between current and previous keyframe
		if prev_key is not None:
			prev_diff_x = keyframe.co.x - prev_key.co.x
			prev_diff_y = keyframe.co.y - prev_key.co.y
			prev_handle_diff_x = keyframe.handle_left.x - prev_key.co.x
		else: # Mirror the difference if there is no previous keyframe
			prev_diff_x = next_key.co.x - keyframe.co.x
			prev_diff_y = next_key.co.y - keyframe.co.y
			prev_handle_diff_x = next_key.co.x - keyframe.handle_left.x

		# Calculate differences between current and next keyframe
		if next_key is not None:
			next_diff_x = next_key.co.x - keyframe.co.x
			next_diff_y = next_key.co.y - keyframe.co.y
			next_handle_diff_x = next_key.co.x - keyframe.handle_right.x
		else: # Mirror the difference if there is no next keyframe
			if prev_key is not None:
				next_diff_x = keyframe.co.x - prev_key.co.x
				next_diff_y = keyframe.co.y - prev_key.co.y
				next_handle_diff_x = keyframe.handle_right.x - prev_key.co.x
	
	# Calculate the y-axis direction of the keyframe on the f-curve,
	# whether it keeps the direction or changes it
	value_direction = None
	if prev_diff_y * next_diff_y > 0:
		value_direction = 1.0
	elif prev_diff_y * next_diff_y < 0:
		value_direction = -1.0
	else:
		value_direction = 0.0
	
	# Append data to keyframe_context list as tuples
	keyframe_context.append((
			prev_diff_x, next_diff_x,
			prev_handle_diff_x, next_handle_diff_x,
			left_handle_own_diff_x, left_handle_own_diff_y,
			right_handle_own_diff_x, right_handle_own_diff_y,
			value_direction
	))

	return keyframe_context


# Function to calculate the handles' relative position for copy ease
def get_handles_relative_position(keyframe_data):
	handles_relative_position = []

	# Import keyframe_context variables
	fcurve, keyframe = keyframe_data
	keyframe_context = get_keyframe_context(keyframe_data)

	prev_diff_x, next_diff_x, prev_handle_diff_x, next_handle_diff_x, \
	left_handle_own_diff_x, left_handle_own_diff_y, \
	right_handle_own_diff_x, right_handle_own_diff_y, \
	value_direction = keyframe_context[0]

	# Calculate relative easing in percentage values
	handle_left_relative_x = round(abs(prev_handle_diff_x / prev_diff_x *100 -100), 2)
	handle_right_relative_x = round(abs(next_handle_diff_x / next_diff_x *100 -100), 2)
	
	# Calculate handles angle in radians
	handle_left_angle = math.atan2(left_handle_own_diff_y, left_handle_own_diff_x)
	handle_right_angle = math.atan2(right_handle_own_diff_y, right_handle_own_diff_x)
	
	# Get handle direction
	copied_value_direction = value_direction

	# Append and return handles' relative position list as a tuple
	handles_relative_position = (
		handle_left_relative_x, handle_right_relative_x,
		handle_left_angle, handle_right_angle, copied_value_direction
	)

	return handles_relative_position


# Get selected keyframes or handles in the scene
def get_selected_keys():
	selected_keys = []

	for fcurve in bpy.context.editable_fcurves:
		for keyframe in fcurve.keyframe_points:
			if keyframe.select_control_point:
				selected_keys.append((fcurve, keyframe))

			elif keyframe.select_left_handle or keyframe.select_right_handle:
				new_keyframe = fcurve.keyframe_points.insert(
					keyframe.co.x, keyframe.co.y
				)

				new_keyframe.handle_left = keyframe.handle_left
				new_keyframe.handle_right = keyframe.handle_right
				selected_keys.append((fcurve, new_keyframe))

	return selected_keys


# Get first selected f-curve keyframes
def get_first_selected_fcurve_keys():
	selected_keys = get_selected_keys()
	first_fcurve_keys = []
	first_fcurve_selected = None

	# Find the first selected f-curve
	for fcurve, keyframe in selected_keys:
		first_fcurve_selected = fcurve
		break
	# Get the selected keys of the first f-curve
	if first_fcurve_selected is not None:
		for fcurve, keyframe in selected_keys:
			if fcurve == first_fcurve_selected:
				first_fcurve_keys.append((fcurve, keyframe))

	return first_fcurve_keys


# Function to set handles according to the sliders values
def set_handle(influence):
	selected_keys = get_selected_keys()
	
	for keyframe in selected_keys:
		selected_key = keyframe[1]
		selected_key.interpolation = 'BEZIER'

		if selected_key.handle_left_type in {'AUTO', 'AUTO_CLAMPED'}:
			selected_key.handle_left_type = 'ALIGNED'

		if selected_key.handle_right_type in {'AUTO', 'AUTO_CLAMPED'}:
			selected_key.handle_right_type = 'ALIGNED'

		keyframe_contexterence = get_keyframe_context(keyframe_data=keyframe)
		prev_diff_x = keyframe_contexterence[0][0]
		next_diff_x = keyframe_contexterence[0][1]
		angle_l = math.atan2(
			selected_key.handle_left.y - selected_key.co.y,
			selected_key.handle_left.x - selected_key.co.x
		)

		angle_r = math.atan2(
			selected_key.handle_right.y - selected_key.co.y,
			selected_key.handle_right.x - selected_key.co.x
		)

		if influence == 'left':
			# Prevent projecting to infinity if the handle is fully vertical
			# (math.degrees used to convert radians to degrees)
			if math.degrees(angle_l) > 90 or math.degrees(angle_l) < -90:
				selected_key.handle_left.x = selected_key.co.x - \
					(bpy.context.scene.influence_left / 100) * prev_diff_x

				selected_key.handle_left.y = selected_key.co.y - \
					(bpy.context.scene.influence_left / 100) * \
						prev_diff_x * math.tan(angle_l)

			# In that case, flatten the handle
			else:
				selected_key.handle_left.y = selected_key.co.y
				selected_key.handle_left.x = selected_key.co.x - \
					(bpy.context.scene.influence_left / 100) * prev_diff_x
				selected_key.handle_left_type = 'FREE'

		# The same goes for the right handle
		if influence == 'right':
			if math.degrees(angle_r) > -90 and math.degrees(angle_r) < 90:
				selected_key.handle_right.x = selected_key.co.x + \
					(bpy.context.scene.influence_right / 100) * next_diff_x

				selected_key.handle_right.y = selected_key.co.y + \
					(bpy.context.scene.influence_right / 100) * \
						next_diff_x * math.tan(angle_r)

			else:
				selected_key.handle_right.y = selected_key.co.y
				selected_key.handle_right.x = selected_key.co.x + \
					(bpy.context.scene.influence_right / 100) * next_diff_x

				selected_key.handle_right_type = 'FREE'

		# If both handles are flat, change the type to aligned
		if selected_key.handle_left.y == selected_key.co.y and \
			selected_key.handle_right.y == selected_key.co.y:
			
			selected_key.handle_left_type = 'ALIGNED'
			selected_key.handle_right_type = 'ALIGNED'

# Functions to round slider values and avoid divide by zero error
def get_influence_left(self):
	if "influence_left" not in self:
		return 33
	return round(self["influence_left"]) \
		if self["influence_left"] >= 1 else 0.01


def set_influence_left(self, value):
	self["influence_left"] = value if value < 1 else round(value)


def get_influence_right(self):
	if "influence_right" not in self:
		return 33
	return round(self["influence_right"]) if self["influence_right"] >= 1 else 0.01


def set_influence_right(self, value):
	self["influence_right"] = value if value < 1 else round(value)


# Show Message Box for copied keyframes easing
def ShowMessageBox(message, title="Message Box", icon='INFO'):
	def draw(self, context):
		for line in message.split("\n"):
			self.layout.label(text=line)
		
	bpy.context.window_manager.popup_menu(draw, title="", icon=icon)


### Properties
class PropertiesList(PropertyGroup):

	# Clipboard_keyframes Property
	bpy.types.Scene.clipboard_keyframes = IntProperty(
		default = 0,
		options = set(),
		description = "Number of keyframes' easing data on the clipboard"
	)

	# Left Influence Property
	bpy.types.Scene.influence_left = FloatProperty(
		name = "Left Handle Influence",
		default = 33,
		min = 0.4,
		soft_min = 0.4,
		max = 100,
		soft_max = 100,
		precision = 0,
		subtype = 'PERCENTAGE',
		get = get_influence_left,
		set = set_influence_left,
		update = lambda self, context: set_handle('left'),
		options = set(),
		description = "Relative to previous keyframe"
	)

	# Right Influence Property
	bpy.types.Scene.influence_right = FloatProperty(
		name = "Right Handle Influence",
		default = 33,
		min = 0.4,
		soft_min = 0.4,
		max = 100,
		soft_max = 100,
		precision = 0,
		subtype = 'PERCENTAGE',
		get = get_influence_right,
		set = set_influence_right,
		update = lambda self, context: set_handle('right'),
		options = set(),
		description = "Relative to next keyframe"
	)
	
#####################################################
### Operators

# Set Button
class Set_Operator(Operator):
	bl_idname = 'object.set_operator'
	bl_label = "Set"
	bl_description = "Set the influence for selected keyframes. Hold Alt to read values"

	# Define alt_key variable
	alt_key = False

	def invoke(self, context, event):
		if event.alt:
			self.report({'INFO'}, "Reading values")
			self.alt_key = True
		return self.execute(context)

	def execute(self, context):
		# Alt key behavior
		if self.alt_key:
			selected_keys = get_selected_keys()
			if len(selected_keys) == 0:
				self.report({'ERROR'}, "No keyframes selected")
				return {'CANCELLED'}			
			if len(selected_keys) != 1:
				self.report({'ERROR'}, "Read values only works with one selected keyframe")
				return {'CANCELLED'}
			
			keyframe_data = selected_keys[0]
			handles_relative_position = get_handles_relative_position(keyframe_data)
			handle_left_relative_x = handles_relative_position[0]
			handle_right_relative_x = handles_relative_position[1]
			bpy.context.scene.influence_left = handle_left_relative_x
			bpy.context.scene.influence_right = handle_right_relative_x

			self.report({'INFO'}, "Reading influence values from selected keyframe")
		# Standard behavior
		selected_keys = get_selected_keys()
		if not selected_keys:
			self.report({'ERROR'}, "No keyframes selected")
			return {'CANCELLED'}
		else:
			current_left = bpy.context.scene.influence_left
			current_right = bpy.context.scene.influence_right
			bpy.context.scene.influence_left = current_left
			bpy.context.scene.influence_right = current_right

			return {'FINISHED'}


# Flat Handles Button
class FlatHandles_Operator(Operator):
	bl_idname = "object.flat_handles_operator"
	bl_label = "Flat Handles"
	bl_description = "Flatten handles on the y-axis (turning keyframes into rest points)"

	def execute(self, context):
		selected_keys = get_selected_keys()
		for keyframe in selected_keys:
			keys_selection = keyframe[1]
			keys_selection.interpolation = 'BEZIER'
			keyframe_y = keys_selection.co.y
			keys_selection.handle_left.y = keyframe_y
			keys_selection.handle_right.y = keyframe_y
			keys_selection.handle_left_type = 'ALIGNED'
			keys_selection.handle_right_type = 'ALIGNED'
		return {'FINISHED'}


# Auto Smooth Button 
class AutoHandles_Operator(Operator):
	bl_idname = "object.auto_handles_operator"
	bl_label = "Auto Smooth"
	bl_description = "Set handles type to Automatic, with Blender’s default influence of 33.3%. You can then set a custom influence"

	def execute(self, context):
		selected_keys = get_selected_keys()
		bpy.ops.graph.handle_type(type='AUTO')   
		return {'FINISHED'}
	

# Auto Clamped Button 
class ClampedHandles_Operator(Operator):
	bl_idname = "object.clamped_handles_operator"
	bl_label = "Auto Clamped"
	bl_description = "Set handles type to Auto Clamped (no overshooting), with Blender’s default influence of 33.3%. You can then set a custom influence"

	def execute(self, context):
		selected_keys = get_selected_keys()
		bpy.ops.graph.handle_type(type='AUTO_CLAMPED')   
		return {'FINISHED'}


# Copy Ease Button
class CopyEase_Operator(Operator):
	bl_idname = "object.copy_ease_operator"
	bl_label = "Copy"
	bl_description = "Copy the relative ease of selected keyframes"

	def execute(self, context):
		selected_keys = get_first_selected_fcurve_keys()

		if len(selected_keys) == 0:
			self.report({'ERROR'}, "Select at least one keyframe")
			return {'CANCELLED'}					
		
		handles_relative_positions = []

		for keyframe_data in (selected_keys):
			handles_relative_position = get_handles_relative_position(
				keyframe_data
			)

			# Convert the tuples to lists and store the data
			handles_relative_position = list(handles_relative_position)
			handles_relative_positions.extend(handles_relative_position)

		# Store the handles' relative positions as
		# a custom property in the Scene
		bpy.types.Scene.handles_relative_positions = FloatVectorProperty(
			name="Handles Relative Positions",
			default=handles_relative_positions,
			size=len(handles_relative_positions),
			description="Stored data for copied keyframes"
		)

		# Update the clipboard_keyframes variable with the number of copied keyframes
		context.scene.clipboard_keyframes = len(selected_keys)

		# Display popup window message and report info
		selection = get_selected_keys()

		selected_fcurves = set()
		for fcurve, _ in selection:
			selected_fcurves.add(fcurve)

		if len(selected_fcurves) == 1:
			message = f"Copied easing from {len(selected_keys)} keyframes"
			ShowMessageBox(message)
			
		elif len(selected_fcurves) > 1:
			message = f"Copied easing from {len(selected_keys)} keyframes of first channel.\n"
			message += "(Multiple channels selected)."
			ShowMessageBox(message)
		
		message = f"Copied easing for {len(selected_keys)} keyframes\n"
		keys_info = []
		for idx in range(len(selected_keys)):
			handle_left_relative_x = handles_relative_positions[5 * idx + 0]
			handle_right_relative_x = handles_relative_positions[5 * idx + 1]
			handle_left_angle = handles_relative_positions[5 * idx + 2]
			handle_right_angle = handles_relative_positions[5 * idx + 3]
			direction = handles_relative_positions[5 * idx + 4]
			left = round(handle_left_relative_x)
			right = round(handle_right_relative_x)
			
			# For development, to see angle or direction data, add the variables below:
			keys_info.append(f"// Kf-{idx+1}, Left: {left}, Right: {right}")
		message += ", ".join(keys_info) + "]"
		self.report({'INFO'}, message)

		return {'FINISHED'}
	
# Paste Ease Button
class PasteEase_Operator(Operator):
	bl_idname = "object.paste_ease_operator"
	bl_label = "Paste"
	bl_description = "Apply ease to selected keyframes"

	def execute(self, context):
		if bpy.context.scene.clipboard_keyframes <1:
			self.report({'ERROR'}, "You need to copy the easing of at least one keyframe first")
			return {'CANCELLED'}

		# Get the handles relative positions and selected keyframes
		handles_relative_positions = bpy.context.scene.handles_relative_positions
		selected_keys = get_selected_keys()

		# Split the keyframes by f-curve
		kf_by_fcurve = {}
		for keyframe_data in selected_keys:
			fcurve, keyframe = keyframe_data
			if fcurve not in kf_by_fcurve:
				kf_by_fcurve[fcurve] = []
			kf_by_fcurve[fcurve].append(keyframe_data)

		# Loop through each f-curve and apply the action to selected keyframes
		for fcurve, kf_data_list in kf_by_fcurve.items():
			# Check if the number of copied keyframes matches the number of keyframes to paste
			if bpy.context.scene.clipboard_keyframes != len(kf_data_list):
				self.report({'ERROR'}, "The number of copied keyframes doesn't match the number of keyframes to paste")
				return {'CANCELLED'}

			for idx, keyframe_data in enumerate(kf_data_list):
				fcurve, keyframe = keyframe_data

				# Get keyframes differences
				keyframe_context = get_keyframe_context(keyframe_data)
				prev_diff_x, next_diff_x, prev_handle_diff_x, next_handle_diff_x, \
				left_handle_own_diff_x, left_handle_own_diff_y, \
				right_handle_own_diff_x, right_handle_own_diff_y, \
				value_direction = keyframe_context[0]

				# Extract the relevant data from handles_relative_positions based on the keyframe index
				handle_left_relative_x = handles_relative_positions[5 * idx + 0]
				handle_right_relative_x = handles_relative_positions[5 * idx + 1]
				handle_left_angle = handles_relative_positions[5 * idx + 2]
				handle_right_angle = handles_relative_positions[5 * idx + 3]
				copied_value_direction = handles_relative_positions[5 * idx + 4]

				# Paste the ease
				keyframe.interpolation = 'BEZIER'
				if keyframe.handle_right_type in {'AUTO', 'AUTO_CLAMPED'}:
					keyframe.handle_left_type = 'ALIGNED'

				if keyframe.handle_right_type in {'AUTO', 'AUTO_CLAMPED'}:	 
					keyframe.handle_right_type = 'ALIGNED'

				keyframe.handle_left.x = keyframe.co.x - \
					(handle_left_relative_x / 100) * prev_diff_x
				keyframe.handle_right.x = keyframe.co.x + \
					(handle_right_relative_x / 100) * next_diff_x
				
				angle_l = math.atan2(left_handle_own_diff_y, left_handle_own_diff_x)
				angle_r = math.atan2(right_handle_own_diff_y, right_handle_own_diff_x)
				
				# If copied handles were flat, flat handles
				if round(handle_left_angle,6) == round(math.pi,6):
					if handle_right_angle == 0:
						angle_l = math.pi
						angle_r = 0
						keyframe.handle_left_type = 'ALIGNED'
						keyframe.handle_right_type = 'ALIGNED'
				
				keyframe.handle_left.y = keyframe.co.y - \
					(handle_left_relative_x / 100) * prev_diff_x * math.tan(angle_l)

				keyframe.handle_right.y = keyframe.co.y + \
					(handle_right_relative_x / 100) * next_diff_x * math.tan(angle_r)
				
				# To do: work on a feature of alt+click that also pastes the angle
				# But the problem of the different scales units of values must also be solved. Work on normalize the scales first.
				# The value_direction could help to change the direction of the angle if needed
				# This would be the code, without considering those issues:
				#keyframe.handle_left.y = keyframe.co.y - (handle_left_relative_x / 100) * prev_diff_x * math.tan(handle_left_angle)
				#keyframe.handle_right.y = keyframe.co.y + (handle_right_relative_x / 100) * next_diff_x * math.tan(handle_right_angle)

		return {'FINISHED'}

#####################################################
### UI Panles and Register


# Graph Editor Panel
class RelativeEase_GraphEditor_Panel(Panel):
	bl_idname = "GRAPH_PT_relative_ease_panel"
	bl_label = "Relative Ease"
	bl_space_type = "GRAPH_EDITOR"
	bl_region_type = "UI"
	bl_category = "Relative Ease"

	def draw(self, context):
		layout = self.layout
		scene = context.scene

		# Left & Right Influence - Set Button
		row = layout.row(align=True)
		row.scale_y = 0.5
		row.label(text="Left Handle ")
		row.label(text="Right Handle ")
		split = layout.split(align=True)
		colMain = split.column(align=True)
		split = colMain.split(align=True)
		col = split.column(align=True)
		col.prop(scene, "influence_left", text="")
		col = split.column(align=True)
		col.prop(scene, "influence_right", text="")
		colMain.operator("object.set_operator")
	
		#F-Curve Shape
		split = layout.split(align=True)
		col = split.column(align=True)
		col.label(text="F-Curve Shape")
		col.operator("object.flat_handles_operator", icon="HANDLE_ALIGNED")
		col.operator("object.auto_handles_operator", icon="HANDLE_AUTO")
		col.operator("object.clamped_handles_operator", icon="HANDLE_AUTOCLAMPED")
		
		#Copy Paste
		split = layout.split(align=True)
		colMain = split.column(align=True)
		colMain.label(text="Copy Ease")	 
		split = colMain.split(align=True)		
		col = split.column(align=True)
		col.operator("object.copy_ease_operator")
		col = split.column(align=True)
		col.operator("object.paste_ease_operator")
		sub = colMain.row(align=True)
		sub.prop(scene, "clipboard_keyframes", slider=True, text="")
		sub.enabled = False


# Dope Sheet Editor Panel
class RelativeEase_DopeSheet_Panel(Panel):
	bl_idname = "DOPE_PT_relative_ease_panel"
	bl_label = "Relative Ease"
	bl_space_type = "DOPESHEET_EDITOR"
	bl_region_type = "UI"
	bl_category = "Relative Ease"

	def draw(self, context):
		layout = self.layout
		scene = context.scene

		# Left & Right Influence - Set Button
		row = layout.row(align=True)
		row.scale_y = 0.5
		row.label(text="Left Handle ")
		row.label(text="Right Handle ")
		split = layout.split(align=True)
		colMain = split.column(align=True)
		split = colMain.split(align=True)
		col = split.column(align=True)
		col.prop(scene, "influence_left", text="")
		col = split.column(align=True)
		col.prop(scene, "influence_right", text="")
		colMain.operator("object.set_operator")
	
		#F-Curve Shape
		split = layout.split(align=True)
		col = split.column(align=True)
		col.label(text="F-Curve Shape")
		col.operator("object.flat_handles_operator", icon="HANDLE_ALIGNED")
		col.operator("object.auto_handles_operator", icon="HANDLE_AUTO")
		col.operator("object.clamped_handles_operator", icon="HANDLE_AUTOCLAMPED")
		
		#Copy Paste
		split = layout.split(align=True)
		colMain = split.column(align=True)
		colMain.label(text="Copy Ease")	 
		split = colMain.split(align=True)		
		col = split.column(align=True)
		col.operator("object.copy_ease_operator")
		col = split.column(align=True)
		col.operator("object.paste_ease_operator")
		sub = colMain.row(align=True)
		sub.prop(scene, "clipboard_keyframes", slider=True, text="")
		sub.enabled = False


classes = {
	PropertiesList,
	Set_Operator,
	FlatHandles_Operator,
	AutoHandles_Operator,
	ClampedHandles_Operator,
	CopyEase_Operator,
	PasteEase_Operator,
	RelativeEase_GraphEditor_Panel,
	RelativeEase_DopeSheet_Panel,
}


def register():
	for cls in classes:
		bpy.utils.register_class(cls)


def unregister():
	for cls in classes:
		bpy.utils.unregister_class(cls)


if __name__ == "__main__":
	register()