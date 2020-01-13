import bpy
from bpy.types import Menu
from bsmax.state import is_object_mode

# Mesh create menu
class BsMax_MT_VertexCreate(Menu):
	bl_idname = "BSMAX_MT_vertexcreatemenu"
	bl_label = "Vertex"
	def draw(self,ctx):
		layout=self.layout
		layout.operator("bsmax.createvertex",text="Vertex",icon="DOT").fill_type='NONE'
		layout.operator("bsmax.createvertex",text="Vertexs",icon="STICKY_UVS_DISABLE").fill_type='VERT'
		layout.operator("bsmax.createvertex",text="Edge",icon="CON_TRACKTO").fill_type='EDGE'
		layout.operator("bsmax.createvertex",text="Face",icon="LIGHTPROBE_PLANAR").fill_type='FACE'

# Mesh create menu
class BsMax_MT_MeshCreate(Menu):
	bl_idname = "BSMAX_MT_meshcreatemenu"
	bl_label = "Mesh"
	def draw(self,ctx):
		layout=self.layout
		layout.operator("bsmax.createplane",text="Plane",icon="MESH_PLANE")
		layout.operator("bsmax.createbox",text="Box",icon="MESH_CUBE")
		layout.operator("bsmax.createcone",text="Cone",icon="MESH_CONE")
		layout.operator("bsmax.createsphere",text="Sphere",icon="MESH_UVSPHERE")
		#layout.operator("bsmax.creategeosphere",icon="MESH_ICOSPHERE")
		layout.operator("bsmax.createuicosphere",text="IcoSphere",icon="MESH_ICOSPHERE")
		layout.operator("bsmax.createcapsule",text="Capsule",icon="META_CAPSULE")
		layout.operator("bsmax.createoiltank",text="OilTank",icon="META_CAPSULE")
		layout.operator("bsmax.createcylinder",text="Cylinder",icon="MESH_CYLINDER")
		layout.operator("bsmax.createtube",text="Tube",icon="MESH_TORUS")
		layout.operator("bsmax.createtorus",text="Torus",icon="MESH_TORUS")
		layout.operator("bsmax.createpyramid",text="Pyramid",icon="MARKER")
		layout.operator("bsmax.createteapot",text="Teapot",icon="NODE_MATERIAL")
		layout.operator("bsmax.createmonkey",text="Monkey",icon="MESH_MONKEY")
		layout.separator()
		layout.menu("BSMAX_MT_vertexcreatemenu",icon='DOT')
		#layout.separator()
		#layout.operator("bsmax.createmesher",text="Mesher",icon="META_CUBE")
		
# curve / shape / spline create menu
class BsMax_MT_CurveCreate(Menu):
	bl_idname = "BSMAX_MT_curvecreatemenu"
	bl_label = "Curve"
	def draw(self,ctx):
		layout = self.layout
		layout.operator("bsmax.createline",text="Line",icon="CURVE_PATH")
		layout.operator("bsmax.createrectangle",text="Rectangle",icon="META_PLANE")
		layout.operator("bsmax.createcircle",text="Circle",icon="MESH_CIRCLE")
		layout.operator("bsmax.createellipse",text="Ellipse",icon="MESH_CAPSULE")
		layout.operator("bsmax.createarc",text="Arc",icon="SPHERECURVE")
		layout.operator("bsmax.createdonut",text="Donut",icon="MESH_CIRCLE")
		layout.operator("bsmax.createngon",text="Ngon",icon="SEQ_CHROMA_SCOPE")
		layout.operator("bsmax.createstar",text="Start",icon="SOLO_OFF")
		layout.operator("bsmax.createhelix",text="Helix",icon="FORCE_VORTEX")
		layout.operator("bsmax.createprofilo",text="Profilo",icon="MOD_BOOLEAN")

# Surface create menu
class BsMax_MT_SurfaceCreate(Menu):
	bl_idname = "BSMAX_MT_surfacecreatemenu"
	bl_label = "Surface"
	def draw(self,ctx):
		layout = self.layout
		layout.label(text="coming soon")

