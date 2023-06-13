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


function getmasterandtarget_fn =
(
    masterbone = undefined
    targetbone = undefined
    
    if selection.count == 1 do (
        if classof selection[1] == BoneGeometry or (filterstring (selection[1] as string) "$:")[1] == "Bone" do (
            masterbone = selection[1]
            targetbone = masterbone.children[1]

            while true do (
                if targetbone.children.count == 1 then (
                    targetbone = targetbone.children[1]
                )
                else (
                    exit
                )
            )
        )
    )

    if selection.count == 2 do (
        A = selection[1]
        B = selection[2]

        while true do (
            if A.parent == undefined then (
                exit
            )
            else if A.parent == B then (
                targetbone = selection[1]
                masterbone = selection[2]
                exit
            )
            else (
                A = A.parent
            )
        )

        while true do (
            if B.parent == undefined then (
                exit
            )
            else if B.parent == A then (
                targetbone = selection[2]
                masterbone = selection[1]
                exit
            )
            else (
                B = B.parent
            )
        )
    )
    
    return #(masterbone, targetbone)
)


function listofbones_fn =
(
    retval = #()
    MT = getmasterandtarget_fn()
    masterbone = MT[1]
    targetbone = MT[2]
    currentbone = masterbone
    
    if masterbone != undefined and targetbone != undefined do (
        while true do (
            if currentbone.children[1] != targetbone then (
                append retval currentbone
                currentbone = currentbone.children[1]
            )
            else (
                append retval currentbone
                append retval targetbone
                exit
            )
        )
    )
    
    return retval
)


