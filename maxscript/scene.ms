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

rollout instancerro "Instancer" width:235
(
    local target = #()

    pickbutton maternodepb "Pick Master" autodisplay:true width:150 pos:[8,8]
    multilistbox targetnodelb "" width:150 height:10 pos:[8,32]
    button addbt "+" width:70 pos:[8,170]
    button removbt "-" width:70 pos:[88,170]
    button findsimillarbt "Find simmilars" width:150 pos:[8,195]
    button makeinstancebt "Make it instance" width:150 pos:[8,220]
    checkbox fcheckcb "Advance" pos:[165,199] tooltip:"Advance check"
    checkbox mattcb "Material" pos:[165,223] tooltip:"apply materials too"

    on maternodepb rightclick do if selection.count == 1 do
    (
        maternodepb.object = selection[1]
        maternodepb.caption = selection[1].name
    )

    on addbt pressed do
    (
        local names = #()
        for i in selection do (
            if i != maternodepb.object do (
                appendifunique target i
            )
        )
        
        for i in target do (
            append names i.name
        )
        
        targetnodelb.items = names
    )
    
    on removbt pressed do
    (
        target = #()
        targetnodelb.items = #()
    )
    
    on findsimillarbt pressed do
    (
        if maternodepb.object != undefined do (
            local names = #()
            target = #()

            if superclassof maternodepb.object == GeometryClass then (
                for i in objects do (
                    if classof i != LinkComposite then (
                        if superclassof i.baseobject == GeometryClass do (
                            if not i.isHidden do (
                                Pface = #{1}
                                Cface = #{1}
                                try (
                                    --## check if poly count > 0 do
                                    if meshop.getNumFaces i.baseobject.mesh == meshop.getNumFaces maternodepb.object.baseobject.mesh do (
                                        if fcheckcb.checked do (
                                            Pface = execute ("#{1.."+ (meshop.getNumFaces maternodepb.object.baseobject.mesh) as string + "}")
                                            Cface = execute ("#{1.."+ (meshop.getNumFaces i.baseobject.mesh) as string + "}")
                                        )
                                    )
                                )
                                catch (
                                    print (">>: " + i.name)
                                ) 

                                try (
                                    if meshop.getFaceArea i.baseobject.mesh Cface == meshop.getFaceArea maternodepb.object.baseobject.mesh Pface do (
                                        if i != maternodepb.object do (
                                            append target i
                                        )
                                    )
                                )
                                catch (
                                    print (">>: " + i.name)
                                )
                            )
                        )
                    )
                )
            )
            else (
                for i in objects do (
                    if classof i == classof maternodepb.object and i != maternodepb.object do (
                        append target i
                    )
                )
            )
            /*else if superclassof maternodepb.object == shape then for i in objects do if classof i == classof maternodepb.object and i != maternodepb.object do append target i
            else if superclassof maternodepb.object == light then ()
            else if superclassof maternodepb.object == camera then ()
            else if superclassof maternodepb.object == helper then ()
            else if superclassof maternodepb.object == SpacewarpObject then ()*/
            for i in target do (
                append names i.name
            )
            targetnodelb.items = names
            select target
        )
    )
    
    on makeinstancebt pressed do (
        if maternodepb.object != undefined do (
            for i in target do (
                i.baseobject = maternodepb.object.baseobject
            )

            if mattcb.checked do (
                for i in target do (
                    i.material = maternodepb.object.material
                )
            )
        )
    )
)


function open_instancer_dialog =
(
	try(destroydialog instancerro)catch()
    createdialog instancerro
)



