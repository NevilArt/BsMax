###########################################################################
#	BsMax, Tool for excahnge data between Blender, 3Dsmax and Unreal engine
#	Copyright (C) 2023  Naser Merati (Nevil)
#
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
import unreal
from tkinter import Tk


# https://docs.unrealengine.com/5.0/en-US/python-scripting-in-sequencer-in-unreal-engine/


class ClipBoard:
	def set_clipboard_text(self, text):
		Tk.clipboard_clear()
		Tk.clipboard_append(text)

	def get_clipboard_text(self):
		return Tk().clipboard_get()



class FloatKey:
	def __init__(self):
		self.frame = 0
		self.value = 0
		self.type = None
	
	def from_string(self, string, pick):
		field = string.split(',')
		self.frame = int(field[0])
		self.value = float(field[pick])

	def to_string(self):
		return ""
	


class TransformKey:
	def __init__(self):
		self.frame = 0

		self.px = 0
		self.py = 0
		self.pz = 0

		self.rx = 0
		self.ry = 0
		self.rz = 0

		# scale has no use for camera
		self.sx = 1
		self.sy = 1
		self.sz = 1
	
	def from_string(self, string):
		field = string.split(',')

		self.frame = int(field[0])

		self.px = float(field[1])
		self.py = float(field[2])
		self.pz = float(field[3])

		self.rx = float(field[4])
		self.ry = float(field[5])
		self.rz = float(field[6])

	def to_string(self):
		return ""



"""
# Field format
# line0 = identefyKey
# line1 = camera name
# line2 = scene name
#             0           1         2
# line3 = startFrame, endFrame, frameRate
# line4+ data fields
#   0     1   2   3   4   5   6   7
# frame, px, py, pz, rx, ry, rz, fov
"""
class ClipboardCameraAnimation:
	def __init__(self):
		self.identefyKey = "3DSMAXTOCLIPBOARNEVILDCAMERACOPYPASTDATAVERSION01"
		self.cameraName = "Camera"
		self.sequenceName = "Sequence"
		self.startFrame = 0
		self.endFrame = 250
		self.frameRate = 25
		self.fov = []
		self.transform = []
	
	def read_clipboard(self):
		cb = ClipBoard()
		text = cb.get_clipboard_text()
		lines = text.splitlines()

		# ignore if data not detected
		if not lines:
			return

		# ignore if ID key not detcted
		if lines[0] != self.identefyKey:
			return
		
		# read camera and sequence name
		self.cameraName = lines[1]
		self.sequenceName = lines[2]
		
		# read sequence settings
		field = lines[3].split(',')
		self.startFrame = int(field[0])
		self.endFrame = int(field[1])
		self.frameRate = int(field[2])
		
		# read keyframes
		for line in lines[4:]:
			newFov = FloatKey()
			newFov.from_string(line, 7)
			newTransformKey = TransformKey()
			newTransformKey.from_string(line)
			self.fov.append(newFov)
			self.transform.append(newTransformKey)
	


def bind_camera_to_sequence(camera, sequence):
	# Add a spawnable using that cine camera actor
	camera_binding = sequence.add_spawnable_from_instance(camera)
	
	# Add a cine camera component binding using the component of the camera actor
	camera_component_binding = sequence.add_possessable(camera.get_cine_camera_component())
	camera_component_binding.set_parent(camera_binding)

	return camera_component_binding



def add_tracks(camera_component_binding, clipboardData):
	fovKeys = clipboardData.fov
	transformKeys = clipboardData.transform

	camera_component_binding.set_display_name(clipboardData.cameraName)

	# Add a focal length track
	focal_length_track = camera_component_binding.add_track(unreal.MovieSceneFloatTrack)
	focal_length_track.set_property_name_and_path('FOV', 'CurrentFocalLength')
	focal_length_section = focal_length_track.add_section()
	focal_length_section.set_range(clipboardData.startFrame, clipboardData.endFrame)

	channel = focal_length_section.find_channels_by_type(unreal.MovieSceneScriptingFloatChannel)[0]
	channel.set_default(45.0)
	for fov in fovKeys:
		channel.add_key(unreal.FrameNumber(fov.frame), fov.value)

	# Add a transform track
	camera_transform_track = camera_component_binding.add_track(unreal.MovieScene3DTransformTrack)
	camera_transform_section = camera_transform_track.add_section()
	camera_transform_section.set_range(clipboardData.startFrame, clipboardData.endFrame)

	for tr in transformKeys:
		frame = unreal.FrameNumber(tr.frame)
		value = [tr.px, tr.py, tr.pz, tr.rx, tr.ry, tr.rz]
		for i in range(len(value)):
			chanel =  camera_transform_section.get_channels()[i]
			chanel.add_key(time=frame, new_value=value[i])



def create_sequence(name="Sequence"):
	sequence = unreal.AssetToolsHelpers.get_asset_tools().create_asset(
							name,
							'/Game/',
							unreal.LevelSequence,
							unreal.LevelSequenceFactoryNew()
				)
	return sequence



def create_camera():
	location = unreal.Vector(0,0,0)
	rotation = unreal.Rotator(0,0,0)
	newCamera = unreal.EditorLevelLibrary().spawn_actor_from_class(
							unreal.CineCameraActor, location, rotation
				)
	return newCamera



def setup_sequence(sequence, start, end, fps):
	frame_rate = unreal.FrameRate(numerator=fps, denominator=1)
	sequence.set_display_rate(frame_rate)
	sequence.set_playback_start(start + 1)
	sequence.set_playback_end(end + 1)



def paste_camera_from_clipboard():
	cbca = ClipboardCameraAnimation()
	cbca.read_clipboard()
	camera = create_camera()
	sequence = create_sequence(name=cbca.sequenceName)
	camera_component_binding = bind_camera_to_sequence(camera, sequence)
	setup_sequence(sequence, cbca.startFrame, cbca.endFrame, cbca.frameRate)
	add_tracks(camera_component_binding, cbca)



if __name__ == "__main__":
	paste_camera_from_clipboard()