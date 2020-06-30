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

import bpy, math
from bpy.types import Operator
from bpy.props import *
from primitive.primitive import *
from bsmax.actions import delete_objects

def get_snake_shape(scale):
	S1, S2, S3, s = [], [], [], scale
	S1.append(([ 0.342151*s, 0.491310*s,0],[  0.165044*s,  0.447320*s,0],'FREE',[  0.345222*s, 0.448056*s,0],'FREE'))
	S1.append(([ 0.351363*s, 0.360185*s,0],[  0.348292*s,  0.403438*s,0],'FREE',[  0.166411*s, 0.369848*s,0],'FREE'))
	S1.append(([-0.309806*s, 0.271567*s,0],[ -0.172608*s,  0.383790*s,0],'FREE',[ -0.425704*s, 0.176768*s,0],'FREE'))
	S1.append(([-0.289115*s,-0.310711*s,0],[ -0.383367*s, -0.238145*s,0],'FREE',[ -0.186417*s, -0.38978*s,0],'FREE'))
	S1.append(([ 0.339681*s,-0.287461*s,0],[  0.262386*s, -0.384004*s,0],'FREE',[  0.385556*s,-0.230163*s,0],'FREE'))
	S1.append(([ 0.339489*s,0.0778509*s,0],[  0.410325*s,-0.0117743*s,0],'FREE',[  0.243731*s,  0.19901*s,0],'FREE'))
	S1.append(([-0.163104*s,0.0426644*s,0],[-0.0158188*s,  0.222558*s,0],'FREE',[0.00131834*s,-0.141842*s,0],'FREE'))
	S1.append(([ 0.288056*s, -0.14006*s,0],[   0.10982*s, 0.0618023*s,0],'FREE',[  0.139572*s, -0.29958*s,0],'FREE'))
	S1.append(([-0.208599*s,-0.190378*s,0],[ -0.116147*s, -0.284987*s,0],'FREE',[ -0.287098*s,-0.110048*s,0],'FREE'))
	S1.append(([-0.197213*s, 0.216928*s,0],[ -0.288918*s,  0.140207*s,0],'FREE',[-0.0738501*s, 0.320134*s,0],'FREE'))
	S1.append(([ 0.380188*s, 0.215289*s,0],[  0.263369*s,  0.297943*s,0],'FREE',[  0.509473*s, 0.123816*s,0],'FREE'))
	S1.append(([ 0.403778*s,-0.380297*s,0],[  0.543244*s, -0.269729*s,0],'FREE',[  0.233927*s,-0.514954*s,0],'FREE'))
	S1.append(([-0.383219*s,-0.378286*s,0],[ -0.252043*s, -0.512853*s,0],'FREE',[ -0.509569*s,-0.248672*s,0],'FREE'))
	S1.append(([-0.385707*s, 0.348414*s,0],[ -0.540677*s,  0.230025*s,0],'FREE',[ -0.222445*s, 0.473139*s,0],'FREE'))
	S2.append(([-0.051879*s,0.0507449*s,0],[-0.0104687*s, 0.0415498*s,0],'FREE',[-0.0010163*s,0.0718359*s,0],'FREE'))
	S2.append(([ 0.100709*s, 0.114018*s,0],[ 0.0498464*s, 0.0929269*s,0],'FREE',[ 0.0912567*s,0.0837317*s,0],'FREE'))
	S2.append(([ 0.072352*s,0.0231595*s,0],[ 0.0818044*s, 0.0534456*s,0],'FREE',[ 0.0309417*s,0.0323546*s,0],'FREE'))
	S3.append(([ 0.173819*s,-0.146211*s,0],[  0.123728*s, -0.167174*s,0],'FREE',[  0.133052*s,-0.137338*s,0],'FREE'))
	S3.append(([0.0515172*s,-0.119591*s,0],[ 0.0922845*s, -0.128464*s,0],'FREE',[ 0.0421935*s,-0.149427*s,0],'FREE'))
	S3.append(([ 0.023546*s,-0.209099*s,0],[ 0.0328697*s, -0.179263*s,0],'FREE',[  0.073637*s,-0.188136*s,0],'FREE'))
	return (S1, S2, S3)

