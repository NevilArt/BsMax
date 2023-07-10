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

from bpy.props import (StringProperty, FloatProperty, IntProperty,
	BoolProperty, EnumProperty)



def get_children(ctx, obj):
	children =[]
	for ob in ctx.scene.objects:
		if ob.parent == obj:
			children.append(ob)
	return children



def get_knots_count(obj):
	knots_count = 0
	for spline in obj.data.splines:
		knots_count += len(spline.bezier_points)
	return knots_count



def get_bone_count(obj):
	normal_bone, deform_bone = 0, 0
	for bone in obj.data.bones:
		if bone.use_deform:
			deform_bone += 1
		else:
			normal_bone += 1
	return (normal_bone, deform_bone)



def read_info(self, ctx):
	obj = ctx.active_object
	# Object informations
	self.name = obj.name
	self.material = obj.active_material.name if obj.active_material else "Undefined"
	self.layer = obj.users_collection[0].name
	self.parent = obj.parent.name if obj.parent else "Scene Root"
	self.num_children = len(get_children(ctx, obj))
	
	if obj.type == 'MESH':
		self.verteces = len(obj.data.vertices)
		self.faces = len(obj.data.polygons)

	elif obj.type == 'CURVE':
		self.verteces = get_knots_count(obj)
		self.faces = len(obj.data.splines)

	elif obj.type == 'ARMATURE':
		normal_bone, deform_bone = get_bone_count(obj)
		self.verteces = normal_bone
		self.faces = deform_bone

	self.dim_x, self.dim_y, self.dim_z = obj.dimensions		

	# Interactivity
	self.hide = obj.hide_viewport and obj.hide_render
	self.freeze = obj.hide_select

	# Display Properties
	self.see_trough = (obj.display_type == 'WIRE')
	self.box_display = (obj.display_type == 'BOUNDS')
	self.back_face_cull = ctx.space_data.overlay.show_face_orientation

	# self.edge_only = obj.show_all_edges
	self.vertex_tick = False
	self.trajectory = False
	self.motin_paths = False
	self.ignore_extents = False
	self.show_frozenin_gray = (obj.display_type == 'SOLID')
	self.never_degread = False
	self.vertices_chanel_display =False
	self.vertex_chanel ='VER_COL' 
	self.map_chanel =1

	# Rendering Control
	self.visablity = 100
	self.renderable = not obj.hide_render
	self.inherit_visablity = True
	if ctx.scene.render.engine == 'CYCLES':
		self.visable_to_camera = obj.visible_camera
		self.visable_to_reflection_refraction = obj.visible_glossy
		self.recive_shadow = True
		self.cast_shadow = obj.visible_shadow
	# self.apply_atmospherics = True
	# self.render_occluded_objects = True
	self.object_id = obj.pass_index
	#Motion Blur
	# self.multiplier = 1
	# self.enabled = False
	# self.mode = 'NONE'



def hide(self, ctx):
	for obj in ctx.selected_objects:
		obj.hide_viewport = obj.hide_render = self.hide



def freeze(self, ctx):
	for obj in ctx.selected_objects:
		obj.hide_select = self.freeze
		if self.show_frozenin_gray:
			obj.display_type = 'SOLID'



def see_trough(self, ctx):
	for obj in ctx.selected_objects:
		if obj.display_type != 'BOUNDS':
			obj.display_type = 'WIRE' if self.see_trough else 'TEXTURED'



def	box_display(self, ctx):
	for obj in ctx.selected_objects:
		if self.box_display:
			obj.display_type = 'BOUNDS'
			obj.display_bounds_type = 'BOX'
		else:
			obj.display_type = 'TEXTURED'




def back_face_cull(self, ctx):
	ctx.space_data.overlay.show_face_orientation = self.back_face_cull



def	edge_only(self, ctx):
	pass



def	vertex_tick(self, ctx):
	pass



def	trajectory(self, ctx):
	pass



def	motin_paths(self, ctx):
	pass



def	ignore_extents(self, ctx):
	pass



def	never_degread(self, ctx):
	pass



def	vertices_chanel_display(self, ctx):
	pass



def	vertex_chanel(self, ctx):
	pass



def map_chanel(self, ctx):
	pass



def visablity(self, ctx):
	pass



def renderable(self, ctx):
	for obj in ctx.selected_objects:
		obj.hide_render = not self.renderable



def inherit_visablity(self, ctx):
	pass



def	visable_to_camera(self, ctx):
	if ctx.scene.render.engine == 'CYCLES':
		for obj in ctx.selected_objects:
			obj.visible_camera = self.visable_to_camera



