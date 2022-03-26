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
from bpy.types import Menu
from bsmax.state import is_object_mode



# Mesh create menu
class BsMax_MT_VertexCreate(Menu):
	bl_idname = "BSMAX_MT_vertex_create_menu"
	bl_label = "Vertex"
	def draw(self, ctx):
		layout=self.layout
		layout.operator("create.vertex", text="Vertex", icon="DOT").fill_type='NONE'
		layout.operator("create.vertex", text="Vertexs", icon="STICKY_UVS_DISABLE").fill_type='VERT'
		layout.operator("create.vertex", text="Edge", icon="CON_TRACKTO").fill_type='EDGE'
		layout.operator("create.vertex", text="Face", icon="LIGHTPROBE_PLANAR").fill_type='FACE'



# Mesh create menu
class BsMax_MT_Mesh_Extera(Menu):
	bl_idname = "BSMAX_MT_mesh_extera_menu"
	bl_label = "Mesh Extera"
	def draw(self, ctx):
		layout=self.layout
		layout.operator("mesh.add_spider_web", text="Spider Web", icon="FREEZE")
		layout.operator("mesh.make_pillow", text="Pillow", icon="GHOST_ENABLED")
		


# Mesh create menu
class BsMax_MT_MeshCreate(Menu):
	bl_idname = "BSMAX_MT_mesh_create_menu"
	bl_label = "Mesh"
	def draw(self, ctx):
		layout=self.layout
		layout.operator("create.plane", text="Plane", icon="MESH_PLANE")
		layout.operator("create.box", text="Box", icon="MESH_CUBE")
		layout.operator("create.cone", text="Cone", icon="MESH_CONE")
		layout.operator("create.sphere", text="Sphere", icon="MESH_UVSPHERE")
		#layout.operator("bsmax.creategeosphere", icon="MESH_ICOSPHERE")
		layout.operator("create.uicosphere", text="IcoSphere", icon="MESH_ICOSPHERE")
		layout.operator("create.capsule", text="Capsule", icon="META_CAPSULE")
		layout.operator("create.oiltank", text="OilTank", icon="META_CAPSULE")
		layout.operator("create.cylinder", text="Cylinder", icon="MESH_CYLINDER")
		layout.operator("create.tube", text="Tube", icon="MESH_TORUS")
		layout.operator("create.torus", text="Torus", icon="MESH_TORUS")
		layout.operator("create.pyramid", text="Pyramid", icon="MARKER")
		layout.operator("create.teapot", text="Teapot", icon="NODE_MATERIAL")
		layout.operator("create.monkey", text="Monkey", icon="MESH_MONKEY")
		layout.separator()
		layout.menu("BSMAX_MT_vertex_create_menu", icon='DOT')
		layout.separator()
		#layout.operator("create.mesher", text="Mesher", icon="META_CUBE")
		layout.operator("create.extrude", text="Extrude Mesh (Add)", icon="EXPORT").mode='Mesh'
		layout.separator()
		layout.menu("BSMAX_MT_mesh_extera_menu", icon='DOCUMENTS')



# curve / shape / spline create menu
class BsMax_MT_CurveCreate(Menu):
	bl_idname = "BSMAX_MT_curve_create_menu"
	bl_label = "Curve"
	def draw(self, ctx):
		layout = self.layout
		layout.operator("create.line", text="Line", icon="CURVE_PATH")
		layout.operator("create.rectangle", text="Rectangle", icon="META_PLANE")
		layout.operator("create.circle", text="Circle", icon="MESH_CIRCLE")
		layout.operator("create.ellipse", text="Ellipse", icon="MESH_CAPSULE")
		layout.operator("create.arc", text="Arc", icon="SPHERECURVE")
		layout.operator("create.donut", text="Donut", icon="MESH_CIRCLE")
		layout.operator("create.ngon", text="Ngon", icon="SEQ_CHROMA_SCOPE")
		layout.operator("create.star", text="Start", icon="SOLO_OFF")
		layout.operator("create.helix", text="Helix", icon="FORCE_VORTEX")
		layout.operator("create.profilo", text="Profilo", icon="MOD_BOOLEAN")
		layout.separator()
		layout.operator("create.extrude",text="Extrude Curve (Add)",icon="EXPORT").mode='Curve'



