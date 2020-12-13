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

from .animationkey import register_animationkey, unregister_animationkey
from .character_lister import register_character_lister, unregister_character_lister
from .frameupdate import register_frameupdate, unregister_frameupdate
from .parent import register_parent, unregister_parent
from .pose import register_pose, unregister_pose
from .menu import register_menu, unregister_menu

def register_animation():
	register_animationkey()
	register_character_lister()
	register_frameupdate()
	register_parent()
	register_pose()
	register_menu()

def unregister_animation():
	unregister_animationkey()
	unregister_character_lister()
	unregister_frameupdate()
	unregister_menu()
	unregister_pose()
	unregister_parent()