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


rollout TransformToKeyro "Transform2Key" width:152 height:120
(
    groupBox grpb01 "Time" pos:[8,8] width:136 height:64 align:#left
    spinner Fromsp "From: " type:#integer range:[-999999, 999999, 0] pos:[16,24] width:105 height:16 align:#left
    button Frombtn "G" pos:[120,24] width:16 height:16 align:#left tooltip:"Get Current time"
    spinner Tosp "   To: " type:#integer range:[-999999, 999999, 0] pos:[16,48] width:106 height:16 align:#left
    button Tobtn "G" pos:[120,48] width:16 height:16 align:#left tooltip:"Get Current time"
    groupBox grpb02 "" pos:[8,72] width:136 height:40 align:#left
    button Bakebtn "Bake Transform" pos:[16,88] width:100 height:16 align:#left
    button Aboutbtn "?" pos:[120,88] width:16 height:16 align:#left

    function Updatefn =
    (
        Fromsp.value = (filterstring (animationRange.start as string) "f")[1] as integer
        Tosp.value = (filterstring (animationRange.end as string) "f")[1] as integer
    )

    on TransformToKeyro open do
    (
        Updatefn()
    )

    on TransformToKeyro lbuttondblclk p do
    (
        Updatefn()
    )

    on Frombtn pressed do
    (
        Fromsp.value = (filterstring (slidertime as string) "f")[1] as integer
    )
    
    on Tobtn pressed do
    (
        Tosp.value = (filterstring (slidertime as string) "f")[1] as integer
    )

    on Bakebtn pressed do undo on
    (
        local StartFrame = Fromsp.value
        local EndFrame = Tosp.value
        local Objs = deepcopy (selection as array)
        local Trans = #()
        for f = StartFrame to EndFrame do (
            at time f (
                local NewTrans = #()
                for o in Objs do
                    append NewTrans o.transform
                append Trans NewTrans
            )
        )
        
        for o in Objs do (
            try(
                o.Transform.controller = prs ()
                o.pos.controller = Position_XYZ ()
                
                for i = 1 to 3 do (
                    o.pos.controller[i].controller = bezier_float()
                )
                
                o.rotation.controller = Euler_XYZ ()
                
                for i = 1 to 3 do (
                    o.rotation.controller[i].controller = bezier_float()
                )
                
                o.scale.controller = bezier_scale ()
            )
            catch()
            o.parent = undefined
        )
        select Objs
        maxOps.deleteSelectedAnimation()
        on animate on (
            for f = StartFrame to EndFrame do
                at time f for i = 1 to Objs.count do (
                    frameCurrent = f + 1 - StartFrame
                    Objs[i].transform = Trans[frameCurrent][i]
                )
        )
    )

    on Aboutbtn pressed do
    (
        rollout Aboutro "About"
        (
            label lbl1 "Transform To Key V02.0.0"
            label lbl2 "Contact The Author: NevilArt@Gmail.Com"
            hyperlink web "Www.NevilArt.BlogSpot.Com" address:"www.nevilart.blogspot.com" offset:[45,0]
        )
        createdialog Aboutro modal:true width:250
    )
)



function open_transform_to_key_dialog =
(
	createdialog TransformToKeyro
)



