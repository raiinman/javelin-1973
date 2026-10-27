require "ISUI/ISButton"
require "ISUI/ISLabel"

local Order = {}
local installed = false
local undo
local backupFile = "DeadSignalFastLoad-startup-order-backup.txt"

local function readOrder(active)
    local list = active:getMods()
    local ids, seen = {}, {}
    for index = 0, list:size() - 1 do
        local id = list:get(index)
        if type(id) ~= "string" or id == "" or id:find("[\r\n]") or seen[id] then
            error("Invalid or duplicate mod ID; startup mods unchanged.")
        end
        ids[#ids + 1], seen[id] = id, true
    end
    return ids, seen
end

local function equal(a, b)
    if #a ~= #b then return false end
    for index, id in ipairs(a) do
        if b[index] ~= id then return false end
    end
    return true
end

local function validateEnabled(ids, enabled)
    for _, id in ipairs(ids) do
        local info = getModInfoByID(id)
        if not info or not info:isAvailable() then
            error("Required mod is missing or unavailable: " .. id .. ". Nothing changed.")
        end
        local required = info:getRequire()
        if required then
            for index = 0, required:size() - 1 do
                local dependency = required:get(index)
                if not enabled[dependency] then
                    error("The saved list omits a dependency: " .. dependency .. ". Nothing changed.")
                end
            end
        end
    end
end

local function difference(before, currentSet, after, saveSet)
    local added, removed = {}, {}
    for _, id in ipairs(after) do if not currentSet[id] then added[#added + 1] = id end end
    for _, id in ipairs(before) do if not saveSet[id] then removed[#removed + 1] = id end end
    local detail = "Enable: " .. (#added > 0 and table.concat(added, ", ") or "none")
        .. "\nDisable: " .. (#removed > 0 and table.concat(removed, ", ") or "none")
        .. "\nCopies the save's exact mod order. Applies after a manual restart; never loads a save."
    if not saveSet.DeadSignalFastLoad then
        detail = detail .. "\nFast Load will also be disabled next launch. Use Undo before restarting to keep it."
    end
    return "Enable " .. #added .. "; disable " .. #removed, detail
end

local function selectedMods(screen)
    local row = screen.listbox.items[screen.listbox.selected]
    if not row then error("Select a single-player save first.") end
    local info = getSaveInfo(row.text)
    if not info or type(info.gameMode) ~= "string"
        or info.gameMode == "Multiplayer" or info.gameMode == "LastStand" then
        error("Select an ordinary single-player save.")
    end
    if not info.activeMods then error("This save has no stored mod list.") end
    return readOrder(info.activeMods)
end

local function setOrder(active, ids)
    local list = active:getMods()
    list:clear()
    for _, id in ipairs(ids) do list:add(id) end
end

local function backup(ids)
    local writer = getFileWriter(backupFile, true, false)
    if not writer then error("Cannot write startup-mod backup; nothing changed.") end
    local ok, err = pcall(function()
        writer:write("Dead Signal Fast Load startup enabled mods and order backup\n")
        for _, id in ipairs(ids) do writer:write(id .. "\n") end
    end)
    local closed, closeError = pcall(function() writer:close() end)
    if not ok then error(err) end
    if not closed then error(closeError) end
end

local function persist(active, before, after)
    if type(saveModsFile) ~= "function" then error("Native preset saving is unavailable.") end
    backup(before)
    local ok, err = pcall(function()
        setOrder(active, after)
        saveModsFile()
    end)
    if not ok then
        pcall(function() setOrder(active, before); saveModsFile() end)
        error("Startup update failed; restoration attempted: " .. tostring(err))
    end
    -- Native saveModsFile returns void and logs disk failures internally.
    -- Do not change the loaded-mod snapshot or trigger a Lua reset here.
end

function Order.match(screen)
    if getPlayer() or isIngameState() or isClient() or isServer() then
        error("Startup mods can only be changed at the main menu.")
    end
    local active = ActiveMods.getById("default")
    local before, currentSet = readOrder(active)
    local after, saveSet = selectedMods(screen)
    validateEnabled(after, saveSet)
    if equal(before, after) then return "Already matches", "Startup enabled mods and order already match this save." end
    local _, detail = difference(before, currentSet, after, saveSet)
    persist(active, before, after)
    undo = { before = before, after = after }
    return "Updated; restart manually", "Startup enabled mods and order updated.\n" .. detail
end

function Order.undo()
    if getPlayer() or isIngameState() or isClient() or isServer() then
        error("Undo is available only at the main menu.")
    end
    if not undo then error("Nothing to undo in this session.") end
    local active = ActiveMods.getById("default")
    local current = readOrder(active)
    if not equal(current, undo.after) then
        error("Startup mods changed since matching. Undo will not overwrite those edits.")
    end
    local enabled = {}
    for _, id in ipairs(undo.before) do enabled[id] = true end
    validateEnabled(undo.before, enabled)
    persist(active, current, undo.before)
    undo = nil
    return "Previous mods restored", "Previous startup enabled mods and order restored. Restart manually to use them."
end

local function act(screen, operation)
    local ok, short, detail = pcall(operation, screen)
    screen.deadSignalOrderStatus:setName(ok and short or "Could not finish: see tooltip")
    screen.deadSignalOrderButton.tooltip = ok and detail or tostring(short)
    screen.deadSignalOrderUndo:setEnable(undo ~= nil)
    screen.deadSignalOrderResult = true
end

function Order.attach(screen)
    if screen.deadSignalOrderButton or not screen.listbox or not screen.infoPanel
        or not screen.configPanel or not screen.backButton then return end
    local x, y = screen.listbox.x, screen.listbox.y
    local height = screen.backButton.height
    local gap = UI_BORDER_SPACING or 8
    local rowHeight = height + gap
    for _, panel in ipairs({screen.listbox, screen.infoPanel, screen.configPanel}) do
        panel:setY(panel.y + rowHeight)
        panel:setHeight(math.max(height, panel.height - rowHeight))
    end
    local width = getTextManager():MeasureStringX(UIFont.Small, "Match startup mods") + gap * 4
    local button = ISButton:new(x, y, width, height, "Match startup mods", screen,
        function(owner) act(owner, Order.match) end)
    button:initialise()
    button:instantiate()
    button:setFont(UIFont.Small)
    button.tooltip = "Match startup enabled mods and order to the selected save. Hover after selecting for enable/disable details. Never loads a save."
    screen:addChild(button)
    screen.deadSignalOrderButton = button
    local undoButton = ISButton:new(button:getRight() + gap, y, 80, height, "Undo", screen,
        function(owner) act(owner, Order.undo) end)
    undoButton:initialise()
    undoButton:instantiate()
    undoButton.tooltip = "Restore the last change in this session. A text backup is also kept by Fast Load."
    undoButton:setEnable(undo ~= nil)
    screen:addChild(undoButton)
    screen.deadSignalOrderUndo = undoButton
    local status = ISLabel:new(undoButton:getRight() + gap, y, height,
        "Select a save, then match", 1, 1, 1, 1, UIFont.Small, true)
    status:initialise()
    screen:addChild(status)
    screen.deadSignalOrderStatus = status
end

function Order.install()
    if installed or not LoadGameScreen or not LoadGameScreen.create
        or not LoadGameScreen.prerender then return end
    local create = LoadGameScreen.create
    LoadGameScreen.create = function(self, ...)
        create(self, ...)
        Order.attach(self)
    end
    local prerender = LoadGameScreen.prerender
    LoadGameScreen.prerender = function(self, ...)
        prerender(self, ...)
        if self.deadSignalOrderButton then
            local row = self.listbox.items[self.listbox.selected]
            self.deadSignalOrderButton:setEnable(row ~= nil)
            self.deadSignalOrderUndo:setEnable(undo ~= nil)
            if self.deadSignalOrderRow ~= row then
                self.deadSignalOrderRow = row
                self.deadSignalOrderResult = false
            end
            if not self.deadSignalOrderResult and row then
                local ok, short, detail = pcall(function()
                    local before, currentSet = readOrder(ActiveMods.getById("default"))
                    local after, saveSet = selectedMods(self)
                    return difference(before, currentSet, after, saveSet)
                end)
                self.deadSignalOrderStatus:setName(ok and short or "Select a valid save")
                self.deadSignalOrderButton.tooltip = ok and detail or tostring(short)
                self.deadSignalOrderResult = true
            end
        end
    end
    installed = true
    local screen = LoadGameScreen.instance or (MainScreen and MainScreen.instance and MainScreen.instance.loadScreen)
    if screen then Order.attach(screen) end
end

return Order
