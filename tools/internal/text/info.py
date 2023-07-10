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



class Info_OT_Clear(Operator):
	bl_idname = "info.clear"
	bl_label = "Clear"
	def execute(self, ctx):
		bpy.ops.info.select_all(action='SELECT')
		bpy.ops.info.report_delete('INVOKE_DEFAULT')
		return {'FINISHED'}



class Info_OT_NewScript(Operator):
	bl_idname = "info.new_script"
	bl_label = "New Script"
	def execute(self, ctx):
		# bpy.ops.info.report_copy()
		# ctx.area.type = 'TEXT_EDITOR'
		# bpy.ops.text.new()
		# bpy.data.texts[-1].name = "New Script"
		# bpy.ops.text.paste()

		# for area in ctx.screen.areas:
		# 	if area.type == 'TEXT_EDITOR':
		# 		bpy.ops.text.new()
		# 		bpy.data.texts[-1].name = "New Script"
		# 		bpy.ops.text.paste()
		return {'FINISHED'}



def register_info():
	bpy.utils.register_class(Info_OT_Clear)



def unregister_info():
	bpy.utils.unregister_class(Info_OT_Clear)
