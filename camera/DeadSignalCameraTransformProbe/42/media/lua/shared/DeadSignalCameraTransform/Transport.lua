local Transport = {}
Transport.__index = Transport
Transport.MAGIC = 32
Transport.MAX_PAN = 0.35
Transport.MAX_YAW = math.pi
Transport.MAX_PITCH = math.pi * 80 / 180

local channels = {"Blur", "Radius", "Desat", "Darkness"}

local function finite(value)
    return type(value) == "number" and value == value and math.abs(value) < math.huge
end

local function read_values(field)
    return {field:getExterior(), field:getTargetExterior(), field:getInterior(), field:getTargetInterior()}
end

local function restore_values(field, values)
    field:setExterior(values[1])
    field:setTargetExterior(values[2])
    field:setInterior(values[3])
    field:setTargetInterior(values[4])
end

function Transport.new(search_mode, player_index)
    assert(search_mode, "SearchMode is required")
    assert(player_index == 0, "The transform probe supports local player zero only")
    return setmetatable({search_mode = search_mode, player_index = player_index}, Transport)
end

-- Restore only the four borrowed visual channels. Never change search enable or override flags.
function Transport:release()
    if not self.saved then return true end
    local saved = self.saved
    local failed = false
    for i = 1, #channels do
        local ok = pcall(restore_values, saved[i].field, saved[i].values)
        if not ok then failed = true end
    end
    if failed then return false, "Search-mode restoration failed" end
    self.saved = nil
    return true
end

-- Pan is a fraction of viewport width/height, positive right/down. Angles are radians.
-- The client must call release on pause, text entry, player replacement and menu return.
function Transport:apply(state, blocked)
    if blocked then
        self:release()
        return false, "Camera input is blocked"
    end
    if type(state) ~= "table" or not finite(state.pan_x) or not finite(state.pan_y)
        or not finite(state.yaw) or not finite(state.pitch)
        or math.abs(state.pan_x) > self.MAX_PAN or math.abs(state.pan_y) > self.MAX_PAN
        or math.abs(state.yaw) > self.MAX_YAW or math.abs(state.pitch) > self.MAX_PITCH then
        self:release()
        return false, "Transform values are outside the probe limits"
    end

    local mode = self.search_mode
    local ok, player_mode = pcall(function()
        local player = mode:getSearchModeForPlayer(self.player_index)
        if mode:isEnabled(self.player_index) or player:isShaderEnabled()
            or mode:isOverride(self.player_index) or mode:isOverrideSearchManager(self.player_index) then
            return nil
        end
        return player
    end)
    if not ok or not player_mode then
        self:release()
        return false, "Search mode is active or unavailable"
    end

    local success, reason = pcall(function()
        if not self.saved then
            local saved = {}
            for i = 1, #channels do
                local field = player_mode["get" .. channels[i]](player_mode)
                saved[i] = {field = field, values = read_values(field)}
            end
            local blur = saved[1].values
            if (blur[1] > 31.5 and blur[1] < 32.5) or (blur[3] > 31.5 and blur[3] < 32.5) then
                return "Another transform transport owns these channels"
            end
            self.saved = saved
        end
        -- WeatherShader: SearchMode.x/y, ParamInfo.w and VarInfo.y respectively.
        local encoded = {self.MAGIC + state.pan_x, state.pan_y, state.yaw, state.pitch}
        for i = 1, #channels do self.saved[i].field:setAll(encoded[i]) end
    end)
    if not success or reason then
        self:release()
        return false, reason or "Search-mode transport write failed"
    end
    return true
end

return Transport