rollout TimesliderToolro "Time Slider"
(
    local TheList = #()
    local Thefile = maxFilePath + getFilenameFile maxFileName + ".maxtsp"

    listbox Listmlb "" width:140
    button Addbtn "+" width:60 across:2
    button Removebtn "-" width:60
    button previewbtn "<" width:60 across:2
    button Nextbtn ">" width:60
    button Startbtn "|<" width:35 across:3
    button allbtn "||" width:35
    button endbtn ">|" width:35

    on TimesliderToolro resized size do
    (
        TimesliderToolro.width = 162
        Listmlb.height = size.y - 89 
        Addbtn.pos = [17, size.y - 78]
        Removebtn.pos = [85, size.y - 78]
        previewbtn.pos = [17, size.y - 52]
        Nextbtn.pos = [85, size.y - 52]
        Startbtn.pos = [18, size.y - 26]
        allbtn.pos = [63, size.y - 26]
        endbtn.pos = [108, size.y - 26]
    )		

    function Savefn =
    (
        str = "TheList = #("
        for i = 1 to TheList.count do (
            str += "\"" + TheList[i] + "\""
            if i < TheList.count do str += ","
        )
        str += ")"
        openedfile = openfile Thefile mode:"w"
        format Str to:openedfile
        close openedfile
    )

    on TimesliderToolro open do
    (
        try(TheList = filein Thefile)catch()
        Listmlb.items = TheList
        print TimesliderToolro.height
        print Addbtn.pos
    )

    on Addbtn pressed do 
    (
        appendIfUnique TheList (animationRange.start as string + " " + animationRange.end as string)
        Tarray = #()
        for i = 1 to TheList.count do (
            index = 0
            newitem = TheList[1]

            for j = 1 to TheList.count do (
                Fnum = (filterstring newitem " fF")[1] as integer
                Snum = (filterstring TheList[j] " fF")[1] as integer

                if Snum < Fnum do (
                    newitem = TheList[j]
                    index = j
                )
                
                if Snum == Fnum do (
                    Fnum = (filterstring newitem " fF")[2] as integer
                    Snum = (filterstring TheList[j] " fF")[2] as integer
                    if Snum <= Fnum do (
                        newitem = TheList[j]
                        index = j
                    )
                )
            )

            if index > 0 do (
                append Tarray newitem
                deleteItem TheList index
            )
        )

        join TheList Tarray
        Savefn()
        Listmlb.items = TheList
    )

    on Removebtn pressed do
    (
        try(deleteItem TheList Listmlb.selection)catch()
        Savefn()
        Listmlb.items = TheList
    )

    on Listmlb selected  arg do
    (
        execute ("animationRange = interval " + Listmlb.items[arg])
        redrawViews() 
    )

    on previewbtn pressed do
    (
        if Listmlb.selection > 1 do (
            Listmlb.selection -= 1
        )
        
        if Listmlb.selection > 0 do(
            execute ("animationRange = interval " + Listmlb.items[Listmlb.selection])
        )

        redrawViews() 
    )

    on Nextbtn pressed do
    (
        if Listmlb.selection < Listmlb.items.count do(
            Listmlb.selection += 1
        )

        if Listmlb.selection > 0 do (
            execute ("animationRange = interval " + Listmlb.items[Listmlb.selection])
        )

        redrawViews() 
    )

    function min_fn numa numb = if numa > numb then return numb else return numa
    function max_fn numa numb = if numa < numb then return numb else return numa
 
    function Setrangebykeyfn mode =
    (
        if selection.count == 0 do (
            select $*
        )

        firstkey = at time slidertime trackbar.getPreviousKeyTime()

        if firstkey != undefined do(
            firstkey = firstkey  as integer / (4800 / framerate)
        )

        lastkey = at time slidertime trackbar.getPreviousKeyTime()
        
        if lastkey != undefined do(
            lastkey = lastkey  as integer / (4800 / framerate)
        )

        basek = trackbar.getPreviousKeyTime()
        startk = basek; anykey = false;

        if basek != undefined  and selection.count != 0 then (
            basek = basek as integer / (4800 / framerate)	
            while true do (
                basek = at time basek trackbar.getPreviousKeyTime() as integer / (4800 / framerate)	
                firstkey = min_fn (firstkey) (basek)
                lastkey = max_fn (lastkey) (basek)
                
                if startk == basek do (
                    exit
                )
            )
        --------------------------------------------------------------------------------	
            firstselectedkey = lastkey
            lastselectedkey = firstkey
            
            for i = 1 to selection.count do (
                ---------------------------------------------------------------------
                keycount = numKeys selection[i].pos.controller
                if keycount > 0 do (
                    mink = keycount
                    maxk = 1
                    
                    for j = 1 to keycount do (
                        if isKeySelected  selection[i].pos.controller j do (
                            if mink > j do mink = j
                            if maxk < j do maxk = j
                            anykey = true
                        )
                    )

                    mint = (getKeyTime (selection[i].pos.controller) mink) as integer / (4800 / framerate)

                    if firstselectedkey > mint do (
                        firstselectedkey = mint
                    )

                    maxt = (getKeyTime (selection[i].pos.controller) maxk) as integer / (4800 / framerate)

                    if lastselectedkey < maxt do (
                        lastselectedkey = maxt
                    )
                )
                -----------------------------------------------------------------------
                keycount = numKeys selection[i].rotation.controller
                if keycount > 0 do (
                    mink = keycount
                    maxk = 1
                    
                    for j = 1 to keycount do (
                        if isKeySelected  selection[i].rotation.controller j do (
                            if mink > j do mink = j
                            if maxk < j do maxk = j
                            anykey = true
                        )
                    )
                    
                    mint = (getKeyTime (selection[i].rotation.controller) mink) as integer / (4800 / framerate)
                    
                    if firstselectedkey > mint do (
                        firstselectedkey = mint
                    )
                    
                    maxt = (getKeyTime (selection[i].rotation.controller) maxk) as integer / (4800 / framerate)
                    
                    if lastselectedkey < maxt do (
                        lastselectedkey = maxt
                    )
                )
                --------------------------------------------------------------------
                keycount = numKeys selection[i].scale.controller
                if keycount > 0 do (
                    mink = keycount
                    maxk = 1
                    
                    for j = 1 to keycount do (
                        if isKeySelected  selection[i].scale.controller j do (
                            if mink > j do mink = j
                            if maxk < j do maxk = j
                            anykey = true
                        )
                    )
                    
                    mint = (getKeyTime (selection[i].scale.controller) mink) as integer / (4800 / framerate)
                    
                    if firstselectedkey > mint do (
                        firstselectedkey = mint
                    )
                    
                    maxt = (getKeyTime (selection[i].scale.controller) maxk) as integer / (4800 / framerate)
                    
                    if lastselectedkey < maxt do (
                        lastselectedkey = maxt
                    )
                )
                ----------------------------------------------------------------------------
            )
            if anykeydo (
                firstkey = firstselectedkey
                lastkey = lastselectedkey
            )
            
            if firstkey == lastkey do (
                lastkey += 1
            )
            --------------------------------------------------------------------------------
        )-- end of iff
        else (
            firstkey = 0
            lastkey = 100
        )
        case mode of (
            "start" : animationrange = interval firstkey animationRange.end
            "end" : animationrange = interval animationRange.start lastkey
            "start & End" : animationrange = interval firstkey lastkey
        )
        animationrange = interval firstkey animationRange.end
    )
    
    on Startbtn pressed do (
        Setrangebykeyfn "start"
    )
    
    on allbtn pressed do (
        Setrangebykeyfn "start & End"
    )
    
    on endbtn pressed do (
        Setrangebykeyfn "end"
    )
)

