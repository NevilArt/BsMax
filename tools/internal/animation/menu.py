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
from bsmax.state import is_object_mode

class BsMax_MT_Animation_Tools(bpy.types.Menu):
	bl_idname = "BSMAX_MT_animationtools"
	bl_label = "Animation"
	bl_context = "objectmode"

	@classmethod
	def poll(self, ctx):
		return is_object_mode(ctx)

	def draw(self, ctx):
		layout=self.layout
		layout.operator("anim.character_lister",text="Character Lister",icon="GHOST_DISABLED")
		if ctx.mode != 'POSE': # this is temprary
			layout.separator()
			layout.operator("anim.path_constraint",text="Path Constraint",icon="CON_FOLLOWPATH")
			layout.operator("anim.location_constraint",text="Location Constraint",icon="CON_LOCLIMIT")
		layout.separator()
		layout.operator("anim.link_constraint",text="Parent Constraint",icon="LINKED")
		layout.operator("anim.link_to_world",text="Parent to World",icon="UNLINKED")
		if ctx.mode != 'POSE': # this is temprary
			layout.separator()
			layout.operator("anim.lookat_constraint",text="Lookat Constraint",icon="CON_TRACKTO")
			layout.operator("anim.orientation_constraint",text="Orientation Constraint",icon="CON_ROTLIMIT")
		layout.separator()
		layout.operator("anim.driver_fixer",text="Fix Override Driver Issue",icon="GHOST_ENABLED")

def animation_menu(self, ctx):
	self.layout.menu("BSMAX_MT_animationtools")

def register_menu():
	bpy.utils.register_class(BsMax_MT_Animation_Tools)

def unregister_menu():
	bpy.utils.unregister_class(BsMax_MT_Animation_Tools)