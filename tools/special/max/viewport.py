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

class View3DData:
	def __init__(self):
		self._shading_type = 'SOLID'
v3dd = View3DData()

# new one will cretae for NewStyle mode
class View3D_OT_Wireframe_Toggle(Operator):
	bl_idname = "view3d.wireframe_toggle"
	bl_label = "Wireframe Toggle"

	@classmethod
	def poll(self, ctx):
		return ctx.area.type == 'VIEW_3D'

	def execute(self, ctx):
		shading = ctx.area.spaces[0].shading
		if shading.type == 'WIREFRAME':
			shading.type = v3dd._shading_type #'SOLID''MATERIAL''RENDERED'
		else:
			v3dd._shading_type = shading.type
			shading.type = 'WIREFRAME'
		self.report({'INFO'},'bpy.ops.view3d.wireframe_toggle()')
		return{"FINISHED"}

class View3D_OT_Lighting_Toggle(Operator):
	bl_idname = "view3d.lighting_toggle"
	bl_label = "Lighting Toggle"

	@classmethod
	def poll(self, ctx):
		return ctx.area.type == 'VIEW_3D'
	
	def execute(self, ctx):
		shading = ctx.area.spaces[0].shading
		if shading.type == 'RENDERED':
			shading.type = 'MATERIAL' #'SOLID''RENDERED'
		else:
			shading.type = 'RENDERED'
		self.report({'INFO'},'bpy.ops.view3d.lighting_toggle()')
		return{"FINISHED"}

class View3D_OT_Edge_Face_Toggle(Operator):
	bl_idname = "view3d.edge_faces_toggle"
	bl_label = "Edge Shaded Toggle"

	@classmethod
	def poll(self, ctx):
		return ctx.area.type == 'VIEW_3D'

	def execute(self, ctx):
		overlay = ctx.space_data.overlay
		if overlay.show_wireframes:
			overlay.show_wireframes = False
			overlay.wireframe_threshold = 0.5
		else:
			overlay.show_wireframes = True
			overlay.wireframe_threshold = 1
		self.report({'INFO'},'bpy.ops.view3d.edge_faces_toggle()')
		return{"FINISHED"}

class View3D_OT_Shade_Selected_Faces(Operator):
	bl_idname = "view3d.shade_selected_faces"
	bl_label = "Shade Selected Faces"

	@classmethod
	def poll(self, ctx):
		return ctx.area.type == 'VIEW_3D'

	def execute(self, ctx):
		FaceShade = ctx.preferences.themes['Default'].view_3d
		if FaceShade.face_select[3] != 0.0:
			FaceShade.face_select = (0.0, 0.0, 0.0, 0.0)
		else:
			FaceShade.face_select = (0.8156, 0.0, 0.0, 0.5)
		self.report({'INFO'},'bpy.ops.view3d.shade_selected_faces()')
		return{"FINISHED"}

class View3D_OT_Show_Hide_Gride(Operator):
	bl_idname = "view3d.show_hide_gride"
	bl_label = "Show Hide Gride"

	@classmethod
	def poll(self, ctx):
		return ctx.area.type == 'VIEW_3D'

	def execute(self, ctx):
		overlay = ctx.space_data.overlay
		state = overlay.show_floor
		overlay.show_floor = not state
		overlay.show_axis_x = not state
		overlay.show_axis_y = not state
		overlay.show_axis_z = False
		self.report({'INFO'},'bpy.ops.view3d.show_hide_gride()')
		return{"FINISHED"}

class View3D_OT_Show_Statistics(Operator):
	bl_idname = "view3d.show_statistics"
	bl_label = "Show Statistics Toggle"

	@classmethod
	def poll(self, ctx):
		return ctx.area.type == 'VIEW_3D'

	def execute(self, ctx):
		overlay = ctx.space_data.overlay
		overlay.show_text = not overlay.show_text
		self.report({'INFO'},'bpy.ops.view3d.show_statistics()')
		return{"FINISHED"}

class Object_OT_Xray_Toggle(Operator):
	bl_idname = "object.xray_toggle"
	bl_label = "Xray Mode"

	@classmethod
	def poll(self, ctx):
		return ctx.area.type == 'VIEW_3D'

	def execute(self, contecxt):
		# TODO Xray Toggle mode for selection
		self.report({'INFO'},'bpy.ops.object.xray_toggle()')
		return{"FINISHED"}

