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
# 2025/10/16

from bpy.types import Menu
from bpy.utils import register_class, unregister_class

from .numpadpie import get_menu_pie


def pie_editor_type(pie, text, icon, space_type, subtype=None):
	pie.operator(
		'screen.space_type_set_or_cycle',
		text=text,
		icon=icon
	).space_type=space_type


class VIEW3D_MT_PIE_Screen_Editor_General(Menu):
	bl_idname = "BSMAX_MT_pie_screen_editor_genereal"
	bl_label = "General"

	def draw(self, _):
		pie = self.layout.menu_pie()
		pie_editor_type(pie, "3D Viewport", 'VIEW3D', 'VIEW_3D')
		pie_editor_type(pie, "Image Editor", 'IMAGE', 'IMAGE_EDITOR')
		pie_editor_type(pie, "UV Editor", "UV", 'IMAGE_EDITOR')	# 'UV'
		pie_editor_type(pie, "Geometry Node Editor", 'NODETREE', 'NODE_EDITOR')# GeometryNodeTree
		pie_editor_type(pie, "Compositor", 'NODE_COMPOSITING', 'NODE_EDITOR')# 'CompositorNodeTree'
		pie_editor_type(pie, "Shader Editor", 'NODE_MATERIAL', 'NODE_EDITOR')# 'ShaderNodeTree'
		pie_editor_type(pie, "Video Sequencer", 'SEQUENCE', 'SEQUENCE_EDITOR')
		pie_editor_type(pie, "Movie Clip Editor", 'TRACKER', 'CLIP_EDITOR')


class VIEW3D_MT_PIE_Screen_Editor_Animation(Menu):
	bl_idname = "BSMAX_MT_pie_screen_editor_animation"
	bl_label = "Animation"

	def draw(self, _):
		pie = self.layout.menu_pie()
		pie_editor_type(pie, "Dope sheet", 'ACTION', 'DOPESHEET_EDITOR')
		pie_editor_type(pie, "Graph Editor", 'GRAPH', 'GRAPH_EDITOR')
		pie_editor_type(pie, "Drivers", 'DRIVER', '') #TODO
		pie_editor_type(pie, "Nonelinier Animation", 'NLA', '')#TODO


class VIEW3D_MT_PIE_Screen_Editor_Scripting(Menu):
	bl_idname = "BSMAX_MT_pie_screen_editor_scripting"
	bl_label = "Scripting"

	def draw(self, _):
		pie = self.layout.menu_pie()
		pie_editor_type(pie, "Text Editor", 'TEXT', 'TEXT_EDITOR')
		pie_editor_type(pie, "Python Console", 'CONSOLE', 'CONSOLE')
		pie_editor_type(pie, "Info", 'INFO', 'INFO')


class VIEW3D_MT_PIE_Screen_Editor_Data(Menu):
	bl_idname = "BSMAX_MT_pie_screen_editor_data"
	bl_label = "Data"

	def draw(self, _):
		pie = self.layout.menu_pie()
		pie_editor_type(pie, "Outliner", 'OUTLINER', 'OUTLINER')
		pie_editor_type(pie, "Properties", 'PROPERTIES', 'PROPERTIES')
		pie_editor_type(pie, "File Browser", 'FILE_FOLDER', 'FILES')
		pie_editor_type(pie, "Asset Browser", 'ASSET_MANAGER', 'ASSETS')
		pie_editor_type(pie, "Spreadsheet", 'SPREADSHEET', 'SPREADSHEET')
		pie_editor_type(pie, "Preference", 'PREFERENCES', 'PREFERENCES')


class VIEW3D_MT_PIE_Screen_Editor(Menu):
	bl_idname = "BSMAX_MT_pie_screen_editor"
	bl_label = "Editor"

	def draw(self, _):
		pie = self.layout.menu_pie()
		get_menu_pie(pie, "General", None, 'BSMAX_MT_pie_screen_editor_genereal')
		get_menu_pie(pie, "Animation", None, 'BSMAX_MT_pie_screen_editor_animation')
		get_menu_pie(pie, "Scripting", None, 'BSMAX_MT_pie_screen_editor_scripting')
		get_menu_pie(pie, "Data", None, 'BSMAX_MT_pie_screen_editor_data')


classes = {
	VIEW3D_MT_PIE_Screen_Editor,
	VIEW3D_MT_PIE_Screen_Editor_General,
	VIEW3D_MT_PIE_Screen_Editor_Animation,
	VIEW3D_MT_PIE_Screen_Editor_Scripting,
	VIEW3D_MT_PIE_Screen_Editor_Data,
}

def register_pie_editor():
	for cls in classes:
		register_class(cls)

def unregister_pie_editor():
	for cls in classes:
		unregister_class(cls)

if __name__ == '__main__':
	register_pie_editor()