# Metaball create menu
class BsMax_MT_MetaballCreate(Menu):
	bl_idname = "BSMAX_MT_metaballcreatemenu"
	bl_label = "Metaball"
	def draw(self,ctx):
		layout = self.layout
		layout.operator("bsmax.createmetaball",text="Ball",
						icon="META_BALL").metaball_type='BALL'
		layout.operator("bsmax.createmetaball",text="Capcule",
						icon="META_CAPSULE").metaball_type='CAPSULE'
		layout.operator("bsmax.createmetaball",text="Plane",
						icon="META_PLANE").metaball_type='PLANE'
		layout.operator("bsmax.createmetaball",text="Ellipsoid",
						icon="META_ELLIPSOID").metaball_type='ELLIPSOID'
		layout.operator("bsmax.createmetaball",text="Cube",
						icon="META_CUBE").metaball_type='CUBE'

# Text create menu
class BsMax_MT_TextCreate(Menu):
	bl_idname = "BSMAX_MT_textcreatemenu"
	bl_label = "Text"
	def draw(self,ctx):
		layout = self.layout
		layout.operator("bsmax.createtext",text="Text",
			icon="OUTLINER_OB_FONT").fill_mode='BOTH'
		layout.operator("bsmax.createtext",text="Text",
			icon="FONT_DATA").fill_mode="NONE"

# Greace Pencil create menu
class BsMax_MT_GreacePencilCreate(Menu):
	bl_idname = "BSMAX_MT_gracepencilcreatemenu"
	bl_label = "Greace Pencil"
	def draw(self,ctx):
		layout = self.layout
		layout.operator("bsmax.creategreacepencil",text="Blank",
				icon="EMPTY_AXIS").gpencil_type="EMPTY"
		layout.operator("bsmax.creategreacepencil",text="Stroke",
				icon="OUTLINER_OB_GREASEPENCIL").gpencil_type='STROKE'
		layout.operator("bsmax.creategreacepencil",text="Monkey",
				icon="MESH_MONKEY").gpencil_type="MONKEY"

# Armature create menu
class BsMax_MT_ArmatureCreate(Menu):
	bl_idname = "BSMAX_MT_armaturecreatemenu"
	bl_label = "Armature"
	def draw(self,ctx):
		layout = self.layout
		layout.operator("bsmax.createbone",text="Bone",icon="BONE_DATA")
		#layout.operator("bsmax.createbone",text="Armature",icon="ARMATURE_DATA")

# Lattice create menu
class BsMax_MT_LatticeCreate(Menu):
	bl_idname = "BSMAX_MT_latticecreatemenu"
	bl_label = "Lattice"
	def draw(self,ctx):
		layout = self.layout
		layout.operator("bsmax.createlattice",text='Lattice 2x2x2 (Create)',
						icon="OUTLINER_OB_LATTICE").resolution=2
		layout.operator("bsmax.createlattice",text='Lattice 3x3x3 (Create)',
						icon="OUTLINER_OB_LATTICE").resolution=3
		layout.operator("bsmax.createlattice",text='Lattice 4x4x4 (Create)',
						icon="OUTLINER_OB_LATTICE").resolution=4

# Empty create menu
class BsMax_MT_EmptyCreate(Menu):
	bl_idname = "BSMAX_MT_emptycreatemenu"
	bl_label = "Empty"
	def draw(self,ctx):
		layout = self.layout
		layout.operator("bsmax.createempty",text="Plane Axis",
						icon="EMPTY_AXIS").empty_type='PLAIN_AXES'
		layout.operator("bsmax.createempty",text="Arrows",
						icon="EMPTY_ARROWS").empty_type='ARROWS'
		layout.operator("bsmax.createempty",text="Single Arrows",
						icon="EMPTY_SINGLE_ARROW").empty_type='SINGLE_ARROW'
		layout.operator("bsmax.createempty",text="Circle",
						icon="MESH_CIRCLE").empty_type='CIRCLE'
		layout.operator("bsmax.createempty",text="Cube",
						icon="CUBE").empty_type='CUBE'
		layout.operator("bsmax.createempty",text="Sphere",
						icon="SPHERE").empty_type='SPHERE'
		layout.operator("bsmax.createempty",text="Cone",
						icon="CONE").empty_type='CONE'
		layout.operator("bsmax.createempty",text="Image",
						icon="FILE_IMAGE").empty_type='IMAGE'

