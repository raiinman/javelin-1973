-- Development-only gameplay checks, copied exclusively into a marked build cache.
require "Vehicles/ISUI/ISVehicleMenu"
require "TimedActions/ISTimedActionQueue"

J73GameplayAudit = {}
local TAG = "[J73_AUDIT] "
local RECORD = "j73-persistence-test.txt"
local TOKEN = "J73-disposable-persistence-v1"
local function check(value, message)
    if not value then error(message) end
end

function J73GameplayAudit.tryResume()
    local reader = getFileReader(RECORD, false)
    if not reader then return false end
    local token, mode, world = reader:readLine(), reader:readLine(), reader:readLine()
    reader:close()
    check(token == TOKEN and mode == "Sandbox" and world and world:match("^%w+$"),
        "Invalid disposable persistence record")
    J73GameplayAudit.resuming = true
    getCore():setNoSave(false)
    getWorld():setGameMode(mode)
    getWorld():setWorld(world)
    MainScreen.instance:setDefaultSandboxVars()
    print(TAG .. "RELOAD_BEGIN exact isolated world " .. world)
    MainScreen.continueLatestSaveAux()
    return true
end

local function save_snapshot(car)
    check(getDebug(), "Persistence test requires debug scenario")
    getCore():setNoSave(false)
    car:shutOff()
    car:setHeadlightsOn(false)
    local gas = car:getPartById("GasTank")
    gas:setContainerContentAmount(12.25)
    local fuel, capacity = gas:getContainerContentAmount(), gas:getContainerCapacity()
    check(math.abs(fuel-12.25)<.05 and fuel>0 and fuel<capacity and fuel<=capacity,
        "Persistence fuel marker was clamped or exceeds tank capacity")
    print(TAG .. "SAVE_FUEL requested=12.25; readback=" .. tostring(fuel) .. "; capacity=" .. tostring(capacity))
    car:getPartById("Engine"):setCondition(83)
    car:getPartById("WindowFrontLeft"):getWindow():setOpen(true)
    car:getPartById("WindowFrontLeft"):getWindow():setOpenDelta(1)
    car:getModData().J73PersistenceToken = TOKEN
    local item = car:getPartById("TruckBed"):getItemContainer():AddItem("Base.Screwdriver")
    check(item, "Could not create persistence loot marker")
    item:getModData().J73PersistenceToken = TOKEN
    save(true)
    local mode, world = getWorld():getGameMode(), getWorld():getWorld()
    check(mode == "Sandbox", "Persistence scenario must use Sandbox mode")
    local writer = getFileWriter(RECORD, true, false)
    writer:write(TOKEN .. "\n" .. mode .. "\n" .. world .. "\n")
    writer:close()
    print(TAG .. "SAVE_CREATED native world save; world=" .. world
        .. "; quit this isolated game normally and relaunch the same cache to verify")
end

function J73GameplayAudit.visualFinal(car)
    check(getDebug(), "Visual inspection requires isolated debug scenario")
    local original_lights = car:getHeadlightsOn()
    local original_time = getGameTime():getTimeOfDay()
    local started = getTimestampMs()
    local function lights(active)
        car:setHeadlightsOn(active)
        for _, id in ipairs({ "HeadlightLeft", "HeadlightRight" }) do
            Vehicles.Update.Headlight(car, car:getPartById(id), 0)
        end
    end
    getGameTime():setTimeOfDay(22)
    lights(true)
    print(TAG .. "VISUAL_FINAL_NIGHT headlight beams and lens texture hold 60 seconds; inspect both ends")
    print(TAG .. "VISUAL_FINAL_STEERING manual inspection prompt: wheels nearest hood must steer; no automated steering claim")
    local function finish()
        if getTimestampMs()-started<60000 then return end
        Events.OnTick.Remove(finish)
        lights(original_lights)
        getGameTime():setTimeOfDay(original_time)
        print(TAG .. "VISUAL_FINAL_RESTORED lamp/time state; no save requested; visual results require inspection")
    end
    Events.OnTick.Add(finish)
end

