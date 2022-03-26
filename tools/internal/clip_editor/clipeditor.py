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



# create a camera from view 
class Clip_OT_Auto_Frame(Operator):
	bl_idname = "clip.autoframe"
	bl_label = "Frame (Auto)"
	# bl_description = ""

	@classmethod
	def poll(self, ctx):
		return ctx.area.type == 'CLIP_EDITOR'

	def execute(self, ctx):
		bpy.ops.clip.view_selected('INVOKE_DEFAULT')
		# bpy.ops.clip.view_all('INVOKE_DEFAULT')
		self.report({'OPERATOR'},'bpy.ops.clip.autoframe()')
		return{"FINISHED"}



classes = [Clip_OT_Auto_Frame]

def register_clipeditor():
	for c in classes:
		bpy.utils.register_class(c)

def unregister_clipeditor():
	for c in classes:
		bpy.utils.unregister_class(c)