function make_ik_stretchable =
(	
	IKS = (for i in selection where classof i == IK_Chain_Object collect i)
	
    for i in IKS do (
		mode = ""
		if i.transform.controller[1] as string == "SubAnim:Swivel_Angle" do (
            mode = "HIK"
        )
		
        if i.transform.controller[1] as string == "SubAnim:Twist_Start_Angle" do (
            mode = "SPIK"
        )

        if mode == "HIK" then (
			select #(i.transform.controller.startJoint, i.transform.controller.endJoint)
			Mybone = listofbones_fn()
			-- XreftoXYZ_fn Mybone
			bsize = #()
            orig = 0

            for j = 1 to Mybone.count-1 do (
                append bsize (distance Mybone[j] Mybone[j+1])
            )

            for j = 1 to bsize.count do (
                orig += bsize[j]
            )

            for j = 2 to Mybone.count do (
				mynewcontroller = float_script()
				mynewcontroller.AddNode "start" Mybone[1]
				mynewcontroller.AddNode "end" i
				myscript = "orig = " + orig as string + "\n"
				myscript += "D = distance start.pos end.pos\n"
				myscript += "if D > orig then xpos = " + bsize[j-1] as string + " + ((D - orig)/ "+ (Mybone.count-1) as string +")\n"
				myscript += "else xpos = "  + bsize[j-1] as string
				mynewcontroller.script = myscript
				Mybone[j].transform.controller.FK_Sub_Control.controller.Position.controller.X_Position.controller = mynewcontroller
			)
		) 
		else if mode == "SPIK" then (
			select #(i.transform.controller.startJoint, i.transform.controller.endJoint)
			Mybone = listofbones_fn()
			-- XreftoXYZ_fn Mybone
			myspline = i.transform.controller.startJoint.position.controller.path_constraint.path
			bsize = #()
            orig = curveLength myspline

            for j = 1 to Mybone.count-1 do (
                append bsize (distance Mybone[j] Mybone[j+1])
            )

            for j = 1 to bsize.count do (
                orig += bsize[j]
            )

            for j = 2 to Mybone.count do (
				mynewcontroller = float_script()
				mynewcontroller.AddNode "start" Mybone[1]
				mynewcontroller.AddNode "end" i
				mynewcontroller.AddNode "spline" myspline
				myscript = "orig = " + (orig / 2) as string + "\n"
				myscript += "D = curveLength spline\n"
				myscript += "if D > orig then xpos = " + bsize[j-1] as string + " + ((D - orig)/ "+ (Mybone.count-1) as string +")\n"
				myscript += "else xpos = "  + bsize[j-1] as string
				mynewcontroller.script = myscript
				Mybone[j].transform.controller.FK_Sub_Control.controller.Position.controller.X_Position.controller = mynewcontroller
			)
			
            thepoint = myspline.modifiers[#Spline_IK_Control].helper_list
			addcontroller_fn i "Position_XYZ" undefined
			addcontroller_fn i "Position_Constraint" thepoint[thepoint.count]
		)
	)
    select IKS
)
make_ik_stretchable()


function clear_transform_controllers =
(
	for obj in selection do (
		local OrigTransform = obj.transform
		try( obj.Transform.controller = prs())catch()
		
        try( obj.pos.controller = Position_XYZ())catch()
        
        try(obj.pos.controller.X_Position.controller = bezier_float ())catch()
        try(obj.pos.controller.Y_Position.controller = bezier_float ())catch()
        try(obj.pos.controller.Z_Position.controller = bezier_float ())catch()
		
        try(obj.rotation.controller = Euler_XYZ())catch()
        
        try(obj.rotation.controller.X_Rotation.controller = bezier_float ())catch()
        try(obj.rotation.controller.Y_Rotation.controller = bezier_float ())catch()
        try(obj.rotation.controller.Z_Rotation.controller = bezier_float ())catch()
		
        try(obj.scale.controller = bezier_scale())catch()
		try(obj.transform = OrigTransform)catch()
	)
)



function spline_control =
(
    -- if selection.count != 1 do (
    --     return False
    -- )

    -- obj = selection[1]

    -- if superclassof obj != shape do (
    --     return False
    -- )

    -- master = obj.baseObject[#Master]
    -- animateVertex obj #all

    -- TMDef = attributes pointTM attribID:#(0x174e3aa5, 0x67203398) \
    --         (parameters data (pos type:#point3; invTM type:#matrix3))

    -- fn getMatricesAlongSplineCurve spl curve count closed: =
    -- (
    --     lastTangent = tangentCurve3D spl curve 0
    --     lastRot = arbAxis lastTangent as quat
    --     step = 1d0 / (count - (if closed then 0 else 1))

    --     for i = 0 to count collect (
    --         location = interpCurve3D spl curve (i * step) pathParam:on
    --         tangent = tangentCurve3D spl curve (i * step) pathParam:on

    --         axis = normalize (cross tangent lastTangent)
    --         theta = acos (dot tangent lastTangent)
    --         rotation = quat theta axis

    --         lastTangent = tangent
    --         lastRot *= rotation
    --         translate (lastRot as matrix3) location
    --     )
    -- )

    -- fn addCtrl subAnim obj pt =
    -- (
    --     ctrl = Point3_Script()
    --     custAttributes.add ctrl TMDef

    --     subAnim.controller = ctrl
    --     ctrl.addObject #pt (NodeTransformMonitor node:pt)
    --     ctrl.addObject #master (NodeTransformMonitor node:obj)
    --     ctrl.script = "if isValidNode pt do this.pos = pt.objectTransform.pos\n" + \
    --         "if isValidNode master do this.invTM = inverse master.objectTransform\n" + \
    --         "this.pos * this.invTM"
    -- )

    -- for spl = 1 to numSplines obj do (
    --     local knotCount = numKnots obj spl
    --     local knotTMs = getMatricesAlongSplineCurve obj spl knotCount closed:(isClosed obj spl)

    --     for knot = 1 to knotCount do (
    --         local knotPos = master["Spline_" + spl as string + "___Vertex_" + knot as string]
    --         local knotInVec = master["Spline_" + spl as string + "___InVec_" + knot as string]
    --         local knotOutVec = master["Spline_" + spl as string + "___OutVec_" + knot as string]

    --         local posPt = in obj Point prefix:"Knot" wirecolor:green cross:on box:off transform:knotTMs[knot]
    --         addCtrl knotPos obj posPt

    --         if getKnotType obj spl knot != #corner do (
    --             addCtrl knotInVec obj (in posPt Point prefix:"Tangent" wirecolor:green cross:off box:off centerMarker:on pos:(knotInVec.value * obj.objectTransform))
    --             addCtrl knotOutVec obj (in posPt Point prefix:"Tangent" wirecolor:green cross:off box:off centerMarker:on pos:(knotOutVec.value * obj.objectTransform))
    --         )
    --     )
    -- )
)



rollout MorpherConnectorRO "Morph Chanel Connector"
(
    local Leftlist = #()
    local RightList = #()

    pickbutton leftpbtn "Pic object"  width:120 height:30 align:#Left autoDisplay:true across:2
    pickbutton rightpbtn "Pic object"  width:120 height:30 align:#Right autoDisplay:true
    listbox leftlb "" width:120 height:30 align:#Left across:2
    listbox Righttlb "" width:120 height:30 align:#Right
    button CLtRbtn ">" width:25 align:#Center offset:[0, -leftlb.height ] tooltip:"Copy Left to Right"
    button CRtLbtn "<"  width:25 align:#Center tooltip:"Copy Right to Left"
    button ILtRbtn ":>"  width:25 align:#Center tooltip:"Instance left to Right"
    button IRtLbtn "<:"  width:25 align:#Center tooltip:"Instance Right to Left"

    function GetMTList Obj =
    (
        hasmorpher = false
        Targets = #()

        for i in Obj.Modifiers do (
            if IsValidMorpherMod i do (
                hasmorpher = true
                break
            )
        )

        if hasmorpher do (
            Local T = #()

            for i = 1 to 100 do (
                if WM3_MC_GetName Obj.morpher i != "- empty -" do (
                    append T #(i, (i as string + ":" + WM3_MC_GetName Obj.morpher i))
                    if T.count >= 10 do ( 
                        join Targets T
                        T = #()
                    )
                )

                if i == 100 do if T.count > 0 do join Targets T
            )
        )
        return Targets
    )
    
    function connector Obj1 Obj2 Ind1 Ind2 Mode =
    (
        if Obj1 != undefined and Obj2 != undefined and Ind1 > 0 and Ind2 > 0 do (
            case Mode of (
                "copy": Obj2.morpher[Ind2].controller = copy Obj1.morpher[Ind1].controller
                "instance": Obj2.morpher[Ind2].controller = Obj1.morpher[Ind1].controller
            )
        )
    )

    on leftpbtn picked obj do
    (
        LeftObj = leftpbtn.object
        if LeftObj != undefined do (
            Leftlist = GetMTList LeftObj
            leftlb.items = for n in Leftlist collect n[2]
        )
    )
    
    on rightpbtn picked obj do
    (
        RightObj = rightpbtn.object
        if RightObj != undefined do (
            RightList = GetMTList RightObj
            Righttlb.items = for n in RightList collect n[2]
        )
    )
    
    on CLtRbtn pressed do (
        connector leftpbtn.object rightpbtn.object leftlb.selection Righttlb.selection "copy"
    )

    on CRtLbtn pressed do (
        connector rightpbtn.object leftpbtn.object Righttlb.selection leftlb.selection "copy"
    )
    
    on ILtRbtn pressed do (
        connector leftpbtn.object rightpbtn.object leftlb.selection Righttlb.selection "instance"
    )
    
    on IRtLbtn pressed do (
        connector rightpbtn.object leftpbtn.object Righttlb.selection leftlb.selection "instance"
    )
)

function morpher_connector =
(
	Createdialog MorpherConnectorRO width:300
)



globaljoystickMode = ""
function get_joy_mode_from_selected_rectangles =
(
    rectangels = #()
    joyMode = undefined

    for rect in selection do (
        if classof rect != rectectangle or rect.children.count > 0 do (
            continue
        )
 
        if rect.width == rect.length then (
            NewMode = "J"
        )
        else if rect.width > rect.Length then (
            if rect.Length > rect.width / 2.0 then (
                NewMode = "J"
            )
            else (
                NewMode = "H"
            )
        )
        else if rect.length > rect.width then (
            if rect.width > rect.length / 2.0 then (
                NewMode = "J"
            )
            else (
                NewMode = "V"
            )
        )

        if joyMode == undefined then (
            joyMode = NewMode
            append rectangels rect
        )
        else if NewMode == joyMode do (
            append rectangels rect
            break
        )

    )

    globaljoystickMode = joyMode

    Return #(joyMode, rectangels)
)



function freeze_transform obj =
(
    -- Frease Position -- 
    obj.pos.controller = Position_List()
    obj.pos.controller.Position_XYZ.controller = bezier_position()
    obj.pos.controller.setname 1 "Frozen Position"
    obj.pos.controller.Available.controller = Position_XYZ()
    obj.pos.controller.setname 2 "Zero Pos XYZ"
    obj.position.controller.SetActive 2

    -- Frease rotation --
    obj.rotation.controller = rotation_list()
    obj.rotation.controller.setname 1 "Frozen Rotation"
    obj.rotation.controller.Available.controller  = Euler_XYZ()
    obj.rotation.controller.setname 2 "Zero Euler XYZ"
)



function set_joystic_limit_controllers this =
(
    joyZero = this.joystick.pos.controller.Zero_Pos_XYZ.controller
    
    joyZero.X_Position.controller = float_limit()
    if this.horizontal then (
        upper_limit = joyZero.X_Position.controller.upper_limit
        upper_limit = 0
        if this.left then (
            upper_limit = this.width - this.cornerRadius * 2 
        )
        else if not this.right then (
            upper_limit = this.width / 2 - this.cornerRadius
        )
      
        lower_limit = joyZero.X_Position.controller.lower_limit
        lower_limit = 0
        if this.right then (
            lower_limit = -(this.width - this.cornerRadius * 2)
        )
        else if not this.left then (
            lower_limit = -(this.width / 2 - this.cornerRadius)
        )
    )

    joyZero.Y_Position.controller = float_limit()
    if this.vertical then (
        upper_limit = joyZero.Y_Position.controller.upper_limit
        upper_limit = 0
        if this.down then (
            upper_limit = this.Length - this.cornerRadius * 2
        )
        else if not this.up then (
            upper_limit = this.Length / 2 - this.cornerRadius
        )
    
        lower_limit = joyZero.Y_Position.controller.lower_limit
        lower_limit = 0
        if this.up then (
            lower_limit = -(this.Length - this.cornerRadius * 2)
        )
        else if not this.down then (
            lower_limit = -(this.Length / 2 - this.cornerRadius)
        )
    )

    joyZero.Z_Position.controller = float_limit()
    joyZero.Z_Position.controller.upper_limit = 0
    joyZero.Z_Position.controller.lower_limit = 0
)


struct MorpherInfo
(
    name = "",
    index = 0,
    function set name index =
    (
        this.name = name
        this.index = index
    )
)


JoysticCustomAttributes = attributes Joystick
(
    parameters params_pr rollout:params_ro
    (
        Up type:#float range:[0.0,100.0,0.0] ui:Usp
        Down type:#float range:[0.0,100.0,0.0] ui:Dsp
        Left type:#float range:[0.0,100.0,0.0] ui:Lsp
        Rigth type:#float range:[0.0,100.0,0.0] ui:Rsp
    )
    
    rollout params_ro "Params"
    ( 
        Global _ME_ = undefined

        function get_btn_pos index colCount btnWidth btnHeight =
        (
            y = floor((index-1)* (1.0/colCount)) * btnHeight + 5
            x = index - (y*colCount) + 5
            return [x, y] as string
        )
    
        function Connectfn Controller Target =
        (
            if _ME_ == undefined or Target == undefined do (
                return False
            )

            Global _TheSpecialTargetNode_ = Target
            hasmorpher = false

            for i in Target.Modifiers do (
                if IsValidMorpherMod i do (
                    hasmorpher = true
                    break
                )
            )
            
            if hasmorpher then (
                morphers = #()

                -- TODO 100 morph is for older 3DsMaxes need a beeter way to newer max
                for i = 1 to 100 do (
                    morpherName = WM3_MC_GetName Target.morpher i

                    if morpherName != "- empty -" do (

                        newMorpfer = MorpherInfo()
                        newM1orpfer.set morpherName i
                        append morphers newM1orpfer
                )
                
                btnWidth = 100
                btnHeight = 23
                windowWidth = morphers.count * (btnWidth + 5)
                colCount = floor(sqrt(morphers.count))

                script = "rollout Connectorro \"Connector\"\n"
                script += "(\n"

                for i = 1 to morphers do (
                    morpher = morphers[i]
                    buttonName = "Btn" + i as string
                    index = morpher.index as string

                    script += "	Button " + buttonName + " "
                    script += "\""+ morpher.name + "\" "
                    script += "width:" + BtnWidth as string + " "
                    script += "pos:" + get_btn_pos i colCount btnWidth btnHeight +"\n"

                    script += "	on " + buttonName + " pressed do\n"
                    script += "	(\n"
                    script += "		" + "_TheSpecialTargetNode_"
                    script += ".morpher[" + index +"].controller = $'"
                    script += _ME_.name + "'.modifiers[#Controller]." + Controller + ".controller\n"
                    script += "		Destroydialog Connectorro\n"
                    script += "	)\n"
                )
              
                script += ")\n"
                script += "createdialog Connectorro width:" + W as string
                execute s
            )
        )

        on params_ro open do (
            if selection.count == 1 do(
                _ME_ = selection[1]
            )
        )

        pickbutton Cubt "Up" width:50 across:2 tooltip:"Connect To.." offset:[-15,0]
        spinner Usp "" type:#float range:[0.0,100.0,0.0] width:70 offset:[-30,3] enabled:false

        pickbutton CDbt "Down" width:50 across:2 tooltip:"Connect To.." offset:[-15,0]
        spinner Dsp "" type:#float range:[0.0,100.0,0.0] width:70 offset:[-30,3] enabled:false

        pickbutton CLbt "Left" width:50 across:2 tooltip:"Connect To.." offset:[-15,0]
        spinner Lsp "" type:#float range:[0.0,100.0,0.0] width:70 offset:[-30,3] enabled:false

        pickbutton CRbt "Right" width:50 across:2 tooltip:"Connect To.." offset:[-15,0] 
        spinner Rsp "" type:#float range:[0.0,100.0,0.0] width:70 offset:[-30,3] enabled:false

        on Cubt picked Targ do Connectfn "up" Targ
        on CDbt picked Targ do Connectfn "down" Targ
        on CLbt picked Targ do Connectfn "left" Targ
        on CRbt picked Targ do Connectfn "rigth" Targ
    )
)



function set_joystic_attribute_holder joy =
(
    AttributeHolder = (EmptyModifier ())
    AttributeHolder.name = "Controller"

    custAttributes.add AttributeHolder JoysticCustomAttributes

    joyPosXYZ = joy.pos.controller.Zero_Pos_XYZ
    -- Up --
    AttributeHolder.Joystick.Up.controller = Float_script()
    theLimit = joyPosXYZ.Y_position.controller.Limits.Upper_Limit
    value = joyPosXYZ.Y_position.controller
    AttributeHolder.Joystick.Up.controller.addTarget "Value" value
    script = "if Value > 0 then (Value / " + theLimit as string + ") * 100 else 0"
    AttributeHolder.Joystick.Up.controller.Script = script

    -- Down --
    AttributeHolder.Joystick.Down.controller = Float_script()
    theLimit = joyPosXYZ.Y_position.controller.Limits.Lower_Limit
    value = joyPosXYZ.Y_position.controller
    AttributeHolder.Joystick.Down.controller.addTarget "Value" value
    script = "if Value < 0 then (Value / " + theLimit as string + ") * 100 else 0"
    AttributeHolder.Joystick.Down.controller.Script = script

    -- Left --
    AttributeHolder.Joystick.Left.controller = Float_script()
    theLimit = joyPosXYZ.X_position.controller.Limits.Lower_Limit
    value = joyPosXYZ.X_position.controller
    AttributeHolder.Joystick.Left.controller.addTarget "Value" value
    script = "if Value < 0 then (Value / " + theLimit as string + ") * 100 else 0"
    AttributeHolder.Joystick.Left.controller.Script = script

    --Right --
    AttributeHolder.Joystick.Rigth.controller = Float_script()
    theLimit = joyPosXYZ.X_position.controller.Limits.Upper_Limit
    value = joyPosXYZ.X_position.controller
    AttributeHolder.Joystick.Rigth.controller.addTarget "Value" value
    script = "if Value > 0 then (Value / " + theLimit as string + ") * 100 else 0"
    AttributeHolder.Joystick.Rigth.controller.Script = script
        
    addModifier joy AttributeHolder 
)


struct JoystickClass
(
    frame = undefined,
    joystick = undefined,
    vertical = False,
    horizontal = False,
    width = 0,
    length = 0,
    cornerRadius = 0,
    left = False,
    right = False,
    up = False,
    down = False,

    function get_orient =
    (
        if this.width == this.length then (
            this.horizontal = True
            this.vertical = True
        )
        else if this.width > this.Length then (
            this.horizontal = True
            this.vertical = this.Length > this.width / 2.0
        )
        else if this.length > this.width then (
            this.vertical = True
            this.horizontal = this.width > this.length / 2.0
        )
    )

    function from_rectangle rect left right up down =
    (
        if classOf rect != Rectangle do (
            return False
        )

        this.frame = rect
        this.width = rect.width
        this.length = rect.length
        this.get_orient()

        if this.horizontal and this.vertical then (
            this.cornerRadius = (this.width + this.length) / 15.0
        )
        else if this.width < this.length then (
            this.cornerRadius = this.width / 2.0 
        )
        else (
            this.cornerRadius = this.length / 2.0
        )

        this.joystick = Circle radius:this.cornerRadius
        this.joystick.transform = this.frame.transform
        this.joystick.parent = this.frame

        xl = if left then this.width / 2.0 - this.cornerRadius else 0
        xr = if right then this.width / 2.0 - this.cornerRadius else 0
        in coordsys this.frame this.joystick.pos.x += xr - xl
        
        yu = if down then this.Length / 2.0 - this.cornerRadius else 0
        yd = if up then this.Length / 2.0 - this.cornerRadius else 0
        in coordsys this.frame this.joystick.pos.Y -= yu - yd

        freeze_transform  this.joystick

        this.left = left
        this.right = right
        this.up = up
        this.down = down

        set_joystic_limit_controllers this
        set_joystic_attribute_holder this.joystick
    )
)


function CreateJoystickfn rects left right up down =
(
    for frame in rects do (
        joystick = JoystickClass()
        joystick.from_rectangle frame left right up down
    )
    destroydialog JoystickCreatorRo
)



rollout JoystickCreatorRo ""
(
    timer clock interval:30
    button ULbt "" width:50 height:50 across:3
    button UCbt "" width:50 height:50
    button URbt "" width:50 height:50
    button MLbt "" width:50 height:50 across:3
    button MCbt "" width:50 height:50
    button MRbt "" width:50 height:50
    button DLbt "" width:50 height:50 across:3
    button DCbt "" width:50 height:50
    button DRbt "" width:50 height:50

    on clock tick do (
        if keyboard.escPressed do (
            destroydialog JoystickCreatorRo
        )
    )
    
    on JoystickCreatorRo open do
    (
        buttons = #()

        -- case joyMode of (
        case globaljoystickMode of (
            "J": (
                Horizontal = true
                Vertival = true
            )
            
            "H": (
                buttons = #(ULbt, UCbt, URbt, DLbt, DCbt, DRbt)
                Horizontal = true
                Vertival = false
            )
            
            "V": (
                buttons = #(ULbt, MLbt, DLbt, URbt, MRbt, DRbt)
                Horizontal = false
                Vertival = true
            )
        )
        
        for b in buttons do (
            b.visible = false
        )
    )

    on ULbt pressed do CreateJoystickfn true false true false
    on UCbt pressed do CreateJoystickfn false false true false
    on URbt pressed do CreateJoystickfn false true true false
    on MLbt pressed do CreateJoystickfn true false false false
    on MCbt pressed do CreateJoystickfn false false false false
    on MRbt pressed do CreateJoystickfn false true false false
    on DLbt pressed do CreateJoystickfn true false false true
    on DCbt pressed do CreateJoystickfn false false false true
    on DRbt pressed do CreateJoystickfn false true false true
)



function create_joystick_creator_dialog = 
(
    if selection.count == 0 do (
        return False
    )

    result = get_joy_mode_from_selected_rectangles()
    joyMode = result[1]
    rectangels = result[2]

    if rectangels.count == 0 do (
        return undefined
    )

    select rectangels
    rect = rectangels[1]
    
    -- Geus Mode --
    Horizontal = false
    Vertival = false
    
    if rect.width == rect.length then (
        joyMode = "J"
    )
    else if rect.width > rect.Length then (
        if rect.Length > rect.width / 2.0 then (
            joyMode = "J"
        )
        else (
            joyMode = "H"
        )
    )
    else if rect.length > rect.width then (
        if rect.width > rect.length / 2.0 then (
            joyMode = "J"
        )
        else (
            joyMode = "V"
        )
    )

    globaljoystickMode = joyMode

    createDialog JoystickCreatorRo width:190 --style:#()
)



rollout MorphargetPicker "Morph Target Picker"
(
    pickbutton pickmasterpbtn "Pick Master" autoDisplay:true width:150
    label Msglb ""
    button selectionorderbtn "By Selection Order" enabled:false width:150
    button Alphbetorcerbtn "By Alphabet Order" enabled:false width:150
    button DistanceOrder "By Distance Order" enabled:false width:150

    function PickMaster Obj =
    (
        if superclassof Obj.baseobject == GeometryClass then (
            pickmasterpbtn.object = Obj
            Msglb.caption = "Select the targets now"
            selectionorderbtn.enabled = true
            Alphbetorcerbtn.enabled = true
            DistanceOrder.enabled = true
        )
        else (
            pickmasterpbtn.object = undefined
            Msglb.caption = "	Pick a Geometry Object"
            selectionorderbtn.enabled = false
            Alphbetorcerbtn.enabled = false
            DistanceOrder.enabled = false
        )
    )

    function AddMorpher obj =
    (
        hasmorpher = false
        for i in pickmasterpbtn.object.Modifiers do (
            if IsValidMorpherMod i do (
                hasmorpher = true 
            )
        )
        if not hasmorpher do (
            addModifier pickmasterpbtn.object (Morpher())
        )
    )

    function NextEmptySlot Obj =
    (
        index = 1
        for i = 100 to 1 by -1 do (
            if WM3_MC_GetTarget Obj.morpher i == undefined do (
                index = i
                break
            )
        )
        return index
    )

    on pickmasterpbtn picked obj do (
        PickMaster Obj
    )
    
    on pickmasterpbtn rightclick do (
        if selection.count == 1 do (
            PickMaster selection[1]
        )
    )
   
    on selectionorderbtn pressed do
    (
        AddMorpher pickmasterpbtn.object
        Targets = #()
        for Sel in selection do (
            append Targets Sel
        )

        for T in Targets do (
            index = NextEmptySlot pickmasterpbtn.object
            WM3_MC_BuildFromNode pickmasterpbtn.object.morpher index T
        )
    )

    on Alphbetorcerbtn pressed do
    (
        AddMorpher pickmasterpbtn.object
        SelectedTargets = #()
        Targets = #()
        Names = #()
        
        for Sel in selection do (
            append SelectedTargets Sel
            append Names Sel.name
        )

        sort Names

        for N in Names do (
            for ST in SelectedTargets do (
                if ST.Name == N do (
                    append Targets ST
                    break
                )
            )
        )

        for T in Targets do (
            index = NextEmptySlot pickmasterpbtn.object
            WM3_MC_BuildFromNode pickmasterpbtn.object.morpher index T
        )
    )

    on DistanceOrder pressed do
    (
        AddMorpher pickmasterpbtn.object
        Targets = #()

        for Sel in selection do (
            append Targets Sel
        )

        for i = 1 to Targets.count do (
            Dist = Distance pickmasterpbtn.object Targets[i]
            index = i
            
            for j = i + 1 to Targets.count do (
                if Distance pickmasterpbtn.object Targets[j] < Dist do (
                    index = j
                )
            )

            if index > i do (
                T = Targets[index]
                DeleteItem Targets index
                InsertItem T Targets i
            )
        )

        for T in Targets do (
            index = NextEmptySlot pickmasterpbtn.object
            WM3_MC_BuildFromNode pickmasterpbtn.object.morpher index T
        )
    )
)



rollout JoystickConnectorro "Joystick Creator"
(
    button Convertobtn "Convert to Joystick" width:150
    button MorphTargetPickerbtn "Morph Target Picker" width:150
    
    on Convertobtn pressed do (
        create_joystick_creator_dialog()
    )

    on MorphTargetPickerbtn pressed do
    (
        createdialog MorphargetPicker
        destroydialog JoystickConnectorro
    )
)



function joystick_creator =
(
	
	-- Analioze the object on scene and cose compatibles for create joysticks --
    result = get_joy_mode_from_selected_rectangles()
    joyMode = result[1]
    rects = result[2]

    if rects.count > 0 then (
        create_joystick_creator_dialog()
    )
	else (
		createdialog JoystickConnectorro
	)
)



function hi_solver =
(   
    if selection.count == 0 do (
        return undefined
    )

    Mybone = listofbones_fn()
    MT = getmasterandtarget_fn()
    masterbone = MT[1]
    targetbone = MT[2]
    
    if masterbone == undefined and targetbone == undefined then (
        parents = (for i in selection where i.children.count == 1 and (filterstring (i.children[1] as string) "$:")[1] == "Bone" collect i)
        IKS = #()

        for i in parents do (
            select i
            Mybone = listofbones_fn()
            MT = getmasterandtarget_fn()
            masterbone = MT[1]
            targetbone = MT[2]

            if masterbone != undefined and targetbone != undefined then (
                local NewIK = IKSys.ikChain masterbone targetbone "IKHISolver"
                try(
                    NewIK.transform.controller.VHTarget = upnode_pb.object
                )
                catch(
                    --pass
                )
                append IKS NewIK
            )
        )
        select IKS
    )
    else (
        NewIK = IKSys.ikChain masterbone targetbone "IKHISolver"
        try(
            NewIK.transform.controller.VHTarget = upnode_pb.object
        )
        catch(
            --pass
        )
        select NewIK
    )
)



-- macroscript TransformHolder tooltip:"Transform Holder" category:"Animation Tools"

rollout TransformHolderRO "Transform Holder"
(
    local Transforms = #(), Objs = #()
    
    button GetTransformbt "Get Selected transform" width:150
    button SetTransformbt "Set Transfrom" width:150

    on GetTransformbt pressed do
    (
        Transforms = #()
        Objs = #()
        for i in selection do (
            append Transforms i.transform
            append Objs i
        )
    )

    on SetTransformbt pressed do (
        for i = 1 to Objs.count do (
            try (
                Objs[i].transform = Transforms[i]
            )
            catch (
                -- Pass
            )
        )
    )
)

function open_transform_holder_dialog =
(
	createdialog TransformHolderRO
)