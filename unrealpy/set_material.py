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

def get_selected_actors():
    selected_actors = unreal.EditorLevelLibrary.get_selected_level_actors()
    return selected_actors

def spawn_asset(asset):
    assetPath = asset.get_path_name()
    bp_class= unreal.EditorAssetLibrary.load_asset(assetPath)
    newActor = unreal.EditorLevelLibrary.spawn_actor_from_object(
        bp_class,
        unreal.Vector(0,0,0)
    )
    return newActor

def get_material_index(mattList):
    indexList = []
    for matt in mattList:
        name = matt.get_name()
        digit = name.split('_')[-1]
    
        if digit.isdigit():
            indexList.append(int(digit))
        else:
            return []

    return indexList

def respam_actor(actor):
    pass

def get_asset_selected_materials():
    materials = []
    for asset in get_selected_assets():
        if asset.get_class().get_name() in {
                                        "Material",
                                        "MaterialInstanceConstant"
                                    }:
            materials.append(asset)
    return materials

def sort_material(mattList):
    nameList = [matt.get_name() for matt in mattList]
    nameList.sort()
    newList = []

    for name in nameList:
        for matt in mattList:
            if matt.get_name() == name:
              newList.append(matt)  

    return newList

def set_multi_material_to_selected_actor():
    selected = get_selected_actors()
    actor = selected[0] if len(selected) == 1 else None
    matts = sort_material(get_asset_selected_materials())

    if not actor or not matts:
        return False  

    if actor.get_class().get_name() == "StaticMeshActor":
        component = actor.get_component_by_class()
        asset = component.get_editor_property("static_mesh")
        asset.set_material(0, matts[0])
    
    elif actor.get_class().get_name() == "GeometryCacheActor":
        component = actor.get_component_by_class()
        asset = component.get_editor_property("geometry_cache")
        actorMatts = asset.get_editor_property('materials')
       
        newIDList = get_material_index(actorMatts)

        newMattList = []
        for index in newIDList:
            newMattList.append(matts[index])
        

        if len(newMattList) < len(actorMatts):
            unreal.log("Selected matt Count is less than Slots Count")
            return False
        
        asset.set_editor_property('materials', newMattList)
        actor.destroy_actor()
        spawn_asset(asset)
    
    return True


if __name__ == "__main__":
    set_multi_material_to_selected_actor()
