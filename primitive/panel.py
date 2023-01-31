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
# from bpy.props import *
from bpy.types import Panel, Operator


def get_adaptive_plane_panel(self, layout):
	layout.label(text="Adaptive Plane", icon='MOD_BEVEL')
	col = layout.column(align=True)
	col.prop(self, "width", text="width")
	col.prop(self, "length", text="length")
	col.prop(self, "thickness", text="Min Size")
	col.prop(self, "bias", text="Bias")


def get_plane_panel(self, layout):
	layout.label(text="Plane", icon='MESH_PLANE')
	col = layout.column(align=True)
	col.prop(self, "width", text="width")
	col.prop(self, "length", text="length")
	col = layout.column(align=True)
	col.prop(self, "wsegs", text="WSegs")
	col.prop(self, "lsegs", text="LSegs")



def get_box_panel(self, layout):
	layout.label(text="Box", icon='MESH_CUBE')
	col = layout.column(align=True)
	col.prop(self, "width", text="width")
	col.prop(self, "length", text="length")
	col.prop(self, "height", text="Height")
	col = layout.column(align=True)
	col.prop(self, "wsegs", text="WSegs")
	col.prop(self, "lsegs", text="LSegs")
	col.prop(self, "hsegs", text="HSegs")



def get_cone_panel(self, layout):
	layout.label(text="Cone",icon='MESH_CONE')
	col = layout.column(align=True)
	col.prop(self,"radius1", text="Radius1")
	col.prop(self,"radius2", text="Radius2")
	col.prop(self,"height", text="Height")
	col = layout.column(align=True)
	col.prop(self,"hsegs", text="Height Segs")
	col.prop(self,"csegs", text="Cap Segs")
	col.prop(self,"ssegs", text="Side Segs")
	col = layout.column(align=True)
	col.prop(self,"sliceon", text="Slice on")
	if self.sliceon:
		col.prop(self,"sfrom", text="From")
		col.prop(self,"sto", text="To")



def get_sphere_panel(self, layout):
	layout.label(text="Sphere",icon='MESH_UVSPHERE')
	col = layout.column(align=True)
	col.prop(self,"radius1", text="Radius")
	if not self.seglock:
		col.prop(self,"ssegs", text="Side Segs")
		col.prop(self,"hsegs", text="Height Segs")
	else:
		col.prop(self,"ssegs", text="Segments")
	col.prop(self,"seglock", text="Lock Segments")
	col.prop(self,"bias", text="Hemisphere")
	#Col.prop(self,"chop")
	col.prop(self,"sliceon", text="Sliceon")
	if self.sliceon:
		col.prop(self,"sfrom", text="From")
		col.prop(self,"sto", text="To")
	col.prop(self,"base", text="Base")



def get_icosphere_panel(self, layout):
	layout.label(text="Icosphere",icon='MESH_ICOSPHERE')
	col = layout.column(align=True)
	col.prop(self,"radius1", text="Radius")
	col.prop(self,"wsegs", text="subdiv")



def get_capsule_panel(self, layout):
	layout.label(text="Capsule",icon='META_CAPSULE')
	col = layout.column(align=True)
	col.prop(self,"radius1", text="Radius")
	col.prop(self,"height", text="Height")
	col = layout.column(align=True)
	col.prop(self,"center", text="Center/Overall")
	col = layout.column(align=True)
	col.prop(self,"hsegs", text="Height segs")
	col.prop(self,"ssegs", text="Side segs")
	if not self.seglock:
		col.prop(self,"csegs", text="Cap")
	col.prop(self,"seglock", text="Segs Lock")
	col = layout.column(align=True)
	col.prop(self,"sliceon", text="Sliceon")
	if self.sliceon:
		col.prop(self,"sfrom", text="From")
		col.prop(self,"sto", text="To")



def get_oiltank_panel(self, layout):
	layout.label(text="Capsule",icon='META_CAPSULE')
	col = layout.column(align=True)
	col.prop(self,"radius1", text="Radius")
	col.prop(self,"height", text="Height")
	col.prop(self,"thickness", text="Cap Height")
	col = layout.column(align=True)
	col.prop(self,"center", text="Center/Overall")
	col = layout.column(align=True)
	#col.prop(self,"chamfer1", text="Blend")
	col.prop(self,"hsegs", text="Height segs")
	col.prop(self,"ssegs", text="Side segs")
	if not self.seglock:
		col.prop(self,"csegs", text="Cap")
	col.prop(self,"seglock", text="Segs Lock")
	col = layout.column(align=True)
	col.prop(self,"sliceon", text="Sliceon")
	if self.sliceon:
		col.prop(self,"sfrom", text="From")
		col.prop(self,"sto", text="To")



