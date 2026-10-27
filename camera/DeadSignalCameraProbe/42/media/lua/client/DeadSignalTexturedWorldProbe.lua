require "ISUI/ISCollapsableWindow"
require "ISUI/ISPanel"
require "ISUI/ISButton"
local Orbit = require "DeadSignalCamera/Orbit"

local Ground = ISPanel:derive("DeadSignalTexturedGround")
local Window = ISCollapsableWindow:derive("DeadSignalTexturedWorldWindow")
local active_window
local PREFIX = "[DeadSignalTexturedWorld] "

function Window:refresh()
    local player = getSpecificPlayer(self.player_index)
    if not player then return end
    local anchor_x, anchor_y, level = math.floor(player:getX()), math.floor(player:getY()), math.floor(player:getZ())
    local snapshot = {x=anchor_x, y=anchor_y, z=level, tiles={}, loaded=0, floors=0, missing=0}
    local density = (IsoUtils.XToScreen(1,0,0,0) - IsoUtils.XToScreen(0,0,0,0)) / 32
    local first_metadata
    local ok, problem = pcall(function()
        for dy=-6,6 do
            for dx=-6,6 do
                local square = getCell():getGridSquare(anchor_x+dx, anchor_y+dy, level)
                if square then
                    snapshot.loaded = snapshot.loaded + 1
                    local floor = square:getFloor()
                    if floor then
                        snapshot.floors = snapshot.floors + 1
                        local sprite = floor:getSprite()
                        local texture = sprite and sprite:getTextureForCurrentFrame(IsoDirections.N)
                        if texture and texture:isReady() then
                            local meta = {width=texture:getWidth(), height=texture:getHeight(),
                                offset_x=texture:getOffsetX(), offset_y=texture:getOffsetY()}
                            -- shortcut: floor sprite shifts are assumed zero; add a verified accessor if a shifted floor is found.
                            local origin_u = floor:getOffsetX()
                            local origin_v = floor:getOffsetY()
                            local texture_density = density
                            if density == 2 and texture:getWidthOrig() == 64 and texture:getHeightOrig() == 128 then
                                texture_density = 1
                                origin_u, origin_v = origin_u / 2, origin_v / 2
                            end
                            local corners = Orbit.sprite_plane(meta, dx, dy, texture_density, origin_u, origin_v, 0)
                            snapshot.tiles[#snapshot.tiles+1] = {texture=texture, corners=corners}
                            if not first_metadata then
                                first_metadata = string.format("%s trimmed=%dx%d offset=%.1f,%.1f canvas=%dx%d density=%.1f origin=%.1f,%.1f spriteShift=%s",
                                    tostring(sprite:getName()), meta.width, meta.height, meta.offset_x, meta.offset_y,
                                    texture:getWidthOrig(), texture:getHeightOrig(), texture_density, origin_u, origin_v,
                                    "assumed zero")
                            end
                        else
                            snapshot.missing = snapshot.missing + 1
                        end
                    end
                end
            end
        end
    end)
    if not ok then
        self.status = "Floor sampling failed; see console."
        print(PREFIX .. "sampling failed: " .. tostring(problem))
        return
    end
    self.snapshot = snapshot
    self.status = string.format("%d loaded tiles, %d floors, %d actual textures, %d unavailable.", snapshot.loaded, snapshot.floors, #snapshot.tiles, snapshot.missing)
    self.pick_status = "Click a floor to inspect coordinates. No game action is issued."
    print(PREFIX .. self.status .. string.format(" anchor=%d,%d,%d",anchor_x,anchor_y,level))
    if first_metadata then print(PREFIX .. "first texture: " .. first_metadata) end
    print(PREFIX .. string.format("player marker=%.3f,%.3f level=%.1f", player:getX()-anchor_x,player:getY()-anchor_y,player:getZ()))
end

function Ground:render()
    ISPanel.render(self)
    local snapshot = self.parent.snapshot
    if not snapshot then return end
    self.view.center_x, self.view.center_y = self.width / 2, self.height / 2
    self:setStencilRect(0,0,self.width,self.height)
    for _, tile in ipairs(snapshot.tiles) do
        Orbit.project_plane(self.view, tile.corners, function(x1,y1,x2,y2,x3,y3,x4,y4)
            self:drawPolygon(tile.texture,x1,y1,x2,y2,x3,y3,x4,y4,1,1,1,1)
        end)
    end
    local player = getSpecificPlayer(self.parent.player_index)
    if player and math.floor(player:getZ()) == snapshot.z then
        local px, py = Orbit.project(self.view,player:getX()-snapshot.x,player:getY()-snapshot.y,0)
        self:drawRect(px-3,py-3,6,6,1,0.1,0.9,1)
    end
    self:clearStencilRect()
    self:drawText(string.format("Yaw %.1f  Tilt %.1f  Scale %.1f",self.view.yaw,self.view.pitch,self.view.scale),8,8,1,1,1,1,UIFont.Small)
end

function Ground:onMouseDown(x,y)
    self.orbiting, self.drag_distance = true, 0
    return true
end

function Ground:onMouseUp(x,y)
    if self.orbiting then
        if self.drag_distance < 3 and x >= 0 and x <= self.width and y >= 0 and y <= self.height and self.parent.snapshot then
            local wx, wy = Orbit.pick(self.view,x,y,0)
            local snapshot = self.parent.snapshot
            self.parent.pick_status = string.format("Floor %.2f, %.2f, level %d (tile %d,%d).",wx+snapshot.x,wy+snapshot.y,snapshot.z,math.floor(wx+snapshot.x),math.floor(wy+snapshot.y))
        end
        print(PREFIX .. string.format("orbit yaw=%.2f pitch=%.2f",self.view.yaw,self.view.pitch))
    end
    self.orbiting = false
    return true
end

function Ground:onRightMouseDown(x,y)
    self.panning = true
    return true
end

function Ground:onRightMouseUp(x,y)
    if self.panning then print(PREFIX .. string.format("pan offset=%.2f,%.2f",self.view.pan_x,self.view.pan_y)) end
    self.panning = false
    return true
end

function Ground:onMouseMove(dx,dy)
    if self.orbiting then
        self.drag_distance = self.drag_distance + math.abs(dx) + math.abs(dy)
        self.view.yaw = (self.view.yaw + dx * 0.4) % 360
        self.view.pitch = math.max(5,math.min(85,self.view.pitch + dy * 0.4))
    elseif self.panning then
        self.view.pan_x = self.view.pan_x + dx
        self.view.pan_y = self.view.pan_y + dy
    end
    return true
end

function Ground:onMouseMoveOutside(dx,dy)
    if self.orbiting then self:onMouseUp(-10000,-10000) end
    if self.panning then self:onRightMouseUp(0,0) end
end
Ground.onMouseUpOutside = Ground.onMouseUp
Ground.onRightMouseUpOutside = Ground.onRightMouseUp

function Ground:onMouseWheel(delta)
    self.view.scale = math.max(12,math.min(120,self.view.scale * (1-delta*0.1)))
    return true
end

function Ground:new(x,y,width,height)
    local panel = ISPanel.new(self,x,y,width,height)
    panel.view = Orbit.new({scale=48})
    panel.backgroundColor = {r=0.035,g=0.045,b=0.055,a=1}
    return panel
end

function Window:preset(button)
    local view = self.ground.view
    if button.action == "rotate" then view.yaw = (view.yaw+90)%360
    elseif button.action == "low" then view.pitch = 5
    elseif button.action == "top" then view.pitch = 85
    elseif button.action == "reset" then self.ground.view = Orbit.new({scale=48}) end
    view = self.ground.view
    print(PREFIX .. string.format("preset=%s yaw=%.1f pitch=%.1f scale=%.1f",button.action,view.yaw,view.pitch,view.scale))
end

function Window:createChildren()
    ISCollapsableWindow.createChildren(self)
    self.ground = Ground:new(8,30,self.width-16,self.height-150)
    self.ground:initialise()
    self:addChild(self.ground)
    local actions = {{"Rotate 90","rotate"},{"Low 5","low"},{"Top 85","top"},{"Reset","reset"}}
    for i, action in ipairs(actions) do
        local button = ISButton:new(10+(i-1)*100,self.height-110,94,24,action[1],self,Window.preset)
        button.action = action[2]
        button:initialise()
        self:addChild(button)
    end
    local refresh = ISButton:new(410,self.height-110,110,24,"Refresh ground",self,Window.refresh)
    refresh:initialise()
    self:addChild(refresh)
    self:refresh()
end

function Window:render()
    ISCollapsableWindow.render(self)
    self:drawText(self.status or "Waiting for floor snapshot",10,self.height-78,0.9,0.9,0.9,1,UIFont.Small)
    self:drawText(self.pick_status or "",10,self.height-60,0.7,0.9,1,1,UIFont.Small)
    self:drawText("Real floor textures only. No characters or buildings. Native world view stays unchanged.",10,self.height-42,1,0.8,0.4,1,UIFont.Small)
    self:drawText("Left-drag orbit/tilt, right-drag pan, wheel zoom. Cyan square = live player position.",10,self.height-24,0.7,0.7,0.7,1,UIFont.Small)
end

function Window:close()
    self:setVisible(false)
    self:removeFromUIManager()
    active_window = nil
end

local function open_ground(player_index)
    if active_window then active_window:close() end
    local window = Window:new(25,25,math.min(1000,getCore():getScreenWidth()-50),math.min(760,getCore():getScreenHeight()-50))
    window.player_index = player_index
    window.title = "Camera research - real textured ground"
    window.resizable = false
    window:initialise()
    window:instantiate()
    window:addToUIManager()
    active_window = window
end

Events.OnFillWorldObjectContextMenu.Add(function(player_index,context,objects,test)
    if test or not getDebug() or isClient() or isServer() then return end
    context:addOption("Camera research: textured ground",player_index,open_ground)
end)