# Surface create menu
class BsMax_MT_SurfaceCreate(Menu):
	bl_idname = "BSMAX_MT_surface_create_menu"
	bl_label = "Surface"
	def draw(self, ctx):
		layout = self.layout
		layout.label(text="coming soon")



# Metaball create menu
class BsMax_MT_MetaballCreate(Menu):
	bl_idname = "BSMAX_MT_metaball_create_menu"
	bl_label = "Metaball"
	def draw(self, ctx):
		layout = self.layout
		layout.operator("create.metaball", text="Ball",
						icon="META_BALL").metaball_type='BALL'
		layout.operator("create.metaball", text="Capcule",
						icon="META_CAPSULE").metaball_type='CAPSULE'
		layout.operator("create.metaball", text="Plane",
						icon="META_PLANE").metaball_type='PLANE'
		layout.operator("create.metaball", text="Ellipsoid",
						icon="META_ELLIPSOID").metaball_type='ELLIPSOID'
		layout.operator("create.metaball", text="Cube",
						icon="META_CUBE").metaball_type='CUBE'



# Text create menu
class BsMax_MT_TextCreate(Menu):
	bl_idname = "BSMAX_MT_text_create_menu"
	bl_label = "Text"
	def draw(self, ctx):
		layout = self.layout
		layout.operator("create.text", text="Text",
			icon="OUTLINER_OB_FONT").fill_mode='BOTH'
		layout.operator("create.text", text="Text",
			icon="FONT_DATA").fill_mode="NONE"



# Greace Pencil create menu
class BsMax_MT_GreacePencilCreate(Menu):
	bl_idname = "BSMAX_MT_gracepencil_create_menu"
	bl_label = "Greace Pencil"
	def draw(self, ctx):
		layout = self.layout
		layout.operator("create.greacepencil", text="Blank",
				icon="EMPTY_AXIS").gpencil_type="EMPTY"
		layout.operator("create.greacepencil", text="Stroke",
				icon="OUTLINER_OB_GREASEPENCIL").gpencil_type='STROKE'
		layout.operator("create.greacepencil", text="Monkey",
				icon="MESH_MONKEY").gpencil_type="MONKEY"



# Armature create menu
class BsMax_MT_ArmatureCreate(Menu):
	bl_idname = "BSMAX_MT_armature_create_menu"
	bl_label = "Armature"
	def draw(self, ctx):
		layout = self.layout
		layout.operator("create.bone", text="Bone", icon="BONE_DATA")
		#layout.operator("create.bone",text="Armature",icon="ARMATURE_DATA")



# Lattice create menu
class BsMax_MT_LatticeCreate(Menu):
	bl_idname = "BSMAX_MT_lattice_create_menu"
	bl_label = "Lattice"
	def draw(self, ctx):
		layout = self.layout
		layout.operator("create.lattice", text='Lattice 2x2x2 (Create)',
						icon="OUTLINER_OB_LATTICE").resolution=2
		layout.operator("create.lattice", text='Lattice 3x3x3 (Create)',
						icon="OUTLINER_OB_LATTICE").resolution=3
		layout.operator("create.lattice", text='Lattice 4x4x4 (Create)',
						icon="OUTLINER_OB_LATTICE").resolution=4



# Empty create menu
class BsMax_MT_EmptyCreate(Menu):
	bl_idname = "BSMAX_MT_empty_create_menu"
	bl_label = "Empty"
	def draw(self, ctx):
		layout = self.layout
		layout.operator("create.empty", text="Plane Axis",
						icon="EMPTY_AXIS").empty_type='PLAIN_AXES'
		layout.operator("create.empty", text="Arrows",
						icon="EMPTY_ARROWS").empty_type='ARROWS'
		layout.operator("create.empty", text="Single Arrows",
						icon="EMPTY_SINGLE_ARROW").empty_type='SINGLE_ARROW'
		layout.operator("create.empty", text="Circle",
						icon="MESH_CIRCLE").empty_type='CIRCLE'
		layout.operator("create.empty", text="Cube",
						icon="CUBE").empty_type='CUBE'
		layout.operator("create.empty", text="Sphere",
						icon="SPHERE").empty_type='SPHERE'
		layout.operator("create.empty", text="Cone",
						icon="CONE").empty_type='CONE'
		layout.operator("create.empty", text="Image",
						icon="FILE_IMAGE").empty_type='IMAGE'



