###########################################################################
#	BsMax, Tool for excahnge data between Blender, 3Dsmax and Unreal engine
#	Copyright (C) 2023  Naser Merati (Nevil)
#
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

import unreal

def spawn_selected_asset():
    utilty_base = unreal.GlobalEditorUtilityBase.get_default_object()
    for assetPath in utilty_base.get_selected_assets():
        asset_path = assetPath.get_path_name()
        bp_class= unreal.EditorAssetLibrary.load_asset(asset_path)
        unreal.EditorLevelLibrary.spawn_actor_from_object(
            bp_class,
            unreal.Vector(0,0,0)
        )


if __name__ == "__main__":
    spawn_selected_asset()
