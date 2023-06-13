/*
    3DsMax to Unreal character exporter pack
    Author Naser Merat (Nevil)
    Update 2023/05/04
*/

/* A class that contains
matt: Material
owner: object that contain the material
id: material ID this material on object]
faceList: List of facec that contains this material
*/
struct mattPack (matt, owner, id, faceList)


function turnBaseobjectToPoly obj =
(
    /* convrt baseobject to editable poly
        args:
            obj: mesh or primitive object
        return:
            None
    */

    WSMs = #()

    for m in obj.modifiers do
        if superclassof m == SpacewarpModifier do
            append WSMs m
    
    for wsm in WSMs do
        deleteModifier obj wsm

    addModifier obj (Edit_Poly()) before:obj.modifiers.count
    maxops.CollapseNodeTo obj obj.modifiers.count on

    for m in WSMs do
        addModifier obj m
)



function getIDs obj =
(
    /* get objects list and return List of IDs used on faces
        args:
            obj: Array of objects
        return:
            Array of IDs as Integer
    */
    IDList = #()
    
    if ClassOf obj.baseobject == Editable_Poly then (
        faceCount = polyop.getNumFaces obj.baseobject
        for index = 1 to faceCount do
            appendIfUnique IDList (polyop.getFaceMatID obj.baseobject index)
    )
    
    -- else if ClassOf obj.baseobject == Editable_Mesh then (
    --     -- faceCount = obj.baseobject.mesh.numFaces
    --     faceCount = meshop.getNumFaces obj.baseobject.mesh
    --     for index = 1 to faceCount do
    --         appendIfUnique IDList (getFaceMatID obj.baseobject index)
    -- )

    else (
        turnBaseobjectToPoly obj
        return getIDs obj
    )

    return IDList
)



function getFaceListFromID obj ID =
(
    /* Collect facelist with given ID number
        args:
            obj: Mesh or Poly Object
            ID: Integer
        return:
            array of integer
    */
    faceList = #()
    
    if ClassOf obj.baseobject == Editable_Poly then (
        faceCount = polyop.getNumFaces obj.baseobject
        for index = 1 to faceCount do
            if polyop.getFaceMatID obj.baseobject index == ID do
                append faceList index
    )
    
    else if ClassOf obj == Editable_Mesh then (
        faceCount = obj.baseobject.mesh.numFaces
        for index = 1 to faceCount do
            if getFaceMatID obj index == ID do
                append faceList index
    )

    else (
    )

    return faceList
)



function setFaceIDs obj faceList newID =
(
    /* change face list to given ID
        Args:
            obj: mesh or poly object
            faceList: integer array
            newID: integer given ID
        return:
            None
    */

    if ClassOf obj.baseobject == Editable_Poly then
        polyop.setFaceMatID obj.baseobject faceList newID 
    
    else if ClassOf obj.baseobject == Editable_Mesh then (
        for index in faceList do
            setFaceMatID obj.baseobject.mesh i newID
        
        update obj
    )

    else (
    )
)



function switchFaceIDs obj oldID newID =
(
    /* switch old face IDs to new ID
        args:
            obj: Poly or Mesh objects
            oldID: integer
            newID: integer
        return:
            None
    */
    faceList = getFaceListFromID obj oldID
    setFaceIDs obj faceList newID
)



function getMaterialByID obj ID =
(
    /* get material of the given ID on object
        ars:
            obj: Poly or Mesh object
            ID: integer
        return:
            Material
    */
    if obj.material == undefined do(
        newMatt = Standardmaterial()
        newMatt.name = obj.name + "_matt"
        newMatt.Diffuse = obj.wirecolor
        return newMatt
    )

    if ClassOf obj.material != Multimaterial do
        return obj.material
    
    for index = 1 to obj.material.materialIDList.count do
        if obj.material.materialIDList[index] == ID do
            return obj.material.materialList[index]
    
    return Undefined
)



function sortObjectsByName objectList =
(
    /* Sort object arry by name alphabetic order
        args:
            objectList: array of objects
        return:
            sorted of the same array
    */

    nameList = sort(for obj in objectList collect obj.name)
    sortedObjList = #()

    /* Slow method but safe in scene with duplicated obj name */
    for objName in nameList do
        for obj in objectList do
            if obj.name == objName do (
                append sortedObjList obj
                exit
            )

    return sortedObjList
)



