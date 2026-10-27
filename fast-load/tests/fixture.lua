Events = {}
-- Existing startup fixture excludes the separate native Load-screen integration.
function require(name)
    if name == "DeadSignalFastLoad/StartupOrder" then return {install = function() end} end
    if name == "DeadSignalFastLoad/StartupScene" then
        return {install=function() end, boot=function() end, closeBoot=function() end,
            setEnabled=function() end, setReducedMotion=function() end}
    end
    if name == "DeadSignalFastLoad/SurvivalTips" then return {setEnabled=function() end} end
end
for _, name in ipairs({"OnGameBoot", "OnMainMenuEnter", "OnFETick", "OnResetLua", "OnPreMapLoad", "OnGameStart", "OnRenderTick"}) do
    local handlers = {}
    Events[name] = { Add = function(fn) handlers[#handlers + 1] = fn end,
        Remove = function(fn) for i = #handlers, 1, -1 do if handlers[i] == fn then table.remove(handlers, i) end end end,
        fire = function(...) local copy = {}; for i, fn in ipairs(handlers) do copy[i] = fn end; for _, fn in ipairs(copy) do fn(...) end end }
end
clock, escaped, clicked, client, server, continues = 0, false, false, false, false, 0
Keyboard = { KEY_ESCAPE = 1 }
function getTimestampMs() return clock end
function isKeyDown() return escaped end
function isMouseButtonDown() return clicked end
function isClient() return client end
function isServer() return server end
function getPlayer() return nil end
function isIngameState() return false end
function getFileReader() return nil end
function getFileWriter() return { write = function() end, close = function() end } end
function getLatestSave() return { "FixtureWorld", "Sandbox" } end
MainScreen = { instance = { inGame = false, delay = 500, warningFade = 10,
    latestSaveOption = { isVisible = function() return true end } },
    continueLatestSave = function(mode, name)
        assert(mode == "Sandbox" and name == "FixtureWorld")
        continues = continues + 1
    end }

videoEffects, optionsVisible = true, false
local core = {
    getOptionDoVideoEffects = function() return videoEffects end,
    setOptionDoVideoEffects = function(self, value) videoEffects = value end
}
function getCore() return core end
MainOptions = {
    instance = {getIsVisible = function() return optionsVisible end},
    toUI = function() assert(videoEffects == true, "Restore before options read native value") end
}

startupRequests, menuState = {}, nil
MainScreenState = {getInstance = function() return menuState end}
TermsOfServiceState = {new = function() return {kind = "nativeTermsCheck"} end}
function forceChangeState(target) startupRequests[#startupRequests + 1] = target end
