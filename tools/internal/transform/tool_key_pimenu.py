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
from bpy.types import Menu


class VIEW3D_MT_move_rotate_scale_pie(Menu):
    bl_label = "Transform Tools"
    bl_idname = "VIEW3D_MT_move_rotate_scale_pie"

    def draw(self, context):
        layout = self.layout
        pie = layout.menu_pie()

        # Pie slot order for a 4-way pie: West, East, South, North

        # Left -> Move
        op = pie.operator("wm.tool_set_by_id", text="Move", icon='ORIENTATION_GLOBAL')
        op.name = "builtin.move"

        # Right -> Scale
        op = pie.operator("wm.tool_set_by_id", text="Scale", icon='FULLSCREEN_ENTER')
        op.name = "builtin.scale"

        # Down -> Transform
        op = pie.operator("wm.tool_set_by_id", text="Transform", icon='OBJECT_ORIGIN')
        op.name = "builtin.transform"

        # Up -> Rotate
        op = pie.operator("wm.tool_set_by_id", text="Rotate", icon='FILE_REFRESH')
        op.name = "builtin.rotate"


addon_keymaps = []


def register_tool_key_pimenu():
    bpy.utils.register_class(VIEW3D_MT_move_rotate_scale_pie)

    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    if kc:
        km = kc.keymaps.new(name="3D View", space_type='VIEW_3D')
        kmi = km.keymap_items.new(
            "wm.call_menu_pie", "Q", "PRESS"
        )
        kmi.properties.name = "VIEW3D_MT_move_rotate_scale_pie"
        addon_keymaps.append((km, kmi))


def unregister_tool_key_pimenu():
    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)
    addon_keymaps.clear()

    bpy.utils.unregister_class(VIEW3D_MT_move_rotate_scale_pie)


if __name__ == "__main__":
    register_tool_key_pimenu()