require "ISUI/ISPanel"
require "ISUI/ISCollapsableWindow"
require "ISUI/ISButton"
local Transport=require "DeadSignalCameraTransform/Transport"
local Overlay=ISPanel:derive("DeadSignalTransformOverlay")
local Toolbar=ISCollapsableWindow:derive("DeadSignalTransformToolbar")
local active
local LIMIT=0.35
local function clamp(value) return math.max(-LIMIT,math.min(LIMIT,value)) end
local function wrap(value) return (value+math.pi)%(math.pi*2)-math.pi end

function Overlay:blocked()
    local player=getSpecificPlayer(0)
    return not isIngameState() or not player or getNumActivePlayers()~=1 or isClient() or isServer()
        or isGamePaused() or getCore():isDoingTextEntry() or player:isDead() or player:isAiming() or player:getVehicle()
end

function Overlay:close()
    self.transport:release()
    self:setCapture(false)
    self:setVisible(false)
    self:removeFromUIManager()
    active=nil
    print("[DeadSignalTransform] Closed; native visual values restored")
end

function Overlay:onMouseDown()
    if self.enabled and not self:blocked() then self.drag="pan"; self:setCapture(true) end
    return true
end
function Overlay:onRightMouseDown()
    if self.enabled and not self:blocked() then self.drag="orbit"; self:setCapture(true) end
    return true
end
function Overlay:stop_drag()
    self.drag=nil
    self:setCapture(false)
    print(string.format("[DeadSignalTransform] pose pan=%.4f,%.4f yaw=%.1f pitch=%.1f",self.pose.pan_x,self.pose.pan_y,
        self.pose.yaw*180/math.pi,self.pose.pitch*180/math.pi))
    return true
end
Overlay.onMouseUp=Overlay.stop_drag
Overlay.onMouseUpOutside=Overlay.stop_drag
Overlay.onRightMouseUp=Overlay.stop_drag
Overlay.onRightMouseUpOutside=Overlay.stop_drag
function Overlay:onMouseMove(dx,dy)
    if self:blocked() then self.drag=nil; self:setCapture(false); return true end
    if self.drag=="pan" then
        self.pose.pan_x=clamp(self.pose.pan_x+dx/self.width)
        self.pose.pan_y=clamp(self.pose.pan_y+dy/self.height)
    elseif self.drag=="orbit" then
        self.pose.yaw=wrap(self.pose.yaw+dx*math.pi/450)
        self.pose.pitch=math.max(0,math.min(math.rad(80),self.pose.pitch+dy*math.pi/450))
    end
    return true
end
Overlay.onMouseMoveOutside=Overlay.onMouseMove
function Overlay:onMouseWheel(direction)
    if not self:blocked() then getCore():doZoomScroll(0,direction>0 and -1 or 1) end
    return true
end

function Overlay:update_transport()
    local player=getSpecificPlayer(0)
    if not player or player~=self.player or not isIngameState() then self:close(); return end
    local px=IsoUtils.XToScreen(player:getX(),player:getY(),player:getZ(),0)
    local py=IsoUtils.YToScreen(player:getX(),player:getY(),player:getZ(),0)
    local blocked=self:blocked()
    if self.hold and self.last_x and not blocked then
        local zoom=getCore():getZoom(0)
        local dx,dy=(px-self.last_x)/zoom,(py-self.last_y)/zoom
        local cosine,sine=math.cos(self.pose.yaw),math.sin(self.pose.yaw)
        self.pose.pan_x=clamp(self.pose.pan_x+(cosine*dx+sine*dy)/self.width)
        self.pose.pan_y=clamp(self.pose.pan_y+(-sine*dx+cosine*dy)*math.cos(self.pose.pitch)/self.height)
    end
    self.last_x,self.last_y=px,py
    local ok,reason=self.transport:apply(self.pose,blocked or not self.enabled)
    self.status=ok and "Transform active, mouse captured" or (self.enabled and ("Suspended: "..tostring(reason)) or "Normal world image")
end

