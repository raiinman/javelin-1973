"""Prepare a disposable, isolated game cache, never launch the game or edit user data."""
import argparse
import json
from pathlib import Path

from install_mod import install
from validate_mod import MOD_ID, ROOT


AUDIT = r'''
-- Development-only hook, copied exclusively into build/game-test.
require "J73GameplayAudit"
local TAG = "[J73_AUDIT] "
local function check(condition, message)
    if not condition then error(TAG .. message) end
end

local function initialize_visual_mods()
    -- Native SOLO initializes this list; DebugScenarios bypasses that route.
    local defaults = ActiveMods.getById("default")
    check(defaults:isModActive("Javelin73PC"), "Default test mods do not enable Javelin73PC")
    local current = ActiveMods.getById("currentGame")
    current:copyFrom(defaults)
    check(current:isModActive("Javelin73PC"), "Current test mods do not enable Javelin73PC")
    print(TAG .. "MODS_READY currentGame copied from default before debug world creation")
end

local function run_audit()
    local script = ScriptManager.instance:getVehicle("Base.Javelin73PC")
    check(script, "Vehicle script missing")
    check(script:getWheelCount() == 4, "Expected four wheels")
    check(script:getPassengerCount() == 4, "Expected four passengers")
    check(script:getSeats() == 4, "Expected four seats")
    check(script:getModel():getFile() == "J73_Body", "Wrong body model")
    local models = { "J73_Body", "J73_Interior", "J73_Wheel", "J73_DoorLeft",
        "J73_DoorRight", "J73_Hood", "J73_Trunk", "J73_WindowLeft",
        "J73_WindowRight", "J73_Windshield", "J73_RearGlass" }
    for _, name in ipairs(models) do
        check(ScriptManager.instance:getModelScript("Base." .. name), "Missing model " .. name)
    end
    local parts = { "Engine", "GasTank", "Battery", "Muffler", "TruckBed", "TrunkDoor",
        "EngineDoor", "DoorFrontLeft", "DoorFrontRight", "Windshield", "WindshieldRear",
        "WindowFrontLeft", "WindowFrontRight", "SeatFrontLeft", "SeatFrontRight",
        "SeatRearLeft", "SeatRearRight", "HeadlightLeft", "HeadlightRight", "J73Interior" }
    for _, name in ipairs(parts) do
        check(script:getPartById(name), "Missing part " .. name)
    end
    for _, corner in ipairs({ "FrontLeft", "FrontRight", "RearLeft", "RearRight" }) do
        check(script:getWheelById(corner), "Missing wheel " .. corner)
        for _, kind in ipairs({ "Tire", "Brake", "Suspension" }) do
            check(script:getPartById(kind .. corner), "Missing running gear " .. kind .. corner)
        end
        local tire = script:getPartById("Tire" .. corner)
        check(tire:getModelById("InflatedTirePlusWheel"):getFile() == "J73_Wheel", "Wrong tire model")
    end
    check(not script:getPartById("DoorRearLeft"), "Unexpected third door")
    check(not script:getPartById("DoorRearRight"), "Unexpected fourth door")
    for _, zone in ipairs({ "parkingstall", "medium", "good" }) do
        check(VehicleZoneDistribution[zone].vehicles["Base.Javelin73PC"], "Missing spawn zone " .. zone)
    end
    print(TAG .. "PASS script, eleven model definitions, four seats, two doors, wheels, native parts and spawn registration; parts=" .. script:getPartCount())
    -- Server mechanic functions may only be loaded when starting a world.
    if Vehicles and Vehicles.Create and Vehicles.Create.Tire then
        check(type(Vehicles.Create.Door) == "function", "Missing native door callback")
        check(type(Vehicles.Update.Headlight) == "function", "Missing native light callback")
        print(TAG .. "PASS native mechanic callback availability")
    else
        print(TAG .. "DEFERRED native server callbacks until world load")
    end
end

Events.OnGameBoot.Add(function()
    local ok, err = pcall(run_audit)
    if not ok then print(TAG .. "FAIL " .. tostring(err)) end
end)

Events.OnMainMenuEnter.Add(function()
    print(TAG .. "MAIN_MENU_READY")
end)

debugScenarios = debugScenarios or {}
local visual_test_active = false

local function exercise_vehicle(car)
    local player = getPlayer()
    local x, y, z = player:getX(), player:getY(), player:getZ()
    for seat = 0, 3 do
        check(car:isSeatInstalled(seat), "Seat not installed " .. seat)
        check(car:enter(seat, player), "Native enter failed " .. seat)
        check(car:getSeat(player) == seat and car:getCharacter(seat) == player,
            "Wrong native seat attachment " .. seat)
        car:setCharacterPosition(player, seat, "inside")
        check(car:exit(player), "Native exit failed " .. seat)
    end
    print(TAG .. "PASS four native seat attachments and exits; walk-up door actions untested")
    check(car:enter(0, player), "Driver entry failed for engine test")
    car:setCharacterPosition(player, 0, "inside")
    car:tryStartEngine()
    local elapsed = 0
    local driving, braking = false, false
    local start_x, start_y, peak_speed = car:getX(), car:getY(), 0
    local function restore_player()
        car:setRegulator(false)
        car:shutOff()
        car:exit(player)
        player:setX(x)
        player:setY(y)
        player:setZ(z)
    end
    local function finish_engine_test()
        elapsed = elapsed + 1
        if elapsed < 180 then return end
        local ok, err = pcall(function()
            if not driving then
                check(car:isEngineRunning(), "Repaired fuelled engine did not start")
                print(TAG .. "PASS native engine running; power=" .. car:getEnginePower())
                if not __DRIVE__ then
                    Events.OnTick.Remove(finish_engine_test)
                    restore_player()
                    return
                end
                check(getDebug() and visual_test_active, "Drive exercise requires isolated debug scenario")
                driving = true
                car:setRegulatorSpeed(10)
                car:setRegulator(true)
                print(TAG .. "DRIVE_BEGIN native regulator 10; manual controls untested")
            end
            local speed = math.abs(car:getCurrentSpeedKmHour())
            peak_speed = math.max(peak_speed, speed)
            if elapsed < 480 then return end
            if not braking then
                car:setRegulator(false)
                braking = true
                local distance = math.sqrt((car:getX()-start_x)^2+(car:getY()-start_y)^2)
                check(peak_speed>1 and distance>.5, "No powered vehicle movement")
                print(TAG .. "PASS powered movement; peak_kmh=" .. peak_speed .. "; distance=" .. distance
                    .. "; delta_x=" .. (car:getX()-start_x) .. "; delta_y=" .. (car:getY()-start_y))
            end
            car:setForceBrake()
            check(elapsed<900, "Vehicle did not stop within exercise timeout")
            if speed<.8 then
                Events.OnTick.Remove(finish_engine_test)
                restore_player()
                print(TAG .. "PASS native braking below 0.8 km/h; manual road handling untested")
            end
        end)
        if not ok then
            Events.OnTick.Remove(finish_engine_test)
            car:setForceBrake()
            restore_player()
            print(TAG .. "EXERCISE_FAIL " .. tostring(err))
        end
    end
    Events.OnTick.Add(finish_engine_test)
end
local panel_cycle_active = false
local function cycle_panels(car)
    check(getDebug() and visual_test_active, "Panel cycle requires isolated debug scenario")
    panel_cycle_active = true
    local last_tick = getTimestampMs()
    local elapsed = 0
    local stage = 0
    print(TAG .. "POSE_CLOSED hold 20 seconds")
    local function update_pose()
        local now = getTimestampMs()
        -- Editors suspend world ticks. Do not catch up through unseen poses.
        elapsed = elapsed + math.min(math.max(now-last_tick, 0), 100)
        last_tick = now
        local target = math.min(3, math.floor(elapsed / 20000))
        if target == stage then return end
        stage = target
        local ok, err = pcall(function()
            if stage == 1 or stage == 3 then
                local opened = stage == 1
                for _, id in ipairs({ "DoorFrontLeft", "DoorFrontRight", "EngineDoor", "TrunkDoor" }) do
                    local part = car:getPartById(id)
                    part:getDoor():setOpen(opened)
                    car:playPartAnim(part, opened and "Opened" or "Closed")
                end
            end
            if stage == 2 or stage == 3 then
                for _, id in ipairs({ "WindowFrontLeft", "WindowFrontRight" }) do
                    local part = car:getPartById(id)
                    part:getWindow():setOpen(stage == 2)
                    part:getWindow():setOpenDelta(stage == 2 and 1 or 0)
                    car:playPartAnim(part, "ClosedToOpen")
                end
            end
            local labels = { "POSE_PANELS_OPEN", "POSE_WINDOWS_LOWERED_WITH_DOORS_OPEN", "POSE_RESTORED_CLOSED" }
            print(TAG .. labels[stage] .. "; inspect visual alignment, this log is not a visual pass")
        end)
        if not ok then print(TAG .. "POSE_FAIL " .. tostring(err)) end
        if not ok or stage == 3 then
            if ok then panel_cycle_active = false end
            Events.OnTick.Remove(update_pose)
        end
    end
    Events.OnTick.Add(update_pose)
end

debugScenarios.J73VisualTest = {
    name = "J73 Original Car Visual Test",
    world = "Muldraugh, KY",
    startLoc = { x = 10601, y = 8834, z = 0 },
    setSandbox = function()
        initialize_visual_mods()
        getCore():setNoSave(not __SAVE_TEST__)
        getWorld():setGameMode("Sandbox")
        SandboxVars.Zombies = 6
        SandboxVars.CarSpawnRate = 1
        SandboxVars.VehicleEasyUse = true
        SandboxVars.StartMonth = 7
        SandboxVars.StartDay = 9
        SandboxVars.StartTime = 2
        SandboxVars.ZombieConfig = SandboxVars.ZombieConfig or {}
        SandboxVars.ZombieConfig.PopulationMultiplier = 0
        SandboxVars.ZombieConfig.PopulationStartMultiplier = 0
        SandboxVars.ZombieConfig.PopulationPeakMultiplier = 0
        SandboxVars.ZombieConfig.RespawnHours = 0
        SystemDisabler.setDoZombieCreation(false)
    end,
    onStart = function()
        visual_test_active = true
        local player = getPlayer()
        player:setGodMod(true)
        getGameTime():setTimeOfDay(12)
        getCore():setNoSave(not __SAVE_TEST__)
        print(TAG .. "SCENARIO_READY isolated cache, no zombies, native god mode; saving=" .. tostring(__SAVE_TEST__))
    end,
}

if __AUTO_START__ then
    Events.OnMainMenuEnter.Add(function()
        local function start_visual_test()
            if not MainScreen or not MainScreen.instance or not DebugScenarios
                or not DebugScenarios.instance then return end
            Events.OnRenderTick.Remove(start_visual_test)
            local ok, err = pcall(function()
                check(getDebug(), "Auto-start requires -debug")
                print(TAG .. "AUTO_START native visual scenario")
                if __SAVE_TEST__ and J73GameplayAudit.tryResume() then return end
                DebugScenarios.instance:launchScenario(debugScenarios.J73VisualTest)
            end)
            if not ok then print(TAG .. "SCENARIO_FAIL " .. tostring(err)) end
        end
        Events.OnRenderTick.Add(start_visual_test)
    end)
end

Events.OnGameStart.Add(function()
    print(TAG .. "WORLD_READY")
    local audit_ok, audit_error = pcall(run_audit)
    if not audit_ok then print(TAG .. "FAIL " .. tostring(audit_error)) end
    if J73GameplayAudit.resuming then
        J73GameplayAudit.verifyReload(__VISUAL_FINAL__)
        return
    end
    if not visual_test_active then return end
    local ticks = 0
    local vehicle_spawned = false
    local function initialize_visual_test()
        ticks = ticks + 1
        if ticks < 60 then return end
        local ok, err = pcall(function()
            if not vehicle_spawned then
                local player = getPlayer()
                check(player, "No scenario player")
                getGameTime():setTimeOfDay(12)
                local square = getCell():getGridSquare(math.floor(player:getX()) + 4,
                    math.floor(player:getY()), 0)
                check(square, "Test spawn square not loaded")
                local car = addVehicleDebug("Base.Javelin73PC", IsoDirections.N, 0, square)
                check(car, "Vehicle spawn returned nil")
                -- Mark immediately so later setup failures cannot duplicate the car.
                vehicle_spawned = true
                car:repair()
                local fuel = car:getPartById("GasTank")
                fuel:setContainerContentAmount(fuel:getContainerCapacity())
                player:getInventory():AddItem(car:createVehicleKey())
                print(TAG .. "VEHICLE_SPAWNED repaired, full fuel, matching key, script=" .. car:getScript():getFullName())
                if __EXERCISE__ then exercise_vehicle(car) end
                if __PANEL_CYCLE__ then cycle_panels(car) end
                if __GAMEPLAY__ then
                    local started = getTimestampMs()
                    local function begin_gameplay()
                        if panel_cycle_active then return end
                        if getTimestampMs()-started<__SUITE_DELAY__ then return end
                        Events.OnTick.Remove(begin_gameplay)
                        J73GameplayAudit.start(car, __SAVE_TEST__)
                    end
                    Events.OnTick.Add(begin_gameplay)
                end
                ticks = 0
                return
            end
            if __OPEN_EDITOR__ then
                showVehicleEditor("Base.Javelin73PC")
                print(TAG .. "EDITOR_REQUESTED_IN_WORLD")
            end
            Events.OnTick.Remove(initialize_visual_test)
        end)
        if not ok then
            Events.OnTick.Remove(initialize_visual_test)
            print(TAG .. "SCENARIO_FAIL " .. tostring(err))
        end
    end
    Events.OnTick.Add(initialize_visual_test)
end)
'''


