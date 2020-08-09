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

from .max import register_max, unregister_max
from .blender import register_blender, unregister_blender
from .cinema4d import register_cinema4d, unregister_cinema4d
from .maya import register_maya, unregister_maya
from .modo import register_modo, unregister_modo
from .softimage import register_softimage, unregister_softimage
from .unrealengin import register_unreal, unregister_unreal


def register_keymaps(preferences):
	register_max(preferences)
	register_maya(preferences)
	register_modo(preferences)
	register_blender(preferences)
	register_cinema4d(preferences)
	register_softimage(preferences)
	register_unreal(preferences)

def unregister_keymaps():
	unregister_max()
	unregister_blender()
	unregister_cinema4d()
	unregister_maya()
	unregister_modo()
	unregister_softimage()
	unregister_unreal()