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

# The Original Code Creator by 'Hidesato Ikeya'
# https://github.com/Bombaba
# https://blenderartists.org/u/bon_baba

import bpy, bmesh
from bpy.types import Operator
from bpy.props import FloatProperty, BoolProperty, EnumProperty
from math import sin, cos, pi, radians, degrees, atan, sqrt
from bpy_extras import view3d_utils
from mathutils import Vector



X_UP, Y_UP, Z_UP = Vector((1, 0, 0)), Vector((0, 1, 0)), Vector((0, 0, 1))
ZERO_VEC = Vector((0, 0, 0))
ANGLE_1, ANGLE_90, ANGLE_180, ANGLE_360 = pi/180, pi/2, pi, 2*pi



class OffsetBase:
	threshold: FloatProperty(name="Flat Face Threshold", precision=5,
		 default=radians(0.05), step=1.0e-4, subtype='ANGLE',options={'HIDDEN'},
		description="If difference of angle between two adjacent faces is "
					"below this value, those faces are regarded as flat.")

	caches_valid: BoolProperty(name="Caches Valid", default=False, options={'HIDDEN'})

	_cache_offset_infos = None
	_cache_edges_orig = None

	def use_caches(self, ctx):
		self.caches_valid = True

	def get_caches(self, bm):
		bmverts = tuple(bm.verts)
		bmedges = tuple(bm.edges)

		offset_infos = [(bmverts[vix], co, d) for vix, co, d in self._cache_offset_infos]
		edges_orig = [bmedges[eix] for eix in self._cache_edges_orig]

		for e in edges_orig:
			e.select = False
		for f in bm.faces:
			f.select = False

		return offset_infos, edges_orig

	def save_caches(self, offset_infos, edges_orig):
		self._cache_offset_infos = tuple((v.index, co, d) for v, co, d in offset_infos)
		self._cache_edges_orig = tuple(e.index for e in edges_orig)

	@staticmethod
	def is_face_selected(ob_edit):
		bpy.ops.object.mode_set(mode="OBJECT")
		me = ob_edit.data
		for p in me.polygons:
			if p.select:
				bpy.ops.object.mode_set(mode="EDIT")
				return True
		bpy.ops.object.mode_set(mode="EDIT")
		return False

	@staticmethod
	def is_mirrored(ob_edit):
		for mod in ob_edit.modifiers:
			if mod.type == 'MIRROR' and mod.use_mirror_merge:
				return True
		return False

	@staticmethod
	def reorder_loop(verts, edges, lp_normal, adj_faces):
		for i, adj_f in enumerate(adj_faces):
			if adj_f is None:
				continue
			v1, v2 = verts[i], verts[i+1]
			e = edges[i]
			fv = tuple(adj_f.verts)
			if fv[fv.index(v1)-1] is v2:
				# Align loop direction
				verts.reverse()
				edges.reverse()
				adj_faces.reverse()
			if lp_normal.dot(adj_f.normal) < .0:
				lp_normal *= -1
			break
		else:
			# All elements in adj_faces are None
			for v in verts:
				if v.normal != ZERO_VEC:
					if lp_normal.dot(v.normal) < .0:
						verts.reverse()
						edges.reverse()
						lp_normal *= -1
					break

		return verts, edges, lp_normal, adj_faces

	@staticmethod
	def get_cross_rail(vec_tan, vec_edge_r, vec_edge_l, normal_r, normal_l):
		# Cross rail is a cross vector between normal_r and normal_l.

		vec_cross = normal_r.cross(normal_l)
		if vec_cross.dot(vec_tan) < .0:
			vec_cross *= -1
		cos_min = min(vec_tan.dot(vec_edge_r), vec_tan.dot(-vec_edge_l))
		cos = vec_tan.dot(vec_cross)
		if cos >= cos_min:
			vec_cross.normalize()
			return vec_cross
		else:
			return None

	@staticmethod
	def get_edge_rail(vert, set_edges_orig):
		co_edges = co_edges_selected = 0
		vec_inner = None
		for e in vert.link_edges:
			if (e not in set_edges_orig and
			   (e.select or (co_edges_selected == 0 and not e.hide))):
				v_other = e.other_vert(vert)
				vec = v_other.co - vert.co
				if vec != ZERO_VEC:
					vec_inner = vec
					if e.select:
						co_edges_selected += 1
						if co_edges_selected == 2:
							return None
					else:
						co_edges += 1
		if co_edges_selected == 1:
			vec_inner.normalize()
			return vec_inner
		elif co_edges == 1:
			# No selected edges, one unselected edge.
			vec_inner.normalize()
			return vec_inner
		else:
			return None

	@staticmethod
	def get_mirror_rail(mirror_plane, vec_up):
		p_norm = mirror_plane[1]
		mirror_rail = vec_up.cross(p_norm)
		if mirror_rail != ZERO_VEC:
			mirror_rail.normalize()
			# Project vec_up to mirror_plane
			vec_up = vec_up - vec_up.project(p_norm)
			vec_up.normalize()
			return mirror_rail, vec_up
		else:
			return None, vec_up

	@staticmethod
	def get_vert_mirror_pairs(set_edges_orig, mirror_planes):
		if mirror_planes:
			set_edges_copy = set_edges_orig.copy()
			vert_mirror_pairs = dict()
			for e in set_edges_orig:
				v1, v2 = e.verts
				for mp in mirror_planes:
					p_co, p_norm, mlimit = mp
					v1_dist = abs(p_norm.dot(v1.co - p_co))
					v2_dist = abs(p_norm.dot(v2.co - p_co))
					if v1_dist <= mlimit:
						# v1 is on a mirror plane.
						vert_mirror_pairs[v1] = mp
					if v2_dist <= mlimit:
						# v2 is on a mirror plane.
						vert_mirror_pairs[v2] = mp
					if v1_dist <= mlimit and v2_dist <= mlimit:
						# This edge is on a mirror_plane, so should not be offsetted.
						set_edges_copy.remove(e)
			return vert_mirror_pairs, set_edges_copy
		else:
			return None, set_edges_orig

	@staticmethod
	def collect_mirror_planes(ob_edit):
		mirror_planes = []
		eob_mat_inv = ob_edit.matrix_world.inverted()
		for m in ob_edit.modifiers:
			if (m.type == 'MIRROR' and m.use_mirror_merge):
				merge_limit = m.merge_threshold
				if not m.mirror_object:
					loc = ZERO_VEC
					norm_x, norm_y, norm_z = X_UP, Y_UP, Z_UP
				else:
					mirror_mat_local = eob_mat_inv * m.mirror_object.matrix_world
					loc = mirror_mat_local.to_translation()
					norm_x, norm_y, norm_z, _ = mirror_mat_local.adjugated()
					norm_x = norm_x.to_3d().normalized()
					norm_y = norm_y.to_3d().normalized()
					norm_z = norm_z.to_3d().normalized()
				if m.use_x:
					mirror_planes.append((loc, norm_x, merge_limit))
				if m.use_y:
					mirror_planes.append((loc, norm_y, merge_limit))
				if m.use_z:
					mirror_planes.append((loc, norm_z, merge_limit))
		return mirror_planes

	@staticmethod
	def collect_edges(bm):
		set_edges_orig = set()
		for e in bm.edges:
			if e.select:
				co_faces_selected = 0
				for f in e.link_faces:
					if f.select:
						co_faces_selected += 1
						if co_faces_selected == 2:
							break
				else:
					set_edges_orig.add(e)

		if not set_edges_orig:
			return None

		return set_edges_orig
	@staticmethod
	def collect_loops(set_edges_orig):
		set_edges_copy = set_edges_orig.copy()

		loops = []  # [v, e, v, e, ... , e, v]
		while set_edges_copy:
			edge_start = set_edges_copy.pop()
			v_left, v_right = edge_start.verts
			lp = [v_left, edge_start, v_right]
			reverse = False
			while True:
				edge = None
				for e in v_right.link_edges:
					if e in set_edges_copy:
						if edge:
							# Overlap detected.
							return None
						edge = e
						set_edges_copy.remove(e)
				if edge:
					v_right = edge.other_vert(v_right)
					lp.extend((edge, v_right))
					continue
				else:
					if v_right is v_left:
						# Real loop.
						loops.append(lp)
						break
					elif reverse is False:
						# Right side of half loop.
						# Reversing the loop to operate same procedure on the left side.
						lp.reverse()
						v_right, v_left = v_left, v_right
						reverse = True
						continue
					else:
						# Half loop, completed.
						loops.append(lp)
						break
		return loops

	@staticmethod
	def calc_loop_normal(verts, fallback=Z_UP):
		# Calculate normal from verts using Newell's method.
		normal = ZERO_VEC.copy()

		if verts[0] is verts[-1]:
			# Perfect loop
			range_verts = range(1, len(verts))
		else:
			# Half loop
			range_verts = range(0, len(verts))

		for i in range_verts:
			v1co, v2co = verts[i-1].co, verts[i].co
			normal.x += (v1co.y - v2co.y) * (v1co.z + v2co.z)
			normal.y += (v1co.z - v2co.z) * (v1co.x + v2co.x)
			normal.z += (v1co.x - v2co.x) * (v1co.y + v2co.y)

		if normal != ZERO_VEC:
			normal.normalize()
		else:
			normal = fallback

		return normal

	@staticmethod
	def get_adj_faces(edges):
		adj_faces = []
		for e in edges:
			adj_f = None
			co_adj = 0
			for f in e.link_faces:
				# Search an adjacent face.
				# Selected face has precedance.
				if not f.hide and f.normal != ZERO_VEC:
					adj_f = f
					co_adj += 1
					if f.select:
						adj_faces.append(adj_f)
						break
			else:
				if co_adj == 1:
					adj_faces.append(adj_f)
				else:
					adj_faces.append(None)
		return adj_faces

	@staticmethod
	def get_directions(lp, vec_upward, normal_fallback, vert_mirror_pairs, **options):
		opt_follow_face = options.get("follow_face")
		opt_edge_rail = options.get("edge_rail")
		opt_er_only_end = options.get("edge_rail_only_end")
		opt_threshold = options.get("threshold")
		opt_normal_override = options.get("normal_override")

		verts, edges = lp[::2], lp[1::2]
		set_edges = set(edges)
		if opt_normal_override is None:
			lp_normal = OffsetBase.calc_loop_normal(verts, fallback=normal_fallback)
		else:
			lp_normal = opt_normal_override
			opt_follow_face = False

		##### Loop order might be changed below.
		if lp_normal.dot(vec_upward) < .0:
			# Make this loop's normal towards vec_upward.
			verts.reverse()
			edges.reverse()
			lp_normal *= -1

		if opt_follow_face:
			adj_faces = OffsetBase.get_adj_faces(edges)
			verts, edges, lp_normal, adj_faces = \
				OffsetBase.reorder_loop(verts, edges, lp_normal, adj_faces)
		else:
			adj_faces = (None, ) * len(edges)
		##### Loop order might be changed above.

		vec_edges = tuple((e.other_vert(v).co - v.co).normalized()
						  for v, e in zip(verts, edges))

		if verts[0] is verts[-1]:
			# Real loop. Popping last vertex.
			verts.pop()
			HALF_LOOP = False
		else:
			# Half loop
			HALF_LOOP = True

		len_verts = len(verts)
		directions = []
		for i in range(len_verts):
			vert = verts[i]
			ix_right, ix_left = i, i-1

			VERT_END = False
			if HALF_LOOP:
				if i == 0:
					# First vert
					ix_left = ix_right
					VERT_END = True
				elif i == len_verts - 1:
					# Last vert
					ix_right = ix_left
					VERT_END = True

			edge_right, edge_left = vec_edges[ix_right], vec_edges[ix_left]
			face_right, face_left = adj_faces[ix_right], adj_faces[ix_left]

			norm_right = face_right.normal if face_right else lp_normal
			norm_left = face_left.normal if face_left else lp_normal
			if norm_right.angle(norm_left) > opt_threshold:
				# Two faces are not flat.
				two_normals = True
			else:
				two_normals = False

			tan_right = edge_right.cross(norm_right).normalized()
			tan_left = edge_left.cross(norm_left).normalized()
			tan_avr = (tan_right + tan_left).normalized()
			norm_avr = (norm_right + norm_left).normalized()

			rail = None
			if two_normals or opt_edge_rail:
				# Get edge rail.
				# edge rail is a vector of an inner edge.
				if two_normals or (not opt_er_only_end) or VERT_END:
					rail = OffsetBase.get_edge_rail(vert, set_edges)
			if vert_mirror_pairs and VERT_END:
				if vert in vert_mirror_pairs:
					rail, norm_avr = \
						OffsetBase.get_mirror_rail(vert_mirror_pairs[vert], norm_avr)
			if (not rail) and two_normals:
				# Get cross rail.
				# Cross rail is a cross vector between norm_right and norm_left.
				rail = OffsetBase.get_cross_rail(
					tan_avr, edge_right, edge_left, norm_right, norm_left)
			if rail:
				dot = tan_avr.dot(rail)
				if dot > .0:
					tan_avr = rail
				elif dot < .0:
					tan_avr = -rail

			vec_plane = norm_avr.cross(tan_avr)
			e_dot_p_r = edge_right.dot(vec_plane)
			e_dot_p_l = edge_left.dot(vec_plane)
			if e_dot_p_r or e_dot_p_l:
				if e_dot_p_r > e_dot_p_l:
					vec_edge, e_dot_p = edge_right, e_dot_p_r
				else:
					vec_edge, e_dot_p = edge_left, e_dot_p_l

				vec_tan = (tan_avr - tan_avr.project(vec_edge)).normalized()
				# Make vec_tan perpendicular to vec_edge
				vec_up = vec_tan.cross(vec_edge)

				vec_width = vec_tan - (vec_tan.dot(vec_plane) / e_dot_p) * vec_edge
				vec_depth = vec_up - (vec_up.dot(vec_plane) / e_dot_p) * vec_edge
			else:
				vec_width = tan_avr
				vec_depth = norm_avr

			directions.append((vec_width, vec_depth))

		return verts, directions

	def get_offset_infos(self, bm, ob_edit, **options):
		opt_mirror_modifier = options.get("mirror_modifier")

		set_edges_orig = self.collect_edges(bm)
		if set_edges_orig is None:
			self.report({'WARNING'},
						"No edges are selected.")
			return False, False

		if opt_mirror_modifier:
			mirror_planes = self.collect_mirror_planes(ob_edit)
			vert_mirror_pairs, set_edges = \
				self.get_vert_mirror_pairs(set_edges_orig, mirror_planes)

			if set_edges:
				set_edges_orig = set_edges
			else:
				#self.report({'WARNING'},
				#			"All selected edges are on mirror planes.")
				vert_mirror_pairs = None
		else:
			vert_mirror_pairs = None
		edges_orig = list(set_edges_orig)

		loops = self.collect_loops(set_edges_orig)
		if loops is None:
			self.report({'WARNING'},
						"Overlapping edge loops detected. Select discrete edge loops")
			return False, False

		vec_upward = (X_UP + Y_UP + Z_UP).normalized()
		# vec_upward is used to unify loop normals when follow_face is off.
		normal_fallback = Z_UP
		# normal_fallback = Vector(ctx.region_data.view_matrix[2][:3])
		# normal_fallback is used when loop normal cannot be calculated.

		offset_infos = []
		for lp in loops:
			verts, directions = self.get_directions(
				lp, vec_upward, normal_fallback, vert_mirror_pairs,
				**options)

			if verts:
				# convert vert objects to vert indexs
				for v, d in zip(verts, directions):
					offset_infos.append((v, v.co.copy(), d))

		for e in edges_orig:
			e.select = False
		for f in bm.faces:
			f.select = False

		return offset_infos, edges_orig

	@staticmethod
	def extrude_and_pairing(bm, edges_orig, ref_verts):
		""" ref_verts is a list of vertices, each of which should be
		one end of an edge in edges_orig"""
		extruded = bmesh.ops.extrude_edge_only(bm, edges=edges_orig)['geom']
		n_edges = n_faces = len(edges_orig)
		n_verts = len(extruded) - n_edges - n_faces

		exverts = set(extruded[:n_verts])
		exedges = set(extruded[n_verts:n_verts + n_edges])
		#faces = set(extruded[n_verts + n_edges:])
		side_edges = set(e for v in exverts for e in v.link_edges if e not in exedges)

		# ref_verts[i] and ret[i] are both ends of a side edge.
		exverts_ordered = [e.other_vert(v) for v in ref_verts for e in v.link_edges if e in side_edges]

		return exverts_ordered, list(exedges), list(side_edges)

	@staticmethod
	def move_verts(bm, me, width, depth, offset_infos, verts_offset=None, update=True):
		if verts_offset is None:
			for v, co, (vec_w, vec_d) in offset_infos:
				v.co = co + width * vec_w + depth * vec_d
		else:
			for (_, co, (vec_w, vec_d)), v in zip(offset_infos, verts_offset):
				v.co = co + width * vec_w + depth * vec_d

		if update:
			bm.normal_update()
			bmesh.update_edit_mesh(me)