function J73GameplayAudit.verifyReload(visual_final)
    local started = getTimestampMs()
    local function probe()
        local ok, done = pcall(function()
            local vehicles = getCell():getVehicles()
            local iterator = vehicles:iterator()
            while iterator:hasNext() do
                local car = iterator:next()
                if car:getModData().J73PersistenceToken == TOKEN then
                    check(car:getScript():getFullName() == "Base.Javelin73PC", "Reloaded wrong script")
                    check(math.abs(car:getPartById("GasTank"):getContainerContentAmount()-12.25)<.05,
                        "Fuel did not persist")
                    check(car:getPartById("Engine"):getCondition() == 83, "Engine condition did not persist")
                    local window = car:getPartById("WindowFrontLeft"):getWindow()
                    check(window:isOpen() and window:getOpenDelta()>.98, "Native window open state did not persist")
                    local items = car:getPartById("TruckBed"):getItemContainer():getItems()
                    local found = false
                    for item_index = 0, items:size()-1 do
                        if items:get(item_index):getModData().J73PersistenceToken == TOKEN then found = true end
                    end
                    check(found, "Tagged trunk loot did not persist")
                    print(TAG .. "PASS real save/reload: original vehicle, fuel, engine condition, window open state and tagged trunk loot")
                    if visual_final then J73GameplayAudit.visualFinal(car) end
                    return true
                end
            end
            check(getTimestampMs()-started<60000, "Saved tagged vehicle did not load nearby")
            return false
        end)
        if not ok then print(TAG .. "RELOAD_FAIL " .. tostring(done)) end
        if not ok or done then Events.OnTick.Remove(probe) end
    end
    Events.OnTick.Add(probe)
end

