# Actual performance and QoL audit

Scope: installed 42.20.4, standalone Steam Workshop, manual save loading. Read-only REA, javap, shipped Lua and existing logs. No benchmark, test, compilation, launch, runtime patch or mod-list change was performed. No new release or speedup claim results from this audit.

## Concrete opportunity in the isolated profile: avoid a second Lua environment load

MainScreen.continueLatestSaveAux reads the chosen save's activeMods and copies them to currentGame. Unless already returning from a reset, ActiveMods.requiresResetLua(currentMods) causes Core.ResetLua(currentGame, continueSave). The installed ActiveMods bytecode compares the ordered Java mod lists with ArrayList.equals. Both membership and order matter. The game already skips this reset when the ordered lists match; overriding the predicate or pretending a different set is loaded would be incorrect.

The owned Toolkit profile's startup/default list and isolated save have the same six IDs, but differ in two positions:

| Position | Startup/default | Save |
|---|---|---|
| 1 | PZToolkitBridge | PZToolkitBridge |
| 2 | Javelin73PC | Javelin73PC |
| 3 | DeadSignalCameraProbe | DeadSignalCamera |
| 4 | DeadSignalCamera | DeadSignalCameraProbe |
| 5 | DeadSignalCameraTransformProbe | DeadSignalCameraTransformProbe |
| 6 | DeadSignalFastLoad | DeadSignalFastLoad |

For a future launch, use the game's Mods/preset UI to put startup/default in the save's existing order. Preserve every ID and the save's order. That makes the native ordered-list condition false for this save, avoiding its Lua-reset branch when no later change intervenes. This reduces work between selecting Continue and world loading, not the mandatory first cold startup. No seconds saved are measured. Do not sort both lists arbitrarily or skip a required reset.

The historical console has two Lua boot messages separated by 22.5 seconds and a world-loading report of 31 seconds. That is evidence of a repeated boot path in that older session, not a benchmark of this correction or a claim that the whole interval would be saved. Profile files were left unchanged because mod management belongs in the game's UI and the user requested no game launch/testing.

A useful standalone Fast Load feature would report startup/save differences and offer an explicit, reviewed preset workflow through native mod-management UI. Never silently rewrite global profiles, remove mods, fake loaded-mod state, auto-load a save, or call requiresResetLua false for unequal lists. Implemented later as the untested 0.0.5 Match startup order action, restricted to reordering identical enabled mod sets. The audit itself did not apply it or measure savings.

## Java loader limits confirmed in installed bytes

TextureIDAssetManager.waitFileTask loops while DirectBufferAllocator.getBytesAllocated exceeds 52,428,800 bytes (50 MiB), sleeping 20 ms per check. FileSystemImpl constructs a fixed pool of two threads on machines with at most four processors, otherwise four threads. Async in-progress work is bounded using 16. These are real work/budget controls, unlike warning suppression. The inspected public APIs and normal Lua exposure provide no supported setter to replace those hardcoded controls. Assigning fields on a copied Lua class table would not patch the Java instructions.

Changing those controls, parallelizing native script/folder scanning and retaining compiled Lua across engine resets are engine modifications. No Workshop-only execution mechanism was established for them. The author of Lugli Fast Loading explicitly requires ZombieBuddy for engine changes; its Lua-only fallback covers two loot paths. Its reported gains are not evidence that our plain Workshop package has those gains. [Author source](https://raw.githubusercontent.com/ViniciosLugli/PZWorkspace/main/Lugli_FastLoading/README.md).

## Lua-only candidates, with boundaries

- Repeated loot rebuilds: coalescing third-party Lua requests can remove duplicate full parses on affected mod lists. However, no ItemPickerJava.Parse call was found in shipped Lua in this audit; IsoWorld.parseDistributions calls it directly in Java. A Lua-table wrapper cannot intercept that native call. Deferring a third-party parse can also break callers that immediately inspect its output. Do not ship unconditional deferral or claim a vanilla benefit.
- Inventory/menu stalls: current ISInventoryPane.refreshContainer rebuilds only when requested and the rendering path already checks native draw-dirty state. Do not throttle refresh blindly or cache item state without invalidating on transfers, names, weight, equipped/hotbar state and language changes.
- Tooltip work: ISToolTipInv performs a measurement pass and a drawing pass. Those calls are not established as redundant. Removing measurement without preserving layout is not an optimization.
- Crafting/recipe browsing: indexed name/ingredient search, recent/favorite recipes and quick reopening are useful UI QoL candidates. Any cache must be invalidated when recipes, language or mod state change; ingredient availability must remain live. This is a candidate, not a measured bottleneck in this installation.

## Community signal and version checks

1. Presets and clear mod-order/dependency diagnostics: the author describes these as core features of [Mod Manager Reforged](https://steamcommunity.com/sharedfiles/filedetails/?id=3737874810). This supports demand, not a recommendation to install an unverified dependency.
2. Inventory organization, container rules, hotbar/container ordering, condition indicators and direct crafting lookup appear in [community QoL requests](https://www.reddit.com/r/projectzomboid/comments/1l4uaob/qol_mods/). These save player actions and can fit ordinary client Lua; they are not engine FPS fixes. Avoid replacing whole UI classes when a small hook is sufficient.
3. Right-click crafting freezes have historical demand, but the [official-community bug thread](https://steamcommunity.com/app/108600/discussions/6/592887534192729789/) marks its reported 42.2.0 issue improved/fixed in 42.4.0. Do not repackage that old report as proof the same bug exists in 42.20.4.
4. Main-menu stutter has [player reports](https://www.reddit.com/r/projectzomboid/comments/1vis936/build_42_startup_menu_lag/). The existing light-menu option avoids background video while enabled, but we have no measured CPU/FPS/startup gain. It is distinct from completing loading sooner.

## Priority

First: align the isolated startup preset to the existing save order through the game UI when the no-launch constraint permits it. The native selected-save order action is now implemented in 0.0.5 but untested. Further candidates are recipe navigation and inventory organization if selected for implementation. Keep the camera as its separate product. Defer native asset-budget/concurrency patches under the standalone-only contract. Avoid fake progress from another cosmetic release or unmeasured global caching.

Read-only artifact identity remains projectzomboid.jar SHA-256 80e405a4bfc42f6072e75b3735f458a6514143da011d3226007ded305a442f44. Additional extracts are ignored build/fast-load/{texture-loader,file-task,active-mods,world-loader}-bytecode.txt. Root/camera/vehicle contracts are unchanged: this audit does not add a product or alter their runtime behavior.

The selected-save order action is now packaged in 0.0.5. Its prospective benefit remains the same conditional native branch avoidance, not a measured speed claim.

Version 0.0.6 expands that explicit action to the selected save's exact enabled list as well as order, with availability/dependency checks and an enable/disable preview. It can disable startup-only mods, including Fast Load itself if omitted from the save. Backup and session Undo now restore both membership and order. No profile change or benchmark was executed during development.
