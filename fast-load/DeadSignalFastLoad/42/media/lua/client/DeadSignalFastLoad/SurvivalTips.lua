local entries=require "DeadSignalFastLoad/TipIndex"
local Tips={}
local enabled=true
local deck,seed,cursor,current
local due=0
local file="DeadSignalFastLoad-tip-deck.txt"
local modulus=2147483647
local failed=false
local persistenceFailed=false
local lines,layoutWidth,layoutText,layoutFont

-- Private deterministic shuffle: never consumes the world's random stream.
local function shuffle(value)
    local result={}
    for i=1,#entries do result[i]=i end
    for i=#result,2,-1 do
        value=(value*48271)%modulus
        local other=(value%i)+1
        result[i],result[other]=result[other],result[i]
    end
    return result
end

local function remember()
    if persistenceFailed then return end
    local writer
    local ok,err=pcall(function()
        writer=getFileWriter(file,true,false)
        if not writer then error("Tip deck writer unavailable") end
        writer:write(string.format("1 %d %d %d\n",#entries,seed,cursor))
        writer:close()
        writer=nil
    end)
    if writer then pcall(function() writer:close() end) end
    if not ok then
        persistenceFailed=true
        print("[DeadSignalFastLoad] Tip order is session-only: "..tostring(err))
    end
end

local function initialize()
    seed=math.floor(getTimestampMs()%2147483646)+1
    cursor=1
    local reader
    pcall(function()
        reader=getFileReader(file,false)
        if not reader then return end
        local value=reader:readLine()
        local version,count,savedSeed,savedCursor
        if value then version,count,savedSeed,savedCursor=value:match("^(%d+) (%d+) (%d+) (%d+)$") end
        count,savedSeed,savedCursor=tonumber(count),tonumber(savedSeed),tonumber(savedCursor)
        if version=="1" and count==#entries and savedSeed and savedSeed>=1
            and savedSeed<modulus and savedCursor and savedCursor>=1 and savedCursor<=#entries+1 then
            seed,cursor=savedSeed,savedCursor
        end
    end)
    if reader then pcall(function() reader:close() end) end
    deck=shuffle(seed)
end

local function advance(now)
    if not deck then initialize() end
    if cursor>#deck then
        local last=deck[#deck]
        repeat
            seed=(seed*48271)%modulus
            deck=shuffle(seed)
        until #deck<2 or deck[1]~=last
        cursor=1
    end
    local entry=entries[deck[cursor]]
    local text=getText(entry.key)
    current={text=text,category=entry.category,number=cursor}
    if text==entry.key then current=nil end
    cursor=cursor+1
    due=now+12000
    remember()
end

local function wrap(text,width,font)
    if lines and layoutWidth==width and layoutText==text and layoutFont==font then return end
    lines={}
    local line=""
    for word in text:gmatch("%S+") do
        local candidate=line=="" and word or line.." "..word
        if line~="" and getTextManager():MeasureStringX(font,candidate)>width then
            lines[#lines+1]=line
            line=word
        else line=candidate end
    end
    if line~="" then lines[#lines+1]=line end
    layoutWidth,layoutText,layoutFont=width,text,font
end

local function render(ui,boot)
    local w,h=ui:getWidth(),ui:getHeight()
    if w<640 or h<420 then return end
    local x=math.max(w*0.48,32)
    if not boot and ui.bottomPanel then x=math.max(x,ui.bottomPanel:getRight()+24) end
    local width=math.min(620,w-x-32)
    if width<240 then return end
    local now=getTimestampMs()
    if now>=due then
        -- Do not advance a card while someone is reading under the pointer.
        local mx,my=ui:getMouseX(),ui:getMouseY()
        local hover=current and mx>=x and mx<=x+width and my>=h-190 and my<=h-64
        if hover then due=now+12000 else advance(now) end
    end
    if not current then return end
    local font=UIFont.Medium
    wrap(current.text,width-32,font)
    local lineHeight=getTextManager():getFontHeight(font)
    local headerHeight=getTextManager():getFontHeight(UIFont.Small)
    local height=headerHeight+#lines*lineHeight+40
    local y=h-64-height
    ui:drawRect(x,y,width,height,0.84,0.018,0.027,0.029)
    ui:drawRect(x,y,2,height,0.85,0.58,0.52,0.33)
    ui:drawText("SURVIVAL / "..current.category.." / "..current.number.." of "..#entries,
        x+16,y+12,0.68,0.65,0.53,1,UIFont.Small)
    for i,line in ipairs(lines) do
        ui:drawText(line,x+16,y+20+headerHeight+(i-1)*lineHeight,0.85,0.86,0.82,1,font)
    end
end

function Tips.setEnabled(value) enabled=value==true end
function Tips.draw(ui,boot)
    if not enabled or failed then return end
    local ok,err=pcall(render,ui,boot)
    if not ok then
        failed=true
        print("[DeadSignalFastLoad] Tip carousel disabled after draw error: "..tostring(err))
    end
end
return Tips
