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


def fill_sequence_gaps(seq, size):
	ret = []
	for i in range(len(seq)):
		""" Fill sequence """
		ret.append(seq[i])
		if i < len(seq)-1:
			""" start of Gap """
			if seq[i + 1] > seq[i] + 1:
				""" accept of gap size """
				if seq[i] + size > seq[i + 1]:
					""" Fill gap """
					for j in range(seq[i] + 1, seq[i + 1] - 1):
						ret.append(j)
	return ret


def remove_tinys(seq, size):
	ret,i = [], 1
	while i < len(seq):
		""" Check is sequence """
		if seq[i] + 1 == seq[i + 1]:
			new_seq = []
			""" collect sequenses """
			for j in range(i, len(seq)):
				if seq[j] + 1 == seq[j + 1]:
					new_seq.append(seq[j])
				else:
					new_seq.append(seq[j])
					break
			""" ignore is to short """
			if len(new_seq) > size:
				ret += new_seq
			i += len(new_seq)
		else:
			ret.append(seq[i])
			i += 1
	if not seq[-1] in ret:
		ret.append(seq[-1])
	return ret


def frames_to_string(frames):
	print("-Frames> ",frames)
	string = ''
	for i in range(len(frames) - 1):
		if frames[i] + 1 == frames[i + 1]:
			if string[-1] != '-':
				if len(string) > 0 and string[-1] != ',':
					string += ','
				string += str(frames[i]) + '-'
		else:
			if len(string) > 0 and string[-1] != '-' and string[-1] != ',':
				string += ','
			string += str(frames[i])
	if len(string) > 0:
		if string[-1] == '-':
			string += str(frames[-1])
	return string


def has_right(frames, index):
	if index < len(frames):
		if frames[index] + 1 == frames[index + 1]:
			return True
	return False


def has_left(frames, index):
	if index > 0:
		if frames[index] - 1 == frames[index - 1]:
			return True
	return False


def is_right_stand(frames, index, count):
	if index + 1 < len(frames):
		if frames[index] + count < frames[index + 1]:
			return True
	return False


def is_left_stand(frames, index, count):
	if index - 1 > 0:
		if frames[index - 1] + count < frames[index]:
			return True
	return False


def is_right_seq(frames, index, count):
	ret = True
	for i in range(index, index + count):
		if i <= len(frames):
			ret = (frames[i] + 1 == frames[i + 1])
			if not ret:
				break
	return ret


def is_left_seq(frames, index, count):
	ret = True
	for i in range(index - count, index):
		if i > 0:
			ret = (frames[i] + 1 == frames[i + 1])
			if not ret:
				break
		else:
			return False
	return ret


class Transform_Data:
	def __init__(self):
		self.matrix_world = None
		self.frame = None
		self.fov = None
	
	@property
	def location(self):
		return self.matrix_world.translation
	
	@property
	def rotation(self):
		return self.matrix_world.to_euler()


def collect_transform_data(ctx, obj, first, last):
	transform_data = []
	""" store time line condition """
	frame_current = ctx.scene.frame_current
	""" isolate scene """
	bpy.ops.object.select_all(action = 'DESELECT')
	obj.select_set(state = True)
	bpy.ops.view3d.localview(frame_selected=False)
	""" record the transform """
	for f in range(first, last+1):
		ctx.scene.frame_current = f
		# ctx.scene.update()
		ctx.scene.update_tag()
		td = Transform_Data()
		td.matrix_world = obj.matrix_world
		td.frame = f
		td.fov = 45
		transform_data.append(td)
		print("record", f, obj.matrix_world)
	""" restore timeline and local_view """
	ctx.scene.frame_current = frame_current
	return transform_data


def compar_params(cam, time1, time2):
	""" this function checs the FOV changes """
	# Ret = True
	# fov1 = at time time1 cam.fov #TODO :O
	# fov2 = at time time2 cam.fov
	# if fov1 == fov2 then
	# 	Ret = True
	# else
	# 	Ret = False
	# return Ret
	return True


def compar_f(f1, f2, tol):
	if f1 != f2:
		heigher, lower = [f1, f2] if f1 >= f2 else [f2, f1]
		return heigher <= lower + tol
	return True


def compar_p3(p1, p2, tol):
	x = compar_f(p1.x, p2.x, tol)
	y = compar_f(p1.y, p2.y, tol)
	z = compar_f(p1.z, p2.z, tol)
	return  x and y and z


def compar_transform(tr1, tr2, tol):
	if tr1 != None and tr2 != None:
		cp = tr1.location == tr2.location
		print(">> tr >>",tr1.location, tr2.location)
		# cq = compar_p3(tr1.rotation, tr2.rotation, tol)
		# return (cp and cq)
		return cp
	return False


def collect_move_frames(ctx, cam):
	first, last = ctx.scene.frame_start, ctx.scene.frame_end
	transform_datas = collect_transform_data(ctx, cam, first, last)
	frames = []

	for i in range(len(transform_datas)-1):
		current_frame = transform_datas[i]
		next_frame = transform_datas[i+1]
		frame = transform_datas[i]
		
		tr = not compar_transform(current_frame, next_frame, 0.01)
		# pa = not compar_params(cam, (t - 1), t)
		print("frame>",current_frame.frame, tr)
			
		if tr: # or pa: compar fov ignore for now
			if not frame in frames:
				frames.append(frame)

	""" Make sure end frame is in list """
	if not last in frames:
		frames.append(last)

	return frames


def catch_camera_frames(ctx):
	cam = ctx.scene.camera
	if cam != None:
		""" Collect and refine frames """
		frames = collect_move_frames(ctx, cam)
		print("-- collect_move_frames >",frames)
		frames = fill_sequence_gaps(frames, 5)
		print("-- fill_sequence_gaps >",frames)
		frames = remove_tinys(frames, 5)
		print("-- remove_tinys >",frames)
		string = frames_to_string(frames)
		""" Note: back burner has 498 character limit for frames list string """

	return string


class Camera_OT_Catch_Frames(Operator):
	bl_idname = 'camera.catch_frames'
	bl_label = "Catch Frames"
	bl_description = ""
	bl_options = {'REGISTER', 'UNDO'}
	
	def execute(self, ctx):
		if ctx.active_object != None:
			if ctx.active_object.type == "CAMERA":
				frames = catch_camera_frames(ctx)
				# ctx.view_layer.update() #check with/whitout this #
				print("-->", frames)
		# self.report({'OPERATOR'},'bpy.ops.camera.set_active()')
		return{"FINISHED"}


def register_camera_catcher():
	bpy.utils.register_class(Camera_OT_Catch_Frames)


def unregister_camera_catcher():
	bpy.utils.unregister_class(Camera_OT_Catch_Frames)


if __name__ == '__main__':
	register_camera_catcher()