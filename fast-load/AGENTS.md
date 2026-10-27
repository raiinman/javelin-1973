# Purpose

- Own the independent Dead Signal Fast Load Workshop mod and startup/load-time investigation.

# Ownership

- `DeadSignalFastLoad/` owns original ordinary-mod runtime files, the Knox County background texture, client/DeadSignalFastLoad/StartupScene.lua for animated front-end artwork and StartupOrder.lua for native Load-screen enabled-list/order matching.
- `startup-art.md` owns the original artwork prompt, animation contract and rendering limits.
- `startup-preview.html` is a development-only browser animation preview, not native-game evidence or a distributed mod file.
- `survival-tips-research.md` records three sequential content research passes, source limits and native loading evidence. `survival-tips.tsv` is the original120-tip content source; `build_tip_data.py` generates the EN UI keys, TipIndex.lua and development preview data without executing tests.
- `SurvivalTips.lua` owns the independent menu/boot carousel, wrapping and mod-owned persistent shuffle cursor. Native existing-save loading consumes the additive `UI_quick_tip_FL_*` translation keys through its own picker.
- `research.md` owns startup ordering, supported optimization evidence and limits.
- `performance-audit.md` owns actual-work bottlenecks, the isolated ordered-mod mismatch and community-backed QoL candidates. Read it before adding performance claims, caching, parse deferral or preset integration.
- `verification.md` owns executable checks and native timing/results.
- `tests/` owns the actual runtime adapter's controlled Kahlua lifecycle fixture; `check_fast_load.py` compiles, checks and packages the independent mod.
- Generated ZIP and private Workshop upload draft stay under ignored root `build/fast-load/`. Publication and preview validation are separate gates.

# Local Contracts

- This is a separate product from the camera mod, without a runtime dependency on it or Toolkit.
- Target faster startup to the menu and faster entry into a saved game, including removal of unnecessary intro/wait steps wherever ordinary mod APIs permit.
- Preserve saves, required initialization, validation, installed game files and existing user preferences. Do not silently disable content or degrade graphics as a loading optimization.
- Use ordinary Workshop loading without an external installer or engine file replacement. Debug-only capabilities must be labeled and cannot establish normal-mode support.
- First native tests use the owned isolated Toolkit profile. Launch through Toolkit Connection and verify staged PC-side files through Remote Desktop Commander.

# Work Guidance

- Inspect shipped startup code and mod-load ordering before claiming an intro or loading-stage bypass.
- Prefer supported native menu/load functions. Do not force an unrelated game state or bypass incomplete world initialization.
- User-requested preset action: Match startup mods on the native Load screen copies the selected single-player save's exact enabled IDs and order, enabling saved mods and disabling startup-only mods on explicit click. Preview counts and affected IDs first. Preserve map order, saves and loaded-state metadata. Never call setLoadedMods, download mods, auto-load a save or bypass requiresResetLua.
- Reject missing/unavailable mods, saved lists omitting required dependencies, duplicate/invalid IDs and absent saved mod metadata before writing. Explicitly empty lists are valid. If the save omits Fast Load, disable it too on next launch and say so in the preview; do not add it back implicitly.
- Write the mod-owned text backup before changing the startup preset; offer session-only Undo for both enabled IDs and order, refusing to overwrite later edits or restore unavailable mods. Persist only through native saveModsFile, never through direct profile-file writes. Apply on the next manual launch, with no automatic restart or reset. Native void persistence cannot report success reliably; keep that limitation explicit.
- Always stop at the main menu. Do not auto-load any save, expose an auto-resume toggle or honor legacy autoContinue preferences.
- Current user instruction: edit/package further optimizations without running tests or launching the game. Mark this revision untested; do not transfer earlier test results to it.
- Startup artwork must be Project Zomboid themed, without Dead Signal branding in the scene. Keep native logo, controls and terms readable. No added waiting timer, auto-load, fake loading percentage, flashing effects or sound. Provide scene-off and reduced-motion preferences. Remove the former whitespace warning overrides; the pre-Lua screen retains native warning text because ordinary Workshop Lua cannot animate it.
- Prioritize removing actual work over hiding screens. QoL research is authorized; do not equate fewer clicks or shifted prefetch work with an engine speedup. Keep unmeasured candidates distinct from implemented features.
- Record native elapsed times and skipped steps separately from source/static checks. Report load work that a Lua mod cannot accelerate.
- Tip selection requires three documented research passes, checking experienced-player advice against the installed build and challenging dated or universal claims before settling content. Keep citations and personal creator names outside the mod; never claim to have watched unavailable video content. Bundle tips offline, without startup web requests.
- Maintain a broad original tip library with no duplicates before the menu deck cycles. Preserve its seed/cursor in a mod-owned preferences file, outside saves. Native save-loading tips still sample with replacement and can show stock jokes; do not claim shuffle guarantees there. Never touch native random state, loading state fields, progress or save selection to rotate tips.
- Survival cards toggle controls only menu/boot cards. Native additive translation tips remain enabled with the mod. New-game loading, loading errors and pre-Lua initialization are not covered by the native quick-tip path. Keep these limits explicit.

# Verification

- Run `python fast-load/check_fast_load.py --game C:/Games/ProjectZomboid` for actual-adapter lifecycle checks and independent package validation. Native startup timings and menu/loading behavior remain separate gates.
- Candidate 0.0.8 retains the ordinary exposed TermsOfServiceState constructor and forceChangeState at cold OnGameBoot to bypass queued logo update/render. Keep native terms handling, original state queue and normal menu entry. Never target IngameState or world-loading states for a startup skip.
- Preserve the boot-once guard and MainScreenState.getInstance reset guard; exclude loaded/in-game players, clients/servers and Escape bypass. Missing APIs retain native startup. Do not claim native bypass success without observation.
- The requested terms state may be followed by the queued terms state because forceNext preserves stateIndex. Keep this documented until native lifecycle evidence establishes its effects. Pre-Lua initialization/loading frame and required asset/world loading remain. Revision0.0.7 removes warning suppression. Artwork can start only after Lua loading and when native states render UI, with no claimed world-loading coverage or engine speedup.
- The old animation multiplier/watchdog are removed. Do not reintroduce GameTime acceleration as if it were a complete logo skip. Detach menu ticks before map load/gameplay and reattach on menu/reset events.
- Light menu borrows the video-effects option only while at the front end, restores it before Options reads native controls and before map load/gameplay/reset, and never calls native saveOptions. Native interaction with other mods/options persistence remains untested.
- Current no-test instruction covers the new order action too. Source inspection and packaging are not tests. The opt-in checker compiles StartupOrder.lua but the old lifecycle fixture stubs its install hook; native UI/persistence, failed writes, Undo and avoided reload remain unverified.
- The same instruction covers StartupScene.lua. Its optional compile-only entry and lifecycle stub are future scaffolding, not animation verification. No native render, crop, performance or reset results exist for0.0.7.
- The0.0.8 tip revision is also untested. Future compile-only inputs and stubbed lifecycle integration do not establish translation discovery, rotation, persistence, text fit, localization or native loading visibility. Generating data and copying/zipping files are not tests.
- The 0.0.1 lifecycle fixture and native evidence are historical. The replacement lifecycle fixture is not executed under the current no-test instruction. Verification.md records that boundary.
# Child DOX Index

- None.
