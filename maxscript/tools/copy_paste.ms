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



function open_copy_dialog =
(
    createdialog CopyDialogRo width:110 style:#()
)


function open_paste_dialog =
(
	createdialog PasteDialogRo width:110 style:#()
)