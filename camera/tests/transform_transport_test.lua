local Transport = sample
local function field(seed)
    local f = {exterior = seed, target_exterior = seed + 1, interior = seed + 2, target_interior = seed + 3}
    function f:getExterior() return self.exterior end
    function f:getTargetExterior() return self.target_exterior end
    function f:getInterior() return self.interior end
    function f:getTargetInterior() return self.target_interior end
    function f:setExterior(value) self.exterior = value end
    function f:setTargetExterior(value) self.target_exterior = value end
    function f:setInterior(value) self.interior = value end
    function f:setTargetInterior(value) self.target_interior = value end
    function f:setAll(value)
        self.exterior, self.target_exterior, self.interior, self.target_interior = value, value, value, value
    end
    return f
end
local fields = {Blur = field(0.1), Radius = field(4), Desat = field(0.2), Darkness = field(0.3)}
local player_mode = {shader_enabled = false}
for name, value in pairs(fields) do player_mode["get" .. name] = function() return value end end
function player_mode:isShaderEnabled() return self.shader_enabled end
local mode = {enabled = false, override = false, manager_override = false}
function mode:getSearchModeForPlayer(index) assert(index == 0); return player_mode end
function mode:isEnabled() return self.enabled end
function mode:isOverride() return self.override end
function mode:isOverrideSearchManager() return self.manager_override end

local transport = Transport.new(mode, 0)
local state = {pan_x = 0.2, pan_y = -0.3, yaw = math.pi / 2, pitch = math.pi / 4}
local function restored()
    for name, seed in pairs({Blur = 0.1, Radius = 4, Desat = 0.2, Darkness = 0.3}) do
        local f = fields[name]
        assert(f.exterior == seed and f.target_exterior == seed + 1
            and f.interior == seed + 2 and f.target_interior == seed + 3, name .. " was not restored")
    end
end
assert(transport:apply(state, false))
assert(fields.Blur.exterior == 32.2 and fields.Blur.interior == 32.2)
assert(fields.Radius.exterior == -0.3 and fields.Desat.exterior == state.yaw and fields.Darkness.exterior == state.pitch)
state.pan_x = -0.35
assert(transport:apply(state, false), "Repeated updates must retain the original restoration snapshot")
assert(transport:release()); restored()
assert(transport:release(), "Release is idempotent")

for _, reason in ipairs({"pause", "text entry", "menu", "player replacement"}) do
    assert(transport:apply(state, false))
    assert(not transport:apply(state, true), reason .. " must release the transport")
    restored()
end
for _, flag in ipairs({"enabled", "override", "manager_override"}) do
    assert(transport:apply(state, false))
    mode[flag] = true
    assert(not transport:apply(state, false), "Must yield to " .. flag)
    restored()
    assert(mode[flag] == true, "Transport must not change native search flags")
    mode[flag] = false
end
assert(transport:apply(state, false))
player_mode.shader_enabled = true
assert(not transport:apply(state, false), "Native search fade also blocks borrowing")
restored()
player_mode.shader_enabled = false

for _, bad in ipairs({0 / 0, math.huge, -math.huge, 0.35001}) do
    assert(transport:apply(state, false))
    local invalid = {pan_x = bad, pan_y = 0, yaw = 0, pitch = 0}
    assert(not transport:apply(invalid, false)); restored()
end
assert(not transport:apply({pan_x = 0, pan_y = 0, yaw = math.pi + 0.01, pitch = 0}, false))
assert(not transport:apply({pan_x = 0, pan_y = 0, yaw = 0, pitch = Transport.MAX_PITCH + 0.01}, false))
restored()
fields.Blur.exterior = 32
assert(not transport:apply(state, false), "Must not steal another sentinel owner's channel")
assert(fields.Blur.exterior == 32)
fields.Blur.exterior = 0.1
assert(not pcall(Transport.new, mode, 1), "Split-screen indices are unsupported")
restored()

local write_all = fields.Radius.setAll
fields.Radius.setAll = function() error("simulated partial native write failure") end
assert(not transport:apply(state, false), "Partial writes must fail closed")
restored()
fields.Radius.setAll = write_all

assert(transport:apply(state, false))
local set_exterior = fields.Blur.setExterior
fields.Blur.setExterior = function() error("simulated native restore failure") end
assert(not transport:release(), "Native restoration errors must be observable and retryable")
assert(transport.saved, "A failed restore must retain its original snapshot")
fields.Blur.setExterior = set_exterior
assert(transport:release()); restored()

local get_mode = mode.getSearchModeForPlayer
mode.getSearchModeForPlayer = function() error("simulated unavailable native API") end
assert(not transport:apply(state, false)); restored()
mode.getSearchModeForPlayer = get_mode
