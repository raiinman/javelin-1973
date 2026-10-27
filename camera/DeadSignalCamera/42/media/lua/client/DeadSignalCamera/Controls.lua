require "DeadSignalCamera"
require "ISUI/ISCollapsableWindow"
require "ISUI/ISButton"
local Camera=DeadSignalCamera
local Window=ISCollapsableWindow:derive("DeadSignalCameraWindow")

function Window:createChildren()
    ISCollapsableWindow.createChildren(self)
    local definitions={{10,34,"+",function() Camera:zoom(-1) end,"Zoom in"},
        {48,74,"Close",function() Camera:preset("close") end,"Closest enabled zoom"},
        {126,76,"Normal",function() Camera:preset("normal") end,"Enabled zoom nearest 100%"},
        {206,76,"Wide",function() Camera:preset("wide") end,"Widest enabled zoom"},
        {286,34,"-",function() Camera:zoom(1) end,"Zoom out"}}
    for _,item in ipairs(definitions) do
        local button=ISButton:new(item[1],48,item[2],24,item[3],self,item[4])
        button:initialise()
        button.tooltip=item[5]..". Uses your game's zoom settings."
        self:addChild(button)
    end
end

function Window:render()
    ISCollapsableWindow.render(self)
    local core=getCore()
    local percent=math.floor(core:getZoom(0)*200/Core.getTileScale()+0.5)
    self:drawText("Zoom "..percent.."%"..(core:getAutoZoom(0) and " (game auto zoom on)" or ""),10,27,0.65,0.91,0.87,1,UIFont.Small)
    local key=core:getKey("PanCamera")
    self:drawText(key~=0 and ("Pan camera binding: "..getKeyName(key)) or "Native camera pan is unbound",10,82,0.85,0.92,0.94,1,UIFont.Small)
    self:drawText("Options > Key Bindings > Pan camera",10,103,0.72,0.75,0.8,1,UIFont.Small)
    self:drawText("Reopen through the world context menu",10,124,0.72,0.75,0.8,1,UIFont.Small)
end

function Window:close()
    Camera:release()
    self:setVisible(false)
    Camera:save_preferences()
end

function Window:onMouseUp(x,y)
    ISCollapsableWindow.onMouseUp(self,x,y)
    Camera:save_preferences()
end

function Camera:show_controls()
    if not self.panel then
        local core=getCore()
        local prefs=getSpecificPlayer(0):getModData().DeadSignalCamera or {}
        self.panel=Window:new(math.max(0,math.min(core:getScreenWidth()-330,tonumber(prefs.x) or core:getScreenWidth()-350)),
            math.max(0,math.min(core:getScreenHeight()-153,tonumber(prefs.y) or 78)),330,153)
        self.panel.title="Dead Signal Camera"
        self.panel.resizable=false
        self.panel:initialise()
        self.panel:instantiate()
        self.panel:addToUIManager()
    end
    self.panel:setVisible(true)
end

Events.OnGameStart.Add(function()
    Camera:release()
    if getNumActivePlayers()==1 then Camera:show_controls() end
    print("[DeadSignalCamera] Native camera controls loaded 0.1.1")
end)

Events.OnFillWorldObjectContextMenu.Add(function(index,context,objects,test)
    if test or index~=0 or getNumActivePlayers()~=1 then return end
    context:addOption("Camera controls",Camera,Camera.show_controls)
end)

if keyBinding then
    table.insert(keyBinding,{value="[DeadSignalCamera]"})
    table.insert(keyBinding,{value="DSCameraControls",key=Keyboard.KEY_F7})
    for _,name in ipairs({"Close","Normal","Wide"}) do table.insert(keyBinding,{value="DSCamera"..name,key=0}) end
end

Events.OnKeyPressed.Add(function(key)
    if Camera:blocked() then return end
    local core=getCore()
    if core:isKey("DSCameraControls",key) then
        if Camera.panel and Camera.panel:isVisible() then Camera.panel:close() else Camera:show_controls() end
    elseif core:isKey("DSCameraClose",key) then Camera:preset("close")
    elseif core:isKey("DSCameraNormal",key) then Camera:preset("normal")
    elseif core:isKey("DSCameraWide",key) then Camera:preset("wide") end
end)

Events.OnResolutionChange.Add(function()
    Camera:release()
    if Camera.panel then
        Camera.panel:setX(math.max(0,math.min(Camera.panel:getX(),getCore():getScreenWidth()-330)))
        Camera.panel:setY(math.max(0,math.min(Camera.panel:getY(),getCore():getScreenHeight()-153)))
    end
end)
