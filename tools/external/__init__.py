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
# 2024/01/28

from bpy.utils import register_class, unregister_class

from .maxivz_tools.mvztools import (
	MESH_OT_SmartSelectLoop,
	MESH_OT_SmartSelectRing
)

from .spiderwebs import register_spider_web, unregister_spider_web



classes = (
	MESH_OT_SmartSelectLoop,
	MESH_OT_SmartSelectRing
)



def register_external():
	for c in classes:
		register_class(c)

	register_spider_web()



def unregister_external():
	for c in classes:
		unregister_class(c)

	unregister_spider_web()