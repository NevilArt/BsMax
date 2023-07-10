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

from bsmax.actions import modifier_add
from bsmax.state import is_objects_selected



class Modifier_OT_Add_Revolve(Operator):
	bl_idname = "modifier.add_revolve"
	bl_label = "Revolve (add)"
	bl_options = {'REGISTER','UNDO'}

	@classmethod
	def poll(self, ctx):
		return is_objects_selected(ctx)

	def execute(self, ctx):
		modifier_add(ctx,ctx.selected_objects, 'SCREW', name='Revolve')
		return {'FINISHED'}



def register_modifier():
	bpy.utils.register_class(Modifier_OT_Add_Revolve)



def unregister_modifier():
	if hasattr(bpy.types, Modifier_OT_Add_Revolve.bl_idname):
		bpy.utils.unregister_class(Modifier_OT_Add_Revolve)