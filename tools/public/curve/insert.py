# bl_info = {
#     "name": "Insert Bezier Point",
#     "author": "Arun Leander",
#     "category": "Curve",
#     "version": (0, 8),
#     "blender": (2, 79, 0),
#     "description": "Select two points of a bezier curve and press I to insert another bezier point between them.",
#     "warning": "Read the preferences below.",
# }

import bpy,bgl,blf,math,mathutils
import numpy as np
from bpy_extras.view3d_utils import location_3d_to_region_2d
from bpy.types import Operator
from mathutils import Vector, Matrix


class CubicBezier(object):
	def __init__(self, points):
		self.points = np.array(points).astype(np.float32)

	def at(self, t):
		pt =  1 *        (1 - t)**3 * self.points[0]
		pt += 3 * t**1 * (1 - t)**2 * self.points[1]
		pt += 3 * t**2 * (1 - t)**1 * self.points[2]
		pt += 1 * t**3              * self.points[3]
		return pt

	def split(self, t):
		p1, p2, p3, p4 = self.points

		p12 = (p2-p1)*t+p1
		p23 = (p3-p2)*t+p2
		p34 = (p4-p3)*t+p3
		p123 = (p23-p12)*t+p12
		p234 = (p34-p23)*t+p23
		p1234 = (p234-p123)*t+p123

		return [p1,p12,p123,p1234,p234,p34,p4]

def gl_end_and_restore():
	bgl.glEnd()
	bgl.glLineWidth(1)
	bgl.glDisable(bgl.GL_BLEND)
	bgl.glEnable(bgl.GL_DEPTH_TEST)
	bgl.glColor4f(0.0, 0.0, 0.0, 1.0)
	bgl.glPointSize(1)

def draw_callback_bezier_2d(self, context):
	bgl.glEnable(bgl.GL_BLEND)

	font_id = 0
	blf.position(font_id, (context.area.width-84)/2, context.area.height / 8 * 7, 0)
	blf.size(font_id, 12, 72)
	blf.draw(font_id, "Inserting Point: " + "{:10.4f}".format(self.at[2]))

	gl_end_and_restore()

def draw_callback_bezier_3d(self, context):
	bgl.glEnable(bgl.GL_BLEND)
	bgl.glDepthFunc(bgl.GL_ALWAYS)

	bezier = self.beziers[self.at[0]][self.at[1]]
	split = bezier.split(self.at[2])
	points = bezier.points

	bgl.glColor4f(1,1,1,0.5)
	bgl.glLineWidth(1.0)
	bgl.glBegin(bgl.GL_LINES)
	bgl.glVertex3f(*points[0])
	bgl.glVertex3f(*points[1])
	bgl.glVertex3f(*points[2])
	bgl.glVertex3f(*points[3])
	bgl.glEnd()

	bgl.glColor4f(1,1,1,1)
	bgl.glPointSize(6)
	bgl.glBegin(bgl.GL_POINTS)
	bgl.glVertex3f(*points[0])
	bgl.glVertex3f(*points[3])
	bgl.glEnd()

	bgl.glPointSize(2)
	bgl.glBegin(bgl.GL_POINTS)
	bgl.glVertex3f(*points[1])
	bgl.glVertex3f(*points[2])
	bgl.glEnd()

	# draw new bezier anchor
	bgl.glColor4f(0.8, 1.0, 0.0, 0.5)
	bgl.glLineWidth(2)
	bgl.glBegin(bgl.GL_LINE_STRIP)
	bgl.glVertex3f(*split[2])
	bgl.glVertex3f(*split[3])
	bgl.glVertex3f(*split[4])
	bgl.glEnd()

	bgl.glColor4f(0.2,1,0.0, 1.0)
	bgl.glPointSize(10)
	bgl.glBegin(bgl.GL_POINTS)
	bgl.glVertex3f(*split[3])
	bgl.glEnd()

	bgl.glPointSize(6)
	bgl.glBegin(bgl.GL_POINTS)
	bgl.glVertex3f(*split[2])
	bgl.glVertex3f(*split[4])
	bgl.glEnd()

	gl_end_and_restore()


class AddonPreferences:
	snap_to = ['SEGMENT','SINGLE','ALL'][1]
	samples = 13
	epsilon = 0.008
	single_select = ['CLOSEST', 'ACTIVE'][1]
	segment_select = ['CLOSEST','SELECTED'][0]

