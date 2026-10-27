DeadSignalFastLoad = {}
local api = DeadSignalFastLoad
local StartupOrder = require "DeadSignalFastLoad/StartupOrder"
local StartupScene = require "DeadSignalFastLoad/StartupScene"
local SurvivalTips = require "DeadSignalFastLoad/SurvivalTips"
local state = {}
local config = { skipStartup = true, lightweightMenu = true, animatedScene = true, reducedMotion = false, survivalTips = true }
local preferenceFile = "DeadSignalFastLoad.ini"

local function log(message)
    print("[DeadSignalFastLoad] " .. message)
end

local function loadPreferences()
    local reader
    local ok = pcall(function()
        reader = getFileReader(preferenceFile, false)
        if not reader then return end
        local line = reader:readLine()
        while line do
            -- Ignore legacy autoContinue preferences. Never resume a save automatically.
            if line == "lightweightMenu=false" then config.lightweightMenu = false end
            if line == "lightweightMenu=true" then config.lightweightMenu = true end
            if line == "skipStartup=false" then config.skipStartup = false end
            if line == "skipStartup=true" then config.skipStartup = true end
            if line == "animatedScene=false" then config.animatedScene = false end
            if line == "animatedScene=true" then config.animatedScene = true end
            if line == "reducedMotion=false" then config.reducedMotion = false end
            if line == "reducedMotion=true" then config.reducedMotion = true end
            if line == "survivalTips=false" then config.survivalTips = false end
            if line == "survivalTips=true" then config.survivalTips = true end
            line = reader:readLine()
        end
    end)
    if reader then pcall(function() reader:close() end) end
    if not ok then log("Preferences unavailable; using defaults.") end
end

local function savePreferences()
    local writer
    local ok, err = pcall(function()
        writer = getFileWriter(preferenceFile, true, false)
        if not writer then error("Preference writer unavailable") end
        writer:write("skipStartup=" .. tostring(config.skipStartup) .. "\n")
        writer:write("lightweightMenu=" .. tostring(config.lightweightMenu) .. "\n")
        writer:write("animatedScene=" .. tostring(config.animatedScene) .. "\n")
        writer:write("reducedMotion=" .. tostring(config.reducedMotion) .. "\n")
        writer:write("survivalTips=" .. tostring(config.survivalTips) .. "\n")
    end)
    if writer then pcall(function() writer:close() end) end
    if not ok then log("Preference changed for this session only: " .. tostring(err)) end
end

function api.setSkipStartup(enabled)
    config.skipStartup = enabled == true
    savePreferences()
    if state.introButton then
        state.introButton:setTitle("Fast Load: skip startup " .. (config.skipStartup and "ON" or "OFF"))
    end
end

function api.getSkipStartup() return config.skipStartup end

local function skipStartup()
    if state.bootHandled then return end
    state.bootHandled = true
    if not config.skipStartup or isClient() or isServer() or getPlayer()
        or isIngameState() or isKeyDown(Keyboard.KEY_ESCAPE) then return end
    local ok, err = pcall(function()
        if not MainScreenState or not MainScreenState.getInstance
            or not TermsOfServiceState or not TermsOfServiceState.new
            or not forceChangeState then
            log("Startup bypass API unavailable; native startup retained.")
            return
        end
        -- An existing menu identifies a Lua reset, not a fresh application boot.
        if MainScreenState.getInstance() then return end
        -- shortcut: forceNext preserves the queue index, so the queued terms
        -- state can run again before the menu. Keep its native acceptance logic.
        forceChangeState(TermsOfServiceState.new())
        log("Requested native startup-logo bypass; required initialization and terms retained.")
    end)
    if not ok then log("Startup bypass unavailable; native startup retained: " .. tostring(err)) end
end

local function restoreVideo()
    if state.originalVideo == nil then return end
    local ok = pcall(function()
        local core = getCore()
        if core:getOptionDoVideoEffects() == false then
            core:setOptionDoVideoEffects(state.originalVideo)
        end
    end)
    if ok then state.originalVideo = nil end
end

local function protectOptions()
    if not MainOptions or not MainOptions.toUI or state.optionsHooked then return end
    local original = MainOptions.toUI
    MainOptions.toUI = function(self, ...)
        -- Restore before native controls read their values, not one tick later.
        restoreVideo()
        return original(self, ...)
    end
    state.optionsHooked = true
end

function api.setLightweightMenu(enabled)
    config.lightweightMenu = enabled == true
    if not config.lightweightMenu then restoreVideo() end
    savePreferences()
    if state.menuButton then
        state.menuButton:setTitle("Fast Load: light menu " .. (config.lightweightMenu and "ON" or "OFF"))
    end
end

function api.getLightweightMenu() return config.lightweightMenu end

