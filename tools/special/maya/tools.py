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

from bpy.props import EnumProperty
from bpy.types import Operator
from bpy.utils import register_class, unregister_class

# from bui.master import 


class VIEW3D_OT_Maya_Display_Presets(Operator):
	bl_idname = 'view3d.maya_display_presets'
	bl_label = "Maya Dispaly"
	bl_description = "Mimic maya Display shortkeys"
	bl_options = {'REGISTER', 'INTERNAL', 'UNDO'}

	mode: EnumProperty(
		name="Display Mode",
		items=[
				('DEFAULT', "Default", "Default quality display setting"),
				('ROUGH', "Rough", "Rough quality display setting"),
				('MEDIUM', "Medium", "Medium quality display setting"),
				('SMOOTH', "Smooth", "Smooth quality display setting"),
				('WIREFRAME', "Wireframe", "Wireframe"),
				('SHADED', "Shaded", "Shaded display"),
				('TEXTURE', "Textured", "Shaded and Textured display"),
				('RENDER', "Render", "Use All Lights")
		],
		default= "DEFAULT"
	) # type: ignore
	
	@classmethod
	def poll(self, ctx):
		return ctx.area.type == 'VIEW_3D'
	
	def execute(self, ctx):
		print(self.mode)
		if self.mode == 'DEFAULT':
			ctx.space_data.shading.type = 'SOLID'
			ctx.space_data.shading.show_specular_highlight = True
			return{'FINISHED'}

		if self.mode == 'ROUGH':
			ctx.space_data.shading.type = 'SOLID'
			ctx.space_data.shading.show_specular_highlight = False
			return{'FINISHED'}

		if self.mode == 'MEDIUM':
			ctx.space_data.shading.type = 'SOLID'
			return{'FINISHED'}

		if self.mode == 'SMOOTH':
			ctx.space_data.shading.type = 'SOLID'
			return{'FINISHED'}

		if self.mode == 'WIREFRAME':
			ctx.space_data.shading.type = 'WIREFRAME'
			return{'FINISHED'}

		if self.mode == 'SHADED':
			ctx.space_data.shading.type = 'MATERIAL'
			ctx.space_data.shading.color_type = 'MATERIAL'
			return{'FINISHED'}

		if self.mode == 'TEXTURE':
			ctx.space_data.shading.type = 'SOLID'
			ctx.space_data.shading.color_type = 'TEXTURE'
			return{'FINISHED'}

		if self.mode == 'RENDER':
			ctx.space_data.shading.type = 'RENDERED'
			return{'FINISHED'}

		return{'FINISHED'}


class VIEW3D_OT_Maya_switch_view(Operator):
	bl_idname = 'view3d.maya_switch_view'
	bl_label = "Maya Switch View"
	bl_description = "Maya mode view switch"
	# bl_options = {'REGISTER', 'INTERNAL'}

	@classmethod
	def poll(self, ctx):
		return ctx.area.type == 'VIEW_3D'
	
	def execute(self, ctx):
		return {'FINISHED'}

	def invoke(self, ctx, event):
		return {'FINISHED'}
	

classes = {
	VIEW3D_OT_Maya_Display_Presets,
	VIEW3D_OT_Maya_switch_view
}


def register_tools():
	for cls in classes:
		register_class(cls)


def unregister_tools():
	for cls in classes:
		if cls.is_registered:
			unregister_class(cls)


if __name__ == '__main__':
	register_tools()