def get_cylinder_panel(self, layout):
	layout.label(text="Cylinder",icon='MESH_CYLINDER')
	col = layout.column(align=True)
	col.prop(self,"radius1", text="Radius")
	col.prop(self,"height", text="Height")
	col = layout.column(align=True)
	col.prop(self,"hsegs", text="Height Segs")
	col.prop(self,"csegs", text="Cap Segs")
	col.prop(self,"ssegs", text="Side Segs")
	col = layout.column(align=True)
	col.prop(self,"sliceon", text="Slice on")
	if self.sliceon:
		col.prop(self,"sfrom", text="From")
		col.prop(self,"sto", text="To")



def get_teapot_panel(self, layout):
	layout.label(text="Teapot",icon='MESH_CYLINDER')
	col = layout.column(align=True)
	col.prop(self,"radius1", text="Radius1")
	col.prop(self,"csegs", text="Segs")
	col = layout.column(align=True)
	col.prop(self,"bool1", text="Body")
	col.prop(self,"bool2", text="Handle")
	col.prop(self,"bool3", text="Spout")
	col.prop(self,"bool4", text="Lid")



def get_tube_panel(self, layout):
	layout.label(text="Tube",icon='MESH_CYLINDER')
	col = layout.column(align=True)
	col.prop(self,"radius1", text="Radius1")
	col.prop(self,"radius2", text="Radius2")
	col.prop(self,"height", text="Height")
	col = layout.column(align=True)
	col.prop(self,"hsegs", text="Height Segs")
	col.prop(self,"csegs", text="Cap Segs")
	col.prop(self,"ssegs", text="Side segs")
	col = layout.column(align=True)
	col.prop(self,"sliceon", text="Slice on")
	if self.sliceon:
		col.prop(self,"sfrom", text="From")
		col.prop(self,"sto", text="To")



def get_torus_panel(self, layout):
	layout.label(text="Torus",icon='MESH_TORUS')
	col = layout.column(align=True)
	col.prop(self,"radius1", text="Radius1")
	col.prop(self,"radius2", text="Radius2")
	col = layout.column(align=True)
	col.prop(self,"rotation", text="Rotation")
	col.prop(self,"twist", text="Twist")
	col = layout.column(align=True)
	col.prop(self,"ssegs", text="Segments")
	col.prop(self,"ssegs_b", text="Sides")
	col = layout.column(align=True)
	col.prop(self,"sliceon")
	if self.sliceon:
		col.prop(self,"sfrom")
		col.prop(self,"sto")



def get_pyramid_panel(self, layout):
	layout.label(text="Pyramid",icon='MARKER')
	col = layout.column(align=True)
	col.prop(self,"width", text="Width")
	col.prop(self,"length", text="Depth")
	col.prop(self,"height", text="Height")
	col = layout.column(align=True)
	col.prop(self,"wsegs", text="Width Segs")
	col.prop(self,"lsegs", text="Depth Segs")
	col.prop(self,"hsegs", text="Height Segs")



def get_monkey_panel(self, layout):
	layout.label(text="Monkey",icon='MESH_MONKEY')
	col = layout.column(align=True)
	col.prop(self,"radius1", text="Radius")



def get_rectangle_panel(self, layout):
	layout.label(text="Rectangle",icon='META_PLANE')
	col = layout.column(align=True)
	col.prop(self,"width", text="Width")
	col.prop(self,"length", text="Length")
	col.prop(self,"chamfer1", text="Corner Radius")



def get_circle_panel(self, layout):
	layout.label(text="Circle",icon='MESH_CIRCLE')
	col = layout.column(align=True)
	col.prop(self,"radius1", text="Radius")



def get_ellipse_panel(self, layout):
	layout.label(text="Ellipse",icon='MESH_CAPSULE')
	col = layout.column(align=True)
	col.prop(self,"width", text="Width")
	col.prop(self,"length", text="Length")
	col.prop(self,"outline", text="Outline")
	if self.outline:
		col.prop(self,"thickness", text="Thickness")



