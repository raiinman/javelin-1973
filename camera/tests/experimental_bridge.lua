-- Rejected raw-offset research, not part of the distributed runtime.
local Bridge = {}

local function write(camera,x,y)
    camera.setOffX(x)
    camera.setOffY(y)
    camera.setLastOffX(x)
    camera.setLastOffY(y)
end

function Bridge.apply(camera,x,y)
    local base_x = camera.getOffX()-camera.getRightClickOffX()
    local base_y = camera.getOffY()-camera.getRightClickOffY()
    write(camera,base_x+x,base_y+y)
    return {base_x=base_x,base_y=base_y,written_x=camera.getOffX(),written_y=camera.getOffY()}
end

function Bridge.release(camera,owned)
    if not owned then return end
    if math.abs(camera.getOffX()-owned.written_x)<1.1 and math.abs(camera.getOffY()-owned.written_y)<1.1 then
        write(camera,owned.base_x,owned.base_y)
    end
end

return Bridge
