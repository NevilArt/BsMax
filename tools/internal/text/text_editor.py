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
# 2024/09/10

import bpy

from bpy.types import Operator


class Text_OT_Smart_Save(Operator):
	bl_idname = 'text.smart_save'
	bl_label = "Smart Save"
	bl_description = "Save Text if external Save Blend file if internal"

	def execute(self, ctx):
		name = ctx.area.spaces.active.text.name

		if bpy.data.texts[name].filepath == '':
			bpy.ops.wm.save_mainfile('INVOKE_DEFAULT')
		else:
			bpy.ops.text.save('INVOKE_DEFAULT')

		return {'FINISHED'}


def register_text_editor():
	bpy.utils.register_class(Text_OT_Smart_Save)


def unregister_text_editor():
	bpy.utils.unregister_class(Text_OT_Smart_Save)


if __name__ == '__main__':
	register_text_editor()