function Toolbar:createChildren()
    ISCollapsableWindow.createChildren(self)
    local root=self.owner
    local function button(x,y,width,title,callback)
        local item=ISButton:new(x,y,width,24,title,self,callback)
        item:initialise(); self:addChild(item); return item
    end
    root.enable_button=button(10,48,150,"Enable transform",function()
        root.enabled=not root.enabled
        root.last_x,root.last_y=nil,nil
        if not root.enabled then root.transport:release() end
    end)
    root.hold_button=button(170,48,150,"Hold view",function() root.hold=not root.hold; root.last_x=nil end)
    button(10,80,98,"Rotate 90",function() root.pose.yaw=wrap(root.pose.yaw+math.pi/2) end)
    button(116,80,98,"Tilt 55",function() root.pose.pitch=math.rad(55) end)
    button(222,80,98,"Tilt 80",function() root.pose.pitch=math.rad(80) end)
    button(10,112,150,"Reset image",function() root.pose={pan_x=0,pan_y=0,yaw=0,pitch=0}; root.hold=false end)
    button(170,112,150,"Return to game",function() root:close() end)
end
function Toolbar:render()
    ISCollapsableWindow.render(self)
    local root=self.owner
    root.enable_button:setTitle(root.enabled and "Disable transform" or "Enable transform")
    root.hold_button:setTitle(root.hold and "Release hold" or "Hold view")
    self:drawText(root.status or "Ready",10,27,0.75,0.95,0.9,1,UIFont.Small)
    self:drawText(string.format("Image yaw %.0f / tilt %.0f degrees",root.pose.yaw*180/math.pi,root.pose.pitch*180/math.pi),10,150,1,1,1,1,UIFont.Small)
    self:drawText("Left-drag: pan. Right-drag: rotate/tilt.",10,173,0.8,0.85,0.9,1,UIFont.Small)
    self:drawText("Image transform only. Picking stays native.",10,196,1,0.8,0.55,1,UIFont.Small)
    self:drawText("Return to game before interacting.",10,219,1,0.8,0.55,1,UIFont.Small)
end
function Toolbar:close() self.owner:close() end

local function open()
    if active then active:close() end
    local core=getCore()
    local root=Overlay:new(0,0,core:getScreenWidth(),core:getScreenHeight())
    root.backgroundColor={r=0,g=0,b=0,a=0}; root.borderColor={r=0,g=0,b=0,a=0}
    root.pose={pan_x=0,pan_y=0,yaw=0,pitch=0}
    root.player=getSpecificPlayer(0)
    root.transport=Transport.new(getSearchMode(),0)
    root.enabled=false
    root:initialise(); root:instantiate(); root:addToUIManager()
    local toolbar=Toolbar:new(math.max(0,core:getScreenWidth()-350),78,330,250)
    toolbar.owner=root
    toolbar.title="Camera research - image transform"; toolbar.resizable=false
    toolbar:initialise(); toolbar:instantiate(); root:addChild(toolbar)
    active=root
    print("[DeadSignalTransform] Open; opt-in image transform, no geometry rotation")
end
-- SearchMode resets inactive channels earlier in the update. OnTick runs after it.
Events.OnTick.Add(function() if active then active:update_transport() end end)
Events.OnTickEvenPaused.Add(function()
    if active and active:blocked() then
        active.transport:release()
        active.drag=nil
        active:setCapture(false)
        active.last_x,active.last_y=nil,nil
        active.status="Suspended: camera input is blocked"
    end
end)
Events.OnMainMenuEnter.Add(function() if active then active:close() end end)
Events.OnResolutionChange.Add(function() if active then active:close() end end)
Events.OnFillWorldObjectContextMenu.Add(function(index,context,objects,test)
    if not test and index==0 and getDebug() and not isClient() and not isServer() and getNumActivePlayers()==1 then
        context:addOption("Camera research: image transform",nil,open)
    end
end)
Events.OnGameStart.Add(function() print("[DeadSignalTransform] Loaded 0.0.1; shader defaults to native image") end)
