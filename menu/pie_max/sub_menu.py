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
from bpy.utils import register_class, unregister_class
from bpy.types import Menu



class VIEW3D_MT_PIE_Transform(Menu):
	bl_idname = "BSMAX_MT_transform_pi"
	bl_label = "Default"

	def draw(self, ctx):
		layout = self.layout

		layout.operator("wm.tool_set_by_id", text="Move").name='builtin.move'
		layout.operator("wm.tool_set_by_id", text="Rotate").name='builtin.rotate'
		layout.operator("wm.tool_set_by_id", text="Scale").name='builtin.scale'
		layout.operator("object.placment", text="Placment")
		layout.operator("wm.tool_set_by_id", text="Cursor").name='builtin.cursor'
		layout.separator()
		# layout.operator("", text="Select")
		# layout.operator("", text="Select Similar")
		# layout.operator("", text="Select Instance")
		# layout.separator()
		# layout.operator("", text="Clone")
		# layout.operator("", text="Align Objects...")
		# layout.separator()
		# layout.operator("", text="Object Properties...")
		# layout.separator()
		# layout.operator("", text="Curve Editor...")
		# layout.operator("", text="Dope sheet...")
		# layout.operator("", text="Driver Editor...")
		# layout.operator("", text="NLA Editor...")
		# layout.operator("", text="Text Editor...")
		# if version > (2, 92, 0):
		# 	layout.operator("", text="Move")
		# 	layout.operator("", text="Geometry Node Editor...")
		# layout.operator("", text="Conver to")



class VIEW3D_MT_PIE_Create_Light(Menu):
	bl_idname = "BSMAX_MT_create_light_pi"
	bl_label = "Light/Prob"
	def draw(self, ctx):
		layout = self.layout
		layout.operator("create.pointlight", text="Point", icon="LIGHT_POINT")
		layout.operator("create.sunlight", text="Sun", icon="LIGHT_SUN")
		layout.operator("create.spotlight", text="Spot Light Free/Target", icon="LIGHT_SPOT")
		layout.operator("create.arealight",text="Free Area",icon="LIGHT_AREA").free = True
		layout.operator("create.arealight",text="Target Area",icon="LIGHT_AREA")
		layout.separator()
		layout.operator("create.light_probe_cubemap",
			text="Reflection Cubemap", icon="LIGHTPROBE_CUBEMAP")
		layout.operator("create.light_probe_planer",
			text="Reflection Plane", icon="LIGHTPROBE_PLANAR")
		layout.operator("create.light_probe_grid",
			text="Irradiance Volume", icon="LIGHTPROBE_GRID")

classes = [
	VIEW3D_MT_PIE_Transform,
	VIEW3D_MT_PIE_Create_Light]


def register_sub_menu():
	for c in classes:
		register_class(c)


def unregister_sub_menu():
	for c in classes:
		unregister_class(c)


if __name__ == "__main__":
	register_sub_menu()