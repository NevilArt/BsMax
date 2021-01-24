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

from .align_objects import register_align_objects, unregister_align_objects
from .coordinate import register_coordinate, unregister_coordinate
from .mirror import register_mirror, unregister_mirror
from .snap import register_snap, unregister_snap
from .transform_control import register_transform_control, unregister_transform_control
from .transforms import register_transforms, unregister_transforms
from .transform_type_in import register_transform_type_in, unregister_transform_type_in
from .zoom_extended import register_zoom_extended, unregister_zoom_extended

def register_transform(preferences):
	register_align_objects()
	register_coordinate()
	register_mirror()
	register_snap()
	register_transform_control()
	register_transforms(preferences)
	register_transform_type_in()
	register_zoom_extended()

def unregister_transform():
	unregister_align_objects()
	unregister_coordinate()
	unregister_mirror()
	unregister_snap()
	unregister_transform_control()
	unregister_transforms()
	unregister_transform_type_in()
	unregister_zoom_extended()