function arrange_by_distance =
(
    if selection.count < 2 do (
        return undefined
    )

    Obj = Selection
	Local A, B, MD = 0
    A = Obj[1]
    B = Obj[2]

    for i = 1 to Obj.count do (
        for j = i to Obj.count do (
            if Distance Obj[i] Obj[j] > MD do (
                MD = Distance Obj[i] Obj[j]
                A = Obj[i]
                B = Obj[j]
            )
        )
    )

    Local Dis = #(), Sobj = #()

    for i in Obj do (
        append Dis (Distance A i)
    )

    sort Dis

    for i = 1 to Dis.count do (
        for j = 1 to obj.count do (
            if Distance A Obj[j] == Dis[i] do (
                append Sobj Obj[j]
            )
        )
    )

    for i = 2 to (Sobj.count - 1) do (
        Sobj[i].pos = A.pos + (((B.pos - A.pos) / (Sobj.count - 1)) * (i-1))
    )
    
    for i = 2 to (Sobj.count - 1) do (
        Sobj[i].Scale = A.Scale + (((B.Scale - A.Scale) / (Sobj.count - 1)) * (i-1))
    )
    
    local XA,YA,ZA,XB,YB,ZB

    try(XA = A.rotation.controller.X_Rotation)catch(XA = undefined)
    try(YA = A.rotation.controller.Y_Rotation)catch(YA = undefined)
    try(ZA = A.rotation.controller.Z_Rotation)catch(ZA = undefined)
    try(XB = B.rotation.controller.X_Rotation)catch(XB = undefined)
    try(YB = B.rotation.controller.Y_Rotation)catch(YB = undefined)
    try(ZB = B.rotation.controller.Z_Rotation)catch(ZB = undefined)

    if classof XA != UndefinedClass and classof XB != undefined do (
        for i = 2 to (Sobj.count - 1) do (
            Sobj[i].rotation.controller.X_Rotation = XA + ((XB - XA) / (Sobj.count - 1)) * (i - 1)
        )
    )

    if classof YA != UndefinedClass and classof YB != undefined do (
         for i = 2 to (Sobj.count - 1) do (
            Sobj[i].rotation.controller.Y_Rotation = YA + ((YB - YA) / (Sobj.count - 1)) * (i - 1)
         )
    )

    if classof ZA != UndefinedClass and classof ZB != undefined do (
        for i = 2 to (Sobj.count - 1) do (
            Sobj[i].rotation.controller.Z_Rotation = ZA + ((ZB - ZA) / (Sobj.count - 1)) * (i - 1)
        )
    )
)



function arrange_on_shape =
(
	Local S = Selection
	function shapeFilt o = (superClassOf o == Shape)
	
    if S.count > 0 do (
        obj = pickObject message:"Now Get a Shap Object" filter:shapeFilt
    )
	
    if obj != undefined do (
        undo on (
            --## create 2 metjhod for open and close splines ---
            Local pos = point pos:[0,0,0] 
            Pos.pos.controller = Path_Constraint()
            Pos.pos.controller.follow = on
            Pos.pos.controller.path = obj
            for i = 1 to S.count do (	
                Pos.pos.controller.percent = (100.0 / (S.count - 1)) * (i - 1)
                --S[i].pos = Pos.pos
                S[i].transform = Pos.transform
            )
            Delete Pos
        )
    )
)



rollout RootCleanerro "Root Cleaner"
(
    button CustomAttributebtn "" width:150
    button ParticleFlowbtn "" width:150

    on RootCleanerro open do
    (
        CustomAttributebtn.caption = "Clear " + (custAttributes.count rootscene) as string + " CustomAttributes"
        ParticleFlowbtn.caption = "Clear " + (for h in helpers where classof h == Particle_View collect h).count as string + " ParticleViews"
    )
    
    on CustomAttributebtn pressed do
    (
        for i = custAttributes.count rootscene to 1 by -1 do custAttributes.delete rootscene 1
        CustomAttributebtn.caption = "Done"
        
    )
    
    on ParticleFlowbtn pressed do
    (
        Delete (for h in helpers where classof h == Particle_View collect h)
        ParticleFlowbtn.caption = "Done"
    )
)



function open_root_cleaner =
(
	createdialog RootCleanerro
)



