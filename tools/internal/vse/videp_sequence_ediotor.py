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
# 2024/08/30

import bpy

from bpy.types import Operator
from bpy.props import EnumProperty, IntProperty
from bpy.utils import register_class, unregister_class

#TODO show/hide isolate ... tools

# scene = bpy.context.scene 
# active_strip = scene.sequence_editor.active_strip
# active_strip.frame_start
# f = scene.frame_current - active_strip.frame_start

# if 0 <= f <= active_strip.frame_duration:
# 	print(f)
# else:
# 	print('Out of strip')


def get_selected_sequences(scene):
	""" check the sequences return true if detect first selected sequence """
	return [
		sequence for sequence in scene.sequence_editor.sequences
			if sequence.select
	]


def sort_by_channel(sequences, invert=False):
	""" Get list of sequence sort by chanel index 
	* sequences: list of sequence
	* invert: invert the direction of sorting to up to down 
	"""
	# get chanel indexes in unique array
	channels, sorted_sequences = [], []
	for sequence in sequences:
		if sequence.channel not in channels:
			channels.append(sequence.channel)
	channels.sort()

	if invert:
		channels.reverse()

	# collect sequences line by line in in ret array
	for channel in channels:
		for sequence in sequences:
			if sequence.channel == channel:
				sorted_sequences.append(sequence)

	return sorted_sequences


def sort_by_start(sequences, invert=False):
	""" Get list of sequence sort by start Frame
	* sequences: list of sequence
	* invert: invert the direction of sorting to end to start
	"""
	# collect start frames in unique array	
	frames, sorted_sequences = [], []

	for sequence in sequences:
		start_frame = sequence.frame_start + sequence.frame_offset_start
		if start_frame not in frames:
			frames.append(start_frame)

	frames.sort()
	if invert:
		frames.reverse()

	# collect sequences line by line in in ret array
	for frame in frames:
		for sequence in sequences:
			start_frame = sequence.frame_start + sequence.frame_offset_start
			if start_frame == frame:
				sorted_sequences.append(sequence)

	return sorted_sequences


def use_side_shift(sequence):
	return sequence.type in {
		'SOUND', 'MOVIE', 'IMAGE', 'COLOR',
		'TEXT', 'ADJUSTMENT', 'SCENE'
	}


class Sequencer_OT_Shift(Operator):
	bl_idname = 'sequencer.shift'
	bl_label = "Shift Sequences"
	bl_description = "Shift selected strips"
	bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

	direction: EnumProperty(
		items=[
			('UP', "Up", "Move selected Sequences to upper empty chanel"),
			('DOWN', "Down", "Move selected Sequences to lower empty chanel"), 
			('LEFT', "Left", "Shift selected Sequences to one frame to Left"),
			('RIGHT', "Right", "Shift selected Sequences to one frame to Right")
		]
	) # type: ignore

	step: IntProperty(
		name="Step Size", min= 1, max= 64, default=1
	) # type: ignore

	def draw(self, _):
		self.layout.prop(self, 'direction')

	def execute(self, ctx):
		sequences = get_selected_sequences(ctx.scene)

		if self.direction == 'UP':
			sequences = sort_by_channel(sequences, invert=True)

		elif self.direction == 'DOWN':
			sequences = sort_by_channel(sequences)

		elif self.direction == 'LEFT':
			sequences = sort_by_start(sequences)

		elif self.direction == 'RIGHT':
			sequences = sort_by_start(sequences, invert=True)

		""" Shift the sequence by given step """
		for sequence in sequences:
			if self.direction == 'UP':
				sequence.channel += self.step

			elif self.direction == 'DOWN':
				sequence.channel -= self.step

			elif self.direction == 'LEFT' and use_side_shift(sequence):
				sequence.frame_start -= self.step

			elif self.direction == 'RIGHT' and use_side_shift(sequence):
				sequence.frame_start += self.step

		return{'FINISHED'}


class Sequencer_OT_Mute_Toggle(Operator):
	bl_idname = 'sequencer.mute_toggle'
	bl_label = "Mute_toggle"
	bl_description = "Mute Strips"
	bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}
	
	def execute(self, ctx):
		sequences = get_selected_sequences(ctx.scene)
		active_strip = ctx.scene.sequence_editor.active_strip

		if active_strip.select:
			state = not active_strip.mute
			for sequence in sequences:
				sequence.mute = state

		return{'FINISHED'}


class Sequencer_OT_Zoom_Extended(Operator):
	bl_idname = 'sequencer.zoom_extended'
	bl_label = "Zoom Extended"
	bl_description = "Zoom Extended"
	bl_options = {'REGISTER', 'INTERNAL'}

	def execute(self, ctx):
		if ctx.selected_sequences:
			bpy.ops.sequencer.view_selected()
		else:
			bpy.ops.sequencer.view_all()
		return{'FINISHED'}


classes = {
	Sequencer_OT_Shift,
	Sequencer_OT_Mute_Toggle,
	Sequencer_OT_Zoom_Extended
}


def register_video_sequence_ediotor():
	for cls in classes:
		register_class(cls)


def unregister_video_sequence_ediotor():
	for cls in classes:
		unregister_class(cls)


if __name__ == '__main__':
	register_video_sequence_ediotor()