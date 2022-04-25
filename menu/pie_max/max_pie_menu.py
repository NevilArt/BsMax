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

# Piemenu Order by Index
#			4
#		5		6
#	1				2
#		7		8
#			3


class VIEW3D_MT_PIE_Create(Menu):
	bl_idname = "BSMAX_MT_create_pi"
	bl_label = "Create"

	def draw(self, ctx):
		pie = self.layout.menu_pie()

		pie.menu("BSMAX_MT_create_light_pi", text="Light/Prop", icon="OUTLINER_OB_LIGHT")
		pie.menu("BSMAX_MT_curve_create_menu", icon='OUTLINER_OB_CURVE')
		pie.menu("BSMAX_MT_create_menu", text="Armature/Lattice")
		pie.prop(ctx.scene.primitive_setting, 'draw_mode', text='', icon='VIEW3D')
		pie.menu("BSMAX_MT_create_menu", text="Others")
		pie.menu("BSMAX_MT_mesh_create_menu", icon='OUTLINER_OB_MESH')
		pie.menu("BSMAX_MT_forcefield_cecreate_menu", icon='OUTLINER_OB_FORCE_FIELD')
		pie.menu("BSMAX_MT_empty_create_menu", text="Empty/Image")
		
		# pie.menu("BSMAX_MT_surface_create_menu", icon='OUTLINER_OB_SURFACE')
		# pie.menu("BSMAX_MT_metaball_create_menu", icon='OUTLINER_OB_META')
		# pie.menu("BSMAX_MT_text_create_menu", icon='OUTLINER_OB_FONT')
		# pie.menu("BSMAX_MT_gracepencil_create_menu", icon='OUTLINER_OB_GREASEPENCIL')
		# pie.menu("BSMAX_MT_armature_create_menu", icon='OUTLINER_OB_ARMATURE')
		# pie.menu("BSMAX_MT_lattice_create_menu", icon='OUTLINER_OB_LATTICE')
		# pie.menu("BSMAX_MT_empty_create_menu", icon='OUTLINER_OB_EMPTY')
		# pie.menu("BSMAX_MT_image_create_menu", icon='OUTLINER_OB_IMAGE')
		# pie.menu("BSMAX_MT_camera_create_menu", icon='OUTLINER_OB_CAMERA')
		# pie.operator("create.speaker", icon="OUTLINER_OB_SPEAKER")
		# pie.menu("BSMAX_MT_forcefield_cecreate_menu", icon='OUTLINER_OB_FORCE_FIELD')


#			4
#		5		6
#	1				2
#		7		8
#			3

class VIEW3D_MT_PIE_Default(Menu):
	bl_idname = "BSMAX_MT_default_pi"
	bl_label = "Default"

	def draw(self, ctx):
		pie = self.layout.menu_pie()

		pie.separator()
		pie.separator()
		pie.separator()
		pie.menu("VIEW3D_MT_object_context_menu", text="Blender")
		pie.menu("BSMAX_MT_transform_pi", text="Tool 1")
		pie.menu("BSMAX_MT_transform_pi", text="Display")
		pie.menu("BSMAX_MT_transform_pi", text="Tool 2")
		pie.menu("BSMAX_MT_transform_pi", text="TransformA")
		
		# pie.menu("BSMAX_MT_curve_create_menu", icon='OUTLINER_OB_CURVE')
		# pie.menu("BSMAX_MT_create_menu", text="Armature/Lattice")
		# pie.prop(ctx.scene.primitive_setting, 'draw_mode', text='', icon='VIEW3D')
		# pie.menu("BSMAX_MT_create_menu", text="Others")
		# pie.menu("BSMAX_MT_mesh_create_menu", icon='OUTLINER_OB_MESH')
		# pie.menu("BSMAX_MT_forcefield_cecreate_menu", icon='OUTLINER_OB_FORCE_FIELD')
		# pie.menu("BSMAX_MT_empty_create_menu", text="Empty/Image")


classes = [
	VIEW3D_MT_PIE_Default,
	VIEW3D_MT_PIE_Create]


def register_pie_max():
	for c in classes:
		bpy.utils.register_class(c)


def unregister_pie_max():
	for c in classes:
		bpy.utils.unregister_class(c)


if __name__ == "__main__":
	register_pie_max()

	# bpy.ops.wm.call_menu_pie(name="BSMAX_MT_create_pi")