local Camera = {}
DeadSignalCamera = Camera

function Camera:blocked()
    local player=getSpecificPlayer(0)
    return not isIngameState() or not player or getNumActivePlayers()~=1 or player:isDead()
        or isGamePaused() or getCore():isDoingTextEntry()
end

function Camera:release()
    self.zoom_target=nil
end

function Camera:save_preferences()
    local player=getSpecificPlayer(0)
    if player and self.panel then
        player:getModData().DeadSignalCamera={x=self.panel:getX(),y=self.panel:getY()}
    end
end

function Camera:zoom(direction)
    if self:blocked() then return end
    self:release()
    getCore():doZoomScroll(0,direction)
end

function Camera:preset(name)
    if self:blocked() then return end
    local core=getCore()
    self.zoom_target=name=="close" and core:getMinZoom() or (name=="wide" and core:getMaxZoom() or Core.getTileScale()/2)
    self.zoom_steps,self.zoom_time=0,0
end

function Camera:update(player)
    if player~=getSpecificPlayer(0) then return end
    if self:blocked() then self:release(); return end
    local now=getTimeInMillis()
    if self.zoom_target and now-self.zoom_time>=150 then
        local core=getCore()
        local zoom=core:getNextZoom(0,0)*Core.getTileScale()/2
        local direction=self.zoom_target<zoom and -1 or 1
        local next_zoom=core:getNextZoom(0,direction)*Core.getTileScale()/2
        if self.zoom_steps>=16 or math.abs(self.zoom_target-zoom)<0.03
            or math.abs(next_zoom-self.zoom_target)>=math.abs(zoom-self.zoom_target)-0.001 then
            self:release()
        else
            core:doZoomScroll(0,direction)
            self.zoom_steps,self.zoom_time=self.zoom_steps+1,now
        end
    end
end

Events.OnPlayerUpdate.Add(function(player) Camera:update(player) end)
Events.OnTickEvenPaused.Add(function()
    if Camera.zoom_target and Camera:blocked() then Camera:release() end
end)
Events.OnMainMenuEnter.Add(function()
    Camera:release()
    if Camera.panel then Camera.panel:removeFromUIManager(); Camera.panel=nil end
end)
