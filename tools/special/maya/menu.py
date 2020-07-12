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

def lattice_menu(self, ctx):
	layout = self.layout
	layout.separator()
	layout.operator("modifier.lattice_2x2x2_set",text='Lattice 2x2x2 (Set)',icon="OUTLINER_OB_LATTICE")
	layout.operator("modifier.lattice_3x3x3_set",text='Lattice 3x3x3 (Set)',icon="OUTLINER_OB_LATTICE")
	layout.operator("modifier.lattice_4x4x4_set",text='Lattice 4x4x4 (Set)',icon="OUTLINER_OB_LATTICE")

def register_menu():
	bpy.types.BSMAX_MT_latticecreatemenu.append(lattice_menu)

def unregister_menu():
	bpy.types.BSMAX_MT_latticecreatemenu.remove(lattice_menu)