function sortMaterialsByname materialList =
(
    /* Sort material list by name in alphabetic order
        args:
            materialList: array of material
        return:
            sorted of the same array
    */

    nameList = sort(for matt in materialList collect matt.name)
    sortedMattList = #()

    for mattName in nameList do
        for obj in materialList do
            if obj.name == mattName do (
                append sortedMattList obj
                exit
            )

    return sortedMattList
)



function createMultimaterial matterialList =
(
    /* Create new multi material
        args:
            materialList: aray of materilas
        return:
            Multisubobjectmaterial
    */

    newMatt = Multimaterial()
    newMatt.numsubs = matterialList.count
    for i = 1 to matterialList.count do
        newMatt[i] = matterialList[i]

    return newMatt
)



function getIDOfMaterial multiMatt matt =
(
    /* find ID of given material in multimaterial list
        args:
            multiMatt: Multisubobjectmaterial
            matt: Material
        return:
            integer index of material
            undefined if not found
    */

    for i = 1 to multiMatt.materialList.count do
        if multiMatt[i] == matt do
            return multiMatt.materialIDList[i]

    return undefined
)



function filterSelection =
(
    /*filter selected object and keep only rendeable geometry and meshed
        args:
            None
        return:
            array of objects in mesh or poly
    */

    objList = for obj in selection where \
        superClassOf obj.baseobject == GeometryClass collect obj

    return sortObjectsByName objList
)



function filterCameras =
(
    return for obj in selection where \
        superClassOf obj == camera collect obj
)



function get_selected_camera =
(
    if selection.count == 1 do
        if superClassOf selection[1] == camera do
            return selection[1]
    return undefined
)



function make_unique_double_name_materials mattList =
(
    for i = 1 to mattList.count do
        for j = i+1 to mattList.count do
            if mattList[i].name == mattList[j].name do
                mattList[i].name += "_"
    -- TODO get the last digit if exists
    -- check for next digit
    -- if free rename object
    -- else repeate
)



function collectMaterials objList =
(
    /* collect material and mattpackes
        args:
            objList: Array of objects
        return:
            #(Sorted material Array, Sorted mattPack Array)
    */
    mattList = #()
    mattPackList = #()

    for obj in objList do (
        IDs = getIDs obj
        for ID in IDs do (
            matt = getMaterialByID obj ID
            if matt != undefined do (
                faceList = getFaceListFromID obj ID
                newMattPack = mattPack matt:matt owner:obj id:ID faceList:faceList
                append mattPackList newMattPack
                appendIfUnique mattList matt
            )
        )
    )

    make_unique_double_name_materials mattList
    mattList = sortMaterialsByname mattList
    newMattList = #()
    for matt in mattList do
        appendIfUnique newMattList matt

    return #(newMattList, mattPackList)
)



function setMaterialToObjs objList newMaterial =
(
    /*Set given material to list of object
        args:
            objList: Array of objects
            newMaterial: Material
        return:
            None
    */
    for obj in objList do
        obj.material = newMaterial
)



function rearrangeIDs mattPackList newMultiMaterial =
(
    /* Find material ID in new material and Change Face id inmesh
        args:
            mattPackList: Array of mattPack
            newMultiMaterial: Combine multisubobject Material
        return:
            None
    */
    for pack in mattPackList do (
        newID = getIDOfMaterial newMultiMaterial pack.matt

        if newID != undefined do
            setFaceIDs pack.owner pack.faceList newID

        update pack.owner
    )
)


function cloneMeshes objList =
(
    /* clone the given object list and retuen new objects
        args:
            objList: Array of objects
        return:
            array of new cloned objects
    */
    newList = #()
    maxOps.CloneNodes objList cloneType:#copy newNodes:&newList
    return newList
)


function convertListToMesh objList =
(
    /* Conver selected object to mesh
        args:
            objList: Array of objects
        return:
            None
    */
    convertToMesh objList
    
    -- make sure wsm modifiers collapsed too
    for obj in objList do
        if obj.modifiers.count > 0 do
            maxOps.CollapseNodeTo obj 1 true
)



