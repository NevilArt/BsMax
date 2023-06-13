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

-- Tepmrary function has to import from a refrence file --
function transformToKey objs startFrame endFrame =
(
    /* bake object transform by key or parent or driver to key
        args:
            objs: array of max objects
            startFrame: Integer
            endFrame: Integer
        return:
            None
    */
    struct transKey (transform, frame, fov, nearclip, farclip, targetDistance)
    struct transformPack (owner, transKeys=#())
    local transformPackes = #()

    /* Store Transform per mesh */
    for obj in Objs do (
        newTransformPack = transformPack()
        newTransformPack.owner = obj
        for frame = startFrame to endFrame do (
            newTranskey = transKey()
            newTranskey.transform = at time frame obj.transform
            newTranskey.frame = frame
            -- Store camera info
            if superClassOf obj == camera do (
                newTranskey.fov = at time frame obj.fov
                newTranskey.nearclip = at time frame obj.nearclip
                newTranskey.farclip = at time frame obj.farclip
                newTranskey.targetDistance = at time frame obj.targetDistance
            )
            append newTransformPack.transKeys newTranskey
        )
        append transformPackes newTransformPack
    )

    /* Clear Obj controller layers */
    for obj in Objs do (
        try(
            obj.Transform.controller = prs()
            obj.pos.controller = Position_XYZ()

            for i = 1 to 3 do
                obj.pos.controller[i].controller = bezier_float()
            obj.rotation.controller = Euler_XYZ()

            for i = 1 to 3 do
                obj.rotation.controller[i].controller = bezier_float()

            obj.scale.controller = bezier_scale()
        )
        catch()
        obj.parent = undefined
    )
    
    /* Clear animation */
    clearSelection()
    select Objs
    maxOps.deleteSelectedAnimation()

    /* Restore transforms */
    for tfp in transformPackes do (
        on animate on (
            for tk in tfp.transKeys do (
                at time tk.frame (
                    tfp.owner.transform = tk.transform
                    if superClassOf tfp.owner == camera do(
                        tfp.owner.fov = tk.fov
                        tfp.owner.nearclip = tk.nearclip
                        tfp.owner.farclip = tk.farclip
                        tfp.owner.targetDistance = tk.targetDistance
                    )
                )
            )
        )
    )
)




function delete_all_helpers =
(
    for obj in objects do (
        if superclassof obj == helper do (
            delete obj
        )
    )
)



function convert_camera =
(
    abcCams = for cam in cameras where classof cam == AlembicCamera collect cam
    newCams = #()
    for cam in abcCams do (
        newCam = Freecamera()
        newCam.parent = cam
        newCam.transform = cam.transform
        append newCams newCam
    )
    transformToKey newCams animationRange.start animationRange.end
    delete abcCams
)



function does_deform obj =
(
    -- there is no sure method yet
    return False
)



function collect_moving_and_static_objects =
(
    movingObjects = #()
    staticObjects = #()
    diformObjects = #()
    for obj in objects do (
        if ClassOf obj.transform.controller == prs then (
            append staticObjects obj
        )
        else if ClassOf obj.transform.controller == AlembicXform do (
            if does_deform obj then (
                append diformObjects obj
            )
            else (
                append movingObjects obj
            )
        )
    )
    return #(movingObjects, staticObjects, diformObjects)
)



function convert_to_mesh objs =
(
    convertToMesh objs
    for obj in objs do (
        obj.renderbylayer = true
    )
)


fn put_objs_in_layer layerName objArray = 
(
    layer = LayerManager.getLayerFromName layerName
    if layer == undefined do (
        layer = LayerManager.newLayer()
        layer.setName layerName
    )

    for obj in objArray do (
        layer.addnode obj
    )    
)


function layer_arangment movingObjects staticObjects diformObjects =
(
    put_objs_in_layer "EnvProxy" staticObjects
    put_objs_in_layer "Charlayout" movingObjects
    put_objs_in_layer "PropLayout" diformObjects
    put_objs_in_layer "Camera" cameras
)

function abc_from_blender =
(
    delete_all_helpers()
    convert_camera()
    
    objGroups = collect_moving_and_static_objects()
    movingObjects = objGroups[1]
    staticObjects = objGroups[2]
    diformObjects = objGroups[3]
    
    transformToKey movingObjects animationRange.start animationRange.end
    convert_to_mesh movingObjects
    convert_to_mesh staticObjects

    layer_arangment movingObjects staticObjects diformObjects
)

-- TEST
abc_from_blender()