# Image create menu
class BsMax_MT_ImageCreate(Menu):
	bl_idname = "BSMAX_MT_image_create_menu"
	bl_label = "Image"
	def draw(self, ctx):
		layout = self.layout
		layout.operator("create.image", text="Refrence",
						icon="IMAGE_REFERENCE").image_type='REFERENCE'
		layout.operator("create.image", text="BackGround",
						icon="IMAGE_BACKGROUND").image_type='BACKGROUND'



# Light create menu
class BsMax_MT_LightCreate(Menu):
	bl_idname = "BSMAX_MT_light_create_menu"
	bl_label = "Light"
	def draw(self,  ctx):
		layout = self.layout
		layout.operator("create.pointlight", text="Point", icon="LIGHT_POINT")
		layout.operator("create.sunlight", text="Sun", icon="LIGHT_SUN")
		layout.operator("create.spotlight", text="Spot Light Free/Target", icon="LIGHT_SPOT")
		layout.operator("create.arealight",text="Free Area",icon="LIGHT_AREA").free = True
		layout.operator("create.arealight",text="Target Area",icon="LIGHT_AREA")



# Light Probs create menu
class BsMax_MT_LightProbsCreate(Menu):
	bl_idname = "BSMAX_MT_lightProbs_primitives"
	bl_label = "Light Probe"
	def draw(self, ctx):
		layout = self.layout
		layout.operator("create.light_probe_cubemap",
			text="Reflection Cubemap", icon="LIGHTPROBE_CUBEMAP")
		layout.operator("create.light_probe_planer",
			text="Reflection Plane", icon="LIGHTPROBE_PLANAR")
		layout.operator("create.light_probe_grid",
			text="Irradiance Volume", icon="LIGHTPROBE_GRID")



# Camera create menu
class BsMax_MT_CameraCreate(Menu):
	bl_idname = "BSMAX_MT_camera_create_menu"
	bl_label = "Camera"
	def draw(self, ctx):
		layout = self.layout
		layout.operator("create.camera", text="Camera Free/Target", icon="OUTLINER_OB_CAMERA")
		layout.operator("camera.create_from_view", icon="OUTLINER_OB_CAMERA")



# Speaker create menu
class BsMax_MT_SpeakerCreate(Menu):
	bl_idname = "BSMAX_MT_speakercreatemenu"
	bl_label = "Speaker"
	def draw(self, ctx):
		layout = self.layout
		layout.operator("create.speaker", text="Speaker", icon="OUTLINER_OB_SPEAKER")



# Force field create menu
class BsMax_MT_ForceFieldCreate(Menu):
	bl_idname = "BSMAX_MT_forcefield_cecreate_menu"
	bl_label = "Force field"
	def draw(self, ctx):
		layout = self.layout
		layout.operator("create.effector", text="Force",
			icon="FORCE_FORCE").effector_type = 'FORCE'
		layout.operator("create.effector", text="Wind",
			icon="FORCE_WIND").effector_type = 'WIND'
		layout.operator("create.effector", text="Vortex",
			icon="FORCE_VORTEX").effector_type = 'VORTEX'
		layout.operator("create.effector", text="Magnet",
			icon="FORCE_MAGNETIC").effector_type = 'MAGNET'
		layout.operator("create.effector", text="Harmonic",
			icon="FORCE_HARMONIC").effector_type = 'HARMONIC'
		layout.operator("create.effector", text="Charge",
			icon="FORCE_CHARGE").effector_type = 'CHARGE'
		layout.operator("create.effector", text="Lennardj",
			icon="FORCE_LENNARDJONES").effector_type = 'LENNARDJ'
		layout.operator("create.effector", text="Texture",
			icon="FORCE_TEXTURE").effector_type = 'TEXTURE'
		layout.operator("create.effector", text="Guide",
			icon="FORCE_CURVE").effector_type = 'GUIDE'
		layout.operator("create.effector", text="Boid",
			icon="FORCE_BOID").effector_type = 'BOID'
		layout.operator("create.effector", text="Turbulence",
			icon="FORCE_TURBULENCE").effector_type = 'TURBULENCE'
		layout.operator("create.effector", text="Drag",
			icon="FORCE_DRAG").effector_type = 'DRAG'
		layout.operator("create.effector", text="Smoke",
			icon="FORCE_FLUIDFLOW").effector_type = 'SMOKE'