def visable_to_reflection_refraction(self, ctx):
	if ctx.scene.render.engine == 'CYCLES':
		for obj in ctx.selected_objects:
			obj.visible_glossy = self.visable_to_reflection_refraction



def	recive_shadow(self, ctx):
	pass



def cast_shadow(self, ctx):
	if ctx.scene.render.engine == 'CYCLES':
		for obj in ctx.selected_objects:
			obj.visible_shadow = self.cast_shadow



def apply_atmospherics(self, ctx):
	if ctx.scene.render.engine == 'CYCLES':
		for obj in ctx.selected_objects:
			obj.visible_volume_scatter = self.apply_atmospherics



def render_occluded_objects(self, ctx):
	pass



def shadow_catcher(self, ctx):
	if ctx.scene.render.engine == 'CYCLES':
		for obj in ctx.selected_objects:
			obj.is_shadow_catcher = self.shadow_catcher



def hold_out(self, ctx):
	for obj in ctx.selected_objects:
		obj.is_holdout = self.hold_out



def object_id(self, ctx):
	for obj in ctx.selected_objects:
		obj.pass_index = self.object_id



def use_motion_blure(self, ctx):
	if ctx.scene.render.engine == 'CYCLES':
		for obj in ctx.selected_objects:
			obj.cycles.use_motion_blur = self.use_motion_blure



def mb_steps(self, ctx):
	if ctx.scene.render.engine == 'CYCLES':
		for obj in ctx.selected_objects:
			obj.cycles.motion_steps = self.mb_steps



def mb_deformation(self, ctx):
	if ctx.scene.render.engine == 'CYCLES':
		for obj in ctx.selected_objects:
			obj.cycles.use_deform_motion = self.mb_deformation



