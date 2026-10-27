local orbit=sample
local function near(actual, expected)
    assert(math.abs(actual - expected) < 0.000001, tostring(actual) .. " differs from " .. tostring(expected))
end

for _, yaw in ipairs({0, 45, 90, 135, 180, 270, 360, -45}) do
    for _, pitch in ipairs({5, 30, 60, 85}) do
        local view = orbit.new({yaw=yaw, pitch=pitch, scale=47, center_x=400, center_y=300, pan_x=37, pan_y=-12})
        for _, point in ipairs({{0,0,0}, {1,2,0}, {-3.25,6.75,2.44949}}) do
            local sx, sy = orbit.project(view, point[1], point[2], point[3])
            local x, y = orbit.pick(view, sx, sy, point[3])
            near(x, point[1]); near(y, point[2])
        end
    end
end

local native = orbit.new({yaw=45, pitch=30, scale=64 * math.sqrt(2)})
local x, y = orbit.project(native, 1, 0, 0)
near(x,64); near(y,32)
x, y = orbit.project(native, 0, 1, 0)
near(x,-64); near(y,32)

-- A trimmed 128x256 floor canvas holds the 128x64 diamond at rows192..256.
local rectangle = orbit.sprite_plane({width=128,height=64,offset_x=0,offset_y=192}, 0, 0, 2)
local called = false
orbit.project_plane(native, rectangle, function(x1,y1,x2,y2,x3,y3,x4,y4)
    called = true
    near(x1,-64); near(y1,0); near(x2,64); near(y2,0)
    near(x3,64); near(y3,64); near(x4,-64); near(y4,64)
end)
assert(called, "projection must pass all four corners to native draw callback")

-- Adjacent tile diamonds share an edge after changing yaw and pitch.
local a = orbit.sprite_plane({width=128,height=64,offset_y=192}, 0, 0, 2)
local b = orbit.sprite_plane({width=128,height=64,offset_y=192}, 1, 0, 2)
local changed = orbit.new({yaw=123,pitch=62,scale=30})
local function midpoint(quad, i, j)
    return orbit.project(changed, (quad[i].x+quad[j].x)/2, (quad[i].y+quad[j].y)/2, 0)
end
local ax, ay = midpoint(a,2,3)
local bx, by = midpoint(b,1,2)
near(ax,bx); near(ay,by)
ax, ay = midpoint(a,3,4)
bx, by = midpoint(b,4,1)
near(ax,bx); near(ay,by)

-- Cropping and custom object offsets must affect geometry, not stretch the tile.
local cropped = orbit.sprite_plane({width=64,height=32,offset_x=32,offset_y=208}, 7, 9, 2)
local cx, cy = orbit.project(native, cropped[1].x-7, cropped[1].y-9, 0)
near(cx,-32); near(cy,16)
local shifted = orbit.sprite_plane({width=64,height=32,offset_x=32,offset_y=208}, 7, 9, 2, 68, 200)
local sx, sy = orbit.project(native, shifted[1].x-7, shifted[1].y-9, 0)
near(sx,-36); near(sy,8)

assert(not pcall(orbit.new, {pitch=0}), "flat horizon cannot support plane picking")
assert(not pcall(orbit.new, {scale=0}), "zero zoom cannot support picking")
assert(not pcall(orbit.new, {yaw=0/0}), "NaN must be rejected")
assert(not pcall(orbit.sprite_plane, {width=0,height=32}, 0,0,2))
