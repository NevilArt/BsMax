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

from .animation_key import register_animation_key, unregister_animation_key
from .character_lister import register_character_lister, unregister_character_lister
from .driver_fixer import register_driver_fixer, unregister_driver_fixer
from .frame_update import register_frame_update, unregister_frame_update
from .parent import register_parent, unregister_parent
from .pose import register_pose, unregister_pose
from .menu import register_menu, unregister_menu
from .selection_set import register_selection_set, unregister_selection_set
from .time import register_time, unregister_time

def register_animation():
	register_animation_key()
	register_character_lister()
	register_driver_fixer()
	register_frame_update()
	register_parent()
	register_pose()
	register_menu()
	register_selection_set()
	register_time()

def unregister_animation():
	unregister_animation_key()
	unregister_character_lister()
	unregister_driver_fixer()
	unregister_frame_update()
	unregister_menu()
	unregister_pose()
	unregister_parent()
	unregister_selection_set()
	unregister_time()