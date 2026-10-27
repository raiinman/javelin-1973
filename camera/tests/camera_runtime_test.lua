require=function(name) return name=="DeadSignalCamera/State" and state_module or bridge_module end
local function event() return {Add=function(callback) return callback end} end
local pause_tick
Events={OnPlayerUpdate=event(),OnMainMenuEnter=event(),OnTickEvenPaused={Add=function(callback) pause_tick=callback end}}
local now,paused,typing,active_players=0,false,false,1
local zoom,direction,pending=1,nil,nil
local core={}
Core={getTileScale=function() return 2 end}
function core:getMinZoom() return 0.5 end
function core:getMaxZoom() return 2 end
function core:getNextZoom(index,step) return (pending or zoom)+step*0.1 end
function core:doZoomScroll(index,step) direction=step end
function core:getZoom() return zoom end
function core:isDoingTextEntry() return typing end
getCore=function() return core end
local player={isDead=function() return false end,getVehicle=function() end}
getSpecificPlayer=function() return player end
getNumActivePlayers=function() return active_players end
isIngameState=function() return true end
isGamePaused=function() return paused end
getTimeInMillis=function() return now end
return function()
    local camera=DeadSignalCamera
    assert(camera.pan==nil and camera.state==nil, "unsupported raw pan must not be offered as a working feature")
    camera:preset("normal")
    assert(camera.zoom_target==1, "normal preset uses static tile scale")
    camera:preset("close")
    now=200
    camera:update(player)
    assert(direction==-1, "close preset uses native zoom in")
    paused=true
    assert(pause_tick, "pause cancellation needs an event that still runs while paused")
    pause_tick()
    assert(camera.zoom_target==nil, "pause cancels unfinished preset")
    paused=false
    typing=true
    direction=nil
    camera:zoom(1)
    assert(direction==nil, "text entry blocks zoom")
    typing=false
    active_players=2
    camera:preset("wide")
    assert(camera.zoom_target==nil, "split-screen does not start zoom job")
    active_players=1
    camera:preset("wide")
    now=400
    camera:update(player)
    assert(direction==1, "wide preset uses native zoom out")
    zoom=2
    now=600
    camera:update(player)
    assert(camera.zoom_target==nil, "preset stops at target")
    zoom,pending,direction=1,1.1,nil
    camera:preset("normal")
    now=800
    camera:update(player)
    assert(direction==-1, "normal preset must reverse pending native zoom even while displayed zoom is still normal")
end