function turnToMeshObject objs =
(
    /* add turn to mesh modifier if obj type is not mesh
        args:
            objs: array of mesh or poly objects
        return:
            None
    */
    for obj in objs do
        if classOf obj != Editable_mesh do
            addModifier obj (Turn_to_Mesh())
)



function convertListToPoly objList =
(
    /* Conver selected object to mesh
        args:
            objList: Array of objects
        return:
            None
    */
    convertListToMesh objList
    converttopoly objList
)



function combineMeshes meshList =
(
    /* get list of objects and attach them to single object
        args:
            meshList: Array of mesh or poly objects
        return:
            Poly objects
    */

    convertListToMesh meshList
    
    if meshList.count == 0 do
        return Undefined
    
    master = meshList[1]
    for i = meshList.count to 2 by -1 do
        attach master meshList[i]
    
    converttopoly master
    return master
)



function setSkinwrapUp sourceMesh targetMeshes =
(
    /* add a skinwrap modifier to source object and set targets
        args:
            sourceMesh: Object
            targetMeshes: Array of objects
    */
    if sourceMesh == undefined do
        return False

    skinWrap = Skin_Wrap()
    addModifier sourceMesh (skinWrap)
    skinWrap.engine = 1
    skinWrap.falloff = 10
    skinWrap.distance = 0.001
    skinWrap.faceLimit = 1
    skinWrap.threshold = 0.001
    skinWrap.meshList = targetMeshes
    skinWrap.meshDeformOps.reset()
    return True
)


function sceneSetting =
(
    units.SystemType = #Centimeters
    units.displaytype = #metric
    units.MetricType = #Centimeters
)



function comparMultisubObjectMaterial matt1 matt2 =
(
    if matt1.count != matt2.count do
        return false
    
    for i = 1 to matt1.count do
        if matt1[i] != matt2[i] do
            return false

    return true
)



function findInstanceMaretial mattList targMatt =
(
    for matt in mattList do (
        isSame = comparMultisubObjectMaterial matt targMatt
        if isSame do
            return matt
    )
    return targMatt
)



function optimizeSelectionMatewrials =
(
    /* Get all material of selected objects
    Combine all matrials in a multisubobject material for each object sepratly
    set new materail to all objects one by one
    replace old materail IDs with new ID of same material in new material
    args:
        None
    retuen:
        None
    */
    objList = filterSelection()
    newMattList = #()

    for obj in objList do (
        mattDataPack = collectMaterials #(obj)
        mattList = mattDataPack[1]
        mattPackList = mattDataPack[2]
        newMultiMaterial = createMultimaterial mattList
        newMultiMaterial = findInstanceMaretial newMattList newMultiMaterial
        appendIfUnique newMattList newMultiMaterial
        setMaterialToObjs #(obj) newMultiMaterial
        rearrangeIDs mattPackList newMultiMaterial
    )
)



function combineSelectionMaterials =
(
    /* Get all material of selected objects
    Combine all matrials in a multisubobject material
    set new materail to all objects
    replace old materail IDs with new ID of same material in new material
    args:
        None
    retuen:
        None
    */
    objList = filterSelection()
    mattDataPack = collectMaterials objList
    mattList = mattDataPack[1]
    mattPackList = mattDataPack[2]
    newMultiMaterial = createMultimaterial mattList
    setMaterialToObjs objList newMultiMaterial
    rearrangeIDs mattPackList newMultiMaterial
)



function toDeformableSingleMesh =
(
    /* Convert cloneof selected mesh to a single mesh
        skinwrap to orginal objects
        args:
            None
        return:
            None
     */
    selectedObjList = filterSelection()
    newObjList = cloneMeshes selectedObjList
    singleMesh = combineMeshes newObjList
    setSkinwrapUp singleMesh selectedObjList
    
    clearselection()
    if singleMesh != undefined do (
        select singleMesh
        hide selectedObjList
        turnToMeshObject #(singleMesh)
    )  
)



