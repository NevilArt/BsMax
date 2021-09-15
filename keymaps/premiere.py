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
from bsmax.keymaps import KeyMaps



def add_time(km, space):
	km.new(space,'anim.frame_set','HOME','PRESS',[('frame','First')])
	km.new(space,'anim.frame_set','END','PRESS',[('frame','Last')])
	km.new(space,'anim.frame_set','PERIOD','PRESS',[('frame','Next')])
	km.new(space,'anim.frame_set','COMMA','PRESS',[('frame','Previous')])
	km.new(space,'anim.set_key','K','PRESS',[])
	km.new(space,'anim.set_key_filters','K','PRESS',[],ctrl=True,shift=True)
	km.new(space,'anim.keyframe_insert_menu','K','PRESS',[],ctrl=True)
	km.new(space,'anim.keyframe_delete_v3d','K','PRESS',[],alt=True)
	km.new(space,'anim.auto_key_toggle','N','PRESS',[])



def add_side_panel(km, space):
	km.new(space,'wm.context_toggle','LEFT_BRACKET','PRESS',[('data_path','space_data.show_region_toolbar')])
	km.new(space,'wm.context_toggle','RIGHT_BRACKET','PRESS',[('data_path','space_data.show_region_ui')])



def add_search(km, space):
	ver = bpy.app.version
	if ver[0] == 2 and ver[1] < 90:
		km.new(space,'wm.search_menu','X','PRESS',[])
	else:
		km.new(space,'wm.search_menu','X','PRESS',[],ctrl=True,shift=True,alt=True)
		km.new(space,'wm.search_operator','X','PRESS',[])



def sequence_editor(km):
	km.mute('Clip Editor','transform.translate','EVT_TWEAK_L','ANY')
	space = km.space('Sequencer','SEQUENCE_EDITOR','WINDOW')
	add_search(km, space)
	add_side_panel(km, space)
	km.new(space,'wm.multi_item_rename','F2','PRESS',[])

	km.new(space,'sequencer.zoom_extended','Z','PRESS',[])
	km.new(space,'sequencer.mute_toggle','H','PRESS',[])
	km.new(space,'sequencer.shift','UP_ARROW','PRESS',[('direction', 'UP')],alt=True)
	km.new(space,'sequencer.shift','DOWN_ARROW','PRESS',[('direction', 'DOWN')],alt=True)
	km.new(space,'sequencer.shift','RIGHT_ARROW','PRESS',[('direction', 'RIGHT')],alt=True)
	km.new(space,'sequencer.shift','LEFT_ARROW','PRESS',[('direction', 'LEFT')],alt=True)

	km.new(space,'sequencer.select_all','A','PRESS',[('action','SELECT')],ctrl=True)
	km.new(space,'sequencer.select_all','D','PRESS',[('action','DESELECT')],ctrl=True)

	km.new(space,'anim.frame_set','HOME','PRESS',[('frame','First')])
	km.new(space,'anim.frame_set','END','PRESS',[('frame','Last')])
	km.new(space,'anim.frame_set','PERIOD','PRESS',[('frame','Next')])
	km.new(space,'anim.frame_set','COMMA','PRESS',[('frame','Previous')])



km_video_sequencer = KeyMaps()

def register_premiere(preferences):
	if bpy.context.window_manager.keyconfigs.addon:
		if preferences.video_sequencer == 'Premiere':
			sequence_editor(km_video_sequencer)
			km_video_sequencer.register()
		else:
			km_video_sequencer.unregister()

def unregister_premiere():
	km_video_sequencer.unregister()