# Image create menu
class BsMax_MT_ImageCreate(Menu):
	bl_idname = "BSMAX_MT_imagecreatemenu"
	bl_label = "Image"
	def draw(self,ctx):
		layout = self.layout
		layout.operator("bsmax.createimage",text="Refrence",
						icon="IMAGE_REFERENCE").image_type='REFERENCE'
		layout.operator("bsmax.createimage",text="BackGround",
						icon="IMAGE_BACKGROUND").image_type='BACKGROUND'

# Light create menu
class BsMax_MT_LightCreate(Menu):
	bl_idname = "BSMAX_MT_lightcreatemenu"
	bl_label = "Light"
	def draw(self,ctx):
		layout = self.layout
		layout.operator("bsmax.createpointlight",text="Point",icon="LIGHT_POINT")
		layout.operator("bsmax.creatsunlight",text="Sun",icon="LIGHT_SUN")
		layout.operator("bsmax.createspotlight",text="Spot Light Free/Target",icon="LIGHT_SPOT")
		layout.operator("bsmax.createarealight",text="Free Area",icon="LIGHT_AREA").free = True
		layout.operator("bsmax.createarealight",text="Target Area",icon="LIGHT_AREA")

# Light Probs create menu
class BsMax_MT_LightProbsCreate(Menu):
	bl_idname = "BSMAX_MT_lightProbsprimitives"
	bl_label = "Light Probe"
	def draw(self,ctx):
		layout = self.layout
		layout.operator("bsmax.createlightprobecubemap",
			text="Reflection Cubemap",icon="LIGHTPROBE_CUBEMAP")
		layout.operator("bsmax.createlightprobeplaner",
			text="Reflection Plane",icon="LIGHTPROBE_PLANAR")
		layout.operator("bsmax.createlightprobegrid",
			text="Irradiance Volume",icon="LIGHTPROBE_GRID")

# Camera create menu
class BsMax_MT_CameraCreate(Menu):
	bl_idname = "BSMAX_MT_cameracreatemenu"
	bl_label = "Camera"
	def draw(self,ctx):
		layout = self.layout
		layout.operator("bsmax.createcamera",text="Camera Free/Target",icon="OUTLINER_OB_CAMERA")
		layout.operator("bsmax.createcamerafromview",icon="OUTLINER_OB_CAMERA")

# Speaker create menu
class BsMax_MT_SpeakerCreate(Menu):
	bl_idname = "BSMAX_MT_speakercreatemenu"
	bl_label = "Speaker"
	def draw(self,ctx):
		layout = self.layout
		layout.operator("bsmax.createspeaker",text="Speaker",icon="OUTLINER_OB_SPEAKER")

# Force field create menu
class BsMax_MT_ForceFieldCreate(Menu):
	bl_idname = "BSMAX_MT_forcefieldcecreatemenu"
	bl_label = "Force field"
	def draw(self,ctx):
		layout = self.layout
		layout.operator("bsmax.createeffector",text="Force",
			icon="FORCE_FORCE").effector_type = 'FORCE'
		layout.operator("bsmax.createeffector",	text="Wind",
			icon="FORCE_WIND").effector_type = 'WIND'
		layout.operator("bsmax.createeffector",text="Vortex",
			icon="FORCE_VORTEX").effector_type = 'VORTEX'
		layout.operator("bsmax.createeffector",	text="Magnet",
			icon="FORCE_MAGNETIC").effector_type = 'MAGNET'
		layout.operator("bsmax.createeffector",	text="Harmonic",
			icon="FORCE_HARMONIC").effector_type = 'HARMONIC'
		layout.operator("bsmax.createeffector",	text="Charge",
			icon="FORCE_CHARGE").effector_type = 'CHARGE'
		layout.operator("bsmax.createeffector",text="Lennardj",
			icon="FORCE_LENNARDJONES").effector_type = 'LENNARDJ'
		layout.operator("bsmax.createeffector",	text="Texture",
			icon="FORCE_TEXTURE").effector_type = 'TEXTURE'
		layout.operator("bsmax.createeffector",text="Guide",
			icon="FORCE_CURVE").effector_type = 'GUIDE'
		layout.operator("bsmax.createeffector",text="Boid",
			icon="FORCE_BOID").effector_type = 'BOID'
		layout.operator("bsmax.createeffector",text="Turbulence",
			icon="FORCE_TURBULENCE").effector_type = 'TURBULENCE'
		layout.operator("bsmax.createeffector",text="Drag",
			icon="FORCE_DRAG").effector_type = 'DRAG'
		layout.operator("bsmax.createeffector",	text="Smoke",
			icon="FORCE_SMOKEFLOW").effector_type = 'SMOKE'

