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
from bpy.props import BoolProperty, EnumProperty



class Mesh_OT_Connect_Data:
	def __init__(self):
		self.segments = 1
		self.pinch = 0
		self.slide = 0

mocd = Mesh_OT_Connect_Data()



class Mesh_OT_Connect(Operator):
	bl_idname = "mesh.connect"
	bl_label = "Connect"
	bl_options={'REGISTER', 'UNDO'}

	# default: BoolProperty(default=True)
	# segments: IntProperty(name="Segments")
	# pinch: FloatProperty(name="Pinch", min=-1, max=1)
	# slide: FloatProperty(name="Slide", min=-1, max=1)
	
	# @classmethod
	# def poll(self, ctx):
	# 	return ctx.mode == "MESH_EDIT"

	# def draw(self, ctx):
	# 	layout = self.layout
	# 	layout.prop(self,"segments")
	# 	# layout.prop(self,"pinch")
	# 	# layout.prop(self,"slide")

	def devide(self, ctx):
		v,e,f = ctx.tool_settings.mesh_select_mode
		if v: 
			bpy.ops.mesh.vert_connect()
		elif e:
			bpy.ops.mesh.subdivide_edgering(number_cuts=1)
			# bpy.ops.mesh.subdivide()
			# bpy.ops.mesh.select_all(action='DESELECT')
			# TODO select new created edges
			# mocd.segments = self.segments

	def execute(self, ctx):
		self.devide(ctx)
		# self.report({'OPERATOR'},'bpy.ops.mesh.connect()')
		return{"FINISHED"}

	# def invoke(self, ctx, event):
	# 	if not self.default:
	# 		return ctx.window_manager.invoke_props_dialog(self)
	# 	return{"FINISHED"}



class Mesh_OT_Create_Curve_From_Edges(Operator):
	bl_idname = "mesh.create_curve_from_edge"
	bl_label = "Create Shape from Edges"
	bl_options = {'REGISTER', 'UNDO'}
	
	@classmethod
	def poll(self, ctx):
		return ctx.area.type == 'VIEW_3D'
	
	def execute(self, ctx):
		# v,e,f = ctx.tool_settings.mesh_select_mode
		e = ctx.tool_settings.mesh_select_mode[1]
		if ctx.mode == 'EDIT_MESH' and e:
			bpy.ops.mesh.duplicate(mode=1)
			bpy.ops.mesh.separate(type='SELECTED')
		return{"FINISHED"}



class Mesh_OT_Auto_Loop_Select(Operator):
	bl_idname = "mesh.auto_loop_select"
	bl_label = "Auto Loop Select"
	bl_options = {'REGISTER', 'UNDO'}
	
	@classmethod
	def poll(self, ctx):
		return ctx.area.type == 'VIEW_3D'
	
	def execute(self, ctx):
		if ctx.mode == 'EDIT_MESH':
			v,e,f = ctx.tool_settings.mesh_select_mode
			if v or e:
				bpy.ops.mesh.loop_multi_select(ring=False)
			elif f:
				#TODO "Face loop"
				pass
		return{"FINISHED"}



class Mesh_OT_Auto_Ring_Select(Operator):
	bl_idname = "mesh.auto_ring_select"
	bl_label = "Auto Ring Select"
	bl_options = {'REGISTER', 'UNDO'}
	
	@classmethod
	def poll(self, ctx):
		return ctx.area.type == 'VIEW_3D'
	
	def execute(self, ctx):
		if ctx.mode == 'EDIT_MESH':
			v,e,f = ctx.tool_settings.mesh_select_mode
			if v or e:
				bpy.ops.mesh.loop_multi_select(ring=True)
			elif f:
				# TODO face ring
				pass
		return{"FINISHED"}



class Mesh_OT_Dot_Loop_Select(Operator):
	bl_idname = "mesh.dot_loop_select"
	bl_label = "Dot Loop"
	bl_options = {'REGISTER', 'UNDO'}
	
	@classmethod
	def poll(self, ctx):
		return ctx.area.type == 'VIEW_3D'
	
	def execute(self, ctx):
		if ctx.mode == 'EDIT_MESH':
			bpy.ops.mesh.smart_select_loop()
			bpy.ops.mesh.select_nth()
		return{"FINISHED"}



