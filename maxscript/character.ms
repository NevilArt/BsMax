/*##########################################################################
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
##########################################################################*/


rollout CharacterRenamerro "Character renamer"
(
	edittext Newnameet ""
	button Reaname "Rename"
	function Newnamefn OldName =
	(
		NewName = ""
		Res = findstring OldName "_"
		if Res == undefined then
			NewName = Newnameet.text + "_" + OldName
		else (
			KeepPart = substring OldName Res OldName.count
			NewName = Newnameet.text + KeepPart )
		return NewName
	)
	on Reaname pressed do
	(
		Objs = #()
		if selection.count == 0 then
			Objs = objects as array
		else
			Objs = selection as array
		if Newnameet.text != "" do
			undo on
				for o in Objs do
					o.name = Newnamefn o.name
	)
)

function character_auto_rename =
(
    createdialog CharacterRenamerro
)