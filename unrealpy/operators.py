###########################################################################
#	BsMax, Tool for excahnge data between Blender, 3Dsmax and Unreal engine
#	Copyright (C) 2023  Naser Merati (Nevil)
#
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

from spawn_asset import spawn_selected_asset
from set_material import set_multi_material_to_selected_actor
from set_material_twosided import set_selected_materials_twosided
from paste_camera import paste_camera_from_clipboard

def upyop(command):
	if command == "spawn_selected":
		spawn_selected_asset()
	elif command == "set_material":
		set_multi_material_to_selected_actor()
	elif command == "set_twosided":
		set_selected_materials_twosided()
	elif command == "paste_camera":
		paste_camera_from_clipboard()