def get_blender_shape(scale):
	S1, S2, S3, s = [], [], [], scale
	S1.append(([ 0.0481047*s,  0.428945*s,0],[ 0.0080356*s,  0.453882*s,0],'FREE',[   0.11761*s,   0.38239*s,0],'FREE'))
	S1.append(([  0.428365*s,  0.133274*s,0],[  0.307372*s,  0.240382*s,0],'FREE',[  0.595795*s,-0.0499471*s,0],'FREE'))
	S1.append(([  0.152365*s, -0.375552*s,0],[   0.45261*s, -0.374285*s,0],'FREE',[-0.0910671*s, -0.376578*s,0],'FREE'))
	S1.append(([ -0.193646*s, -0.054044*s,0],[ -0.199445*s, -0.182241*s,0],'FREE',[ -0.279417*s, -0.128656*s,0],'FREE'))
	S1.append(([  -0.40098*s, -0.220063*s,0],[ -0.258184*s,   -0.1092*s,0],'FREE',[ -0.462361*s, -0.267718*s,0],'FREE'))
	S1.append(([ -0.478143*s,  -0.13241*s,0],[ -0.533648*s, -0.182801*s,0],'FREE',[ -0.353649*s,-0.0205244*s,0],'FREE'))
	S1.append(([ -0.104445*s,  0.158987*s,0],[ -0.231908*s, 0.0587641*s,0],'FREE',[  -0.22329*s,  0.159674*s,0],'FREE'))
	S1.append(([ -0.311745*s,  0.157944*s,0],[ -0.242874*s,  0.157944*s,0],'FREE',[ -0.366598*s,   0.15955*s,0],'FREE'))
	S1.append(([ -0.305578*s,  0.255428*s,0],[ -0.379551*s,  0.253829*s,0],'FREE',[ -0.182882*s,  0.263597*s,0],'FREE'))
	S1.append(([  0.106752*s,  0.258166*s,0],[-0.0294483*s,  0.255596*s,0],'FREE',[ 0.0822335*s,  0.281801*s,0],'FREE'))
	S1.append(([-0.0234107*s,  0.367642*s,0],[ 0.0187345*s,  0.331151*s,0],'FREE',[ -0.062326*s,  0.402833*s,0],'FREE'))
	S2.append(([  0.152365*s,  0.096901*s,0],[ 0.0847928*s, 0.0953648*s,0],'FREE',[  0.216282*s,  0.098354*s,0],'FREE'))
	S2.append(([  0.289594*s,-0.0236156*s,0],[  0.287025*s, 0.0507261*s,0],'FREE',[  0.292263*s, -0.100851*s,0],'FREE'))
	S2.append(([  0.152365*s,  -0.15028*s,0],[  0.218778*s, -0.149149*s,0],'FREE',[ 0.0887173*s, -0.151363*s,0],'FREE'))
	S2.append(([ 0.0197624*s,-0.0236156*s,0],[ 0.0197144*s,-0.0977039*s,0],'FREE',[ 0.0198135*s, 0.0550511*s,0],'FREE'))
	S3.append(([  0.145986*s,  0.159805*s,0],[ 0.0409008*s,  0.157416*s,0],'FREE',[  0.245386*s,  0.162064*s,0],'FREE'))
	S3.append(([  0.359398*s,-0.0276166*s,0],[  0.355403*s, 0.0879958*s,0],'FREE',[  0.363549*s, -0.147729*s,0],'FREE'))
	S3.append(([  0.145986*s, -0.224598*s,0],[  0.249269*s,  -0.22284*s,0],'FREE',[  0.047004*s, -0.226284*s,0],'FREE'))
	S3.append(([-0.0602312*s,-0.0276166*s,0],[-0.0603059*s, -0.142835*s,0],'FREE',[-0.0601519*s, 0.0947218*s,0],'FREE'))
	return (S1, S2, S3)

class Create_OT_Logo(Operator):
	bl_idname = "create.logo"
	bl_label = "Logo"
	bl_options = {"UNDO"}

	radius = 0.0

	Step = 0
	Start_x = 0
	Start_y = 0

	obj = None

	def modal(self, ctx, event):
		x, y = event.mouse_region_x, event.mouse_region_y
		if ctx.area.type == 'VIEW_3D':
			p = GetMouse3DLocation(x, y, ctx)
			mx, my, mz = p.x, p.y, p.z
			if event.type == 'LEFTMOUSE':
				# Start to Create
				if self.Step == 0:
					self.Step = 1
					self.Start_x = mx
					self.Start_y = my
					Shapes = get_blender_shape(self.radius)
					self.obj = CreatePrimitiveCurve(Shapes, "Blender", True)
					self.obj.location = (mx, my, 0)

				# Click count
				if event.value =='RELEASE':
					self.Step += 1

			# update
			if event.type == 'MOUSEMOVE':
				if self.Step == 1:
					w = abs(self.Start_x - mx)
					l = abs(self.Start_y - my)
					self.radius = math.sqrt(w * w + l * l)

				if self.Step > 0:
					# Update Curve
					Shapes = get_blender_shape( self.radius )
					UpdateCurveData(self.obj, Shapes, True)

			if self.Step == 2:
				params = ( "Blender", self.radius )
				CreatePrimitiveData(self.obj, params)
				#self.Step = 0

		if event.type in {'RIGHTMOUSE', 'ESC'} or self.Step > 1:
			self.Step = 0
			return {'CANCELLED'}

		return {'RUNNING_MODAL'}
		
	def invoke(self, ctx, event):
		ctx.window_manager.modal_handler_add(self)
		return {'RUNNING_MODAL'}

def register_logo():
	bpy.utils.register_class(Create_OT_Logo)

def unregister_logo():
	bpy.utils.unregister_class(Create_OT_Logo)