rollout GroundPicker "Ground Picker V01.0.0"
(
    local Orig = #()
    
    pickbutton Groundpbtn "Pick Ground" width:150 autodisplay:true
    radiobuttons Posrbtn "Position" labels:#("Pivot", "Min", "Center") align:#left
    radiobuttons Rotrbtn "Rotation" labels:#("Non ", "Normal") align:#left
    checkbox RandRotcb "Random  Rotation"
    spinner Zoffset "Z Offset" type:#worldUnits range:[-99999,99999,0]
    button Applybtn "Apply On selections" width:150
    button Resetbtn "Reset" width:150
    
    function Shot Obj =
    (
        -- Calculate Z offset --
        local ZAdd = 0, OScale = Obj.scale
        case Posrbtn.state of (
            1: ZAdd = 0 + Zoffset.value
            2: ZAdd = Obj.pos.z - Obj.min.z + Zoffset.value
            3: ZAdd = Obj.pos.z - Obj.center.z + Zoffset.value
        )
        -- Calculate Transform
        Hit = intersectray Groundpbtn.object (ray [Obj.pos.x, Obj.pos.y, Groundpbtn.object.max.z] [0,0,-1])
        if Hit != undefined do (
            Zv = Hit.dir
            Yv = [0,0,1]
            Xv = normalize (cross Yv Zv)
            Yv = Normalize (cross Zv Xv)
            T = matrix3 Xv Yv Zv hit.pos
            --TODO Retrive Scale
            -- Apply position --
            case Rotrbtn.state of (
                1: (
                    Obj.pos = T.pos + [0,0,ZAdd]
                )
                
                2: (
                    Obj.transform = T
                    in coordsys local obj.pos.z += ZAdd
                    obj.scale = OScale
                )
            )
            
            if RandRotcb.checked do (
                in coordsys local obj.rotation.z  = (random 0.0 2.5)
            )
        )
    )

    function updatefn =
    (
        disableSceneRedraw() 
        seed 1
        for O in Orig do (
            O[1].transform = O[2]
            Shot O[1]
        )
        enableSceneRedraw()
        Redrawviews()
    )

    on Applybtn pressed do 
    (
        if Groundpbtn.object != undefined and selection.count > 0 do (
            Orig = #()
            for O in selection do (
                if O != Groundpbtn.object do (
                    append Orig #(O, O.transform)
                )
            )
            updatefn()
        )
    )

    on Zoffset changed val do updatefn()
    on Posrbtn changed state do updatefn()
    on Rotrbtn changed state do updatefn()
    on RandRotcb changed state do updatefn()
    on Resetbtn pressed do
    (
        for O in Orig do (
            O[1].transform = O[2] -- reset to original position
        )
    )
)

function open_ground_picker_dialog =
(	
	createdialog GroundPicker width:180
)



