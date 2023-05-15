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

def get_selected_assets():
    utilty_base = unreal.GlobalEditorUtilityBase.get_default_object()
    return utilty_base.get_selected_assets()



def get_asset_selected_materials():
    materials = []
    for asset in get_selected_assets():
        if asset.get_class().get_name() in {
                                        "Material",
                                        "MaterialInstanceConstant"
                                    }:
            materials.append(asset)
    return materials


def set_selected_materials_twosided():
    for matt in get_asset_selected_materials():
        baseMatt = matt.get_editor_property(name='base_property_overrides')    
        baseMatt.set_editor_property('override_two_sided', True)
        baseMatt.set_editor_property('two_sided', True)


if __name__ == "__main__":
    set_selected_materials_twosided()