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
from bpy.types import Operator
from mathutils import Matrix

# TODO
# Zoom on armator if no bone selected

class BsMax_OT_HomeView(Operator):
	bl_idname = "bsmax.homeview"
	bl_label = "Home View"
	@classmethod
	def poll(self, ctx):
		return ctx.area.type == 'VIEW_3D'
	def execute(self, ctx):
		homeview = (( 0.4100,0.9120,-0.0133,0),(-0.4017,0.1936,0.8950,-1.9045),
					( 0.8188,-0.3617,0.4458,-17.9866),( 0,0,0,1))
		ctx.area.spaces.active.region_3d.view_matrix = Matrix(homeview)
		return{"FINISHED"}

# simulate zoom extended in 3d max
class BsMax_OT_ZoomExtended(Operator):
	bl_idname = "bsmax.zoomextended"
	bl_label = "Zoom Extended"
	@classmethod
	def poll(self, ctx):
		return ctx.area.type == 'VIEW_3D'
	def execute(self, ctx):
		if len(ctx.scene.objects) == 0:
			bpy.ops.bsmax.homeview('INVOKE_DEFAULT')
		elif len(ctx.selected_objects) == 0:
			bpy.ops.view3d.view_all(use_all_regions=False,center=False)
		else:
			bpy.ops.view3d.view_selected(use_all_regions=False)
		return{"FINISHED"}

classes = [BsMax_OT_ZoomExtended, BsMax_OT_HomeView]

def register_zoomextended():
	[bpy.utils.register_class(c) for c in classes]

def unregister_zoomextended():
	[bpy.utils.unregister_class(c) for c in classes]