class Mesh_OT_Outline_Offset(Operator, OffsetBase):
	"""Outline Offset"""
	bl_idname = "mesh.outline_offset"
	bl_label = "Outline Offset"
	bl_options = {'REGISTER', 'UNDO'}

	follow_face: BoolProperty(name="Follow Face", default=False,
		description="Offset along faces around")
	
	mirror_modifier: BoolProperty(name="Mirror Modifier", default=False,
		description="Take into account of Mirror modifier")
	
	edge_rail: BoolProperty(name="Edge Rail", default=False,
		description="Align vertices along inner edges")
	
	edge_rail_only_end: BoolProperty(name="Edge Rail Only End", default=False,
		description="Apply edge rail to end verts only")
	
	lock_axis: EnumProperty(items=[
			('none', "None", "Don't lock axis"),
			('x', "X", "Lock X axis"),
			('y', "Y", "Lock Y axis"),
			('z', "Z", "Lock Z axis"),
			('view', "VIEW", "Lock view axis")],
		name="Lock Axis", default='none')

	# Functions below are update functions.

	def change_depth_mode(self, ctx):
		if self.depth_mode == 'angle':
			self.width, self.angle = self.depth_to_angle(self.width, self.depth)
		else:
			self.width, self.depth = self.angle_to_depth(self.width, self.angle)


	def angle_to_depth(width, angle):
		"""Returns: (converted_width, converted_depth)"""
		return width * cos(angle), width * sin(angle)


	def depth_to_angle(width, depth):
		"""Returns: (converted_width, converted_angle)"""
		ret_width = sqrt(width * width + depth * depth)

		if width:
			ret_angle = atan(depth / width)
		elif depth == 0:
			ret_angle = 0
		elif depth > 0:
			ret_angle = ANGLE_90
		elif depth < 0:
			ret_angle = -ANGLE_90

		return ret_width, ret_angle

	width: FloatProperty(name="Width", default=.2, precision=4, step=1,
		update=OffsetBase.use_caches)
	
	flip_width: BoolProperty(name="Flip Width", default=False,
		description="Flip width direction",
		update=OffsetBase.use_caches)
	
	depth: FloatProperty(name="Depth", default=.0, precision=4, step=1,
		update=OffsetBase.use_caches)

	flip_depth: BoolProperty(name="Flip Depth", default=False,
		description="Flip depth direction",
		update=OffsetBase.use_caches)

	depth_mode: EnumProperty(
		items=[('angle', "Angle", "Angle"),
			   ('depth', "Depth", "Depth")],
		name="Depth mode", default='angle',
		update=change_depth_mode)

	angle: FloatProperty(
		name="Angle", default=0, precision=3, step=100,
		min=-2*pi, max=2*pi, subtype='ANGLE', description="Angle",
		update=OffsetBase.use_caches)
	flip_angle: bpy.props.BoolProperty(
		name="Flip Angle", default=False,
		description="Flip Angle",
		update=OffsetBase.use_caches)

	def get_lockvector(self, ctx):
		axis = self.lock_axis
		if axis == 'x':
			return X_UP
		elif axis == 'y':
			return Y_UP
		elif axis == 'z':
			return Z_UP
		elif axis == 'view' and ctx.region_data:
			vec = Z_UP.copy()
			vec.rotate(ctx.region_data.view_rotation)
			return vec
		return None

	def get_exverts(self, bm, offset_infos, edges_orig):
		ref_verts = [v for v, _, _ in offset_infos]
		exverts, exedges = ref_verts, edges_orig
		for e in exedges:
			e.select = True
		return exverts

	def do_offset(self, bm, me, offset_infos, verts_offset):
		if self.depth_mode == 'angle':
			w = self.width if not self.flip_width else -self.width
			angle = self.angle if not self.flip_angle else -self.angle
			width = w * cos(angle)
			depth = w * sin(angle)
		else:
			width = self.width if not self.flip_width else -self.width
			depth = self.depth if not self.flip_depth else -self.depth

		self.move_verts(bm, me, width, depth, offset_infos, verts_offset)

	@classmethod
	def poll(self, ctx):
		return ctx.mode == 'EDIT_MESH'

	def draw(self, ctx):
		layout = self.layout

		row = layout.row(align=True)
		row.prop(self, 'width')
		row.prop(self, 'flip_width', icon='ARROW_LEFTRIGHT', icon_only=True)
		
		layout.label(text="Depth Mode:")
		layout.row().prop(self, 'depth_mode', expand=True)
		if self.depth_mode == 'angle':
			d_mode = 'angle'
			flip = 'flip_angle'
		else:
			d_mode = 'depth'
			flip = 'flip_depth'
		row = layout.row(align=True)
		row.prop(self, d_mode)
		row.prop(self, flip, icon='ARROW_LEFTRIGHT', icon_only=True)

		layout.label(text="Lock Axis:")
		layout.row().prop(self, 'lock_axis', text="Lock Axis", expand=True)

		layout.separator()
		
		row = layout.row()
		row.prop(self, 'follow_face')
		if self.follow_face:
			row.prop(self, "threshold", text="Threshold")
		
		row = layout.row()
		row.prop(self, 'edge_rail')
		if self.edge_rail:
			row.prop(self, 'edge_rail_only_end', text="OnlyEnd", toggle=True)

		layout.prop(self, 'mirror_modifier')

		#layout.operator('mesh.offset_edges', text='Repeat')


	def execute(self, ctx):
		# In edit mode
		edit_object = ctx.edit_object
		me = edit_object.data
		bm = bmesh.from_edit_mesh(me)

		if self.caches_valid and self._cache_offset_infos:
			offset_infos, edges_orig = self.get_caches(bm)
		else:
			offset_infos, edges_orig = self.get_offset_infos(
				bm, edit_object,
				follow_face=self.follow_face,
				edge_rail=self.edge_rail,
				edge_rail_only_end=self.edge_rail_only_end,
				mirror_modifier=self.mirror_modifier,
				normal_override=self.get_lockvector(ctx),
				threshold=self.threshold
			)
			if offset_infos is False:
				return {'CANCELLED'}
			self.save_caches(offset_infos, edges_orig)

		exverts = self.get_exverts(bm, offset_infos, edges_orig)
		self.do_offset(bm, me, offset_infos, exverts)

		self.caches_valid = False
		return {'FINISHED'}

	def invoke(self, ctx, event):
		# in edit mode
		ob_edit = ctx.edit_object
		if self.is_face_selected(ob_edit):
			self.follow_face = True
		if self.is_mirrored(ob_edit):
			self.mirror_modifier = True

		if ctx.space_data.type == 'VIEW_3D':
			ret = self.modal_prepare_bmeshes(ctx, ob_edit)
			if ret is False:
				return {'CANCELLED'}

			self.width = self.angle = self.depth = 0.0
			self.flip_depth = self.flip_angle = self.flip_width = False
			self._mouse_init = self._mouse_prev = Vector((event.mouse_x, event.mouse_y))
			ctx.window_manager.modal_handler_add(self)

			self._factor = self.get_factor(ctx, self._edges_orig)

			# toggle switchs of keys
			self._F = 0
			self._A = 0
			
			return {'RUNNING_MODAL'}
		else:
			return self.execute(ctx)

	def modal(self, ctx, event):
		# In edit mode
		ob_edit = ctx.edit_object
		me = ob_edit.data
		if event.type == 'F':
			# toggle follow_face
			# event.type == 'F' is True both when 'F' is pressed and when released,
			# so these codes should be executed every other loop.
			self._F = 1 - self._F
			if self._F:
				self.follow_face = 1 - self.follow_face

				self.modal_clean_bmeshes(ctx, ob_edit)
				ret = self.modal_prepare_bmeshes(ctx, ob_edit)
				if ret:
					self.do_offset(self._bm, me, self._offset_infos, self._exverts)
					return {'RUNNING_MODAL'}
				else:
					return {'CANCELLED'}

		if event.type == 'A':
			# toggle depth_mode
			self._A = 1 - self._A
			if self._A:
				if self.depth_mode == 'angle':
					self.depth_mode = 'depth'
				else:
					self.depth_mode = 'angle'
					
		ctx.area.header_text_set(self.create_header())#????

		if event.type == 'MOUSEMOVE':
			_mouse_current = Vector((event.mouse_x, event.mouse_y))
			vec_delta = _mouse_current - self._mouse_prev

			if event.ctrl:
				if self.depth_mode == 'angle':
					self.angle += vec_delta.y * ANGLE_1
				elif self.depth_mode == 'depth':
					self.depth += vec_delta.y * self._factor
			else:
				self.width += vec_delta.x * self._factor

			self._mouse_prev = _mouse_current

			self.do_offset(self._bm, me, self._offset_infos, self._exverts)
			return {'RUNNING_MODAL'}

		elif event.type == 'LEFTMOUSE':
			self._bm_orig.free()
			ctx.area.header_text_set(text=None)
			return {'FINISHED'}

		elif event.type in {'RIGHTMOUSE', 'ESC'}:
			self.modal_clean_bmeshes(ctx, ob_edit)
			ctx.area.header_text_set(text=None)
			return {'CANCELLED'}

		return {'RUNNING_MODAL'}

	# methods below are usded in interactive mode
	def create_header(self):
		header = "".join(
			["Width {width: .4}  ",
			 "Depth {depth: .4}('A' to Angle)  " if self.depth_mode == 'depth' else "Angle {angle: 4.0F}В°('A' to Depth)  ",
			 "FollowFace(F):",
			 "(ON)" if self.follow_face else "(OFF)",])

		return header.format(width=self.width, depth=self.depth, angle=degrees(self.angle))

	def modal_prepare_bmeshes(self, ctx, ob_edit):
		bpy.ops.object.mode_set(mode="OBJECT")
		self._bm_orig = bmesh.new()
		self._bm_orig.from_mesh(ob_edit.data)
		bpy.ops.object.mode_set(mode="EDIT")

		self._bm = bmesh.from_edit_mesh(ob_edit.data)

		self._offset_infos, self._edges_orig = self.get_offset_infos(
			self._bm, ob_edit,
			edge_rail=self.edge_rail,
			edge_rail_only_end=self.edge_rail_only_end,
			mirror_modifier=self.mirror_modifier,
			normal_override=self.get_lockvector(ctx),
			threshold=self.threshold)

		if not self._offset_infos:
			return False

		self._exverts = self.get_exverts(self._bm, self._offset_infos, self._edges_orig)
		bmesh.update_edit_mesh(ob_edit.data)
		return True

	def modal_clean_bmeshes(self, ctx, ob_edit):
		bpy.ops.object.mode_set(mode="OBJECT")
		self._bm_orig.to_mesh(ob_edit.data)
		bpy.ops.object.mode_set(mode="EDIT")
		self._bm_orig.free()
		self._bm.free()

	def get_factor(self, ctx, edges_orig):
		"""get the length in the space of edited object
		which correspond to 1px of 3d view. This method
		is used to convert the distance of mouse movement
		to offsetting width in interactive mode.
		"""
		ob = ctx.edit_object
		mat_w = ob.matrix_world
		reg = ctx.region
		reg3d = ctx.space_data.region_3d  # Don't use ctx.region_data
											  # because this will cause error
											  # when invoked from header menu.

		co_median = Vector((0, 0, 0))
		for e in edges_orig:
			co_median += e.verts[0].co
		co_median /= len(edges_orig)
		depth_loc = mat_w @ co_median  # World coords of median point

		win_left = Vector((0, 0))
		win_right = Vector((reg.width, 0))
		left = view3d_utils.region_2d_to_location_3d(reg, reg3d, win_left, depth_loc)
		right = view3d_utils.region_2d_to_location_3d(reg, reg3d, win_right, depth_loc)
		vec_width = mat_w.inverted_safe() @ (right - left)  # width vector in the object space
		width_3d = vec_width.length   # window width in the object space

		return width_3d / reg.width



class Mesh_OT_3DsMax_Like_Bevel(Operator):
	bl_idname = "mesh.mevel"
	bl_label = "3DsMax Like Bevel"
	bl_options = {'REGISTER', 'INTERNAL', 'UNDO'}
	
	@classmethod
	def poll(self, ctx):
		return ctx.mode == "EDIT_MESH"

	def execute(self, ctx):
		bpy.ops.mesh.extrude_region()
		bpy.ops.mesh.outline_offset('INVOKE_DEFAULT')
		return{"FINISHED"}





def draw_offset_edges(self, ctx):
	layout = self.layout
	layout.separator()
	layout.operator('mesh.outline_offset')


classes = [Mesh_OT_Outline_Offset, Mesh_OT_3DsMax_Like_Bevel]

def register_outline():
	for c in classes:
		bpy.utils.register_class(c)
	bpy.types.VIEW3D_MT_edit_mesh_edges.append(draw_offset_edges)

def unregister_outline():
	for c in classes:
		bpy.utils.unregister_class(c)
	bpy.types.VIEW3D_MT_edit_mesh_edges.remove(draw_offset_edges)


if __name__ == '__main__':
	register_outline()
