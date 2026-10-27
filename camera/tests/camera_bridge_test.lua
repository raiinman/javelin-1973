local Bridge = sample
local camera = {x=100,y=200,aim_x=15,aim_y=-10,last_x=100,last_y=200}
function camera.getOffX() return camera.x+camera.aim_x end
function camera.getOffY() return camera.y+camera.aim_y end
function camera.getRightClickOffX() return camera.aim_x end
function camera.getRightClickOffY() return camera.aim_y end
function camera.setOffX(x) camera.x=x end
function camera.setOffY(y) camera.y=y end
function camera.setLastOffX(x) camera.last_x=x end
function camera.setLastOffY(y) camera.last_y=y end
local owned = Bridge.apply(camera,30,40)
assert(camera.x==130 and camera.y==240, "native aim must not be doubled")
camera.x,camera.y = 100,200 -- Native center before the next player-update callback.
owned = Bridge.apply(camera,30,40)
assert(camera.x==130 and camera.y==240, "offsets must not accumulate between updates")
Bridge.release(camera,owned)
assert(camera.x==100 and camera.y==200)
owned = Bridge.apply(camera,30,40)
camera.x = 500 -- Another camera owner changed the state.
Bridge.release(camera,owned)
assert(camera.x==500, "release must not overwrite another owner's camera")
