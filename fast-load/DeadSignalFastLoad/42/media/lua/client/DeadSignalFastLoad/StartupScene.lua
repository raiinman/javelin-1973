require "ISUI/ISPanel"
local Tips=require "DeadSignalFastLoad/SurvivalTips"

local Scene = {}
local enabled, reducedMotion = true, false
local started = getTimestampMs()
local bootPanel, wrappedClass, texture
local failed, textureAttempted = false, false

local function paint(ui)
    if not textureAttempted then
        textureAttempted=true
        texture=getTexture("media/textures/FastLoad_KnoxCounty.png")
    end
    if not texture then return end
    local w,h=ui:getWidth(),ui:getHeight()
    local t=reducedMotion and 0 or (getTimestampMs()-started)/1000
    local scale=math.max(w/texture:getWidth(),h/texture:getHeight())
    local tw,th=texture:getWidth()*scale,texture:getHeight()*scale
    ui:drawTextureScaled(texture,(w-tw)/2,(h-th)/2,tw,th,1,1,1,1)
    -- Bounded native UI draws, no video, audio, shader or background load tasks.
    -- Smooth movement, no flashing lights or random noise each frame.
    for i=0,7 do
        local drift=math.sin(t*0.10+i*0.8)*0.08
        ui:drawRect((0.34+drift)*w,(0.57+i*0.014)*h,0.72*w,0.024*h,
            0.018,0.40,0.45,0.43)
    end
    local sweep=(math.sin(t*0.16)+1)*0.5
    for i=0,7 do
        ui:drawRect((0.48+sweep*0.18-i*0.006)*w,(0.69+i*0.006)*h,
            (0.12+i*0.018)*w,0.003*h,0.012,0.67,0.65,0.44)
    end
    if not reducedMotion then
        for i=1,48 do
            local x=(i*0.6180339+t*0.018)%1
            local y=(i*0.4142136+t*(0.15+(i%4)*0.018))%1
            ui:drawLine2(x*w,y*h,(x-0.006)*w,(y+0.022)*h,
                0.045+(i%3)*0.012,0.51,0.60,0.61)
        end
    end
end

local function draw(ui)
    if not enabled or failed then return end
    local ok,err=pcall(paint,ui)
    if not ok then
        failed=true
        print("[DeadSignalFastLoad] Startup artwork disabled after draw error: "..tostring(err))
    end
end

function Scene.closeBoot()
    if bootPanel then bootPanel:removeFromUIManager(); bootPanel=nil end
end
function Scene.setEnabled(value)
    enabled=value==true
    if not enabled then Scene.closeBoot() end
end
function Scene.setReducedMotion(value) reducedMotion=value==true end

function Scene.boot()
    Scene.closeBoot()
    if not enabled or isClient() or isServer() or getPlayer() or isIngameState()
        or isKeyDown(Keyboard.KEY_ESCAPE) then return end
    -- Native state controls whether this UI can render. No pre-Lua coverage.
    -- Native terms prompts are above this non-interactive background.
    if MainScreenState and MainScreenState.getInstance() then return end
    bootPanel=ISPanel:new(0,0,getCore():getScreenWidth(),getCore():getScreenHeight())
    bootPanel:initialise()
    bootPanel.background=false
    bootPanel:setWantMouseEvents(false)
    bootPanel.prerender=function(self)
        self:setWidth(getCore():getScreenWidth())
        self:setHeight(getCore():getScreenHeight())
        draw(self)
        Tips.draw(self,true)
    end
    bootPanel:addToUIManager()
    bootPanel:backMost()
end

function Scene.install()
    Scene.closeBoot()
    if not MainScreen or not MainScreen.prerender or wrappedClass==MainScreen then return end
    local original=MainScreen.prerender
    MainScreen.prerender=function(self,...)
        -- Native prerender draws its logo afterward, child controls follow.
        -- Submenus and the in-game pause menu retain their original backgrounds.
        local front=not self.inGame and self.bottomPanel and self.bottomPanel:getIsVisible()
        if front then draw(self) end
        local result=original(self,...)
        if front then Tips.draw(self,false) end
        return result
    end
    wrappedClass=MainScreen
end

return Scene