class Mesh_OT_Dot_Ring_Select(Operator):
	bl_idname = "mesh.dot_ring_select"
	bl_label = "Dot Ring"
	bl_options = {'REGISTER', 'UNDO'}
	
	@classmethod
	def poll(self, ctx):
		return ctx.area.type == 'VIEW_3D'
	
	def execute(self, ctx):
		if ctx.mode == 'EDIT_MESH':
			bpy.ops.mesh.smart_select_ring()
			bpy.ops.mesh.select_nth()
		return{"FINISHED"}



class Mesh_OT_Remove(Operator):
	bl_idname = "mesh.remove"
	bl_label = "Remove"
	bl_options = {'REGISTER', 'UNDO'}
	
	vert: BoolProperty(name="Use Verts", default=False)
	
	@classmethod
	def poll(self, ctx):
		return ctx.area.type == 'VIEW_3D'
	
	def execute(self, ctx):
		if ctx.mode == 'EDIT_MESH':
			v,e,f = ctx.tool_settings.mesh_select_mode
			if v:
				bpy.ops.mesh.dissolve_verts()
			if e:
				bpy.ops.mesh.dissolve_edges(use_verts=self.vert)
			if f:
				bpy.ops.mesh.dissolve_faces(use_verts=self.vert)
		return{"FINISHED"}



class Mesh_OT_Delete_Auto(Operator):
	bl_idname = "mesh.delete_auto"
	bl_label = "Delete (Auto)"
	bl_options = {'REGISTER', 'UNDO'}
	
	@classmethod
	def poll(self, ctx):
		return ctx.area.type == 'VIEW_3D'
	
	def execute(self, ctx):
		if ctx.mode == 'EDIT_MESH':
			v,e,f = ctx.tool_settings.mesh_select_mode
			if v:
				bpy.ops.mesh.delete(type='VERT')
			if e:
				""" For remove the extera edges """
				#TODO find the API for this
				# Select expaned to Face mode (Face) Need to find python API for this
				bpy.ops.mesh.delete(type='EDGE')
				# ctx.tool_settings.mesh_select_mode = v,e,f # restore mode
			if f:
				bpy.ops.mesh.delete(type='FACE')
		return{"FINISHED"}



class Mesh_OT_Remove_Isolated_Geometry(Operator):
	bl_idname = "mesh.remove_isolated_geometry"
	bl_label = "Remove Isolated Geometry"
	bl_description = "Remove isolated vertices and edges"
	bl_options = {'REGISTER', 'UNDO'}
	
	@classmethod
	def poll(self, ctx):
		return ctx.area.type == 'VIEW_3D'
	
	def execute(self, ctx):
		v,e,f = ctx.tool_settings.mesh_select_mode
		bpy.ops.mesh.select_loose()
		if v:
			bpy.ops.mesh.delete(type='VERT')
		if e:
			bpy.ops.mesh.delete(type='EDGE')
		if f:
			bpy.ops.mesh.delete(type='FACE')
		return {'FINISHED'}



# Simulate 3DsMax Nurms Toggle operator avalible on Quad menu
class Mesh_OT_NURMS_Toggle(Operator):
	""" Toggle On/Off the subdivision modifier for selected objects """
	bl_idname = "mesh.nurms_toggle"
	bl_label = "Nurms Toggle"
	bl_options = {'REGISTER', 'UNDO'}
	
	@classmethod
	def poll(self, ctx):
		return ctx.mode in {'EDIT_MESH', 'OBJECT'}
	
	def set_subdive(self, obj, state):
		subdive = None

		# Get object subsurface modifier
		for mod in obj.modifiers:
			if mod.type == 'SUBSURF':
				subdive = mod
		
		# Apply if has modifier Add and Apply if not have modifier
		if subdive:
			subdive.show_in_editmode = state
		else:
			subdive = obj.modifiers.new(name='Subdivision', type='SUBSURF')
			subdive.show_in_editmode = state

	def execute(self, ctx):
		# Get active object subdivision modifier
		ative_subdive = None
		for modifier in ctx.object.modifiers:
			if modifier.type == 'SUBSURF':
				ative_subdive = modifier
		
		# Get reverse ofo active object subdivision modifier to apply to all
		state = not ative_subdive.show_in_editmode if ative_subdive else True

		# Set state to all selected mesh objects
		for obj in ctx.selected_objects:
			if obj.type == 'MESH':
				self.set_subdive(obj, state)

		return{"FINISHED"}