def prepare(cache, editor=False, auto_start=False, exercise=False, panel_cycle=False, drive=False,
            gameplay=False, save_test=False, visual_final=False):
    if visual_final and not save_test:
        raise ValueError('Final visual inspection requires the explicit isolated --save-test workflow')
    cache = Path(cache).resolve()
    build = (ROOT / 'build').resolve()
    if not cache.is_relative_to(build) or cache == build:
        raise ValueError('Runtime test cache must be a child of the project build directory')
    marker = cache / '.j73-runtime-test.json'
    if cache.exists() and not marker.is_file():
        raise ValueError('Refusing an existing directory without this runtime test marker')
    cache.mkdir(parents=True, exist_ok=True)
    marker.write_text(json.dumps({'purpose': 'Javelin73PC disposable runtime test',
        'saving_enabled': save_test}, indent=2), encoding='utf-8')
    destination = cache / 'mods' / MOD_ID
    install(ROOT / MOD_ID, destination, update=destination.exists())
    hook = destination / '42' / 'media' / 'lua' / 'client' / 'J73RuntimeAudit.lua'
    hook.parent.mkdir(parents=True, exist_ok=True)
    hook.write_text(AUDIT.replace('__OPEN_EDITOR__', 'true' if editor else 'false')
        .replace('__AUTO_START__', 'true' if auto_start else 'false')
        .replace('__EXERCISE__', 'true' if exercise or drive else 'false')
        .replace('__PANEL_CYCLE__', 'true' if panel_cycle else 'false')
        .replace('__DRIVE__', 'true' if drive else 'false')
        .replace('__GAMEPLAY__', 'true' if gameplay or save_test else 'false')
        .replace('__SAVE_TEST__', 'true' if save_test else 'false')
        .replace('__VISUAL_FINAL__', 'true' if visual_final else 'false')
        .replace('__SUITE_DELAY__', '65000' if panel_cycle else ('15000' if exercise or drive else '2000')), encoding='utf-8')
    gameplay_hook = hook.with_name('J73GameplayAudit.lua')
    gameplay_hook.write_text(gameplay_source(save_test), encoding='utf-8')
    (cache / 'mods' / 'default.txt').write_text('VERSION = 1,\n\nmods\n{\n    mod = Javelin73PC,\n}\n\nmaps\n{\n}\n', encoding='utf-8')
    # Native first-run migration otherwise empties default.txt before loading mods.
    (cache / 'mods' / 'reset-mods-42_00.txt').write_text(
        'If this file does not exist, default.txt will be reset to empty (no mods active).\n', encoding='utf-8')
    print('Prepared isolated cache:', cache)
    print('Launch manually with: -cachedir=' + str(cache) + ' -nosteam -debug')
    print('Read console.txt for [J73_AUDIT] results. No user settings or saves were copied.')
    return cache


