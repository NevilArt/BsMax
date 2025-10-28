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
# 2025/10/15

from bsmax.keymaps import KeyMaps

numpie_keymap = KeyMaps()


def add_key(km):
	# km.mute('3D View Generic', 'view3d.view_persportho', 'NUMPAD_5', 'PRESS')

	spaces = [
		km.space('3D View Generic', 'VIEW_3D', 'WINDOW'),
		km.space('Outliner', 'OUTLINER', 'WINDOW'),
		km.space('Node Editor', 'NODE_EDITOR', 'WINDOW'),
		km.space('Mask Editing', 'NODE_EDITOR', 'WINDOW'),
		km.space('Console', 'CONSOLE', 'WINDOW'),
		km.space('Info', 'INFO', 'WINDOW'),
		km.space('Animation Channels', 'EMPTY', 'WINDOW'),
		km.space('Graph Editor', 'GRAPH_EDITOR', 'WINDOW'),
		km.space('Dopesheet', 'DOPESHEET_EDITOR', 'WINDOW'),
		km.space('NLA Editor', 'NLA_EDITOR', 'WINDOW'),
		km.space('Clip Editor', 'CLIP_EDITOR', 'WINDOW'),
		km.space('Image Generic', 'IMAGE_EDITOR', 'WINDOW'),
		km.space('UV Editor', 'EMPTY', 'WINDOW'),
		km.space('Sequencer', 'SEQUENCE_EDITOR', 'WINDOW'),
		km.space('Spreadsheet Generic', 'SPREADSHEET', 'WINDOW'),
		km.space('File Browser', 'FILE_BROWSER', 'WINDOW')
	]

	for space in spaces:
		km.new(
			space, 'wm.call_menu_pie', 'NUMPAD_5', 'PRESS',
			[('name', 'BSMAX_MT_pie_view3d_object_main')],
		)
	

	space = km.space('3D View Generic', 'VIEW_3D', 'WINDOW')
	km.new(space, 'screen.numpad_override', 'NUMPAD_0', 'PRESS', [("key", "0")])
	km.new(space, 'screen.numpad_override', 'NUMPAD_1', 'PRESS', [("key", "1")])
	km.new(space, 'screen.numpad_override', 'NUMPAD_2', 'PRESS', [("key", "2")])
	km.new(space, 'screen.numpad_override', 'NUMPAD_3', 'PRESS', [("key", "3")])
	km.new(space, 'screen.numpad_override', 'NUMPAD_4', 'PRESS', [("key", "4")])
	km.new(space, 'screen.numpad_override', 'NUMPAD_5', 'PRESS', [("key", "5")])
	km.new(space, 'screen.numpad_override', 'NUMPAD_6', 'PRESS', [("key", "6")])
	km.new(space, 'screen.numpad_override', 'NUMPAD_7', 'PRESS', [("key", "7")])
	km.new(space, 'screen.numpad_override', 'NUMPAD_8', 'PRESS', [("key", "8")])
	km.new(space, 'screen.numpad_override', 'NUMPAD_9', 'PRESS', [("key", "9")])


def register_keymaps():
	global numpie_keymap
	add_key(numpie_keymap)
	numpie_keymap.register()


def unregister_keymaps():
	global numpie_keymap
	numpie_keymap.unregister()


if __name__ == '__main__':
	register_keymaps()