# View 3D Create Menu
class BsMax_MT_Create(Menu):
	bl_idname = "BSMAX_MT_create_menu"
	bl_label = "Create"
	bl_context = "objectmode"

	@classmethod
	def poll(self, ctx):
		return is_object_mode(ctx)

	def draw(self, ctx):
		layout = self.layout
		layout.prop(ctx.scene.primitive_setting, 'draw_mode', text='', icon='VIEW3D')
		layout.separator()
		layout.menu("BSMAX_MT_mesh_create_menu", icon='OUTLINER_OB_MESH')
		layout.menu("BSMAX_MT_curve_create_menu", icon='OUTLINER_OB_CURVE')
		layout.menu("BSMAX_MT_surface_create_menu", icon='OUTLINER_OB_SURFACE')
		layout.menu("BSMAX_MT_metaball_create_menu", icon='OUTLINER_OB_META')
		layout.menu("BSMAX_MT_text_create_menu", icon='OUTLINER_OB_FONT')
		layout.menu("BSMAX_MT_gracepencil_create_menu", icon='OUTLINER_OB_GREASEPENCIL')
		layout.separator()
		layout.menu("BSMAX_MT_armature_create_menu", icon='OUTLINER_OB_ARMATURE')
		layout.menu("BSMAX_MT_lattice_create_menu", icon='OUTLINER_OB_LATTICE')
		layout.separator()
		layout.menu("BSMAX_MT_empty_create_menu", icon='OUTLINER_OB_EMPTY')
		layout.menu("BSMAX_MT_image_create_menu", icon='OUTLINER_OB_IMAGE')
		layout.separator()
		layout.menu("BSMAX_MT_light_create_menu", icon='OUTLINER_OB_LIGHT')
		layout.menu("BSMAX_MT_lightProbs_primitives", icon='OUTLINER_OB_LIGHTPROBE')
		layout.separator()
		layout.menu("BSMAX_MT_camera_create_menu", icon='OUTLINER_OB_CAMERA')
		layout.separator()
		layout.operator("create.speaker", icon="OUTLINER_OB_SPEAKER")
		layout.separator()
		layout.menu("BSMAX_MT_forcefield_cecreate_menu", icon='OUTLINER_OB_FORCE_FIELD')
		# OUTLINER_OB_GROUP_INSTANCE



def objects_context_menu(self, ctx):
	layout = self.layout
	layout.separator()
	layout.operator("primitive.cleardata", text="Convert to Ragular Object")

def CreateMenu_CallBack(self, ctx):
	if ctx.mode == 'OBJECT':
		self.layout.menu("BSMAX_MT_create_menu")

classes = [BsMax_MT_VertexCreate,
	BsMax_MT_Mesh_Extera,
	BsMax_MT_MeshCreate,
	BsMax_MT_CurveCreate,
	BsMax_MT_SurfaceCreate,
	BsMax_MT_MetaballCreate,
	BsMax_MT_TextCreate,
	BsMax_MT_GreacePencilCreate,
	BsMax_MT_ArmatureCreate,
	BsMax_MT_LatticeCreate,
	BsMax_MT_EmptyCreate,
	BsMax_MT_ImageCreate,
	BsMax_MT_LightCreate,
	BsMax_MT_LightProbsCreate,
	BsMax_MT_CameraCreate,
	BsMax_MT_SpeakerCreate,
	BsMax_MT_ForceFieldCreate,
	BsMax_MT_Create]

def register_menu():
	for c in classes:
		bpy.utils.register_class(c)
	#TODO find a way to put Create menu anfter add menu rather than first of the list
	bpy.types.VIEW3D_MT_editor_menus.prepend(CreateMenu_CallBack)
	bpy.types.VIEW3D_MT_object_context_menu.append(objects_context_menu)

def unregister_menu():
	bpy.types.VIEW3D_MT_editor_menus.remove(CreateMenu_CallBack)  
	bpy.types.VIEW3D_MT_object_context_menu.remove(objects_context_menu)
	for c in classes:
		bpy.utils.unregister_class(c)