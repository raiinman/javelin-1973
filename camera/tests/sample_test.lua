local properties = { has = function(self, flag) return flag == "north" end }
local square = { getFloor = function() return {} end, getProperties = function() return properties end }
local visits = 0
local cell = { getGridSquare = function(self, x, y, z)
    visits = visits + 1
    assert(z == 2)
    if x == 100 and y == 200 then return square end
end }
local found = sample.collect(cell, 100.9, 200.1, 2, 1, "north", "west")
assert(visits == 9, "scan must be bounded to the requested neighborhood")
assert(found.loaded == 1 and found.floors == 1 and found.walls == 1)
assert(found.x == 100 and found.y == 200 and found.z == 2)
assert(#found.boxes == 2)
assert(found.boxes[1].x == 0 and found.boxes[1].z == 0, "coordinates must be relative to the sampled anchor")
assert(found.boxes[2].kind == "north")
local before = visits
assert(not pcall(sample.collect, cell, 0, 0, 2, 100, "north", "west"))
assert(visits == before, "invalid radius must fail before accessing the map")
local empty = sample.collect({getGridSquare = function() return nil end}, 0, 0, 2, 0, "north", "west")
assert(empty.loaded == 0 and #empty.boxes == 0, "unloaded squares must be skipped")