# Blender internal hide/show operator affect all Face/Edge/Vertexes
# This operator affects only active one and keep the others
class Mesh_OT_Hide_Plus(Operator):
	""" Hide/Show the (un)selected Face/Edge/Verts by filter """
	bl_idname = "mesh.hide_plus"
	bl_label = "Hide+"
	bl_options = {'REGISTER', 'UNDO'}

	mode: EnumProperty(name="Hide", default='SELECTED',
		items=[('SELECTED', "Selected", "Hide/Show Selected"),
		('UNSELECTED', "Unselected", "Hide/Show Unselected"),
		('UNHIDE', "Unhide", "Unhide All"),
		('INVERT', "Invert", "Invert Hide/Show state")])
	
	@classmethod
	def poll(self, ctx):
		return ctx.mode == 'EDIT_MESH'

	def hide_selected(self, obj, v, e, f):
		if v:
			for vert in obj.data.vertices:
				vert.hide = vert.select
		if e:
			for edge in obj.data.edges:
				edge.hide = edge.select
		if f:
			for poly in obj.data.polygons:
				poly.hide = poly.select
	
	def hide_unselected(self, obj, v, e, f):
		if v:
			for vert in obj.data.vertices:
				vert.hide = not vert.select
		if e:
			for edge in obj.data.edges:
				edge.hide = not edge.select
		if f:
			for poly in obj.data.polygons:
				poly.hide = not poly.select
	
	def unhide(self, obj, v, e, f):
		if v:
			for vert in obj.data.vertices:
				vert.hide = False
		if e:
			for edge in obj.data.edges:
				edge.hide = False
		if f:
			for poly in obj.data.polygons:
				poly.hide = False

	def invert(self, obj, v, e, f):
		if v:
			for vert in obj.data.vertices:
				vert.hide = not vert.hide
		if e:
			for edge in obj.data.edges:
				edge.hide = not edge.hide
		if f:
			for poly in obj.data.polygons:
				poly.hide = not poly.hide
	
	def execute(self, ctx):
		v,e,f = ctx.tool_settings.mesh_select_mode
		bpy.ops.object.mode_set(mode="OBJECT")
		for obj in ctx.selected_objects:
			if obj.type == 'MESH':
				if self.mode == 'SELECTED':
					self.hide_selected(obj, v, e, f)

				elif self.mode == 'UNSELECTED':
					self.hide_unselected(obj, v, e, f)

				elif self.mode == 'UNHIDE':
					self.unhide(obj, v, e, f)

				elif self.mode == 'INVERT':		
					self.invert(obj, v, e, f)

		bpy.ops.object.mode_set(mode="EDIT")
		return{"FINISHED"}



def mesh_show_hide_plus_menu(self, ctx):
	layout = self.layout
	layout.menu("BSMAX_MT_create_menu")
	layout.separator()
	layout.operator("mesh.hide_plus",text="Hide Selected").mode='SELECTED'
	layout.operator("mesh.hide_plus",text="Hide Unselected").mode='UNSELECTED'
	layout.operator("mesh.hide_plus",text="Invert Hide").mode='INVERT'
	layout.operator("mesh.hide_plus",text="Unhide All").mode='UNHIDE'



classes = (
	Mesh_OT_Create_Curve_From_Edges,
	Mesh_OT_Auto_Loop_Select,
	Mesh_OT_Auto_Ring_Select,
	Mesh_OT_Connect,
	Mesh_OT_Delete_Auto,
	Mesh_OT_Dot_Loop_Select,
	Mesh_OT_Dot_Ring_Select,
	Mesh_OT_Hide_Plus,
	Mesh_OT_NURMS_Toggle,
	Mesh_OT_Remove,
	Mesh_OT_Remove_Isolated_Geometry
)



def register_meshs():
	for c in classes:
		bpy.utils.register_class(c)
	bpy.types.VIEW3D_MT_edit_mesh_showhide.append(mesh_show_hide_plus_menu)



def unregister_meshs():
	bpy.types.VIEW3D_MT_edit_mesh_showhide.remove(mesh_show_hide_plus_menu)
	for c in classes:
		bpy.utils.unregister_class(c)



if __name__ == "__main__":
	register_meshs()