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

from bpy.types import Operator, Menu
from bpy.props import StringProperty, BoolProperty



class Editor_OT_Open_As_Float_Window(Operator):
	bl_idname = 'editor.float'
	bl_label = 'Open As Float Window'
	bl_options = {'REGISTER', 'INTERNAL'}
	
	ui_type: StringProperty(default='VIEW_3D')
	shader_type: StringProperty(default='')
	multiple: BoolProperty(default=True)

	def execute(self,ctx):
		""" New Method for Blender 2.93 and Newer """
		windows = ctx.window_manager.windows
		
		""" Pass if exist and single mode"""
		if not self.multiple:
			for window in windows:
				for area in window.screen.areas:
					if area.ui_type == self.ui_type:
						if self.shader_type != '':
							for space in area.spaces:
								if hasattr(space, 'shader_type'):
									try:
										if space.shader_type == self.shader_type:
											return{'FINISHED'}
									except:
										pass
						else:
							return{'FINISHED'}

		""" Create New Window """
		bpy.ops.wm.window_new()
		area = windows[-1].screen.areas[0]
		area.ui_type = self.ui_type
		if self.shader_type != '':
			#TODO check has attribute
			try:
				ctx.space_data.shader_type = self.shader_type
			except:
				pass

		return{'FINISHED'}



class Editor_OT_Script_Listener_Open(Operator):
	bl_idname = 'editor.script_listener'
	bl_label = 'Script Listener(Float)'
	bl_options = {'REGISTER', 'INTERNAL'}
	
	def execute(self, ctx):
		""" New Method for Blender 2.93 and Newer """
		windows = ctx.window_manager.windows
		
		""" Pass if exist """
		for window in windows:
			if len(window.screen.areas) == 2:
				areas = window.screen.areas
				if areas[0].ui_type == 'INFO' and areas[1].ui_type == 'CONSOLE':
					return{'FINISHED'}

		""" Create New Window """
		bpy.ops.wm.window_new()
		area = windows[-1].screen.areas[0]
		area.ui_type = 'CONSOLE'
		bpy.ops.screen.area_split(direction='HORIZONTAL', factor=0.5)
		area = windows[-1].screen.areas[0]
		area.type = 'INFO'
		
		return{'FINISHED'}



class BsMax_MT_New_Editor(Menu):
	bl_idname = 'BSMAX_MT_new_editor'
	bl_label = 'New Editor'
	def draw(self, ctx):
		layout=self.layout
		layout.operator("editor.float", text='3D Viewport',
						icon='VIEW3D').ui_type='VIEW_3D'

		layout.operator("editor.float", text='Image Editor',
						icon='IMAGE').ui_type='IMAGE_EDITOR'

		layout.operator("editor.float", text='UV Editor',
						icon='UV').ui_type='UV'

		layout.operator("editor.float", text='Compositor',
						icon='NODE_COMPOSITING').ui_type='CompositorNodeTree'

		layout.operator("editor.float", text='Texture Node Editor',
						icon='TEXTURE').ui_type='TextureNodeTree'

		layout.operator("editor.float", text='Geometry Node Editor',
						icon='NODETREE').ui_type='GeometryNodeTree'

		layout.operator("editor.float", text='Shader Node Editor',
						icon='NODE_MATERIAL').ui_type='ShaderNodeTree'

		layout.operator("editor.float", text='Video Sequencer',
						icon='SEQUENCE').ui_type='SEQUENCE_EDITOR'

		layout.operator("editor.float", text='Movie Clip Editor',
						icon='TRACKER').ui_type='CLIP_EDITOR'

		layout.separator()

		layout.operator('editor.float', text='Dope Sheet',
						icon='ACTION').ui_type='DOPESHEET'

		layout.operator("editor.float", text='Time Line',
						icon='TIME').ui_type='TIMELINE'

		layout.operator("editor.float", text='Graph Editor',
						icon='GRAPH').ui_type='FCURVES'

		layout.operator("editor.float", text='Drivers',
						icon='DRIVER').ui_type='DRIVERS'

		layout.operator("editor.float", text='Nonlinear Animation',
						icon='NLA').ui_type='NLA_EDITOR'

		layout.separator()

		layout.operator('editor.float', text='Text Editor',
						icon='TEXT').ui_type='TEXT_EDITOR'

		layout.operator("editor.float", text='Python Console',
						icon='CONSOLE').ui_type='CONSOLE'

		layout.operator("editor.float", text='Info',
						icon='INFO').ui_type='INFO'

		layout.separator()

		layout.operator('editor.float', text='Outliner',
						icon='OUTLINER').ui_type='OUTLINER'

		layout.operator("editor.float", text='Properties',
						icon='PROPERTIES').ui_type='PROPERTIES'
		
		layout.operator("editor.float", text='File Browser',
						icon='FILE_FOLDER').ui_type='FILES'

		layout.operator("editor.float", text='Asset Manager',
						icon='ASSET_MANAGER').ui_type='ASSETS'

		layout.operator("editor.float", text='Sepreadsheet',
						icon='SPREADSHEET').ui_type='SPREADSHEET'

		layout.operator("editor.float", text='Prefrences',
						icon='PREFERENCES').ui_type='PREFERENCES'

def float_editor_menu(self, ctx):
	layout = self.layout
	layout.menu('BSMAX_MT_new_editor')



classes = (
	Editor_OT_Open_As_Float_Window,
	Editor_OT_Script_Listener_Open,
	BsMax_MT_New_Editor
)



def register_float_editor():
	for c in classes:
		bpy.utils.register_class(c)
	bpy.types.TOPBAR_MT_window.prepend(float_editor_menu)



def unregister_float_editor():
	bpy.types.TOPBAR_MT_window.remove(float_editor_menu)
	for c in classes:
		bpy.utils.unregister_class(c)



if __name__ == "__main__":
	register_float_editor()