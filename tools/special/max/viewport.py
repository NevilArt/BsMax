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

# new one will cretae for NewStyle mode
class BsMax_OT_WireframeToggle(Operator):
	bl_idname = "bsmax.wireframetoggle"
	bl_label = "Wireframe Toggle"

	@classmethod
	def poll(self, ctx):
		return ctx.area.type == 'VIEW_3D'

	def execute(self, ctx):
		shading = ctx.area.spaces[0].shading
		if shading.type == 'WIREFRAME':
			shading.type = 'MATERIAL' #'SOLID''RENDERED'
		else:
			shading.type = 'WIREFRAME'
		return{"FINISHED"}

class BsMax_OT_LightingToggle(Operator):
	bl_idname = "bsmax.lightingtoggle"
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
		return{"FINISHED"}

class BsMax_OT_EdgeFaceToggle(Operator):
	bl_idname = "bsmax.edgefacestoggle"
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
		return{"FINISHED"}

class BsMax_OT_ShadeSelectedFaces(Operator):
	bl_idname = "bsmax.shadeselectedfaces"
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
		return{"FINISHED"}

class BsMax_OT_ShowHideGride(Operator):
	bl_idname = "bsmax.showhidegride"
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
		return{"FINISHED"}

class BsMax_OT_ShowStatistics(Operator):
	bl_idname = "bsmax.showstatistics"
	bl_label = "Show Statistics Toggle"

	@classmethod
	def poll(self, ctx):
		return ctx.area.type == 'VIEW_3D'

	def execute(self, ctx):
		overlay = ctx.space_data.overlay
		overlay.show_text = not overlay.show_text
		return{"FINISHED"}

class BsMax_OT_XrayToggle(Operator):
	bl_idname = "bsmax.xraytoggle"
	bl_label = "Xray Mode"

	@classmethod
	def poll(self, ctx):
		return ctx.area.type == 'VIEW_3D'

	def execute(self, contecxt):
		# TODO Xray Toggle mode for selection
		return{"FINISHED"}

class BsMax_OT_ShowGeometryToggle(Operator):
	bl_idname = "bsmax.showgeometrytoggle"
	bl_label = "Show Geometry Toggle"

	@classmethod
	def poll(self, ctx):
		return ctx.area.type == 'VIEW_3D'

	def execute(self, ctx):
		state = ctx.space_data.show_object_viewport_mesh
		ctx.space_data.show_object_viewport_mesh = not state
		return{"FINISHED"}

class BsMax_OT_ShowHelperToggle(Operator):
	bl_idname = "bsmax.showhelpertoggle"
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
		return{"FINISHED"}

class BsMax_OT_ShowShapeToggle(Operator):
	bl_idname = "bsmax.showshapetoggle"
	bl_label = "Show Shape Toggle"

	@classmethod
	def poll(self, ctx):
		return ctx.area.type == 'VIEW_3D'

	def execute(self, ctx):
		state = ctx.space_data.show_object_viewport_curve
		ctx.space_data.show_object_viewport_curve = not state
		return{"FINISHED"}

class BsMax_OT_ShowLightToggle(Operator):
	bl_idname = "bsmax.showlighttoggle"
	bl_label = "Show Light Toggle"

	@classmethod
	def poll(self, ctx):
		return ctx.area.type == 'VIEW_3D'

	def execute(self, ctx):
		state = ctx.space_data.show_object_viewport_light
		ctx.space_data.show_object_viewport_light = not state
		return{"FINISHED"}

class BsMax_OT_ShowBoneToggle(Operator):
	bl_idname = "bsmax.showbonetoggle"
	bl_label = "Show Bone Toggle"

	@classmethod
	def poll(self, ctx):
		return ctx.area.type == 'VIEW_3D'

	def execute(self, ctx):
		state = ctx.space_data.show_object_viewport_armature
		ctx.space_data.show_object_viewport_armature = not state
		return{"FINISHED"}

class BsMax_OT_ShowCameraToggle(Operator):
	bl_idname = "bsmax.showcameratoggle"
	bl_label = "Show Camera Toggle"

	@classmethod
	def poll(self, ctx):
		return ctx.area.type == 'VIEW_3D'

	def execute(self, ctx):
		state = ctx.space_data.show_object_viewport_camera
		ctx.space_data.show_object_viewport_camera = not state
		return{"FINISHED"}

classes = [BsMax_OT_WireframeToggle,
	BsMax_OT_EdgeFaceToggle,
	BsMax_OT_ShadeSelectedFaces,
	BsMax_OT_ShowHideGride,
	BsMax_OT_ShowStatistics,
	BsMax_OT_ShowGeometryToggle,
	BsMax_OT_ShowHelperToggle,
	BsMax_OT_ShowShapeToggle,
	BsMax_OT_ShowLightToggle,
	BsMax_OT_ShowBoneToggle,
	BsMax_OT_ShowCameraToggle,
	BsMax_OT_LightingToggle]
	
def register_viewport():
	[bpy.utils.register_class(c) for c in classes]

def unregister_viewport():
	[bpy.utils.unregister_class(c) for c in classes]