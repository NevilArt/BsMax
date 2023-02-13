############################################################################
#	This program is free software: you can redistribute it and/or modify
#	it under the terms of the GNU General Public License as published by
#	the Free Software Foundation,either version 3 of the License,or
#	(at your option) any later version.
#
#	This program is distributed in the hope that it will be useful,
#	but WITHOUT ANY WARRANTY; without even the implied warranty of
#	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#	GNU General Public License for more details.
#
#	You should have received a copy of the GNU General Public License
#	along with this program.  If not,see <https://www.gnu.org/licenses/>.
############################################################################

import bpy
from math import pi, sin, cos, ceil, tan
from mathutils import Vector
from primitive.primitive import Primitive_Curve_Class, Draw_Primitive
from bsmax.math import get_bias


def bezier_helix(radius1, radius2, height, turns, segment, bias, ccw):
	knots = []

	if turns == 0:
		turns = 0.0001

	totalSeg = int(segment * ceil(turns))
	totalRot = turns * pi*2
	
	angle = totalRot / totalSeg if ccw else -(totalRot / totalSeg)
	roundPieces = (radius1 - radius2) / totalSeg
	tangentFactor = (4 / 3) * tan(pi / (2 * segment))
	percentSec = 1 / totalSeg

	for i in range(totalSeg + 1):
		theta = i * angle + pi/2
		tSin, tCos = sin(theta), cos(theta)
		
		localRadius = radius1 - roundPieces * i
		
		x = localRadius * tCos
		y = localRadius * tSin

		tangentDistance = localRadius * tangentFactor
	
		coPercent = i * percentSec
		coBias = get_bias(bias, coPercent)
		co = (x, y, height * coBias)

		sinTangent =  tangentDistance * tSin
		cosTangent =  tangentDistance * tCos

		inBias = get_bias(bias, coPercent - (percentSec/2))
		outBias = get_bias(bias, coPercent + (percentSec/2))

		if ccw:
			in_tangent = (x + sinTangent, y - cosTangent, height * inBias)
			out_tangent = (x - sinTangent, y + cosTangent, height * outBias)
		else:
			in_tangent = (x - sinTangent, y + cosTangent, height * inBias)
			out_tangent = (x + sinTangent, y - cosTangent, height * outBias)

		knots.append((co, in_tangent, 'FREE', out_tangent, 'FREE'))

	return [knots]



def segment_helix(radius1, radius2, height, turns, segment, bias, ccw):

	totalRot = turns * 2 * pi

	if ccw:
		totalRot *= -1

	if turns == 0:
		turns = 0.0001

	totalSeg = int(segment * turns)
	piece = totalRot / (segment * turns)
	heightPieces = height / (totalSeg)
	roundPieces = (radius1 - radius2) / (segment * turns)

	shape = []
	for i in range(totalSeg + 1):
		theta = piece * i
		length = radius1 - roundPieces * i
		percent = (heightPieces * i) / height if height > 0 else 0
		
		point = (
				sin(theta) * length,
				cos(theta) * length,
				height * get_bias(bias, percent)
		)
		
		shape.append((point, point, 'FREE', point, 'FREE'))

	return [shape]



def get_helix_shape(radius1, radius2, height, turns, segment, bias, ccw, bezSeg):
	if bezSeg:
		return bezier_helix(radius1, radius2, height, turns, segment, bias, ccw)
	return segment_helix(radius1, radius2, height, turns, segment, bias, ccw)



class Helix(Primitive_Curve_Class):
	def init(self):
		self.classname = "Helix"
		self.finishon = 4
		self.close = False

	def create(self, ctx):
		shapes = get_helix_shape(0, 0, 0, 3, 20, 0, False, True)
		self.create_curve(ctx, shapes, self.classname)
		pd = self.data.primitivedata
		pd.classname = self.classname
		pd.turns = 3
		pd.ssegs = 20
		pd.bool1 = True

	def update(self):
		pd = self.data.primitivedata
		# radius1, radius2, height, turns, segs, bias, ccw
		shapes = get_helix_shape(pd.radius1, pd.radius2, pd.height,
					pd.turns, pd.ssegs, pd.bias_np, pd.ccw, pd.bool1)
		self.update_curve(shapes)

	def abort(self):
		bpy.ops.object.delete({'selected_objects': [self.owner]})



class Create_OT_Helix(Draw_Primitive):
	bl_idname = "create.helix"
	bl_label = "Helix"
	subclass = Helix()
	use_gride = True
	gride_updated = False

	def create(self, ctx):
		self.subclass.create(ctx)
		self.params = self.subclass.owner.data.primitivedata
		self.subclass.owner.location = self.gride.location
		self.subclass.owner.rotation_euler = self.gride.rotation

	def update(self, ctx, clickcount, dimension):
		if clickcount == 1:
			if self.ctrl:
				self.params.radius1 = dimension.radius
				self.params.radius2 = dimension.radius
				self.params.height = dimension.radius*2
			else:
				self.params.radius1 = dimension.radius
				self.params.radius2 = dimension.radius

		if clickcount == 2:
			if self.use_single_draw:
				self.jump_to_end()
				return

			self.params.height = dimension.height

		if clickcount == 3:
			if not self.gride_updated:
				center = self.gride.gride_matrix @ Vector((0,0,self.params.height))
				self.gride.location = center
				self.gride.update()
				self.gride_updated = True

			self.params.radius2 = dimension.distance

	def finish(self):
		self.gride_updated = False



def register_helix():
	bpy.utils.register_class(Create_OT_Helix)
	
def unregister_helix():
	bpy.utils.unregister_class(Create_OT_Helix)

if __name__ == "__main__":
	register_helix()
	
	new_helix = Helix()
	new_helix.create(bpy.context)
	new_helix.data.primitivedata.radius1 = 1
	new_helix.update()
	bpy.ops.primitive.cleardata()