function J73GameplayAudit.start(car, persistence)
    check(getDebug(), "Gameplay audit requires isolated debug scenario")
    local player = getPlayer()
    local steps = {}
    local function add(name, begin, ready, verify)
        steps[#steps+1] = { name=name, begin=begin, ready=ready, verify=verify }
    end
    local function idle()
        return #ISTimedActionQueue.getTimedActionQueue(player).queue == 0
            and not ISTimedActionQueue.isPlayerDoingAction(player)
    end
    for seat = 0, 3 do
        local target = seat
        add("timed seat entry " .. seat, function()
            check(not player:getVehicle(), "Player already seated")
            local outside = car:getPassengerPosition(target, "outside")
            local position = Vector3f.new()
            car:getWorldPos(outside:getOffset(), position)
            print(TAG .. "ENTRY_TARGET seat=" .. target .. "; blocked=" .. tostring(car:isEnterBlocked(player,target))
                .. "; player=" .. player:getX() .. "," .. player:getY()
                .. "; target=" .. position:x() .. "," .. position:y())
            ISVehicleMenu.onEnter(player, car, target)
            local queue = ISTimedActionQueue.getTimedActionQueue(player).queue
            check(#queue>0, "Native menu queued no entry actions")
            for _, action in ipairs(queue) do
                print(TAG .. "ENTRY_ACTION " .. tostring(action.Type))
                if action.Type == "ISPathFindAction" then
                    action:setOnFail(function()
                        local finder=player:getPathFindBehavior2()
                        print(TAG .. "ENTRY_PATH_FAILED seat=" .. target
                            .. "; path_target=" .. finder:getTargetX() .. "," .. finder:getTargetY() .. "," .. finder:getTargetZ()
                            .. "; player_z=" .. player:getZ() .. "; car=" .. car:getX() .. "," .. car:getY() .. "," .. car:getZ())
                    end)
                end
                local original_stop = action.stop
                action.stop = function(self)
                    print(TAG .. "ENTRY_ACTION_STOP " .. tostring(self.Type)
                        .. "; movement=" .. tostring(player:pressedMovement(false))
                        .. "; cancel=" .. tostring(player:pressedCancelAction()))
                    original_stop(self)
                end
            end
        end, function(step)
            if not idle() then return false end
            if car:getSeat(player) == target then return true end
            if getTimestampMs()-step.started>1500 then
                print(TAG .. "GAMEPLAY_FAIL native entry queue ended before seat attachment " .. target)
                J73GameplayAudit.failed = true
            end
            return false
        end, function()
            check(car:getSeat(player) == target, "Native timed entry did not reach requested seat")
            print(TAG .. "PASS native pathfinding, door and timed seat entry " .. target)
        end)
        add("timed seat exit " .. seat, function()
            ISVehicleMenu.onExit(player, target)
        end, idle, function()
            check(not player:getVehicle(), "Native timed exit left player inside")
            print(TAG .. "PASS native timed seat exit " .. target)
        end)
    end
    for _, id in ipairs({ "DoorFrontLeft", "EngineDoor", "TrunkDoor", "WindowFrontLeft", "TireFrontLeft", "Battery", "Muffler" }) do
        local part_id = id
        add("native mechanics callbacks " .. id, function()
            local part = car:getPartById(part_id)
            local item = part:getInventoryItem()
            check(item, "Missing installed item " .. part_id)
            local uninstall, install = part:getTable("uninstall"), part:getTable("install")
            check(uninstall and install, "Missing mechanics tables " .. part_id)
            part:setInventoryItem(nil)
            if uninstall.complete then VehicleUtils.callLua(uninstall.complete, car, part, item) end
            check(not part:getInventoryItem(), "Part was not removed " .. part_id)
            part:setInventoryItem(item)
            if install.complete then VehicleUtils.callLua(install.complete, car, part) end
            check(part:getInventoryItem() == item, "Part did not reinstall " .. part_id)
            part:setCondition(25)
            part:repair()
            check(part:getCondition() == 100 and part:getInventoryItem(), "Native repair failed " .. part_id)
            print(TAG .. "PASS native remove/install callbacks and repair " .. part_id
                .. "; mechanics inventory/skill UI untested")
        end, function() return true end, function() end)
    end
    add("headlight native state", function()
        car:setHeadlightsOn(true)
        for _, id in ipairs({ "HeadlightLeft", "HeadlightRight" }) do
            local part = car:getPartById(id)
            check(part:getInventoryItem() and part:getLight(), "Missing native lamp " .. id)
            Vehicles.Update.Headlight(car, part, 0)
            check(part:getLight():getActive(), "Native lamp did not activate " .. id)
            check(part:getLight():getIntensity()>0, "Native lamp has zero intensity " .. id)
        end
        getGameTime():setTimeOfDay(22)
        print(TAG .. "HEADLIGHTS_ON hold 10 seconds for beam/texture inspection")
    end, function(step) return getTimestampMs()-step.started>=10000 end, function()
        car:setHeadlightsOn(false)
        for _, id in ipairs({ "HeadlightLeft", "HeadlightRight" }) do
            local part = car:getPartById(id)
            Vehicles.Update.Headlight(car, part, 0)
            check(not part:getLight():getActive(), "Native lamp did not turn off " .. id)
        end
        getGameTime():setTimeOfDay(12)
        print(TAG .. "PASS native headlight activation/deactivation; beam appearance requires visual inspection")
    end)
    local index = 1
    local function tick()
        if J73GameplayAudit.failed then Events.OnTick.Remove(tick) return end
        local step = steps[index]
        if not step then
            Events.OnTick.Remove(tick)
            print(TAG .. "GAMEPLAY_SUITE_COMPLETE")
            if persistence then
                local ok, err = pcall(save_snapshot, car)
                if not ok then print(TAG .. "SAVE_FAIL " .. tostring(err)) end
            end
            return
        end
        local ok, err = pcall(function()
            if not step.started then
                step.started = getTimestampMs()
                print(TAG .. "GAMEPLAY_BEGIN " .. step.name)
                step.begin()
                return
            end
            check(getTimestampMs()-step.started<60000, "Timeout " .. step.name)
            if step.ready(step) then step.verify() index=index+1 end
        end)
        if not ok then
            Events.OnTick.Remove(tick)
            print(TAG .. "GAMEPLAY_FAIL " .. tostring(err))
        end
    end
    Events.OnTick.Add(tick)
end