class InsertBezierPoint(Operator):
	"""Insert a point between two other bezier spline keypoints."""
	bl_idname = "curve.insert_bezier_spline_point"
	bl_label = "Insert Bezier Point"

	def point_in_view(self, context, point3d):
		point2d = location_3d_to_region_2d(context.region, context.region_data, point3d)
		if (point2d[0] >= 0 and point2d[1] >= 0 and
			point2d[0] < context.region.width and point2d[1] < context.region.height):
			return True
		return False

	def get_2d_distance(self, context, point3d, mouse_pos):
		point2d = location_3d_to_region_2d(context.region, context.region_data, point3d)

		if (point2d.x >= 0 and point2d.y >= 0 and
			point2d.x < context.region.width and point2d.y < context.region.height):
			distance = (point2d - mouse_pos).length
			return distance
		return math.inf

	def get_3d_closest(self, context):
		samples = self.addon_prefs.samples
		mindex = 0, 0

		spaceview3d = context.area.spaces[0]
		view_mat = spaceview3d.region_3d.view_matrix
		is_perspective = spaceview3d.region_3d.is_perspective

		points = []
		for a in range(self.a0, self.a1):
			for b in range(len(self.beziers[a])):
				bezier = self.beziers[a][b]
				for i in range(0, samples + 1):
					point3d = bezier.at(i/samples)
					vec = mathutils.Vector(point3d)

					if self.point_in_view(context, vec):
						info_vec = None

						if is_perspective:
							points.append([a, b, (view_mat@vec).length])
						else:
							points.append([a, b, -(view_mat@vec).z])

		if len(points) == 0:
			return -1, -1

		# use a lamda expression to get closest point
		return min(points, key = lambda x: x[2])[0:2]


	def get_2d_closest(self, context, event):
		mouse_pos = mathutils.Vector((event.mouse_x - context.region.x, event.mouse_y  - context.region.y))

		distance = math.inf

		mindex = None
		at = 0
		samples = self.addon_prefs.samples

		for a in range(self.a0, self.a1):
			b0 = 0
			b1 = len(self.beziers[a])
			if self.b >= 0:
				b0 = self.b
				b1 = b0 + 1

			for b in range(b0, b1):
				bezier = self.beziers[a][b]
				for i in range(1, samples):

					point3d = bezier.at(i/samples)
					new_distance = self.get_2d_distance(context, point3d, mouse_pos)
					if (new_distance < distance):
						distance = new_distance
						mindex = a, b
						at = i

		bezier = self.beziers[mindex[0]][mindex[1]]
		index_a = (at-1)/samples
		index_b = (at+1)/samples
		pt_a = location_3d_to_region_2d(context.region, context.region_data, bezier.at(index_a))
		pt_b = location_3d_to_region_2d(context.region, context.region_data, bezier.at(index_b))
		distance_a = (pt_a - mouse_pos).length
		distance_b = (pt_b - mouse_pos).length
		difference = abs(distance_a - distance_b)

		while (difference > self.EPSILON):
			i += 1
			if (distance_a > distance_b):
				distance_a, distance_b = distance_b, distance_a
				pt_a, pt_b = pt_b, pt_a
				index_a, index_b = index_b, index_a
			index_b = (index_a + index_b) / 2
			pt_b = location_3d_to_region_2d(context.region, context.region_data, bezier.at(index_b))
			distance_b = (pt_b - mouse_pos).length
			difference = abs(distance_a - distance_b)

		return [*mindex, index_a]

	def create_new_spline(self, context):
		spline_points = self.ob.data.splines[self.at[0]].bezier_points
		spline_points.add()

		split = self.beziers[self.at[0]][self.at[1]].split(self.at[2])

		for i in range(len(spline_points)-2, self.at[1], -1):
			spline_points[i+1].co           = spline_points[i].co 
			spline_points[i+1].handle_right = spline_points[i].handle_right
			spline_points[i+1].handle_left  = spline_points[i].handle_left

			spline_points[i+1].handle_right_type = spline_points[i].handle_right_type
			spline_points[i+1].handle_left_type  = spline_points[i].handle_left_type

		i = self.at[1]

		spline_points[i+1].handle_right_type = 'ALIGNED'
		spline_points[i+1].handle_left_type  = 'ALIGNED'

		spline_points[i].handle_right = mathutils.Vector(split[1])
		spline_points[i + 1].co = mathutils.Vector(split[3])
		spline_points[i + 1].handle_left = mathutils.Vector(split[2])
		spline_points[i + 1].handle_right = mathutils.Vector(split[4])
		spline_points[i + 2].handle_left = mathutils.Vector(split[5])

		spline_points[i + 1].select_control_point = True
		spline_points[i + 1].select_right_handle = True
		spline_points[i + 1].select_left_handle = True

		bpy.ops.transform.translate('INVOKE_DEFAULT', True)

	def beziers_from_splines(self, splines):
		beziers = []
		for spline in splines:
			spline_beziers = []
			for i in range(len(spline.bezier_points) - 1):

				bezier_points = [  spline.bezier_points[i].co.copy(),
							spline.bezier_points[i].handle_right.copy(),
							spline.bezier_points[i + 1].handle_left.copy(),
							spline.bezier_points[i + 1].co.copy()   ]

				spline_beziers.append(CubicBezier(bezier_points))
			beziers.append(spline_beziers)
		return beziers

	def exit_handler(self):
		bpy.types.SpaceView3D.draw_handler_remove(self._handle_2d, 'WINDOW')
		bpy.types.SpaceView3D.draw_handler_remove(self._handle_3d, 'WINDOW')
		self.ob.select = True
		bpy.ops.object.mode_set(mode='EDIT')

	def modal(self, context, event):
		context.area.tag_redraw()

		if event.type in {'MIDDLEMOUSE', 'WHEELUPMOUSE', 'WHEELDOWNMOUSE'}:
			# allow navigation
			return {'PASS_THROUGH'}
		elif event.type == 'MOUSEMOVE':
			self.at = self.get_2d_closest(context, event)

		elif event.type in {'LEFTMOUSE', 'NUMPAD_ENTER', 'RET'}:
			self.exit_handler()
			bpy.ops.curve.select_all(action="DESELECT")
			self.create_new_spline(context)
			return {'FINISHED'}

		elif event.type in {'RIGHTMOUSE', 'ESC'}:
			self.exit_handler()
			return {'CANCELLED'}

		return {'RUNNING_MODAL'}

	def invoke(self, context, event):
		if context.area.type != 'VIEW_3D':
			self.report({'WARNING'}, "Execute the operator in the VIEW3D.")
			return {'CANCELLED'}

		if (context.object == None or
			context.object.type != 'CURVE' or
			context.object.data.is_editmode == False or
			len(context.object.data.splines) == 0):
			self.report({'WARNING'}, "Enter the edit mode of a curve.")
			return {'CANCELLED'}

		self.ob = context.object
		# convert all splines in to lists of cubic beziers
		splines = self.ob.data.splines
		self.beziers = self.beziers_from_splines(splines)

		self.addon_prefs = AddonPreferences()
		self.EPSILON = self.addon_prefs.epsilon
		self.a0 = 0
		self.a1 = len(self.beziers)
		self.b = -1

		close_a, close_b = self.get_3d_closest(context)
		close_a = max(close_a, 0)


		# choose spline
		if self.addon_prefs.snap_to != 'ALL':

			if self.addon_prefs.single_select == 'ACTIVE':
				for i in range(len(splines)):
					if splines[i] == splines.active:
						self.a0 = i

			if self.addon_prefs.single_select == 'CLOSEST':
				self.a0 = close_a

			self.a1 = self.a0 + 1


		# choose control point
		if self.addon_prefs.snap_to == 'SEGMENT':
			if self.addon_prefs.segment_select == 'SELECTED':
				print("Searching")
				for i in range(len(splines[self.a0].bezier_points) - 1):
					if splines[self.a0].bezier_points[i].select_control_point:
						print("FOUND")
						self.b = i
						break

			if self.addon_prefs.segment_select == 'CLOSEST':
				closest = self.get_2d_closest(context, event)
				self.b = closest[1]



		# at is a triple [spline_id, bezier_id, bezier_parameter (t)]
		self.at = self.get_2d_closest(context, event)
		self.points2d = []

		args = (self, context)            
		self._handle_2d = bpy.types.SpaceView3D.draw_handler_add(draw_callback_bezier_2d, args, 'WINDOW', 'POST_PIXEL')
		self._handle_3d = bpy.types.SpaceView3D.draw_handler_add(draw_callback_bezier_3d, args, 'WINDOW', 'POST_VIEW')

		context.window_manager.modal_handler_add(self)
		bpy.ops.object.mode_set(mode='OBJECT')
		self.ob.select = False
		return {'RUNNING_MODAL'}

def insert_cls(register):
	classes = [InsertBezierPoint]
	for c in classes:
		if register:
			bpy.utils.register_class(c)
		else:
			bpy.utils.unregister_class(c)

if __name__ == '__main__':
	insert_cls(True)

__all__ = ["insert_cls"]