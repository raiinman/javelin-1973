local Sample = {}

function Sample.collect(cell, x, y, z, radius, north_flag, west_flag)
    assert(type(radius) == "number" and radius >= 0 and radius <= 8 and radius == math.floor(radius), "radius must be an integer from 0 to 8")
    local result = {x=math.floor(x), y=math.floor(y), z=math.floor(z), boxes={}, loaded=0, floors=0, walls=0}
    local function box(kind, dx, dy, width, height, depth)
        result.boxes[#result.boxes + 1] = {kind=kind, x=dx, z=dy, width=width, height=height, depth=depth}
    end
    for dy = -radius, radius do
        for dx = -radius, radius do
            local square = cell:getGridSquare(result.x + dx, result.y + dy, result.z)
            if square then
                result.loaded = result.loaded + 1
                if square:getFloor() then
                    box("floor", dx, dy, 0.98, 0.04, 0.98)
                    result.floors = result.floors + 1
                end
                local properties = square:getProperties()
                if properties:has(north_flag) then
                    box("north", dx, dy - 0.5, 1, 1.6, 0.035)
                    result.walls = result.walls + 1
                end
                if properties:has(west_flag) then
                    box("west", dx - 0.5, dy, 0.035, 1.6, 1)
                    result.walls = result.walls + 1
                end
            end
        end
    end
    return result
end

return Sample
