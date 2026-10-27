local Orbit = {}

local function finite(value)
    return type(value) == "number" and value == value and math.abs(value) < math.huge
end

function Orbit.new(options)
    options = options or {}
    local view = {
        yaw=options.yaw or 45, pitch=options.pitch or 30, scale=options.scale or 48,
        center_x=options.center_x or 0, center_y=options.center_y or 0,
        pan_x=options.pan_x or 0, pan_y=options.pan_y or 0,
    }
    for _, value in pairs(view) do assert(finite(value), "camera values must be finite") end
    assert(view.scale > 0, "camera scale must be positive")
    assert(view.pitch >= 5 and view.pitch <= 85, "camera pitch must be from 5 to 85 degrees")
    return view
end

-- x/y are horizontal tiles; z is height in tile units, not game floor levels.
function Orbit.project(view, x, y, z)
    local yaw, pitch = math.rad(view.yaw), math.rad(view.pitch)
    local c, s = math.cos(yaw), math.sin(yaw)
    local along = x * s + y * c
    local up = z or 0
    return view.center_x + view.pan_x + (x * c - y * s) * view.scale,
        view.center_y + view.pan_y + (along * math.sin(pitch) - up * math.cos(pitch)) * view.scale,
        along * math.cos(pitch) + up * math.sin(pitch)
end

-- Inverse projection onto one known horizontal plane; does not intersect walls or roofs.
function Orbit.pick(view, screen_x, screen_y, z)
    local yaw, pitch = math.rad(view.yaw), math.rad(view.pitch)
    local across = (screen_x - view.center_x - view.pan_x) / view.scale
    local along = ((screen_y - view.center_y - view.pan_y) / view.scale + (z or 0) * math.cos(pitch)) / math.sin(pitch)
    return across * math.cos(yaw) + along * math.sin(yaw),
        -across * math.sin(yaw) + along * math.cos(yaw)
end

-- Map the whole trimmed sprite rectangle onto its floor plane, preserving its alpha.
-- Native canvas origin is object offset minus sprite soff, normally (32*s, 96*s).
function Orbit.sprite_plane(texture, tile_x, tile_y, tile_scale, origin_u, origin_v, z)
    assert(finite(tile_scale) and tile_scale > 0, "tile scale must be positive")
    local left, top = texture.offset_x or 0, texture.offset_y or 0
    local width, height = texture.width, texture.height
    assert(finite(left) and finite(top) and finite(width) and finite(height) and width > 0 and height > 0,
        "sprite rectangle must be finite with positive dimensions")
    origin_u, origin_v = origin_u or 32 * tile_scale, origin_v or 96 * tile_scale
    local function point(u, v)
        local across = (u - origin_u) / (32 * tile_scale)
        local along = (v - origin_v) / (16 * tile_scale)
        return {x=tile_x + (along + across) / 2, y=tile_y + (along - across) / 2, z=z or 0}
    end
    return {point(left, top), point(left + width, top),
        point(left + width, top + height), point(left, top + height)}
end

-- emit receives eight screen coordinates in TL, TR, BR, BL texture order.
function Orbit.project_plane(view, corners, emit)
    local x1, y1 = Orbit.project(view, corners[1].x, corners[1].y, corners[1].z)
    local x2, y2 = Orbit.project(view, corners[2].x, corners[2].y, corners[2].z)
    local x3, y3 = Orbit.project(view, corners[3].x, corners[3].y, corners[3].z)
    local x4, y4 = Orbit.project(view, corners[4].x, corners[4].y, corners[4].z)
    return emit(x1, y1, x2, y2, x3, y3, x4, y4)
end

return Orbit