def get_curve_extrude_panel(self, layout):
	layout.label(text="Extrude",icon='EXPORT')
	col = layout.column(align=True)
	col.prop(self,"height", text="Height")
	col.prop(self,"hsegs", text="Segments")
	col = layout.column(align=True)
	col.prop(self,"chamfer1", text="Upper")
	col.prop(self,"chamfer2", text="Lover")
	try:
		# ignore this on float dialog for now but hadto to solve
		col.prop(bpy.context.curve,"use_fill_caps", text="Cap")
	except:
		pass



def get_mesh_extrude_panel(self, layout):
	layout.label(text="Extrude",icon='EXPORT')
	col = layout.column(align=True)
	col.prop(self,"target", text="Target")
	col = layout.column(align=True)
	col.prop(self,"height", text="Height")
	col.prop(self,"hsegs", text="Segments")
	col = layout.column(align=True)
	col.prop(self,"chamfer1", text="Upper")
	col.prop(self,"chamfer2", text="Lover")
	col = layout.column(align=True)
	col.prop(self,"bool1", text="Cap Upper")
	col.prop(self,"bool2", text="Cap Lower")
	col = layout.column(align=True)
	col.prop(self,"extrude_segmode", text="Mode")
	if self.extrude_segmode == "Manual":
		col.prop(self,"csegs", text="Segments")



def get_arc_panel(self, layout):
	layout.label(text="Arc",icon='SPHERECURVE')
	col = layout.column(align=True)
	col.prop(self,"radius1", text="Radius")
	col.prop(self,"sfrom", text="Start")
	col.prop(self,"sto", text="End")
	col.prop(self,"sliceon", text="Pie")



def get_donut_panel(self, layout):
	layout.label(text="Donut",icon='MESH_CIRCLE')
	col = layout.column(align=True)
	col.prop(self,"radius1", text="radius1")
	col.prop(self,"radius2", text="radius2")



def get_ngon_panel(self, layout):
	layout.label(text="NGon",icon='SEQ_CHROMA_SCOPE')
	col = layout.column(align=True)
	col.prop(self,"radius1", text="radius")
	col.prop(self,"ssegs", text="sides")
	#col.prop(self,"chamfer1", text="cornerradius")
	col.prop(self,"smooth", text="circular")



def get_star_panel(self, layout):
	layout.label(text="Star",icon='SOLO_OFF')
	col = layout.column(align=True)
	col.prop(self,"radius1", text="Radius1")
	col.prop(self,"radius2", text="Radius2")
	col.prop(self,"ssegs", text="Points")
	col.prop(self,"twist", text="Distortion")
	#col.prop(self,"chamfer1", text="filletradius1")
	#col.prop(self,"chamfer2", text="filletradius2")
	col.prop(self,"seed", text="Seed")
	col.prop(self,"random", text="Randval")



def get_helix_panel(self, layout):
	layout.label(text="Helix",icon='FORCE_VORTEX')
	col = layout.column(align=True)
	col.prop(self,"radius1", text="Radius1")
	col.prop(self,"radius2", text="Radius2")
	col.prop(self,"height", text="Height")
	col = layout.column(align=True)
	col.prop(self,"turns", text="Turns")
	col.prop(self,"ssegs", text="Segs")
	col = layout.column(align=True)
	col.prop(self,"bias_np", text="Bias")
	col = layout.column(align=True)
	col.prop(self,"ccw", text="ccw")