function open_time_slider_tool_dialog =
(
	createdialog TimesliderToolro style:#(#style_titlebar, #style_border, #style_sysmenu, #style_resizing)
)



function set_slider_time_to_previous_key =
(
	if keyboard.controlPressed then (
        if trackbar.getPreviousKeyTime() != undefined do (
            slidertime = trackbar.getPreviousKeyTime()
        )
    )
	else if keyboard.shiftPressed then (
		newtime = 	slidertime - 5
		if newtime < animationRange.start do (
            animationrange = interval newtime animationRange.end
        )
		slidertime -= 5
	)
	else if keyboard.altPressed then (
        animationrange = interval slidertime animationRange.end
    )
	else (
		newtime = slidertime - 1
		if newtime < animationRange.start then (
            slidertime = animationRange.end
        )
		else (
            slidertime -= 1
        )
	)
)

function set_slider_time_to_next_key =
(
	
	if keyboard.controlPressed then (
        if trackbar.getnextKeyTime() != undefined do (
            slidertime = trackbar.getnextKeyTime()
        )
    )
	else if keyboard.shiftPressed then
	(
		newtime = 	slidertime + 5
		if newtime > animationRange.end do (
            animationrange = interval animationRange.start newtime
        )
		slidertime += 5
	)
	else if keyboard.altPressed then (
        animationrange = interval animationRange.start slidertime
    )
	else (
		newtime = slidertime + 1
		if newtime > animationRange.end then (
            slidertime = animationRange.start
        )
		else (
            slidertime += 1
        )
	)
)