function toMultiDeformableMesh =
(
    /* Convert cloneof selected mesh to a individual meshes
        skinwrap to orginal objects
        args:
            None
        return:
            None
     */
    selectedObjList = filterSelection()
    newObjList = #()

    for obj in selectedObjList do(
        newObj = (cloneMeshes obj)[1]
        convertListToPoly #(newObj)
        setSkinwrapUp newObj #(obj)
        append newObjList newObj
    )

    clearselection()
    select newObjList
    hide selectedObjList

    turnToMeshObject newObjList
)



function hasSkin obj =
(
    /* chack given object has skin modifier or not
        args:
            obj: maxobject
        return:
            boolean
    */
    for m in Obj.modifiers do
        if classof m == Skin do
            return True
    return False
)



function filterSolidMeshes objs =
(
    /* filter given objects with parent but no skin
        artgs:
            objs: array of maxobjects
        return:
            array of maxobjects
    */

    solidObj = #()
    
    for obj in objs do (
        hasParent = obj.parent != undefined
        noSkin = not (hasSkin obj)
        if hasParent and noSkin do
            append solidObj obj
    )

    return solidObj
)


function getRootBone bone =
(
    -- TODO return master root bon of the given bone
    return bone
)



function removeEmptyMeshes objs =
(
    /* delete mesh objects that has no vertecis
        args:
            objs: array of max objects
        return:
            None
    */
    for obj in objs do
        if getNumVerts obj == 0 do
            delete obj
)



function solveNegativeScaleMeshes objs =
(
    for obj in objs do (
        if superclassof obj == GeometryClass do (
            scaleAvrage = obj.scale.x * obj.scale.y * obj.scale.z
            if scaleAvrage < 0 do (
                hasNormalModifier = False

                for m in Obj.modifiers do
                    if classof m == Normalmodifier do(
                        hasNormalModifier =True
                        exit
                    )

                if not hasNormalModifier do
                    addModifier obj (Normalmodifier())
            )
        )
    )
)



function removeHairModifiers objs =
(
    /* remove hair modifoer from selected objects
        args:
            objs: array if max objects
        return:
            None
    */
    for obj in objs do
        for index = 1 to obj.modifiers.count do
            if classof obj.modifiers[index] == HairMod do
                deleteModifier obj index
)



function getCatBoneGizmo catBone =
(
    /* return one of catbone controllers shapes
        args:
            catBone: catBone maxobject
        return:
            Controller shape or undefined
    */
    for obj in catBone.controller.ExtraRigNodes do
        if superClassOf obj == shape do
            return obj

    return undefined
)



function findSkinMeshParent objs =
(
    /* find a suitable parent for skin meshes
        args:
            objs: array of meshobjects
        return:
            maxobject or undefined
    */

    -- find first object with skin modifier
    local skinMesh = undefined
    for obj in objs do (
        if hasSkin obj do (
            skinMesh = obj
            exit
        )
    )
    if skinMesh == undefined do
        return undefined

    -- get skin modifier
    skinMod = undefined
    for modi in skinMesh.modifiers do
        if classof modi == Skin do (
            skinMod = modi
            exit
        )
    if skinMod == undefined do
        return undefined
    
    -- breake if there is no skinbone
    if skinOps.GetNumberBones skinMod == 0 do
        return undefined

    -- get first catbone with controller
    for bone in skinOps.GetBoneNodes skinMod do
        if classof bone == CATBone do (
            firstCatBoneGizmo = getCatBoneGizmo bone
            if firstCatBoneGizmo != undefined do
                return firstCatBoneGizmo
        )

    -- return the root parent of first skin bone
    return getRootBone (skinOps.GetBoneNodes skinMod)[1]
)



function filterUnlinkSkinMeshes objs =
(   
    /* Filter objects that has skin modifier but not parented
        args:
            objs: array of mesh object
        return:
            array of mesh objects
    */
    unLinkSkinMeshes = #()

    for obj in objs do (
        hasSkinMod = hasSkin obj
        hasParent = obj.parent != undefined

        -- Has parent --
        if hasSkinMod and hasParent do (
            isCatBone = ClassOf obj.parent == CATBone
            isHelper = superClassOf obj.parent == helper
            if isCatBone or isHelper do
                append unLinkSkinMeshes obj
        )

        -- No parent --
        if hasSkinMod and (not hasParent) do
            append unLinkSkinMeshes obj
    )

    return unLinkSkinMeshes
)



