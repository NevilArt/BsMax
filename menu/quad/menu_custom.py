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

from .q_items import QuadItem

# Indexes #
# [3] [2] #
#    +    #
# [4] [1] #
###########
t, f, n = True, False, None

def seprator():
	return QuadItem(n, f, f, n, n, n)

def get_custom_submenu(ctx):
	items = []
				#  text,  check,  enabled, menu, action, setting
	action = "bpy.ops.mesh.primitive_cube_add()"
	items.append(QuadItem("Custom", f, f, n, action, n))
	return items

def get_custom_menu():
	items = []
				#  text,  check,  enabled, menu, action, setting
	items.append(QuadItem("Custom", f, f, n, "", n))
	items.append(seprator())
	submenu = get_custom_submenu(ctx)
	items.append(QuadItem("Sub Menu", f, f, submenu, n, n)) # seprator
	return items