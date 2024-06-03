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
# 2024/06/02

import bpy

from bsmax.keymaps import KeyMaps


def add_3dsmax_quad_menu(km, space, preferences):

	if preferences.floatmenus == '3DSMAX':
		km.new(
			space, 'bsmax.view3dquadmenue', 'V', 'PRESS',
	 		[('menu', 'viewport')]
		)

		""" This not needed drop tool can call this """
		# km.new(
		#	space,"bsmax.view3dquadmenue","RIGHTMOUSE","PRESS",
		# 	[('menu', 'default')]
		# )

		km.new(
			space, 'bsmax.view3dquadmenue', 'RIGHTMOUSE', 'PRESS',
			[('menu', 'create')], ctrl=True
		)

		km.new(
			space, 'bsmax.view3dquadmenue', 'RIGHTMOUSE', 'PRESS',
			[('menu', 'snap')], shift=True
		)

		km.new(
			space, 'bsmax.view3dquadmenue', 'RIGHTMOUSE', 'PRESS',
			[('menu', 'render')], alt=True, ctrl=True
		)

		km.new(
			space, 'bsmax.view3dquadmenue', 'RIGHTMOUSE', 'PRESS',
			[('menu', 'fx')], alt=True, shift=True
		)

		km.new(
			space, 'bsmax.view3dquadmenue', 'RIGHTMOUSE', 'PRESS',
			[('menu', 'Selection')], ctrl=True, shift=True
		)

		km.new(
			space, 'bsmax.view3dquadmenue', 'RIGHTMOUSE', 'PRESS',
			[('menu', 'custom')], alt=True, ctrl=True, shift=True
		)

		""" Ignore Alt + RMB in Maya navigation enabled """
		if preferences.navigation_3d != 'Maya':
			km.new(
				space, 'bsmax.view3dquadmenue', 'RIGHTMOUSE', 'PRESS',
				[('menu', 'coordinate')], alt=True
			)

	if preferences.floatmenus == 'PIEMAX':
		km.new(
			space, 'wm.call_menu_pie', 'RIGHTMOUSE', 'PRESS', 
			[('name', 'BSMAX_MT_default_pi')]
		)

		km.new(
			space, 'wm.call_menu_pie', 'RIGHTMOUSE', 'PRESS', 
			[('name', 'BSMAX_MT_create_pi')], ctrl=True
		)
		

floatMenuKaymaps = KeyMaps()

def add_float_menu(km, preferences):
	if bpy.context.window_manager.keyconfigs.addon:
		
		if preferences.floatmenus == '3DSMAX':
			spaces = []
			spaces.append(km.space('3D View', 'VIEW_3D', 'WINDOW'))
			spaces.append(km.space('Object Mode', 'EMPTY', 'WINDOW'))
			spaces.append(km.space('Mesh', 'EMPTY', 'WINDOW'))
			spaces.append(km.space('Curve', 'EMPTY', 'WINDOW'))
			spaces.append(km.space('Armature', 'EMPTY', 'WINDOW'))
			spaces.append(km.space('Grease Pencil', 'EMPTY', 'WINDOW'))
			spaces.append(km.space('Pose', 'EMPTY', 'WINDOW'))
			
			for space in spaces :
				add_3dsmax_quad_menu(floatMenuKaymaps, space, preferences)



def register_float_menu(preferences):
	global floatMenuKaymaps
	add_float_menu(floatMenuKaymaps, preferences)
	floatMenuKaymaps.register()


def unregister_float_menu():
	global floatMenuKaymaps
	floatMenuKaymaps.unregister()