function get_lens_of_fov fov =
(
    /* calculate lense distance from camera fov
        args:
            fov: camera.fov float
        return:
            float
    */
    return 0.5 * (GetRendApertureWidth() / tan(fov/2.0))
)



/*
# Field format
# line0 = identefyKey
# line1 = camera name
# line2 = scene name
#             0           1         2
# line3 = startFrame, endFrame, frameRate
# line4+ data fields
#   0     1   2   3   4   5   6   7    8
# frame, px, py, pz, rx, ry, rz, fov, lense
*/
function camera_to_clipboard =
(
    cam = get_selected_camera()
    if cam == undefined do
        return undefined
    
    startFrame = (filterstring (animationRange.start as string) "f")[1]
    endFrame = (filterstring (animationRange.end as string) "f")[1]
    fRate = frameRate as string

    /* create header part */
    str = "3DSMAXTOCLIPBOARNEVILDCAMERACOPYPASTDATAVERSION02\n"
    str += cam.name + "\n"
    str += getFilenameFile maxFileName + "\n"
    str += startFrame + "," + endFrame + "," + fRate + "\n"
    
    /* create body part */
    for frame=animationRange.start to animationRange.end do
    (
        str += (filterstring (frame as string) "f")[1] + ","
        
        pos = in coordsys world at time frame cam.transform.position
        str += (pos.x) as string + ","
        str += (-pos.y) as string + ","
        str += (pos.z) as string + ","

        rot = in coordsys world at time frame (cam.transform.rotation as eulerAngles)
        str += (rot.y) as string + "," -- Roll
        str += (rot.x-90) as string + "," -- Pitch
        str += (-rot.z-90) as string + "," -- Yaw

        str += at time frame cam.fov as string + ","
        str += at time frame get_lens_of_fov(cam.fov) as string + "\n"
    )

    setclipboardText(str)
)



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


function autoTransformToKey =
(
    selecteObjs = filterSelection()
    solidObjs = filterSolidMeshes selecteObjs
    parentlesDeformobjs = filterUnlinkSkinMeshes selecteObjs

    removeHairModifiers selecteObjs
    turnToMeshObject selecteObjs
    join solidObjs (filterCameras()) -- add cameras to bake list too --
    transformToKey solidObjs animationRange.start animationRange.end

    newParent = findSkinMeshParent parentlesDeformobjs
    for obj in parentlesDeformobjs do
        obj.parent = newParent

    solveNegativeScaleMeshes selecteObjs

    -- restore selection
    select selecteObjs
    removeEmptyMeshes selecteObjs

    sceneSetting()
)



rollout maxtoUnrealToolPackRo "To Unreal"
(
    -- button mattotimizerBtn "Matt Optimizer" width:160
    button mattIDcombinerBtn "Matt ID Combiner" width:160
    button copyCameraBtn "Copy Camera" width:160
    button toSingleWrapMeshBtn "Single Wrap Mesh" width:160
    button toMultiWrapMeshBtn "Multi Warp Mesh" width:160
    button autoTransformToKeyBtn "Auto Character Fix" width:160

    on mattotimizerBtn pressed do (
        undo on (optimizeSelectionMatewrials())
    )
        
    on mattIDcombinerBtn pressed do (
        undo on (combineSelectionMaterials())
    )

    on copyCameraBtn pressed do (
        undo on (camera_to_clipboard())
    )

    on toSingleWrapMeshBtn pressed do (
        undo on (toDeformableSingleMesh())
    )

    on toMultiWrapMeshBtn pressed do (
        undo on (toMultiDeformableMesh())
    )

    on autoTransformToKeyBtn pressed do (
        undo on (autoTransformToKey())
    )
)
CreateDialog maxtoUnrealToolPackRo width:170


-- execute ("macroScript MaxToUnreal tooltip:\"Max To Unreal\" category:\"Scene Tools\" ( filein \"" + getSourceFileName() +"\" )")