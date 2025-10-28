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
# 2025/10/16

import bpy
import sys

from bpy.types import Operator
from bpy.props import EnumProperty
from bpy.utils import register_class, unregister_class

# Platform-specific imports
if sys.platform == "win32":
	import ctypes
elif sys.platform.startswith("linux"):
	from Xlib.display import Display

def get_numlock_state():
	"""Return True if NumLock is ON"""
	if sys.platform == "win32":
		return bool(ctypes.WinDLL("User32.dll").GetKeyState(0x90) & 1)
	elif sys.platform.startswith("linux"):
		display = Display()
		return bool(display.get_keyboard_control().led_mask & 2)
	else:
		# macOS NumLock uncommon
		return False
	

def numlock_on_action(key):
	if key == '0':
		bpy.ops.view3d.view_camera()
	elif key == '1':
		bpy.ops.view3d.view_axis(type='FRONT')
	elif key == '2':
		bpy.ops.view3d.view_orbit(type='ORBITDOWN')
	elif key == '3':
		bpy.ops.view3d.view_axis(type='RIGHT')
	elif key == '4':
		bpy.ops.view3d.view_orbit(type='ORBITLEFT')
	elif key == '5':
		bpy.ops.view3d.view_persportho()
	elif key == '6':
		bpy.ops.view3d.view_orbit(type='ORBITRIGHT')
	elif key == '7':
		bpy.ops.view3d.view_axis(type='TOP')
	elif key == '8':
		bpy.ops.view3d.view_orbit(type='ORBITUP')
	elif key == '9':
		bpy.ops.view3d.view_orbit(type='ORBITRIGHT', angle= 3.1415927)

def numlock_off_action(key):
	if key == '0':
		pass
	elif key == '1':
		bpy.ops.wm.call_menu_pie(name='BSMAX_MT_pie_view3d_transform_quick')
	elif key == '2':
		pass
	elif key == '3':
		pass
	elif key == '4':
		pass
	elif key == '5':
		bpy.ops.wm.call_menu_pie(name='BSMAX_MT_pie_view3d_object_main')
	elif key == '6':
		pass
	elif key == '7':
		pass
	elif key == '8':
		pass
	elif key == '9':
		pass

class Screen_OT_Numpad_Override(Operator):
	bl_idname = 'screen.numpad_override'
	bl_label = "Numpad Override"
	bl_description = "Numpad Override"
	bl_options = {'REGISTER', 'INTERNAL'}

	key: EnumProperty(
		name="Key",
		items=[
			("0", "0", "0"),
			("1", "1", "1"),
			("2", "2", "2"),
			("3", "3", "3"),
			("4", "4", "4"),
			("5", "5", "5"),
			("6", "6", "6"),
			("7", "7", "7"),
			("8", "8", "8"),
			("9", "9", "9")
		]
	)

	def execute(self, context):
		if get_numlock_state():
			numlock_on_action(self.key)
			return {'FINISHED'}

		numlock_off_action(self.key)
		return {'FINISHED'}



classes = {
	Screen_OT_Numpad_Override
}


def register_operators():
	for cls in classes:
		register_class(cls)

def unregister_operators():
	for cls in classes:
		unregister_class(cls)


if __name__ == '__main__':
	register_operators()