def gameplay_source(save_test=False):
    """Add a persistence pre-save guard only to the disposable copied hook."""
    source = Path(__file__).with_name('runtime_gameplay.lua').read_text(encoding='utf-8')
    if save_test:
        anchor = '    check(getDebug(), "Persistence test requires debug scenario")'
        if source.count(anchor) != 1:
            raise ValueError('Persistence pre-save guard anchor changed')
        source = source.replace(anchor, anchor + '''
    local currentMods = ActiveMods.getById("currentGame")
    check(currentMods:isModActive("Javelin73PC"), "Refusing save without Javelin73PC in currentGame mods")
    check(not ActiveMods.requiresResetLua(currentMods), "Refusing save with a mismatched loaded mod set")''')
    return source


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--cache', type=Path, default=ROOT / 'build' / 'game-test')
    parser.add_argument('--editor', action='store_true')
    parser.add_argument('--auto-start', action='store_true', help='Start only the disposable visual scenario after the debug menu initializes')
    parser.add_argument('--exercise', action='store_true', help='Check native seat attachments and engine start in the disposable scenario')
    parser.add_argument('--panel-cycle', action='store_true', help='Hold closed, panels open and windows lowered poses for 20 seconds each, then close')
    parser.add_argument('--drive', action='store_true', help='Run seat/engine checks plus low-speed native regulator movement and braking')
    parser.add_argument('--gameplay', action='store_true', help='Run native timed seat entry, mechanics callback/repair and light-state checks')
    parser.add_argument('--save-test', action='store_true', help='Enable saving only in this isolated cache, run gameplay checks, save tagged car and resume exact test world on next auto-start')
    parser.add_argument('--visual-final', action='store_true', help='After successful isolated save reload, hold night headlights for 60 seconds, then restore lamp/time state; requires --save-test')
    args = parser.parse_args()
    prepare(args.cache, args.editor, args.auto_start, args.exercise, args.panel_cycle, args.drive,
            args.gameplay, args.save_test, args.visual_final)