function hide_bone_toggle =
(
    hideByCategory.bones = not hideByCategory.bones
)



rollout CameraTools "Time Cam Tools"
(
    SceneCameras = #()
    TimeSliderList = #()
    
    group "Camera"
    (
        dropdownlist CamsDDL ""
        button SelectCambtn "Sel. Camera" width:68 offset:[1,0] across:2 tooltip:"Select the Camera only"
        button SelectTargbtn "Sel. Target" width:68 offset:[2,0] tooltip:"Select the Target only"
        button SelCamTargbtn "Select Camera & Target" width:140 tooltip:"Select the Camera and the target"
        button FlatCamerabtn "Horizon" width:140 tooltip:"Flat the camera in horizon"
        button FOV45btn "F.O.V. 45" width:140 tooltip:"Camera F.O.V. = 45"
    )
    Group "Time Slider"
    (
        listbox Listmlb "" width:140 offset:[-2,0]
        edittext Nameet width:140 offset:[-4,0]
        button Addbtn "+" width:30 across:4 tooltip:"Add current frame range to list"
        button Removebtn "-" width:30 tooltip:"Remove selected preset from list"
        button previewbtn "<" width:30 tooltip:"Previews frame range"
        button Nextbtn ">" width:30 tooltip:"Next frame range"
    )
    button aboutbtn "About" width:155 height:15

    function TimeSliderSavefn = -- Time slider
    (
        Local Holder = $TimeSliderPresetHolder
        -- not exist make a new one --
        if Holder == undefined do (
            Holder = Point pos:[0,0,0] isSelected:off Box:false cross:false axistripod:false centermarker:false name:"TimeSliderPresetHolder"
            TSPHCA = attributes TimeSliderPresetHolderCustomAttribute
            (
                parameters Param
                (
                    TimeSliderPresetList type:#stringTab tabSizeVariable:true
                )
                rollout Roll "Holder"
                (
                    label lbl "This Node is a Data Holder"
                )
            )
            custAttributes.add Holder TSPHCA
        )
        if TimeSliderList.count > 0 then (
            Holder.TimeSliderPresetList = TimeSliderList -- put data on holder node --
        )
        else if Holder != undefined do (
            delete Holder
        )
    )

    function Loadfn =
    (
        Local Holder = $TimeSliderPresetHolder
        if Holder != undefined then (
            try (
                TimeSliderList = Holder.TimeSliderPresetList as array
            )
            catch (
                TimeSliderList = #()
            )
        )
        else (
            TimeSliderList = #()
        )
    )

    function Updatefn =
    (
        -- reset values ---------------------------------------------------------
        SceneCameras = #()
        TimeSliderList = #()
        -- Camera tools ----------------------------------------------------------
        CamNames = #()
        for C in Cameras do (
            if superclassof C == camera do (
                append SceneCameras C
                append CamNames C.name
            )
        )
        CamsDDL.Items = CamNames
        -- Time Slider -----------------------------------------------------------
        Loadfn()
        Listmlb.items = TimeSliderList
    )
    --------------------------------------------------------------------------------------------------------------------------------------
    function GetTarget cam = try(cam.target)catch(Updatefn())4

    function SmartDetect str =
    (
        local num = str as integer, IsCommand = false
        if str != "" do (
            if num != undefined then (
                slidertime = num
                IsCommand = true
            )
            else (
                local nums = filterstring str "-"
                if nums.count == 2 do (
                    local Snum = nums[1] as integer
                    local Enum = nums[2] as integer
                    if Snum != undefined and Enum != undefined do (
                        animationRange = (interval Snum enum)
                        IsCommand = true
                    )
                )
            )
            if str == "<" then (
                animationRange = (interval slidertime animationRange.end)
                IsCommand = true
            )
            else if str == ">" then (
                animationRange = (interval animationRange.start (slidertime + 1))
                IsCommand = true
            )
        )
        return IsCommand
    )

    on CameraTools open do Updatefn()
    on CameraTools lbuttondblclk p do Updatefn()
    -- Camera Events ------------------------------------------------------------------------------------------------------------------------------------------------------------------
    on SelectCambtn pressed do (
        if SceneCameras.count > 0 do (
            try(
                if SceneCameras[CamsDDL.selection] != undefined do (
                    select SceneCameras[CamsDDL.selection]
                )
            )
            catch(
                Updatefn()
            )
        )
    )

    on SelectTargbtn pressed do (
        if SceneCameras.count > 0 do (
            try (
                if SceneCameras[CamsDDL.selection] != undefined do (
                    T = GetTarget SceneCameras[CamsDDL.selection]
                )
                if T != undefined do (
                    select T
                )
            )
            catch (
                Updatefn()
            )
        )
    )
    
    on SelCamTargbtn pressed do 
    (
        if SceneCameras.count > 0 do (
            try (
                if SceneCameras[CamsDDL.selection] != undefined do (
                    T = GetTarget SceneCameras[CamsDDL.selection]
                )
                S = #()
                if SceneCameras[CamsDDL.selection] != undefined do (
                    append S SceneCameras[CamsDDL.selection]
                )
                if T != undefined do (
                    append S T
                )
                select S
            )
            catch (
                Updatefn()
            )
        )
    )
    
    on FlatCamerabtn pressed do 
    (
        if SceneCameras.count > 0 do (
            try (
                local cam = SceneCameras[CamsDDL.selection]
                if cam != undefined do (
                    T = SceneCameras[CamsDDL.selection].target
                )
                
                if T != undefined then (
                    T.pos.z = SceneCameras[CamsDDL.selection].pos.z
                )
                else (
                    disableSceneRedraw() 
                    Tcam = Targetcamera pos:[0,0,0] isSelected:off target:(Targetobject transform:(matrix3 [1,0,0] [0,1,0] [0,0,1] [1,0,0]))
                    Targ = point pos:[0,0,0] isSelected:off
                    Targ.transform = cam.transform
                    Targ.Parent = Cam
                    in coordsys parent Targ.pos = [0,0,-10]
                    Tcam.transform = Cam.transform
                    Tcam.target.transform = Targ.transform
                    Tcam.target.pos.z = Tcam.pos.z
                    Cam.transform = Tcam.transform
                    Delete #(Tcam, Targ)
                    enableSceneRedraw()
                )
            )
            catch (
                Updatefn()
            )
        )
    )

    on FOV45btn pressed do
    (
        if SceneCameras.count > 0 do (
            try (
                if SceneCameras[CamsDDL.selection] != undefined do (
                    SceneCameras[CamsDDL.selection].fov = 45
                )
            )
            catch (
                Updatefn()
            )
        )
    )

    -- Time slider Events ----------------------------------------------------------------------------------------------------------------------------------------------------------
    on Addbtn pressed do 
    (
        local UniqueItem = true, TheNewItem = (animationRange.start as string + " " + animationRange.end as string)

        for t in TimeSliderList do (
            Keys = filterstring t ": "
            if TheNewItem == (Keys[1] + " " + Keys[2]) do ( 
                UniqueItem = false
                break
            )
        )

        if UniqueItem do (
            append TimeSliderList TheNewItem -- append if unique --
        )

        Tarray = #()
        for i = 1 to TimeSliderList.count do (
            index = 0
            newitem = TimeSliderList[1]

            for j = 1 to TimeSliderList.count do (
                Fnum = (filterstring newitem " fF")[1] as integer
                Snum = (filterstring TimeSliderList[j] " fF")[1] as integer

                if Snum < Fnum do (
                    newitem = TimeSliderList[j]
                    index = j
                )

                if Snum == Fnum do (
                    Fnum = (filterstring newitem " fF")[2] as integer
                    Snum = (filterstring TimeSliderList[j] " fF")[2] as integer

                    if Snum <= Fnum do (
                        newitem = TimeSliderList[j]
                        index = j
                    )
                )
            )
            
            if index > 0 do (
                append Tarray newitem
                deleteItem TimeSliderList index
            )
        )

        join TimeSliderList Tarray
        TimeSliderSavefn()
        Listmlb.items = TimeSliderList

        for i = 1 to TimeSliderList.count do (
            Keys = filterstring TimeSliderList[i] ": "
            if TheNewItem == (Keys[1] + " " + Keys[2]) do (
                Listmlb.selection = i
                break
            )
        )
        Nameet.text = ""
    )

    on Removebtn pressed do
    (
        try(deleteItem TimeSliderList Listmlb.selection)catch()
        TimeSliderSavefn()
        Listmlb.items = TimeSliderList
        Nameet.text = ""
    )

    on Listmlb selected arg do
    (
        if arg > 0 do (
            NameSplit = filterstring TimeSliderList[Listmlb.selection] ": "
            if NameSplit.count > 2 then (
                Nameet.text = NameSplit[3]
            )
            else (
                Nameet.text = ""
            )
        )
    )

    on Listmlb doubleClicked arg do
    (
        if arg > 0 do (
            execute ("animationRange = interval " + (filterstring Listmlb.items[arg] ":")[1])
            redrawViews()
        )
    )

    on previewbtn pressed do
    (
        if Listmlb.selection > 1 do (
            Listmlb.selection -= 1
        )

        if Listmlb.selection > 0 do (
            execute ("animationRange = interval " + (filterstring Listmlb.items[Listmlb.selection] ":")[1])
        )

        redrawViews() 
    )

    on Nextbtn pressed do
    (
        if Listmlb.selection < Listmlb.items.count do (
            Listmlb.selection += 1
        )

        if Listmlb.selection > 0 do (
            execute ("animationRange = interval " + (filterstring Listmlb.items[Listmlb.selection] ":")[1])
        )

        redrawViews() 
    )

    on Nameet entered arg do
    (
        if not SmartDetect arg then (
            Sel = Listmlb.selection
            OrigName = filterstring TimeSliderList[Listmlb.selection] ": "
            
            if arg == "" then (
                TimeSliderList[Sel] = OrigName[1] + " " + OrigName[2]
            )
            else (
                TimeSliderList[Sel] = OrigName[1] + " " + OrigName[2] + " : " + arg
            )
            
            Listmlb.items = TimeSliderList
            Listmlb.selection = Sel
            TimeSliderSavefn()
        )
        Nameet.text = ""
    )

    on aboutbtn pressed do
    (
        rollout Aboutro "About"
        (
            label lbl1 "Time And Cam Tool V01.0.2"
            label lbl2 "Contact The Author: NevilArt@Gmail.Com"
            hyperlink web "Www.NevilArt.BlogSpot.Com" address:"www.nevilart.blogspot.com" offset:[45,0]
        )
        createdialog Aboutro modal:true width:250
    )
)

function open_camera_tools_dialog =
(
	createdialog CameraTools
)



rollout catRiggBasrListerRo "Cat Rigg Base Lister"
(
    listbox Blist_lb ""

    on CBC_ro open do
    (
        Barray = #()
        for i in shapes do (
            S = filterstring i.name "_"
            if S.count == 3 do (
                if S[2] == "C" and tolower S[3] == "base" do (
                    append Barray i.name
                )
            )
        )
        Blist_lb.items = Barray
    )

    on Blist_lb selected arg do
    (
        execute("select $" + Blist_lb.selected)
        destroydialog CBC_ro
    )
)

function open_cat_character_base_lister =
(
	createdialog catRiggBasrListerRo
)



function display_silhouate_toggle =
(
	isactivesilhouate = false

    for i in objects do (
        if getCVertMode i do (
            isactivesilhouate = true
            exit
        )
    )

    if isactivesilhouate then (
		for o in geometry do (
            setCVertMode o false
        )
		viewPort.setGridVisibility viewport.activeViewport true
	)
	else (
		for o in geometry do (
            setCVertMode o true
        )
		viewPort.setGridVisibility viewport.activeViewport false
	)

    redrawViews()
)


