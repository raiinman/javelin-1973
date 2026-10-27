-- Rejected raw-offset research, not part of the distributed runtime.
local State = {}
State.__index = State
local function finite(value)
    return type(value)=="number" and value==value and math.abs(value)<math.huge
end
local function clamp(value,limit) return math.max(-limit,math.min(limit,value)) end

function State.new()
    local state = setmetatable({limit_x=400,limit_y=240},State)
    state:reset()
    return state
end

function State:reset()
    self.x,self.y,self.target_x,self.target_y = 0,0,0,0
    self.mode = "follow"
    self.last_center_x,self.last_center_y = nil,nil
end

function State:set_bounds(x,y)
    if not finite(x) or not finite(y) or x<0 or y<0 then return false end
    self.limit_x,self.limit_y = x,y
    self.x,self.y = clamp(self.x,x),clamp(self.y,y)
    self.target_x,self.target_y = clamp(self.target_x,x),clamp(self.target_y,y)
    return true
end

function State:pan(dx,dy,zoom)
    if not finite(dx) or not finite(dy) or not finite(zoom) or zoom<=0 then return false end
    self.target_x = clamp(self.target_x-dx*zoom,self.limit_x)
    self.target_y = clamp(self.target_y-dy*zoom,self.limit_y)
    if self.mode~="hold" then self.mode="look" end
    return true
end

function State:recenter()
    self.mode,self.target_x,self.target_y = "follow",0,0
end

function State:set_hold(enabled)
    self.mode = enabled and "hold" or "look"
end

function State:update(dt,center_x,center_y)
    if not finite(dt) or dt<0 or not finite(center_x) or not finite(center_y) then return false end
    if self.mode=="hold" and self.last_center_x then
        local dx,dy = center_x-self.last_center_x,center_y-self.last_center_y
        self.x,self.y = self.x-dx,self.y-dy
        self.target_x = clamp(self.target_x-dx,self.limit_x)
        self.target_y = clamp(self.target_y-dy,self.limit_y)
    end
    self.last_center_x,self.last_center_y = center_x,center_y
    local blend = 1-math.exp(-8*dt)
    self.x = clamp(self.x+(self.target_x-self.x)*blend,self.limit_x)
    self.y = clamp(self.y+(self.target_y-self.y)*blend,self.limit_y)
    if self.mode=="follow" and math.abs(self.x)<0.1 and math.abs(self.y)<0.1 then self.x,self.y=0,0 end
    return true
end

return State