class Object_OT_Properties(bpy.types.Operator):
	bl_idname = "object.properties"
	bl_label = "Object Properties"
	bl_options = {'REGISTER', 'UNDO'}

	# Object information
	name: StringProperty(name="Name")
	material: StringProperty(name="Material")
	layer: StringProperty(name="Layer")
	parent: StringProperty(name="Parent")
	num_children: IntProperty(name="Num. Children")
	faces: IntProperty(name="Faces")
	verteces: IntProperty(name="Vertices")
	dim_x: FloatProperty(name="X", unit='LENGTH')
	dim_y: FloatProperty(name="Y", unit='LENGTH')
	dim_z: FloatProperty(name="Z", unit='LENGTH')

	#interactivity
	hide: BoolProperty(name="Hide")
	freeze: BoolProperty(name="Freeze")
	
	#Display Properties
	see_trough: BoolProperty(name="See-Through", update=see_trough)
	box_display: BoolProperty(name="Display as Box", update=box_display)
	back_face_cull: BoolProperty(name="Backface Call", update=back_face_cull)
	edge_only: BoolProperty(name="Edge Only", update=edge_only)
	vertex_tick: BoolProperty(name="Vertex Tick", update=vertex_tick)
	trajectory: BoolProperty(name="Trajectory", update=trajectory)
	motin_paths: BoolProperty(name="Mothin path", update=motin_paths)
	ignore_extents: BoolProperty(name="Ignore Extents", update=ignore_extents)
	never_degread: BoolProperty(name="Never Degread", update=never_degread)
	show_frozenin_gray: BoolProperty(name="Show Frozen In Gray")
	
	vertices_chanel_display: BoolProperty(
		name="Vertices Chanel Display",
		update=vertices_chanel_display
	)
	
	vertex_chanel: EnumProperty(
		name ='', description ='mode', default ='VER_COL',
		update = vertices_chanel_display,
		items =[
			('VER_COL', 'Vertex Color', ''),
			('VER_ILLUM', 'Vertex Illumination', ''),
			('VER_ALPHA', 'Vertex Alpha', ''),
			('MAP_CHANEL', 'Map Chanel Color', ''),
			('SOFTSEL_COL', 'Soft Selection Colore', '')
		]
	)

	map_chanel: IntProperty(name="Map Chanel", min=1, max=999, update=map_chanel)

	#Rendering Control
	renderable: BoolProperty(name="Renderable", update=renderable)
	inherit_visablity: BoolProperty(name="Inherit Visablity", update=inherit_visablity)
	visable_to_camera: BoolProperty(name="Visable to Camera", update=visable_to_camera)
	
	visable_to_reflection_refraction: BoolProperty(
		name="Visable to Reflection/Refraction",
		update=visable_to_reflection_refraction
	)
	
	recive_shadow: BoolProperty(name="Recive Shadow", update=recive_shadow)
	cast_shadow: BoolProperty(name="Cast Shadow", update=cast_shadow)
	apply_atmospherics: BoolProperty(name="Apply Atmospherics", update=apply_atmospherics)
	
	render_occluded_objects: BoolProperty(
		name="Render Occluded Objects",
		update=render_occluded_objects
	)
	
	shadow_catcher: BoolProperty(name="Shadow Catcher", update=shadow_catcher)
	hold_out: BoolProperty(name="Holdout", update=hold_out)
	
	# Gbuffer Object ID
	object_id: IntProperty(name="Object ID", min=0, update=object_id)
	
	#Motion Blur
	use_motion_blure: BoolProperty(name="Enabled", update=use_motion_blure)
	mb_steps: IntProperty(name="Steps", default=1, min=1, max=7, update=mb_steps)
	mb_deformation: BoolProperty(name="Deformation", update=mb_deformation)


	@classmethod
	def poll(self,ctx):
		return ctx.active_object != None

	def draw(self,ctx):
		if ctx.active_object != None:
			obj = ctx.active_object
			engine = ctx.scene.render.engine

			layout =self.layout
			box =layout.box()
			box.enabled = False
			box.label(text="Object Information")
			box.prop(self,"name")
			row =box.row()
			row.prop(self,"material")
			row.prop(self,"layer")
			row =box.row()
			row.prop(self,"parent")
			row.prop(self,'num_children')
			row =box.row(align=True)
			row.label(text="Dimension")
			row.prop(self,"dim_x")
			row.prop(self,"dim_y")
			row.prop(self,"dim_z")
			row =box.row()

			if obj.type == 'MESH':
				row.prop(self,"verteces", text='Vertexes')
				row.prop(self,"faces", text='Faces')

			elif obj.type == 'CURVE':
				row.prop(self,"verteces", text='Bezier point')
				row.prop(self,"faces", text='Splines')

			elif obj.type == 'ARMATURE':
				row.prop(self,"verteces", text='Bones (NonDeform)')	
				row.prop(self,"faces", text='Bones (Deform)')

			row =layout.row()
			col =row.column()
			box =col.box()
			box.label(text="Interactivity")
			box.prop(self,"hide")
			box.prop(self,"freeze")

			box =col.box()
			box.label(text="Display Properties")
			box.prop(self,"see_trough")
			box.prop(self,"box_display")
			box.prop(self,"back_face_cull")
			# box.prop(self,"edge_only")
			# box.prop(self,"vertex_tick")
			# box.prop(self,"trajectory")
			# box.prop(self,"ignore_extents")
			box.prop(self,"show_frozenin_gray")
			# box.prop(self,"never_degread")
			# box.prop(self,"vertices_chanel_display")
			# box.prop(self,"vertex_chanel")
			# box.prop(self,"map_chanel")

			col =row.column()
			box =col.box()
			box.label(text="Rendering Control")
			if engine == 'BLENDER_EEVEE':
				box.prop(self,"renderable")
				# box.prop(self,"inherit_visablity")
				# box.prop(self,"visable_to_camera")
				# box.prop(self,"visable_to_reflection_refraction")
				# box.prop(self,"recive_shadow")
				# box.prop(self,"cast_shadow")
				# box.prop(self,"apply_atmospherics")

			elif engine == 'BLENDER_WORKBENCH':
				box.prop(self,"renderable")

			elif engine == 'CYCLES':
				box.prop(self,"renderable")
				# box.prop(self,"inherit_visablity")
				box.prop(self,"visable_to_camera")
				box.prop(self,"visable_to_reflection_refraction")
				# box.prop(self,"recive_shadow")
				box.prop(self,"cast_shadow")
				box.prop(self,"apply_atmospherics")
				box.prop(self,"shadow_catcher")
				
			box.prop(self,"hold_out")	

			box =col.box()
			box.label(text="G-Buffer")
			box.prop(self,"object_id")

			if engine == 'CYCLES':
				box =col.box()
				box.label(text="Motion Blur")
				box.prop(self,"use_motion_blure")
				box.prop(self,"mb_steps")
				box.prop(self,"mb_deformation")
		
				

	def execute(self,ctx):
		hide(self, ctx)
		freeze(self, ctx)
		return {'FINISHED'}

	def cancel(self, ctx):
		#restore(self,ctx)
		return None

	def invoke(self, ctx, event):
		read_info(self, ctx)
		return ctx.window_manager.invoke_props_dialog(self, width=400)



def register_object_properties():
	bpy.utils.register_class(Object_OT_Properties)



def unregister_object_properties():
	bpy.utils.unregister_class(Object_OT_Properties)



if __name__ =="__main__":
	register_object_properties()