local function createButtons(menu)
    for _, button in pairs({state.introButton, state.menuButton, state.sceneButton, state.motionButton, state.tipsButton}) do
        if button.parent then button.parent:removeChild(button) end
    end
    state.introButton, state.menuButton = nil, nil
    state.sceneButton, state.motionButton = nil, nil
    state.tipsButton = nil
    if not ISButton then return end
    local intro = ISButton:new(getCore():getScreenWidth() - 320, 16, 300, 28,
        "Fast Load: skip startup " .. (config.skipStartup and "ON" or "OFF"), nil,
        function() api.setSkipStartup(not config.skipStartup) end)
    intro:initialise()
    intro.tooltip = "Applies next launch. Bypasses startup logos; required initialization and terms remain."
    menu:addChild(intro)
    state.introButton = intro
    local light = ISButton:new(getCore():getScreenWidth() - 320, 50, 300, 28,
        "Fast Load: light menu " .. (config.lightweightMenu and "ON" or "OFF"), nil,
        function() api.setLightweightMenu(not config.lightweightMenu) end)
    light:initialise()
    light.tooltip = "Uses the original menu background instead of video effects. Restored before gameplay."
    menu:addChild(light)
    state.menuButton = light
    local scene = ISButton:new(getCore():getScreenWidth() - 320, 84, 300, 28,
        "Rainy Knox County: " .. (config.animatedScene and "ON" or "OFF"), nil,
        function()
            config.animatedScene = not config.animatedScene
            StartupScene.setEnabled(config.animatedScene)
            state.sceneButton:setTitle("Rainy Knox County: " .. (config.animatedScene and "ON" or "OFF"))
            savePreferences()
        end)
    scene:initialise()
    scene.tooltip = "Original animated street scene behind the native menu. Adds no waiting screen."
    menu:addChild(scene)
    state.sceneButton = scene
    local motion = ISButton:new(getCore():getScreenWidth() - 320, 118, 300, 28,
        "Reduced motion: " .. (config.reducedMotion and "ON" or "OFF"), nil,
        function()
            config.reducedMotion = not config.reducedMotion
            StartupScene.setReducedMotion(config.reducedMotion)
            state.motionButton:setTitle("Reduced motion: " .. (config.reducedMotion and "ON" or "OFF"))
            savePreferences()
        end)
    motion:initialise()
    motion.tooltip = "Keeps the street artwork still and removes animated rain. No flashing effects or added sound."
    menu:addChild(motion)
    state.motionButton = motion
    local tips = ISButton:new(getCore():getScreenWidth() - 320, 152, 300, 28,
        "Survival cards: " .. (config.survivalTips and "ON" or "OFF"), nil,
        function()
            config.survivalTips = not config.survivalTips
            SurvivalTips.setEnabled(config.survivalTips)
            state.tipsButton:setTitle("Survival cards: " .. (config.survivalTips and "ON" or "OFF"))
            savePreferences()
        end)
    tips:initialise()
    tips.tooltip = "120 menu cards, rotating every 12 seconds. Hover to hold a card. Native save-loading tips use the game's own random picker."
    menu:addChild(tips)
    state.tipsButton = tips
end

local function menuTick()
    local menu = MainScreen and MainScreen.instance
    if not menu or menu.inGame then return end
    if state.menu ~= menu then
        StartupScene.install()
        menu.delay = 0
        menu.warningFade = 0
        createButtons(menu)
        state.menu = menu
    end
    local options = MainOptions and MainOptions.instance
    if not config.lightweightMenu or (options and options:getIsVisible()) then
        restoreVideo()
    elseif state.originalVideo == nil then
        pcall(function()
            local core = getCore()
            if core:getOptionDoVideoEffects() then
                state.originalVideo = true
                core:setOptionDoVideoEffects(false)
            end
        end)
    end
end

local function leaveMenu()
    StartupScene.closeBoot()
    restoreVideo()
    if state.menuTickAttached then
        Events.OnFETick.Remove(menuTick)
        state.menuTickAttached = false
    end
    state.menu = nil
end

loadPreferences()
StartupScene.setEnabled(config.animatedScene)
StartupScene.setReducedMotion(config.reducedMotion)
SurvivalTips.setEnabled(config.survivalTips)
Events.OnGameBoot.Add(StartupScene.boot)
Events.OnGameBoot.Add(skipStartup)
Events.OnMainMenuEnter.Add(function()
    StartupScene.install()
    StartupOrder.install()
    protectOptions()
    state.menu = nil
    if not state.menuTickAttached then
        Events.OnFETick.Add(menuTick)
        state.menuTickAttached = true
    end
end)
Events.OnResetLua.Add(function()
    leaveMenu()
    local menu = MainScreen and MainScreen.instance
    if menu and not menu.inGame then
        Events.OnFETick.Add(menuTick)
        state.menuTickAttached = true
    end
end)
Events.OnPreMapLoad.Add(leaveMenu)
Events.OnGameStart.Add(leaveMenu)
