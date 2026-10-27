require "ISUI/ISCollapsableWindow"
require "ISUI/ISButton"
require "Vehicles/ISUI/ISUI3DScene"
local Sample = require "DeadSignalCamera/Sample"

local Scene = ISUI3DScene:derive("DeadSignalCameraProbeScene")
local Window = ISCollapsableWindow:derive("DeadSignalCameraProbeWindow")
local active_window
local pending_world_report = false

local function report_access(label, callback)
    local ok, result = pcall(callback)
    print("[DeadSignalWorldProbe] " .. label .. ": " .. (ok and tostring(result) or ("BLOCKED " .. tostring(result))))
    return ok, result
end

local function audit_native_world(player_index)
    local player = getSpecificPlayer(player_index)
    if not player then return end
    print("[DeadSignalWorldProbe] BEGIN live world access audit; debug=" .. tostring(getDebug()))
    local ok, camera = report_access("renderer camera", function()
        return getRenderer():getRenderingPlayerCamera(player_index)
    end)
    if ok and camera then
        report_access("camera method getOffX", function() return camera:getOffX() end)
        report_access("camera method calculateModelViewProjection", function() return type(camera.calculateModelViewProjection) end)
        report_access("camera modelview field", function() return camera.modelview end)
        report_access("camera projection field", function() return camera.projection end)
    end
    report_access("IsoCamera cameras field", function() return IsoCamera.cameras end)
    report_access("Matrix4f global", function() return type(Matrix4f) end)
    report_access("world X axis screen delta", function()
        local x, y, z = player:getX(), player:getY(), player:getZ()
        return string.format("%.2f,%.2f", IsoUtils.XToScreen(x+1,y,z,0)-IsoUtils.XToScreen(x,y,z,0),
            IsoUtils.YToScreen(x+1,y,z,0)-IsoUtils.YToScreen(x,y,z,0))
    end)
    report_access("live object model coverage", function()
        local cell = getCell()
        local x, y, z = math.floor(player:getX()), math.floor(player:getY()), math.floor(player:getZ())
        local loaded, objects, models, floors, floor_models, failures = 0, 0, 0, 0, 0, 0
        local examples = {}
        for dx=-16,16 do
            for dy=-16,16 do
                local square = cell:getGridSquare(x+dx,y+dy,z)
                if square then
                    loaded = loaded + 1
                    local floor = square:getFloor()
                    local list = square:getObjects()
                    for i=0,list:size()-1 do
                        local object = list:get(i)
                        objects = objects + 1
                        local model_ok, model = pcall(function() return object:getSpriteModel() end)
                        if not model_ok then failures = failures + 1 end
                        if model_ok and model then models = models + 1 end
                        if object == floor then
                            floors = floors + 1
                            if model_ok and model then floor_models = floor_models + 1 end
                        end
                        if #examples < 6 and object ~= floor then
                            examples[#examples+1] = tostring(object:getSpriteName()) .. "=" .. (model_ok and model and "model" or "sprite")
                        end
                    end
                end
            end
        end
        return string.format("%d loaded squares, %d objects, %d SpriteModels; %d/%d floors modeled; %d query failures; %s",
            loaded, objects, models, floor_models, floors, failures, table.concat(examples, "; "))
    end)
    pending_world_report = true
    print("[DeadSignalWorldProbe] Waiting for the actual world render callback. No camera state changed.")
end

if Events.RenderOpaqueObjectsInWorld then
    Events.RenderOpaqueObjectsInWorld.Add(function(player_index, x, y, z, square)
        if not pending_world_report then return end
        pending_world_report = false
        print("[DeadSignalWorldProbe] LIVE RenderOpaqueObjectsInWorld player=" .. tostring(player_index)
            .. " focus=" .. tostring(x) .. "," .. tostring(y) .. "," .. tostring(z) .. " square=" .. tostring(square))
    end)
end

function Scene:instantiate()
    ISUI3DScene.instantiate(self)
    self:setView("UserDefined")
    self.javaObject:fromLua1("setDrawGrid", false)
    self.javaObject:fromLua1("setDrawGridAxes", false)
    self.javaObject:fromLua1("setZoom", 4)
    self.javaObject:fromLua3("setViewRotation", self.pitch, self.yaw, 0)
    self.translate = Vector3f.new()
    self.rotation = Vector3f.new()
    self.minimum = Vector3f.new()
    self.maximum = Vector3f.new()
end

function Scene:box(x, y, z, width, height, depth, r, g, b)
    self.translate:set(x, y, z)
    self.rotation:set(0, 0, 0)
    self.minimum:set(-width/2, 0, -depth/2)
    self.maximum:set(width/2, height, depth/2)
    self.javaObject:fromLua9("addBox3D", self.translate, self.rotation, self.minimum, self.maximum, r, g, b, 0.85, true)
end

function Scene:prerender()
    ISUI3DScene.prerender(self)
    self.javaObject:fromLua0("clearBox3Ds")
    local sample = self.parent.sample
    if not sample then return end
    for _, shape in ipairs(sample.boxes) do
        local floor = shape.kind == "floor"
        self:box(shape.x, 0, shape.z, shape.width, shape.height, shape.depth,
            floor and 0.25 or 0.85, floor and 0.32 or 0.6, floor and 0.3 or 0.3)
    end
    local player = getSpecificPlayer(self.parent.player_index)
    if player and math.floor(player:getZ()) == sample.z then
        self:box(player:getX() - sample.x - 0.5, 0.05, player:getY() - sample.y - 0.5, 0.25, 0.8, 0.25, 0.2, 0.85, 1)
    end
end

function Scene:onMouseDown(x, y)
    self.orbiting = true
    return true
end

function Scene:onMouseUp(x, y)
    self.orbiting = false
    return true
end
Scene.onMouseUpOutside = Scene.onMouseUp

function Scene:onRightMouseDown(x, y)
    self.panning = true
    return true
end

function Scene:onRightMouseUp(x, y)
    self.panning = false
    return true
end
Scene.onRightMouseUpOutside = Scene.onRightMouseUp

function Scene:onMouseMove(dx, dy)
    if self.orbiting then
        self.yaw = (self.yaw + dx * 0.4) % 360
        self.pitch = math.max(5, math.min(85, self.pitch + dy * 0.4))
        self.javaObject:fromLua3("setViewRotation", self.pitch, self.yaw, 0)
    elseif self.panning then
        self.javaObject:fromLua2("dragView", dx, dy)
    end
    return true
end

function Scene:onMouseMoveOutside(dx, dy)
    self.orbiting = false
    self.panning = false
end

function Scene:new(x, y, width, height)
    local scene = ISUI3DScene.new(self, x, y, width, height)
    scene.pitch = 30
    scene.yaw = 45
    scene.backgroundColor = {r=0.04, g=0.055, b=0.07, a=1}
    return scene
end

function Window:refresh()
    local player = getSpecificPlayer(self.player_index)
    if not player then return end
    local ok, result = pcall(Sample.collect, getCell(), player:getX(), player:getY(), player:getZ(), 6, IsoFlagType.collideN, IsoFlagType.collideW)
    if ok then
        self.sample = result
        self.status = string.format("%d loaded tiles, %d floors, %d collision edges. Cyan = player marker.", result.loaded, result.floors, result.walls)
        print("[DeadSignalCameraProbe] " .. self.status)
    else
        self.status = "Sampling failed; see console log."
        print("[DeadSignalCameraProbe] Sampling failed: " .. tostring(result))
    end
end

function Window:createChildren()
    ISCollapsableWindow.createChildren(self)
    self.scene = Scene:new(8, 28, self.width - 16, self.height - 108)
    self.scene:initialise()
    self:addChild(self.scene)
    local button = ISButton:new(10, self.height - 70, 100, 24, "Refresh map", self, Window.refresh)
    button:initialise()
    self:addChild(button)
    self:refresh()
end

function Window:render()
    ISCollapsableWindow.render(self)
    self:drawText(self.status or "Waiting for map", 10, self.height - 40, 0.9, 0.9, 0.9, 1, UIFont.Small)
    self:drawText("Left-drag: orbit/tilt. Right-drag: pan. Wheel: zoom. Collision snapshot, not a gameplay camera.", 10, self.height - 23, 0.7, 0.7, 0.7, 1, UIFont.Small)
end

function Window:close()
    self:setVisible(false)
    self:removeFromUIManager()
    active_window = nil
end

local function open_probe(player_index)
    if active_window then active_window:close() end
    local width = math.min(920, getCore():getScreenWidth() - 40)
    local height = math.min(680, getCore():getScreenHeight() - 40)
    local window = Window:new(20, 20, width, height)
    window.player_index = player_index
    window.title = "Camera research - nearby map geometry"
    window.resizable = false
    window:initialise()
    window:instantiate()
    window:addToUIManager()
    active_window = window
end

Events.OnFillWorldObjectContextMenu.Add(function(player_index, context, world_objects, test)
    if test or not getDebug() or isClient() or isServer() then return end
    context:addOption("Camera research: nearby map probe", player_index, open_probe)
    context:addOption("Camera research: audit actual world access", player_index, audit_native_world)
end)

Events.OnGameStart.Add(function()
    print("[DeadSignalCameraProbe] Loaded v0.0.3. Debug world right-click menu opens geometry, textured ground or access audit. UI3DScene=" .. type(UI3DScene))
end)