def get_profilo_panel(self, layout):
	layout.label(text="Profilo",icon='MOD_BOOLEAN')
	col = layout.column(align=True)
	col.prop(self,"profilo_mode")
	col = layout.column(align=True)

	if self.profilo_mode == 'Angle':
		col.prop(self,"length", text="Length")
		col.prop(self,"width", text="Width")
		col.prop(self,"thickness", text="Thickness")
		col = layout.column(align=True)
		col.prop(self,"corner", text="Sync Corner Fillets")
		col = layout.column(align=True)
		col.prop(self,"chamfer1", text="Corner Radius1")
		if not self.corner:
			col.prop(self,"chamfer2", text="Corner Radius2")
		col.prop(self,"chamfer3", text="Edge Radius")

	elif self.profilo_mode == 'Bar':
		col.prop(self,"length", text="Length")
		col.prop(self,"width", text="Width")
		col.prop(self,"chamfer1", text="Corner Radius")

	elif self.profilo_mode == 'Channel':
		col.prop(self,"length", text="Length")
		col.prop(self,"width", text="width")
		col.prop(self,"thickness", text="Thickness")
		col = layout.column(align=True)
		col.prop(self,"corner", text="Sync Corner Fillets")
		col = layout.column(align=True)
		col.prop(self,"chamfer1", text="Corner Radius1")
		if not self.corner:
			col.prop(self,"chamfer2", text="Corner Radius2")

	elif self.profilo_mode == 'Cylinder':
		col.prop(self,"radius1", text="Radius")
		col.prop(self,"slicefrom", text="Slice From")
		col.prop(self,"sliceto", text="Slice To")

	elif self.profilo_mode == 'Pipe':
		col.prop(self,"radius1", text="Radius")
		col.prop(self,"thickness", text="Thickness")

	elif self.profilo_mode == 'Tee':
		col.prop(self,"length", text="Length")
		col.prop(self,"width", text="Width")
		col.prop(self,"thickness", text="Thickness")
		col = layout.column(align=True)
		col.prop(self,"chamfer1", text="Corner Radius")

	elif self.profilo_mode == 'Tube':
		col.prop(self,"length", text="Length")
		col.prop(self,"width", text="Width")
		col.prop(self,"thickness", text="Thickness")
		col = layout.column(align=True)
		col.prop(self,"corner", text="Sync Corner Fillets")
		col.prop(self,"chamfer1", text="Corner Radius1")
		if not self.corner:
			col.prop(self,"chamfer2", text="Corner Radius2")

	elif self.profilo_mode == 'Width_flange':
		col.prop(self,"length", text="Length")
		col.prop(self,"width", text="Width")
		col.prop(self,"thickness", text="Thickness")
		col.prop(self,"chamfer1", text="Corner Radius")

	elif self.profilo_mode == 'Elipse':
		col.prop(self,"length", text="Length")
		col.prop(self,"width", text="Width")
		col = layout.column(align=True)
		col.prop(self,"outline", text="Outline")
		if self.outline:
			col = layout.column(align=True)
			col.prop(self,"thickness", text="Thickness")

	# Transform
	col = layout.column(align=True)
	row = col.row(align = True)
	row.prop(self,"offset_x", text="Offset X")
	row.prop(self,"offset_y", text="Offset Y")
	row = col.row(align = True)
	row.prop(self,"mirror_x", text="Mirror X")
	row.prop(self,"mirror_y", text="Mirror Y")
	col = layout.column(align=True)
	col.prop(self,"rotation", text="Angle")
	
	# Pivot offset
	col = layout.column(align=True)
	row = col.row(align = True)
	row.operator("create.set_profilo_pivotaligne",
				text="",icon="BLANK1").pivotaligne = 1

	row.operator("create.set_profilo_pivotaligne",
				text="",icon="TRIA_UP").pivotaligne = 2

	row.operator("create.set_profilo_pivotaligne",
				text="",icon="BLANK1").pivotaligne = 3

	row = col.row(align = True)
	row.operator("create.set_profilo_pivotaligne",
				text="",icon="TRIA_LEFT").pivotaligne = 4

	row.operator("create.set_profilo_pivotaligne",
				text="",icon='DOT').pivotaligne = 5

	row.operator("create.set_profilo_pivotaligne",
				text="",icon="TRIA_RIGHT").pivotaligne = 6

	row = col.row(align = True)
	row.operator("create.set_profilo_pivotaligne",
				text="",icon="BLANK1").pivotaligne = 7

	row.operator("create.set_profilo_pivotaligne",
				text="",icon="TRIA_DOWN").pivotaligne = 8

	row.operator("create.set_profilo_pivotaligne",
				text="",icon="BLANK1").pivotaligne = 9



def get_compass_panel(self, layout):
	layout.label(text="Compass",icon='LIGHT_SUN')
	col = layout.column(align=True)
	col.prop(self,"radius1", text="Icon Size")



