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
# 2024/02/25

from .fbx_refiner import register_fbx_refiner, unregister_fbx_refiner
from .tools import register_tools, unregister_tools


def register_material(preferences):
    register_tools()

    if preferences.experimental:
        register_fbx_refiner()


def unregister_material():
    unregister_tools()
    unregister_fbx_refiner()