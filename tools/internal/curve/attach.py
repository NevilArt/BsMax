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
# 2024/06/20

import bpy

from bsmax.operator import PickOperator


class Curve_OT_Attach(PickOperator):
	bl_idname = 'curve.attach'
	bl_label = "Attach"

	filters = ['CURVE']

	@classmethod
	def poll(self, ctx):
		if ctx.area.type == 'VIEW_3D':
			return ctx.mode == 'EDIT_CURVE'
		return False

	def picked(self, ctx, source, subsource, target, subtarget):
		bpy.ops.object.mode_set(mode='OBJECT', toggle=False)
		target.select_set(state = True)
		bpy.ops.object.join()
		bpy.ops.object.mode_set(mode='EDIT', toggle=False)
		bpy.ops.ed.undo_push()
		bpy.ops.curve.attach('INVOKE_DEFAULT')


def register_attach():
	bpy.utils.register_class(Curve_OT_Attach)


def unregister_attach():
	bpy.utils.unregister_class(Curve_OT_Attach)


if __name__ == '__main__':
	register_attach()