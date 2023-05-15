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

import unreal


def get_menu_item(name, command):
	entry = unreal.ToolMenuEntry(
		name = name,
		type = unreal.MultiBlockType.MENU_ENTRY,
	)
	entry.set_label(name)  
	entry.set_string_command(unreal.ToolMenuStringCommandType.PYTHON,
							custom_type=unreal.Name(""),
							string=command
			)

	return entry


def create_nevil_menu():

	menus = unreal.ToolMenus.get()
	mainMenu = menus.find_menu("LevelEditor.MainMenu")

	nevilMenu = mainMenu.add_sub_menu("Nevil.Menu", "Python", "Nevil Menu", "Nevil Tools")

	nevilMenu.add_menu_entry("Items",
				get_menu_item("Spawn selected",
							  'from operators import upyop; upyop("spawn_selected");'
				)
	)

	nevilMenu.add_menu_entry("Items",
				get_menu_item("Set Materials",
							  'from operators import upyop; upyop("set_material");'
				)
	)

	nevilMenu.add_menu_entry("Items",
				get_menu_item("Set Twosided",
							  'from operators import upyop; upyop("set_twosided");'
				)
	)

	nevilMenu.add_menu_entry("Items",
				get_menu_item("Paste Camera",
							  'from operators import upyop; upyop("paste_camera");'
				)
	)

	menus.refresh_all_widgets()



def register_menu():
	create_nevil_menu()


if __name__ == "__main__":
	register_menu()