class View3D_OT_Show_Geometry_Toggle(Operator):
	bl_idname = "view3d.show_geometry_toggle"
	bl_label = "Show Geometry Toggle"

	@classmethod
	def poll(self, ctx):
		return ctx.area.type == 'VIEW_3D'

	def execute(self, ctx):
		state = ctx.space_data.show_object_viewport_mesh
		ctx.space_data.show_object_viewport_mesh = not state
		self.report({'INFO'},'bpy.ops.view3d.show_geometry_toggle()')
		return{"FINISHED"}

class View3D_OT_Show_Helper_Toggle(Operator):
	bl_idname = "view3d.show_helper_toggle"
	bl_label = "Show Helper Toggle"

	@classmethod
	def poll(self, ctx):
		return ctx.area.type == 'VIEW_3D'

	def execute(self, ctx):
		data = ctx.space_data
		empty = data.show_object_viewport_empty
		speaker = data.show_object_viewport_speaker
		lightprob = data.show_object_viewport_light_probe
		lattce = data.show_object_viewport_lattice
		state = empty and speaker and lightprob and lattce
		data.show_object_viewport_empty = not state
		data.show_object_viewport_speaker = not state
		data.show_object_viewport_light_probe = not state
		data.show_object_viewport_lattice = not state
		self.report({'INFO'},'bpy.ops.view3d.show_helper_toggle()')
		return{"FINISHED"}

class View3D_OT_Show_Shape_Toggle(Operator):
	bl_idname = "view3d.show_shape_toggle"
	bl_label = "Show Shape Toggle"

	@classmethod
	def poll(self, ctx):
		return ctx.area.type == 'VIEW_3D'

	def execute(self, ctx):
		state = ctx.space_data.show_object_viewport_curve
		ctx.space_data.show_object_viewport_curve = not state
		self.report({'INFO'},'bpy.ops.view3d.show_shape_toggle()')
		return{"FINISHED"}

class View3D_OT_Show_Light_Toggle(Operator):
	bl_idname = "view3d.show_light_toggle"
	bl_label = "Show Light Toggle"

	@classmethod
	def poll(self, ctx):
		return ctx.area.type == 'VIEW_3D'

	def execute(self, ctx):
		state = ctx.space_data.show_object_viewport_light
		ctx.space_data.show_object_viewport_light = not state
		self.report({'INFO'},'bpy.ops.view3d.show_light_toggle()')
		return{"FINISHED"}

class View3D_OT_Show_Bone_Toggle(Operator):
	bl_idname = "view3d.show_bone_toggle"
	bl_label = "Show Bone Toggle"

	@classmethod
	def poll(self, ctx):
		return ctx.area.type == 'VIEW_3D'

	def execute(self, ctx):
		state = ctx.space_data.show_object_viewport_armature
		ctx.space_data.show_object_viewport_armature = not state
		self.report({'INFO'},'bpy.ops.view3d.show_bone_toggle()')
		return{"FINISHED"}

class View3D_OT_Show_Camera_Toggle(Operator):
	bl_idname = "view3d.show_camera_toggle"
	bl_label = "Show Camera Toggle"

	@classmethod
	def poll(self, ctx):
		return ctx.area.type == 'VIEW_3D'

	def execute(self, ctx):
		state = ctx.space_data.show_object_viewport_camera
		ctx.space_data.show_object_viewport_camera = not state
		self.report({'INFO'},'bpy.ops.view3d.show_camera_toggle()')
		return{"FINISHED"}

classes = [View3D_OT_Wireframe_Toggle,
	View3D_OT_Edge_Face_Toggle,
	View3D_OT_Shade_Selected_Faces,
	View3D_OT_Show_Hide_Gride,
	View3D_OT_Show_Statistics,
	View3D_OT_Show_Geometry_Toggle,
	View3D_OT_Show_Helper_Toggle,
	View3D_OT_Show_Shape_Toggle,
	View3D_OT_Show_Light_Toggle,
	View3D_OT_Show_Bone_Toggle,
	View3D_OT_Show_Camera_Toggle,
	View3D_OT_Lighting_Toggle]
	
def register_viewport():
	[bpy.utils.register_class(c) for c in classes]

def unregister_viewport():
	[bpy.utils.unregister_class(c) for c in classes]