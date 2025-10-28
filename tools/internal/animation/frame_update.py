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
# 2025/10/03

import bpy

from bpy.types import Operator
from bpy.app.handlers import persistent
from bpy.utils import register_class, unregister_class
from bpy.app import version

from bsmax.graphic import get_header_color


def mode_updated(cls, context:bpy.types.Context) -> None:
	if version >= (5, 0, 0):
		return
	if not cls.active_auto_use_select_pick_depth:
		return
	""" uspds use_select_pick_depth State """
	uspds = False if (context.mode == 'POSE') else cls.use_select_pick_depth
	context.preferences.system.use_select_pick_depth = uspds


def autokey_state_updated(cls, context:bpy.types.Context) -> None:
	autoKey = context.scene.tool_settings.use_keyframe_insert_auto
	color = (0.5, 0.0, 0.0, 1.0) if autoKey else get_header_color()
	# allow to update if affect_theme active in preference
	if color and cls.preferences.affect_theme:
		#TODO get active theme
		theme = context.preferences.themes['Default']
		theme.dopesheet_editor.space.header = color


class Scene_Stata:
	def __init__(self) -> None:
		self.mode = 'OBJECT'
		self.pose_mode = False
		self.use_select_pick_depth = False
		self.active_auto_use_select_pick_depth = False
		self.use_keyframe_insert_auto = False
		self.preferences = None
	
	def store(
		self,
		context:bpy.types.Context,
		preferences:bpy.types.Preferences
	) -> None:

		if version < (5, 0, 0):
			""" Store use_select_pick_depth State """
			system = context.preferences.system
			self.use_select_pick_depth = system.use_select_pick_depth

		self.preferences = preferences
		
		# """ Store use_keyframe_insert_auto state """
		# ukias = context.scene.tool_settings.use_keyframe_insert_auto
		# self.use_keyframe_insert_auto = ukias

	def check(self, context:bpy.types.Context) -> None:
		""" Calls once on mode changed """
		if self.mode != context.mode:
			mode_updated(self, context)
			self.mode = context.mode

		""" Call once on autokey state changes """
		tool_settings = context.scene.tool_settings
		if tool_settings.use_keyframe_insert_auto != self.use_keyframe_insert_auto:
			autokey_state_updated(self, context)
			self.use_keyframe_insert_auto = tool_settings.use_keyframe_insert_auto

	def restore(self, context:bpy.types.Context) -> None:
		""" Restore use_select_pick_depth State """
		if version < (5, 0, 0):
			system = bpy.context.preferences.system
			system.use_select_pick_depth = self.use_select_pick_depth

		""" Restore dopesheet_editor.header Color """
		color = get_header_color()
		context.preferences.themes['Default'].dopesheet_editor.space.header = color

scene_state = Scene_Stata()


@persistent
def render_init(scene:bpy.types.Scene) -> None:
	""" Fix the overide issue befor render start """
	# Cause the crash on hevy scenes and has to be disable
	# dr = Driver_Reconnect()
	# dr.update()
	pass


@persistent
def depsgraph_update(scene:bpy.types.Scene) -> None:
	global scene_state
	scene_state.check(bpy.context)


# this operator need to see scene_state class #
class Anim_OT_Auto_Key_Toggle(Operator):
	bl_idname = 'anim.auto_key_toggle'
	bl_label = "Auto Key Toggle"
	bl_options = {'REGISTER', 'INTERNAL'}

	def execute(self, context:bpy.types.Context) -> set[str]:
		state = context.scene.tool_settings.use_keyframe_insert_auto
		context.scene.tool_settings.use_keyframe_insert_auto = not state
		global scene_state
		scene_state.check(context)
		return{'FINISHED'}


# this operator need to see scene_state class #
class Anim_OT_Auto_Use_Select_Pick_Depth_Toggle(Operator):
	bl_idname = 'anim.auto_use_select_pick_depth_toggle'
	bl_label = "Auto Use Select Pick Depth Toggle"
	bl_options = {'REGISTER'}

	def execute(self, _) -> set[str]:
		global scene_state
		scene_state.active_auto_use_select_pick_depth = \
			not scene_state.active_auto_use_select_pick_depth
		return{'FINISHED'}


classes = {
	Anim_OT_Auto_Key_Toggle,
	Anim_OT_Auto_Use_Select_Pick_Depth_Toggle
}


def register_frame_update(preferences):
	for cls in classes:
		register_class(cls)

	scene_state.store(bpy.context, preferences)
	# bpy.app.handlers.render_init.append(render_init)
	bpy.app.handlers.depsgraph_update_pre.append(depsgraph_update)


def unregister_frame_update():
	scene_state.restore(bpy.context)
	# bpy.app.handlers.render_init.remove(render_init)
	bpy.app.handlers.depsgraph_update_pre.remove(depsgraph_update)

	for cls in classes:
		unregister_class(cls)


if __name__ == '__main__':
	register_frame_update()