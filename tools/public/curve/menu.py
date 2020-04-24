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

def controlpoints_menu(self, ctx):
	layout = self.layout
	layout.separator()
	layout.operator("curve.mergebydistance",text="Merge by Distance").typein=True
	layout.operator("curve.break",text="Break")
	layout.operator("curve.makefirst",text="Make First")
	layout.operator("curve.chamfer",text="Chamfer/Fillet").typein=True

def segments_menu(self, ctx):
	layout = self.layout
	layout.operator("curve.dividplus",text="Divid plus").typein=True
	layout.separator()
	layout.operator("curve.outline",text="Outline").typein=True
	layout.separator()
	layout.operator("curve.boolean",text="Boolean").typein=True
	bu = layout.operator("curve.boolean",text="Boolean (Union)")
	bu.typein = False
	bu.mode = 'UNION'
	bi = layout.operator("curve.boolean",text="Boolean (Intersection)")
	bi.typein = False
	bi.mode = 'INTERSECTION'
	bd = layout.operator("curve.boolean",text="Boolean (Diffrence)")
	bd.typein = False
	bd.mode = 'DIFFERENCE'
	bc = layout.operator("curve.boolean",text="Boolean (Cut)")
	bc.typein = False
	bc.mode = 'CUT'
		
def register_menu():
	bpy.types.VIEW3D_MT_edit_curve_ctrlpoints.append(controlpoints_menu)
	bpy.types.VIEW3D_MT_edit_curve_segments.append(segments_menu)

def unregister_menu():
	bpy.types.VIEW3D_MT_edit_curve_ctrlpoints.remove(controlpoints_menu)
	bpy.types.VIEW3D_MT_edit_curve_segments.remove(segments_menu)