rollout CopyDialogRo ""
(
    local Sel = for S in selection collect S

    -- UI ----------------------------------------------------------------------------------
    button Objectbtn "Object(s)" width:100
    button Materialbtn "Material" width:100
    button MultiMaterialbtn "Multi Material" width:100
    button Transformbtn "Transform" width:100
    timer clock "" interval:50

    -- functions ---------------------------------------------------------------------------
    function SaveObj Slot =
    (
        local BufferFile = GetDir #autoback + "\objbuffer" + Slot as string + ".max"
        try (
            saveNodes Sel BufferFile
        )
        catch (
            messagebox "Unable to copy"
        )
        destroydialog Copyro
    )

    function SaveObjMenu =
    (
        return rcMenu MenuBar
        (
            -- UI ----------------------------------------------------------------------
            menuItem Slot01mnu "Slot01"
            menuItem Slot02mnu "Slot02"
            menuItem Slot03mnu "Slot03"
            menuItem Slot04mnu "Slot04"
            menuItem Slot05mnu "Slot05"
            menuItem Slot06mnu "Slot06"
            menuItem Slot07mnu "Slot07"
            menuItem Slot08mnu "Slot08"
            menuItem Slot09mnu "Slot09"
            menuItem Slot10mnu "Slot10"
            menuItem ClearSlotsmnu "Clear All Slots"

            on Slot01mnu picked do SaveObj 1
            on Slot02mnu picked do SaveObj 2
            on Slot03mnu picked do SaveObj 3
            on Slot04mnu picked do SaveObj 4
            on Slot05mnu picked do SaveObj 5
            on Slot06mnu picked do SaveObj 6
            on Slot07mnu picked do SaveObj 7
            on Slot08mnu picked do SaveObj 8
            on Slot09mnu picked do SaveObj 9
            on Slot10mnu picked do SaveObj 10

            on MenuBar open do
            (
                Items = #(
                    Slot01mnu, Slot02mnu, Slot03mnu,
                    Slot04mnu, Slot05mnu, Slot06mnu,
                    Slot07mnu, Slot08mnu, Slot09mnu,
                    Slot10mnu
                )

                for i = 1 to Items.count do (
                    local BufferFile = GetDir #autoback + "\objbuffer" + i as string + ".max"
                    if not doesFileExist BufferFile then (
                        Items[i].text = "Slot" + i as string + "-Empty"
                    )
                    else (
                        Items[i].text = "Slot" + i as string
                    )
                )
            )

            on ClearSlotsmnu picked do 
            (
                for i = 1 to 10 do (
                    deleteFile (GetDir #autoback + "\objbuffer" + i as string + ".max")
                )
                destroydialog Copyro
            )
        )
    )
 
    function SaveMaterial Slot =
    (
        local BufferFile = GetDir #autoback + "\Matbuffer" + Slot as string + ".max"
        -- Save Material on bufer file -----------------------------------------------------------------
        MattPoint = Sphere radius:1 pos:[0,0,0] name:"__materialholdernode__"
        MattPoint.material = Sel[1].material
        try (
            saveNodes MattPoint BufferFile
        )
        catch (
            messagebox "Unable to copy"
        )
        
        delete MattPoint
        
        -- Save material on ram buffer ----------------------------------------------------------------
        Global MaterialRamBuffer = Sel[1].material
        
        -- Save maxfile name on clipbourd buffer -----------------------------------------------------
        setclipboardText (maxfilepath + maxfilename)

        destroydialog Copyro
    )
    
    function save_multiatt =
    (
        function create_matt_carier_box obj =
        (
            tBox = Box pos:[0,0,0] width:1 length:1 height:1
            tBox.name = obj.name
            tBox.material = obj.material
            return tBox
        )

        tBoxes = #()
        scene_objects = for obj in selection where superclassof obj == GeometryClass collect obj

        for obj in scene_objects do (
            append tBoxes (create_matt_carier_box obj)
        )

        select tBoxes

        BufferFile = GetDir #autoback + "\MultiMattbuffer.max"
        try (
            saveNodes tBoxes BufferFile
        )
        catch (
            messagebox "Unable to copy"
        )

        delete tBoxes
        destroydialog Copyro
    )
    
    function SaveMattMenu =
    (
        return rcMenu MenuBar
        (
            -- UI ----------------------------------------------------------------------
            menuItem Slot01mnu "Slot01"
            menuItem Slot02mnu "Slot02"
            menuItem Slot03mnu "Slot03"
            menuItem Slot04mnu "Slot04"
            menuItem Slot05mnu "Slot05"
            menuItem Slot06mnu "Slot06"
            menuItem Slot07mnu "Slot07"
            menuItem Slot08mnu "Slot08"
            menuItem Slot09mnu "Slot09"
            menuItem Slot10mnu "Slot10"
            menuItem ClearSlotsmnu "Clear All Slots"

            on Slot01mnu picked do SaveMaterial 1
            on Slot02mnu picked do SaveMaterial 2
            on Slot03mnu picked do SaveMaterial 3
            on Slot04mnu picked do SaveMaterial 4
            on Slot05mnu picked do SaveMaterial 5
            on Slot06mnu picked do SaveMaterial 6
            on Slot07mnu picked do SaveMaterial 7
            on Slot08mnu picked do SaveMaterial 8
            on Slot09mnu picked do SaveMaterial 9
            on Slot10mnu picked do SaveMaterial 10

            on MenuBar open do
            (
                Items = #(
                    Slot01mnu, Slot02mnu, Slot03mnu,
                    Slot04mnu, Slot05mnu, Slot06mnu,
                    Slot07mnu, Slot08mnu, Slot09mnu,
                    Slot10mnu
                )

                for i = 1 to Items.count do (
                    local BufferFile = GetDir #autoback + "\Matbuffer" + i as string + ".max"

                    caption = "Slot" + i as string
                    if not doesFileExist BufferFile do (
                        caption += "-Empty"
                    )
                    Items[i].text = caption
                )
            )	

            on ClearSlotsmnu picked do
            (
                for i = 1 to 10 do (
                    deleteFile (GetDir #autoback + "\Matbuffer" + i as string + ".max")
                )
                
                destroydialog Copyro
            )
        )
    )

    function CopyTransform =
    (
        setclipboardText (Sel[1].transform as string)
        destroydialog Copyro
    )

    -- Events ------------------------------------------------------------------------------
    on Copyro open do
    (
        if selection.count > 1 do (
            Materialbtn.visible = false
            Transformbtn.visible = false
            -- Copyro.height = 31
        )
    )

    on clock tick do
    (
        if keyboard.escPressed do (
            destroydialog Copyro
        )
    )
        
    on Objectbtn pressed do SaveObj 0
    on Objectbtn rightclick do 
    (
        popUpMenu (SaveObjMenu()) rollout:Pastero
    )
        
    on Materialbtn pressed do SaveMaterial 0

    on Materialbtn rightclick do
    (
        popUpMenu (SaveMattMenu()) rollout:Pastero
    )
        
    on MultiMaterialbtn pressed do save_multiatt()
    on Transformbtn pressed do CopyTransform() -- copy to Clipboard
    on ObjectPropertiesbtn pressed do CopyObjectProperties() -- copy to clipboard
)

function open_copy_dialog =
(
    createdialog CopyDialogRo width:110 style:#()
)



