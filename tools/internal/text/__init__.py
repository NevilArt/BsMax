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
# 2025/10/14

from bpy.app import version

from .console import register_console, unregister_console
from .info import register_info, unregister_info
from .text_editor import register_text_editor, unregister_text_editor

if version < (5, 0, 0):
	from .arabic import register_arabic, unregister_arabic


def register_text():
	register_console()
	register_info()
	register_text_editor()

	if version < (5, 0, 0):
		register_arabic()


def unregister_text():
	unregister_console()
	unregister_info()
	unregister_text_editor()

	if version < (5, 0, 0):
		unregister_arabic()