# View 3D Create Menu
class BsMax_MT_Create(Menu):
	bl_idname = "BSMAX_MT_createmenu"
	bl_label = "Create"
	bl_context = "objectmode"

	@classmethod
	def poll(self,ctx):
		return is_object_mode(ctx)

	def draw(self,ctx):
		layout = self.layout
		layout.menu("BSMAX_MT_meshcreatemenu",icon='OUTLINER_OB_MESH')
		layout.menu("BSMAX_MT_curvecreatemenu",icon='OUTLINER_OB_CURVE')
		layout.menu("BSMAX_MT_surfacecreatemenu",icon='OUTLINER_OB_SURFACE')
		layout.menu("BSMAX_MT_metaballcreatemenu",icon='OUTLINER_OB_META')
		layout.menu("BSMAX_MT_textcreatemenu",icon='OUTLINER_OB_FONT')
		layout.menu("BSMAX_MT_gracepencilcreatemenu",icon='OUTLINER_OB_GREASEPENCIL')
		layout.separator()
		layout.menu("BSMAX_MT_armaturecreatemenu",icon='OUTLINER_OB_ARMATURE')
		layout.menu("BSMAX_MT_latticecreatemenu",icon='OUTLINER_OB_LATTICE')
		layout.separator()
		layout.menu("BSMAX_MT_emptycreatemenu",icon='OUTLINER_OB_EMPTY')
		layout.menu("BSMAX_MT_imagecreatemenu",icon='OUTLINER_OB_IMAGE')
		layout.separator()
		layout.menu("BSMAX_MT_lightcreatemenu",icon='OUTLINER_OB_LIGHT')
		layout.menu("BSMAX_MT_lightProbsprimitives",icon='OUTLINER_OB_LIGHTPROBE')
		layout.separator()
		layout.menu("BSMAX_MT_cameracreatemenu",icon='OUTLINER_OB_CAMERA')
		layout.separator()
		#layout.menu("BSMAX_MT_speakercreatemenu",icon='OUTLINER_OB_SPEAKER')
		layout.operator("bsmax.createspeaker",icon="OUTLINER_OB_SPEAKER")
		layout.separator()
		layout.menu("BSMAX_MT_forcefieldcecreatemenu",icon='OUTLINER_OB_FORCE_FIELD')
		# OUTLINER_OB_GROUP_INSTANCE

def CreateMenu_CallBack(self,ctx):
	self.layout.menu("BSMAX_MT_createmenu")

def Prepend_Create_Menu():
	bpy.types.VIEW3D_MT_editor_menus.prepend(CreateMenu_CallBack)

def Remove_Create_Menu():
	bpy.types.VIEW3D_MT_editor_menus.remove(CreateMenu_CallBack)  

def menu_cls(register):
	classes = [BsMax_MT_VertexCreate,
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

	if register:
		[bpy.utils.register_class(c) for c in classes]
		Prepend_Create_Menu()
	else:
		[bpy.utils.unregister_class(c) for c in classes]
		Remove_Create_Menu()

if __name__ == '__main__':
	menu_cls(True)

__all__ = ["menu_cls"]