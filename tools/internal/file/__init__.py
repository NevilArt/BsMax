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

from .after_effect_exporter import (
	register_after_effect_exporter,
	unregister_after_effect_exporter
)
from .sprite_json_import import (
	register_sprite_json_importer,
	unregister_sprite_json_importer
)



def register_file(preferences):
	register_after_effect_exporter()

	if preferences.experimental:
		register_sprite_json_importer()



def unregister_file():
	unregister_after_effect_exporter()
	unregister_sprite_json_importer()