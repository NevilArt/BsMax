import bpy
from bpy.types import Operator
from bpy.props import *

def getChildren(obj):
	children = []
	for ob in bpy.context.scene.objects:
		if ob.parent == obj:
			children.append(ob)
	return children

class ObjectPropertiesDialog(Operator):
	bl_idname: "bmax.dialog_objectproperties"
	bl_label: "Object Properties"
	# Object information
	Name: StringProperty(name= "Name")
	Dimantion_X: FloatProperty(name= "X")
	Dimantion_Y: FloatProperty(name= "Y")
	Dimantion_Z: FloatProperty(name= "Z")
	Material: StringProperty(name= "Material")
	Layer: StringProperty(name= "Layer")
	Numchildren: IntProperty(name= "Num. Children")
	Parent: StringProperty(name= "Parent")
	Verteces: IntProperty(name= "Vertices")
	Faces: IntProperty(name= "Vertices")
	#interactivity
	Hide: BoolProperty(name= "Hide")
	Freeze: BoolProperty(name= "Freeze")
	#Display Properties
	See_Trough: BoolProperty(name= "See-Through")
	DisplayAsBox: BoolProperty(name= "Display as Box")
	BackFaceCull: BoolProperty(name= "Backface Call")
	EdgeOnly: BoolProperty(name= "Edge Only")
	VertexTick: BoolProperty(name= "Vertex Tick")
	Trajectory: BoolProperty(name= "Trajectory")
	Mothinpath: BoolProperty(name= "Mothin path")
	IgnoreExtents: BoolProperty(name= "Ignore Extents")
	ShowFrozeninGray: BoolProperty(name= "Show Frozen in Gray")
	NeverDegread: BoolProperty(name= "Never Degread")
	VerticesChanelDisplay: BoolProperty(name= "Vertices Chanel Display")
	VertexChanel: EnumProperty(
		name = '', description = 'mode', default = 'VER_COL',
		items = [('VER_COL', 'Vertex Color', ''),
				 ('VER_ILLUM', 'Vertex Illumination', ''),
				 ('VER_ALPHA', 'Vertex Alpha', ''),
				 ('MAP_CHANEL', 'Map Chanel Color', ''),
				 ('SOFTSEL_COL', 'Soft Selection Colore', '')])
	MapChanel: IntProperty(name= "Map Chanel", min= 1, max= 999)
	#Rendering Control
	Visablity: IntProperty(name= "Visablity", min= 0, max= 100)
	Renderable: BoolProperty(name= "Renderable")
	InheritVisablity: BoolProperty(name= "Inherit Visablity")
	VisabletoCamera: BoolProperty(name= "Visable to Camera")
	VisabletoReflectionRefraction: BoolProperty(name= "Visable to Reflection/Refraction")
	ReciveShadow: BoolProperty(name= "Recive Shadow")
	CastShadow: BoolProperty(name= "Cast Shadow")
	ApplyAtmospherics: BoolProperty(name= "Apply Atmospherics")
	RenderOccludedObjects: BoolProperty(name= "Render Occluded Objects")
	ObjectID: IntProperty(name= "Object ID")
	#Motion Blur
	Multiplier: IntProperty(name= "Multiplier")
	Enabled: BoolProperty(name= "Enabled")
	Mode: EnumProperty(name = '', description = 'mode', default = 'NONE',
		items = [('NONE', 'None', ''),('OBJECT', 'Object', ''),('IMAGE', 'Image', '')])

	def draw(self, ctx):
		layout = self.layout
		# Object information
		box = layout.box()
		box.label("Object Information")
		box.prop(self, "Name")
		row = box.row()
		row.prop(self, "Material")
		row.prop(self, "Layer")
		row = box.row()
		row.prop(self, "Parent")
		row.prop(self, "Numchildren")
		row = box.row(align=True)
		row.label("Dimantion")
		row.prop(self, "Dimantion_X")
		row.prop(self, "Dimantion_Y")
		row.prop(self, "Dimantion_Z")
		row = box.row()
		row.prop(self, "Verteces")
		row.prop(self, "Faces")
		#---------------------------            
		row = layout.row()
		col = row.column()
		box = col.box()
		box.label("interactivity")
		box.prop(self, "Hide")
		box.prop(self, "Freeze")
		#---------------------------
		box = col.box()
		box.label("Display Properties")
		box.prop(self, "See_Trough")
		box.prop(self, "DisplayAsBox")
		box.prop(self, "BackFaceCull")
		box.prop(self, "EdgeOnly")
		box.prop(self, "VertexTick")
		box.prop(self, "Trajectory")
		box.prop(self, "IgnoreExtents")
		box.prop(self, "ShowFrozeninGray")
		box.prop(self, "NeverDegread")
		box.prop(self, "VerticesChanelDisplay")
		box.prop(self, "VertexChanel")
		box.prop(self, "MapChanel")
		#---------------------------
		col = row.column()
		box = col.box()
		box.label("Rendering Control")
		box.prop(self, "Visablity")
		box.prop(self, "Renderable")
		box.prop(self, "InheritVisablity")
		box.prop(self, "VisabletoCamera")
		box.prop(self, "VisabletoReflectionRefraction")
		box.prop(self, "ReciveShadow")
		box.prop(self, "CastShadow")
		box.prop(self, "ApplyAtmospherics")
		box.prop(self, "RenderOccludedObjects")
		#---------------------------
		box = col.box()
		box.label("G-Buffer")
		box.prop(self, "ObjectID")
		#---------------------------
		box = col.box()
		box.label("Motion Blur")
		box.prop(self, "Multiplier")
		box.prop(self, "Enabled")
		box.prop(self, "Mode")
		#---------------------------
		if len(ctx.selected_objects) > 0:
			#################################################################################
			obj = ctx.selected_objects[0]
			self.Name = obj.name
			self.Dimantion_X = obj.dimensions[0]
			self.Dimantion_Y = obj.dimensions[1]
			self.Dimantion_Z = obj.dimensions[2]
			if (obj.active_material == None): self.Material = "Undefined"
			else: self.Material = obj.active_material.name
			self.Layer = "undefined"
			self.Numchildren = len(getChildren(obj))
			if (obj.parent == None): self.Parent = "Scene Root"
			else: self.Parent = obj.parent.name
			#TODO
			# Some object do not have this data Create a function for this
			self.Verteces = len(obj.data.vertices)
			self.Faces = len(obj.data.polygons)
			#interactivity
			#self.Hide = obj.hide_viewport
				#.hide_render = True
			#self.Freeze = obj.hide_select
			#Display Properties
			self.See_Trough = obj.show_x_ray
			if (obj.draw_type == 'BOUNDS'): self.DisplayAsBox = True
			else: self.DisplayAsBox = False
			#self.BackFaceCull = bpy.context.space_data.show_backface_culling
			self.EdgeOnly = obj.show_all_edges
			self.VertexTick = False
			self.Trajectory = False
			self.Mothinpath = False
			self.IgnoreExtents = False
			self.ShowFrozeninGray = True
			self.NeverDegread = False
			self.VerticesChanelDisplay = False
			self.VertexChanel = 'VER_COL' 
			self.MapChanel = 1
			#Rendering Control
			self.Visablity = 100
			self.Renderable = True
			self.InheritVisablity = True
			self.VisabletoCamera = True
			self.VisabletoReflectionRefraction = True
			self.ReciveShadow = True
			self.CastShadow = True
			self.ApplyAtmospherics = True
			self.RenderOccludedObjects = True
			#self.ObjectID = obj.pass_index
			#Motion Blur
			self.Multiplier = 1
			self.Enabled = False
			#self.Mode = 'NONE'
			#################################################################################
		else:
			print("To Many objects")
		#---------------------------
	#def check(self, context):
		#print(self.Hide)
		#print(context.scene)

	def execute(self, ctx):
		for obj in ctx.selected_objects:
			obj.show_x_ray = self.See_Trough
			if self.DisplayAsBox: obj.draw_type = 'BOUNDS'
			else: obj.draw_type = 'BOUNDS'
			#self.BackFaceCull = bpy.context.space_data.show_backface_culling
			obj.show_all_edges = self.EdgeOnly
			#self.VertexTick = False
			#self.Trajectory = False
			#self.Mothinpath = False
			#self.IgnoreExtents = False
			#self.ShowFrozeninGray = True
			#self.NeverDegread = False
			#self.VerticesChanelDisplay = False
			#self.VertexChanel = 'VER_COL' 
			#self.MapChanel = 1
			#Rendering Control
			#self.Visablity = 100
			#self.Renderable = True
			#self.InheritVisablity = True
			#self.VisabletoCamera = True
			#self.VisabletoReflectionRefraction = True
			#self.ReciveShadow = True
			#self.CastShadow = True
			#self.ApplyAtmospherics = True
			#self.RenderOccludedObjects = True
			obj.pass_index = self.ObjectID
			#Motion Blur
			#self.Multiplier = 1
			#self.Enabled = False
			#self.Mode = 'NONE'
		return {'FINISHED'}
	def cancel(self, ctx):
		print("canceled")

	def invoke(self, ctx, event):
		# on open do
		print ("invok")
		self.Cast = True
		wm = ctx.window_manager
		return wm.invoke_props_dialog(self)
#bpy.utils.register_class(ObjectPropertiesDialog)