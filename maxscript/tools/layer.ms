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


function hide_by_layer =
(
    for S in Selection do (
        S.layer.on = false
    )
)