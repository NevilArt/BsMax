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

# The editor will also look for a specific Python module named 
# init_unreal.py. If this is present in any of the Python folders
# it will run that script during editor initialization.
# During init you also have more options when it comes to
# interfacing with and overriding other classes, 

# UnrealEditor-Cmd.exe "C:\projects\MyProject.uproject" -ExecutePythonScript="c:\my_script.py"

import os, sys

path = os.path.dirname(os.path.realpath(__file__))
if path not in sys.path:
	sys.path.append(path)

from menu import register_menu

def register():
    register_menu()

if __name__ == "__main__":
    register()