rollout PasteDialogRo ""
(
    local Sel = for S in selection collect S

    -- UI ----------------------------------------------------------------------------------
    button Objectbtn "Object(s)" width:100
    button Materialbtn "Material" width:100
    button MultiMaterialbtn "Multi Material" width:100
    button Transformbtn "Transform" width:100 tooltip:"Hold Ctrl for SubTransform Menue"
    timer clock "" interval:50

    -- Functions ---------------------------------------------------------------------------
    function MergObj Slot =
    (
        local BufferFile = GetDir #autoback + "\objbuffer" + Slot as string + ".max"
        if doesFileExist BufferFile do (
            if keyboard.controlPressed then (
                mergeMAXFile BufferFile #select 
            )
            else (
                pasteobj = xrefs.addNewXRefFile  BufferFile
                merge pasteobj
            )
        )
        destroydialog PasteDialogRo
    )

    function MergeObjMenu =
    (
        return rcMenu MenuBar
        (
            function IsValid Slot = if doesFileExist (GetDir #autoback + "\objbuffer" + Slot as string + ".max") then return true else return false
            function Filter1 = IsValid 1
            function Filter2 = IsValid 2
            function Filter3 = IsValid 3
            function Filter4 = IsValid 4
            function Filter5 = IsValid 5
            function Filter6 = IsValid 6
            function Filter7 = IsValid 7
            function Filter8 = IsValid 8
            function Filter9 = IsValid 9
            function Filter10 = IsValid 10

            menuItem Slot01mnu "Slot01" filter:Filter1
            menuItem Slot02mnu "Slot02" filter:Filter2
            menuItem Slot03mnu "Slot03" filter:Filter3
            menuItem Slot04mnu "Slot04" filter:Filter4
            menuItem Slot05mnu "Slot05" filter:Filter5
            menuItem Slot06mnu "Slot06" filter:Filter6
            menuItem Slot07mnu "Slot07" filter:Filter7
            menuItem Slot08mnu "Slot08" filter:Filter8
            menuItem Slot09mnu "Slot09" filter:Filter9
            menuItem Slot10mnu "Slot10" filter:Filter10
            menuItem ClearSlotsmnu "Clear All Slots"

            on Slot01mnu picked do MergObj 1
            on Slot02mnu picked do MergObj 2
            on Slot03mnu picked do MergObj 3
            on Slot04mnu picked do MergObj 4
            on Slot05mnu picked do MergObj 5
            on Slot06mnu picked do MergObj 6
            on Slot07mnu picked do MergObj 7
            on Slot08mnu picked do MergObj 8
            on Slot09mnu picked do MergObj 9
            on Slot10mnu picked do MergObj 10

            on ClearSlotsmnu picked do
            (
                for i = 1 to 10 do (
                    deleteFile (GetDir #autoback + "\objbuffer" + i as string + ".max")
                )
                destroydialog Copyro
            )
        )
    )

    function LoadMaterial Slot =
    (
        local BufferFile = GetDir #autoback + "\Matbuffer" + Slot as string + ".max"
        
        -- Internal method ------------------------------------------------------------
        local isthisfile = getclipboardText() == (maxfilepath + maxfilename)
        local ismaterial = superclassof MaterialRamBuffer == material
        local notempty = (maxfilepath + maxfilename) != ""
        
        if isthisfile and ismaterial and notempty then (
            undo on Sel.material = MaterialRamBuffer
        )
        
        -- External method ------------------------------------------------------------
        else (
                if doesFileExist BufferFile do (
                -- pasteobj = xrefs.addNewXRefFile  BufferFile
                -- merge pasteobj
                objs = getmaxfileobjectnames BufferFile
                mergeMAXFile BufferFile objs #noRedraw #deleteOldDups quiet:true
                
                undo on (
                    Sel.material = $__materialholdernode__.material
                )
                delete $__materialholdernode__
            )
        )

        destroydialog PasteDialogRo
    )
    
    function loadMultiMaterial =
    (
        local BufferFile = GetDir #autoback + "\MultiMattbuffer.max"
        undo on (
            -- Store Selected object on scene --
            oldSelectionList = for obj in Selection collect obj
            -- Merge Temprary refrence objects --
            mergeMAXFile BufferFile #select #noRedraw #mergeDups #useMergedMtlDups #neverReparent quiet:True
            
            newSelectionList = for obj in Selection collect obj

            -- copy material from refrence objects to scene objects if avalible --
            for sceneObj in oldSelectionList do (
                for refrenceObj in newSelectionList do (
                    if sceneObj.name == refrenceObj.name do (
                        sceneObj.material = refrenceObj.material
                        exit
                    )
                )
            )
        )

        -- Delete tempray refrenced objects --
        delete newSelectionList
        destroydialog PasteDialogRo
    )
    
    function LoadMattMenu =
    (
        return rcMenu MenuBar
        (
            function IsValid Slot = if doesFileExist (GetDir #autoback + "\Matbuffer" + Slot as string + ".max") then return true else return false
            function Filter1 = IsValid 1
            function Filter2 = IsValid 2
            function Filter3 = IsValid 3
            function Filter4 = IsValid 4
            function Filter5 = IsValid 5
            function Filter6 = IsValid 6
            function Filter7 = IsValid 7
            function Filter8 = IsValid 8
            function Filter9 = IsValid 9
            function Filter10 = IsValid 10

            menuItem Slot01mnu "Slot01" filter:Filter1
            menuItem Slot02mnu "Slot02" filter:Filter2
            menuItem Slot03mnu "Slot03" filter:Filter3
            menuItem Slot04mnu "Slot04" filter:Filter4
            menuItem Slot05mnu "Slot05" filter:Filter5
            menuItem Slot06mnu "Slot06" filter:Filter6
            menuItem Slot07mnu "Slot07" filter:Filter7
            menuItem Slot08mnu "Slot08" filter:Filter8
            menuItem Slot09mnu "Slot09" filter:Filter9
            menuItem Slot10mnu "Slot10" filter:Filter10
            menuItem ClearSlotsmnu "Clear All Slots"

            on Slot01mnu picked do LoadMaterial 1
            on Slot02mnu picked do LoadMaterial 2
            on Slot03mnu picked do LoadMaterial 3
            on Slot04mnu picked do LoadMaterial 4
            on Slot05mnu picked do LoadMaterial 5
            on Slot06mnu picked do LoadMaterial 6
            on Slot07mnu picked do LoadMaterial 7
            on Slot08mnu picked do LoadMaterial 8
            on Slot09mnu picked do LoadMaterial 9
            on Slot10mnu picked do LoadMaterial 10

            on ClearSlotsmnu picked do
            (
                for i = 1 to 10 do (
                    deleteFile (GetDir #autoback + "\Matbuffer" + i as string + ".max")
                )
                destroydialog Copyro
            )
        )
    )
    -----------------------------------------------------------------------------------------
    function LoadTransform Mode =
    (
        local Tr = undefined, CB = getclipboardText()
        
        if classof CB == string do (
            if findString CB "(matrix3 [" == 1 and CB[CB.count] == ")" do (
                try(Tr = execute CB)catch()
            )
        )
        
        if Tr != undefined do (
            Case Mode of (
                "transform": (
                    undo on (
                        Selection.transform = Tr
                    )
                )

                "position": (
                    undo on (
                        selection.position = Tr.Position
                    )
                )

                "rotation":(
                    undo on (
                        for sel in selection do (
                            local OrigTr = sel.transform
                            sel.Transform = Tr
                            sel.Position = OrigTr.Position
                            sel.Scale = OrigTr.Scale
                        )
                    )
                )

                "scale": (
                    undo on (
                        selection.Scale = Tr.Scale
                    )
                )
            )
        )

        destroydialog PasteDialogRo
    )

    function LoadTransformMenu =
    (
        return rcMenu menuBar
        (
            menuItem Positionmnu "Position"
            menuItem Rotationmnu "Rotation" 
            menuItem Scalemnu "Scale"

            on Positionmnu picked do
            (
                LoadTransform "position"
            )

            on Rotationmnu picked do
            (
                LoadTransform "rotation"
            )

            on Scalemnu picked do
            (
                LoadTransform "scale"
            )
        )
    )

    -- Events ------------------------------------------------------------------------------
    on clock tick do
    (
        if keyboard.escPressed do (
            destroydialog PasteDialogRo
        )
    )
    on Pastero open do
    (
        if selection.count == 0 then (
            Materialbtn.visible = false
            Transformbtn.visible = false
            -- Pastero.height = 31
        )
        else (
            Materialbtn.visible = true
            Transformbtn.visible = true
            -- Pastero.height = 83
        )

        local Tr = undefined, CB = getclipboardText()
        if classof CB == string do (
            if findString CB "(matrix3 [" == 1 and CB[CB.count] == ")" do (
                try(Tr = execute CB)catch()
            )
        )

        if Tr == undefined then (
            Transformbtn.enabled = false
        )
        else (
            Transformbtn.enabled = true
        )
    )

    on Objectbtn pressed do
    (
        MergObj 0
    )

    on Objectbtn rightclick do
    (
        popUpMenu (MergeObjMenu()) rollout:Pastero
    )
        
    on Materialbtn pressed do
    (
        LoadMaterial 0
    )
    
    on Materialbtn rightclick do
    (
        popUpMenu (LoadMattMenu()) rollout:Pastero
    )
    
    on MultiMaterialbtn pressed do
    (
        loadMultiMaterial()
    )
        
    on Transformbtn pressed do
    (
        LoadTransform "transform"
    )
    
    on Transformbtn rightclick do
    (
        popUpMenu (LoadTransformMenu()) rollout:Pastero
    )
)

function open_paste_dialog =
(
	createdialog PasteDialogRo width:110 style:#()
)




function has_skin Obj =
(
    local result = false
    for m in Obj.modifiers do (
        if classof m == Skin do (
            result = true
            exit
        )
    )
    return result
)

function find_skin Objs =
(
    local result = false
    for o in Objs do (
        if has_skin o do (
            result = true
            exit
        )
    )
    return result
)


function get_master_layer Layer =
(
    Ret = undefined
    while true do (
        LP = Layer.getParent()
        if LP != undefined then (
            Ret = LP
            Layer = LP
        )
        else (
            exit
        )
    )
    return ret
)


function mesh_layer_selector =
(
	meshLayers = #()
	MeshObjs = #()

    -- create a beter method to get all characters
    CatParents = ( for obj in helpers where classof obj == CATParent collect obj )

    for C in CatParents do (
        MasterLayer = get_master_layer C.Layer
        for i = 1 to MasterLayer.getNumChildren() do (
            M = MasterLayer.getChild i
            M.Nodes &objs
            if find_skin objs do (
                append meshLayers M
                exit
            )
        )
    )

    for M in meshLayers do (
        M.Nodes &objs
        join MeshObjs objs
    )

    select MeshObjs
)



function fix_dublicated_names =
(
	names = #()
	for o in objects do (
		for n in names do (
            if o.name == n then (
                o.name = uniquename o.name
                break
            )
        )
		append names o.name
	)
)



function select_my_layer =
(
	local Objs = #()
	for S in Selection do (
		NewObjs = #()
		S.layer.Nodes &NewObjs
		join Objs NewObjs
	)
	select Objs
)



function add_note_modifier =
(
	NoteModifier = (EmptyModifier ())
	NoteModifier.name = "Note"
	addModifier selection NoteModifier 

    ca = attributes addNoteAttribute
	(
		parameters params_pr rollout:params_ro
		(
			note type:#string ui:note_et
		)
		rollout params_ro "Note"
		( 
			edittext note_et "" pos:[-1,3] width:160 height:500
		)
	)

    for i in selection do (
        custAttributes.add i.modifiers[#Note] ca
    )
)



function multi_mesh_cache =
(
    if selection.count == 0 do (
        return undefined
    )

    slidertime = 0
    OrigObjs = selection as array
    NewObjs = #()
    maxOps.CloneNodes OrigObjs cloneType:#instance newNodes:&NewObjs
    select NewObjs
    macros.run "Modifier Stack" "Convert_to_Mesh"
    NewNode = NewObjs[1]

    local OrigTransform = NewNode.transform

    try( NewNode.Transform.controller = prs ())catch()
    try( NewNode.pos.controller = Position_XYZ ())catch()
    try(NewNode.pos.controller.X_Position.controller = bezier_float ())catch()
    try(NewNode.pos.controller.Y_Position.controller = bezier_float ())catch()
    try(NewNode.pos.controller.Z_Position.controller = bezier_float ())catch()

    try(NewNode.rotation.controller = Euler_XYZ ())catch()
    try(NewNode.rotation.controller.X_Rotation.controller = bezier_float ())catch()
    try(NewNode.rotation.controller.Y_Rotation.controller = bezier_float ())catch()
    try(NewNode.rotation.controller.Z_Rotation.controller = bezier_float ())catch()

    try(NewNode.scale.controller = bezier_scale ())catch()
    try(NewNode.transform = OrigTransform)catch()

    NewNode.Parent = Undefined	
    NewNode.transform = OrigTransform
    NewNode.name += "_PCache"
    deleteItem NewObjs 1
    addModifier NewNode (Edit_Poly())
    select NewNode
    setCommandPanelTaskMode #modify
    NewNode.modifiers[#Edit_Poly].AttachList NewObjs
    addModifier NewNode (Edit_Mesh())
    maxOps.CollapseNode NewNode true

    addModifier NewNode (Skin_Wrap())
    NewNode.modifiers[#Skin_Wrap].engine = 0
    NewNode.modifiers[#Skin_Wrap].meshList = OrigObjs
    addModifier NewNode (Point_Cache())
)



global MyScriptpath = getINISetting (getMAXIniFile()) "NevilTools" "LocalScriptPath"

Rollout quicktoolrunner_to "Script Runner V01.3.0"
(
    Global _myfile_, _mydire_

    edittext globalserchtb "" offset:[-4,0] across:2
    edittext localserchtb "" offset:[-2,0]
    listbox Folder_lb "" across:2
    listbox File_lb ""
    Button Change_bt "Change Directory" width:117 offset:[-22,0] across:3 tooltip:"Change the defult folder of script archive"
    Button open_bt "Open Directory" width:117 offset:[-61,0] tooltip:"open selected folder on window explorer"
    checkButton edit_cbt "Edit Script Mode" width:238 offset:[-40,0] tooltip:"if checked script will open in script editor\nif not checked script will run"

    function getfolders_fn =
    (
        _mydire_ = #()
        _mydire_ = getDirectories (MyScriptpath+"*.*")

        for i = 1 to _mydire_.count do (
            _mydire_[i] = substring _mydire_[i] (MyScriptpath.count + 1) (_mydire_[i].count - MyScriptpath.count - 1)
        )

        Folder_lb.items = _mydire_
    )

    function getfiles_fn =
    (
        _myfile_ = #()

        try (
                _myfile_ = getFiles (MyScriptpath + Folder_lb.selected + "\*.ms");
                join _myfile_ (getFiles (MyScriptpath + Folder_lb.selected + "\*.mse"));
                join _myfile_ (getFiles (MyScriptpath + Folder_lb.selected + "\*.mcr"));
                join _myfile_ (getFiles (MyScriptpath + Folder_lb.selected + "\*.mzp"));
            )
        catch (
            -- pass
        )

        for i = 1 to _myfile_.count do (
            _myfile_[i] = filenameFromPath _myfile_[i]
        )

        File_lb.items = _myfile_
    )

    on quicktoolrunner_to open do
    (
        getfolders_fn()
        getfiles_fn()
    )

    on Folder_lb selected arg do
    (
        getfiles_fn()
    )

    on globalserchtb changed str do
    (
        newlist = #()

        for i in _mydire_ do (
            if (findstring i str) != undefined do (
                append newlist i
            )
        )

        Folder_lb.items = newlist
        getfiles_fn()
    )

    on localserchtb changed str do
    (
        newlist = #()

        for i in _myfile_ do (
            if (findstring i str) != undefined do (
                append newlist i
            )
        )

        File_lb.items = newlist
    )

    on File_lb selected arg do
    (
        if edit_cbt.checked then (
            edit (MyScriptpath + Folder_lb.selected+"\\" + File_lb.selected)
        )
        else (
            try (
                filein (MyScriptpath + Folder_lb.selected+"\\" + File_lb.selected)
            )
            catch(
                -- pass
            )
        )
        destroydialog quicktoolrunner_to
    )

    on Change_bt pressed do
    (
        try (
            MyScriptpath = getSavePath()  + "\\"
        )
        catch (
            MyScriptpath = undefined
        )
        
        if MyScriptpath != undefined do (
            setINISetting (getMAXIniFile()) "NevilTools" "LocalScriptPath" MyScriptpath
            getfolders_fn()
            getfiles_fn()
        )
    )

    on open_bt pressed do 
    (
        HiddenDOSCommand ("explorer \""+ MyScriptpath + Folder_lb.selected +"\"")
    )

) -- end of rollout




function open_script_runner_dialog =
(
    if quicktoolrunner_to != undefined and quicktoolrunner_to.isDisplayed do (
        destroyDialog quicktoolrunner_to
    )


    if MyScriptpath == "" then (
		try(
            MyScriptpath = getSavePath()  + "\\"
        )
        catch (
            MyScriptpath = undefined
        )

        if MyScriptpath != undefined do (
			setINISetting (getMAXIniFile()) "NevilTools" "LocalScriptPath" MyScriptpath;
			createdialog quicktoolrunner_to width:500;
		)
	)
	else (
        createdialog quicktoolrunner_to width:500
    )
)



function show_non_xform =
(
    select (for obj in objects where obj.scale != [1, 1, 1] collect obj)
)



function hide_by_layer =
(
    for S in Selection do (
        S.layer.on = false
    )
)