def get_panel(self, layout):
	if self.classname == "Adaptive_Plane":
		get_adaptive_plane_panel(self, layout)

	elif self.classname == "Plane":
		get_plane_panel(self, layout)

	elif self.classname == "Box":
		get_box_panel(self, layout)

	elif self.classname == "Cone":
		get_cone_panel(self, layout)

	elif self.classname == "Sphere":
		get_sphere_panel(self, layout)

	elif self.classname == "Icosphere":
		get_icosphere_panel(self, layout)

	elif self.classname == "Capsule":
		get_capsule_panel(self, layout)

	elif self.classname == "OilTank":
		get_oiltank_panel(self, layout)

	elif self.classname == "Cylinder":
		get_cylinder_panel(self, layout)

	elif self.classname == "Teapot":
		get_teapot_panel(self, layout)

	elif self.classname == "Tube":
		get_tube_panel(self, layout)

	elif self.classname == "Torus":
		get_torus_panel(self, layout)

	elif self.classname == "Pyramid":
		get_pyramid_panel(self, layout)

	elif self.classname == "Monkey":
		get_monkey_panel(self, layout)

	elif self.classname == "Rectangle":
		get_rectangle_panel(self, layout)

	elif self.classname == "Circle":
		get_circle_panel(self, layout)

	elif self.classname == "Ellipse":
		get_ellipse_panel(self, layout)

	elif self.classname == "Extrude_Curve":
		get_curve_extrude_panel(self, layout)

	elif self.classname == "Extrude_Mesh":
		get_mesh_extrude_panel(self, layout)

	elif self.classname == "Arc":
		get_arc_panel(self, layout)

	elif self.classname == "Donut":
		get_donut_panel(self, layout)

	elif self.classname == "NGon":
		get_ngon_panel(self, layout)

	elif self.classname == "Star":
		get_star_panel(self, layout)

	elif self.classname == "Helix":
		get_helix_panel(self, layout)

	elif self.classname == "Profilo":
		get_profilo_panel(self, layout)

	elif self.classname == "Compass":
		get_compass_panel(self, layout)

	col = layout.column(align=True)
	col.prop(self,"animatable", text="Animatable")



class Primitive_PT_Panel(Panel):
	bl_label = "Parameters"
	bl_idname = "DATA_PT_Primitives"
	bl_space_type = 'PROPERTIES'
	bl_region_type = 'WINDOW'
	bl_context = "data"

	@classmethod
	def poll(cls,ctx):
		if ctx.object.type in ['MESH','CURVE']:
			if ctx.object.data.primitivedata.classname != "":
				return True
		return False

	def draw(this,ctx):
		layout = this.layout
		self = ctx.object.data.primitivedata
		get_panel(self, layout)
		col = layout.column(align=True)
		col.operator("primitive.cleardata", text="Convert to Ragular Object")



class Primitive_OT_Edit(Operator):
	bl_idname = "primitive.edit"
	bl_label = "Edit Primitive"
	bl_options = {"UNDO"}

	@classmethod
	def poll(self,ctx):
		if ctx.active_object != None:
			if ctx.active_object.type in {'MESH','CURVE'}:
				if ctx.active_object.data.primitivedata != "":
					return True
		return False

	def draw(this,ctx):
		self = ctx.active_object.data.primitivedata
		get_panel(self,this.layout)

	def execute(self,ctx):
		return {'FINISHED'}

	def invoke(self,ctx,event):
		wm = ctx.window_manager
		return wm.invoke_props_dialog(self,width=200)



class BsMax_OT_Set_Object_Mode(Operator):
	bl_idname="bsmax.mode_set"
	bl_label="Set Object Mode"

	@classmethod
	def poll(self, ctx):
		return ctx.active_object != None

	def execute(self, ctx):
		classname = ""
		if ctx.active_object.type in {'MESH', 'CURVE'}:
			classname = ctx.active_object.data.primitivedata.classname

		if classname != "":
			bpy.ops.primitive.edit('INVOKE_DEFAULT')
		else:
			if ctx.active_object.type == 'GPENCIL':
				bpy.ops.gpencil.editmode_toggle()

			elif ctx.active_object.type in {'MESH','CURVE','SURFACE',
											'META','FONT','ARMATURE',
											'LATTICE'}:
				# igone the edit mode for proxy and libraryoverirde #
				# TODO need to a method to check linked or not rather than use try #
				try:
					bpy.ops.object.editmode_toggle()
				except:
					pass
			# ignor this types {'EMPTY','LIGHT','LIGHT_PROBE','CAMERA','SPEAKER',}
		return {"FINISHED"}



classes = [
	Primitive_PT_Panel,
	Primitive_OT_Edit,
	BsMax_OT_Set_Object_Mode
]

def register_panel():
	for c in classes:
		bpy.utils.register_class(c)

def unregister_panel():
	for c in classes:
		bpy.utils.unregister_class(c)