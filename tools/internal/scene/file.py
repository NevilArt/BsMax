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
# 2024/02/25

import bpy

from bpy.types import Operator
from bpy.utils import register_class, unregister_class
from bpy.app import version


class File_OT_Scale_Icons(Operator):
	bl_idname = "filebrowser.scaleicons"
	bl_label = "Scale Icons"
	up: bpy.props.BoolProperty(name="scaleup", default=True)
	
	@classmethod
	def poll(self, ctx):
		return ctx.area.ui_type == 'FILE_BROWSER'

	def execute(self, ctx):
		params = ctx.space_data.params
		small = 'LIST_VERTICAL'
		medium = 'LIST_HORIZONTAL'
		large = 'THUMBNAIL'
		if self.up:
			if params.display_type == large:
				params.display_type = small
			elif params.display_type == medium:
				params.display_type = large
			elif params.display_type == small:
				params.display_type = medium

		else:
			if params.display_type == large:
				params.display_type = medium
			elif params.display_type == medium:
				params.display_type = small
			elif params.display_type == small:
				params.display_type = large

		return{"FINISHED"}


class File_OT_Version(Operator):
	bl_idname = "file.version"
	bl_label = "Version"

	@classmethod
	def poll(self, ctx):
		return ctx.blend_data.filepath

	def draw(self, ctx):
		self.layout.label(text="File: " + self.date_version)
		self.layout.label(text="App: " + self.app_version)

	def execute(self, ctx):
		return{"FINISHED"}
	
	def invoke(self, ctx, event):
		self.date_version = str(bpy.data.version)
		self.app_version = str(version)
		return ctx.window_manager.invoke_props_dialog(self, width=120)


class File_OT_Save_Check(Operator):
	bl_idname = "file.save_check"
	bl_label = "Save Check"

	def compar_versions(self, file_ver, app_ver):
		print(file_ver[0], app_ver[0], file_ver[1], app_ver[1])
		return file_ver[0] == app_ver[0] and file_ver[1] == app_ver[1]

	def draw(self, ctx):
		self.layout.label(text="File Version is " + self.date_version)
		self.layout.label(text="Blender Version is " + self.app_version)
		self.layout.label(text="Are you sure wana overwrite it?")

	def execute(self, ctx):
		bpy.ops.wm.save_mainfile()
		return{"FINISHED"}
	
	def invoke(self, ctx, event):
		# check if file already saved
		if ctx.blend_data.filepath:
			# save normaly if file and blender version are same
			if self.compar_versions(bpy.data.version, bpy.app.version):
				bpy.ops.wm.save_mainfile()
				return{"FINISHED"}

			# open dialog if versions not same
			self.date_version = str(bpy.data.version)
			self.app_version = str(bpy.app.version)
			return ctx.window_manager.invoke_props_dialog(self)

		# just saved unsaved files
		bpy.ops.wm.save_as_mainfile('INVOKE_DEFAULT')
		return{"FINISHED"}


class Scene_OT_Reset(Operator):
	bl_idname = "scene.reset"
	bl_label = "Reset"
	bl_options = {'REGISTER', 'INTERNAL'}

	def draw(self, ctx):
		self.layout.label(
			text="Scene has unsaved data. Do you want to continue?",
			icon="QUESTION"
		)

	def execute(self, ctx):
		bpy.ops.wm.read_homefile(app_template="")
		for obj in ctx.scene.objects:
			bpy.data.objects.remove(obj, do_unlink=True)

		#TODO check this isuue
		if version < (4, 1, 0):
			pass
			# for area in ctx.screen.areas: 
			# 	if area.type == 'VIEW_3D':
			# 		for space in area.spaces: 
			# 			if space.type == 'VIEW_3D':
			# 				space.shading.color_type = 'OBJECT'
		else:
			pass

		return{"FINISHED"}

	
	def invoke(self, ctx, event):
		if bpy.data.is_dirty:
			return ctx.window_manager.invoke_props_dialog(self)
		return self.execute(ctx)


def version_menu(self, ctx):
	layout = self.layout
	layout.separator()
	layout.operator("file.version", text='File Version', icon='BLENDER')


def reset_menu(self, ctx):
	self.layout.operator("scene.reset", text='Reset', icon='FILE')


classes = (
	File_OT_Scale_Icons,
	File_OT_Version,
	File_OT_Save_Check,
	Scene_OT_Reset
)


def register_file():
	for c in classes:
		register_class(c)

	bpy.types.TOPBAR_MT_file.prepend(reset_menu)	
	bpy.types.TOPBAR_MT_file.append(version_menu)


def unregister_file():
	bpy.types.TOPBAR_MT_file.remove(reset_menu)
	bpy.types.TOPBAR_MT_file.remove(version_menu)

	for c in classes:
		unregister_class(c)


if __name__ == "__main__":
	register_file()