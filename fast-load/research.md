# Fast Load startup workaround evidence

Current0.0.7 presentation: see startup-art.md for the Project Zomboid themed scene and exact render boundary. The0.0.4 whitespace warning overrides described below are historical and have been removed. This restores native warning text, without claiming to animate pre-Lua initialization or accelerate it.

Target: installed Project Zomboid 42.20.4. Revision 0.0.3 is based on read-only inspection of shipped Lua and Java bytecode. No tests, game launch or native bypass observation occurred. Earlier native results validate only 0.0.1.

## Why an earlier queue does not prevent a later bypass

- GameWindow.initShared queues TISLogoState, TermsOfServiceState and MainScreenState. This happens before ordinary mod Lua loads. Changing the debug logo option at OnGameBoot therefore cannot remove the queued state.
- GameWindow's later OnGameBoot dispatch occurs after required startup initialization and before the normal game-state loop. A transition can still be requested at that point. The earlier conclusion that there was no ordinary workaround was too broad.
- LuaManager.Exposer.exposeAll explicitly exposes TermsOfServiceState and MainScreenState in its normal class list. LuaJavaClassExposer.exposeStatics exposes public, non-HiddenFromLua constructors as `new`. The installed TermsOfServiceState constructor is public and has no HiddenFromLua annotation. This does not depend on debug-only reflection.
- The public Lua global forceChangeState calls GameWindow.states.forceNextState. It writes the native pending transition, not a copied Lua camera/state field.
- GameStateMachine.update enters the initial state, then handles forceNext before calling current.update. It calls the old state's exit and the requested state's enter. GameWindow.frameStep performs logic before rendering. TISLogoState.enter only suspends UI and initializes alpha; exit unsuspends UI. Consequently a boot-time transition should skip its animation and logo rendering.

## Selected target and lifecycle

- Request the existing next state type, TermsOfServiceState, rather than a world-loading state or an unrelated state. Its enter dispatches OnGameStateEnter. The shipped ISTermsOfServiceUI handler checks the current native accepted version and either exits immediately or presents native terms. Acceptance is never manufactured by this mod.
- A forced state preserves stateIndex. When the requested terms state completes, the queue can enter the original terms state and then the original menu. Accepted terms need no input in either pass. This extra state entry is an explicit compatibility/latency caveat, not a claimed native measurement.
- A native MainScreenState.getInstance result distinguishes a subsequent Lua reset from cold startup. The adapter also handles its boot hook once per Lua environment and excludes loaded/in-game players, clients, servers, Escape bypass and a disabled preference.
- Removed the animation clock boost and restoration watchdog entirely. The current route never changes GameTime, never calls Continue and never selects a save.
- Existing menu optimizations remain: MainScreen's 500ms ready-input delay and warningFade clear once per menu instance; Core's menu video-effects option is borrowed/restored for the original background. MainOptions.toUI is wrapped so native options read the restored value. Compatibility with other mods remains untested.

## Boundaries and retained material

This skips a queued presentation stage after ordinary Lua has loaded. It cannot remove pre-Lua engine initialization or the loading/warning image shown during that work. Shader, asset and world loading remain. No change to final Click to Start is included. There is no camera, Toolkit, Java loader, external installer or engine-file dependency.

Read-only bytecode extracts remain outside distributed files in ignored build/fast-load/{game-window-bytecode,lua-exposer,class-exposer,main-menu-bytecode}.txt. Context7 documentation corroborated native transition signatures; installed bytes supply the actual ordering and exposure evidence. The REA workflow uses the previously identified installed archive, with local javap for focused Java inspection. No REA runtime attachment or target execution was used here.

## Pre-Lua loading/warning audit, revision 0.0.4

Read-only REA open_binary reconfirmed projectzomboid.jar SHA-256 80e405a4bfc42f6072e75b3735f458a6514143da011d3226007ded305a442f44. Focused javap inspection and shipped translation data establish:

- GameWindow.init bytecode calls loadMods(default) at 117, loadModPackFiles at 123, initFonts at 231, Translator.loadFiles at 234, doEpilepsyWarningText at 237, LuaManager.init at 240, initShared at 243 and LuaManager.LoadDirBase at 259. The warning precedes both the mod Lua loader and initial Lua environment creation.
- doEpilepsyWarningText draws a black rectangle, draws UI_EpilepsyWarning_1 through _8 and ends the frame. It has no sleep, countdown, state update or separate acceptance gate. Removing its text does not remove a timer or make the menu ready sooner. DoLoadingText in this archive only logs its argument.
- LuaManager.init constructs the J2SEPlatform, environment, Kahlua threads and exposer. Calling mod Lua earlier through OnGameBoot, shared scripts, require order or a copied Java method cannot affect a warning already drawn before this environment exists.
- ZomboidFileSystem.loadMod registers files in the active file map. loadModPackFiles calls GameWindow.LoadTexturePack and updates texture lookup. The inspected mod.info parser and file/pack-loading path contain no Workshop Java bootstrap/class-loader or early Lua execution mechanism. Changing dependency order does not move execution before Lua initialization.
- Translator.tryFillMapFromMods reads the mod's common and version directories before the warning. tryFillMapFromFile loads JSON data, not Lua source. Its value-merging lambda ignores an empty replacement if the key already exists. A single ASCII space is nonempty and produces no visible warning text.
- The source-derived candidate therefore supplies only eight original whitespace-valued translation entries per installed UI locale. It does not replace entire game language files. It is an early data override and cannot execute a menu transition or skip native initialization. Supported locale names: AR, CA, CH, CN, CS, DA, DE, EN, ES, ES_CL, ES_MX, FI, FR, HU, ID, IT, JP, KO, NL, NO, PL, PT, PTBR, RO, RU, STREW, TH, TR, UA.

No alternative path to a functional main menu before required startup was found within the standalone Workshop contract. Deliberately broken font/pack resources, misleading menu images and uninitialized forced menu entry were rejected as substitutes for a working menu. The only new runtime-package change is warning-text suppression; the 0.0.3 native logo bypass remains unproven. No test, syntax compilation or game launch was performed.

The additional bytecode extracts are ignored build/fast-load/{filesystem,mod-info,mod-parser,translator,lua-manager}-bytecode.txt. Context7 supplied API names but not startup ordering; the installed bytecode is the basis of the ordering above. The requested skill-library was inspected and its installed REA/debugging workflows applied.

## Actual-work follow-up

See performance-audit.md for the native texture budget/thread/task limits, the isolated startup/save ordered-mod mismatch that can trigger an extra Lua reset, and version-qualified community QoL targets. This was read-only investigation. No new runtime code or package was produced, no mod profiles were edited, and no tests or game launch occurred. The 0.0.4 warning suppression remains cosmetic; a measured loading-speed improvement has not been established.

## Selected-save startup order integration, 0.0.5

The native LoadGameScreen list entries expose the selected save path in row.text; getSaveInfo(row.text) reads its ActiveMods. The new module adds a toolbar row above the list/info/config panels, preserving native save selection and play behavior. On explicit button input only, it validates identical unique mod-ID membership, writes a text backup, replaces default.getMods order and invokes saveModsFile. It does not copy map order or touch currentGame, saved ActiveMods or setLoadedMods. Matching lists avoids the normal requiresResetLua mismatch only after a fresh manual launch using the changed startup preset. It does not skip a currently required reset.

Native ZomboidFileSystem.saveModsFile writes the default ActiveMods via ActiveModsFile.write but discards its boolean return and catches/logs exceptions. The exposed Lua API is void; a protected Lua call cannot verify successful disk persistence. The candidate attempts rollback on surfaced Lua errors and provides a session Undo guarded by exact equality with the last applied order. Backup errors abort before preset mutation. Undo after a restart is deliberately not implemented; the retained text file supports manual ordering through Mods.

The implementation was source-inspected and packaged only. The future checker was adapted to compile the new module without executing it; the existing startup fixture stubs its install hook. No test, syntax compilation, game launch, preset action or save action was executed in this session. Root instructions and camera/vehicle documents remain unchanged because their existing contracts already cover this independent mod and no behavior in those domains changed.

## Exact enabled-list matching, 0.0.6

The user expanded the action from same-membership ordering to the chosen save's exact enabled IDs and order. The old same-set guard is removed. The selected native save metadata is still read fresh on action, copied into a validated Lua list, and applied only to default ActiveMods.getMods through native saveModsFile. Map order and saved/current/loaded metadata remain unchanged. The preview reports additions/removals; the click does not request Continue, ResetLua, restart or Workshop downloads.

Native getModInfoByID/isAvailable/getRequire follow the game's own availability/dependency interfaces. The candidate rejects unavailable IDs and dependencies omitted from the target list instead of silently expanding it. An explicit zero-mod save is allowed; a save without activeMods metadata is not guessed. Fast Load is not retained if absent, so its UI will be unavailable after restart unless the user enables it again. Session Undo restores the complete previous list and order, provided no intervening edits occurred and the old target remains valid. The text backup covers those IDs and ordering and remains a manual reference after restart.

Source inspection and packaging only, with no tests, compilation or launch. Native void persistence limitations remain unchanged. Existing checker coverage for the UI module remains compile-only, with the parent startup fixture stubbing installation. Root/camera/vehicle docs remain unchanged; this scope and the expanded explicit-click contract are recorded in the owning Fast Load instructions.
