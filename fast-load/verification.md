# Current revision: 0.0.8, untested

Three sequential research passes preceded final selection of120 original tips. Generated additive EN UI quick-tip entries, matching Lua metadata and preview data from survival-tips.tsv. Native existing-save loading scans the translation prefix, rotates by its native menu-time threshold and samples with replacement, including stock jokes. This is bytecode evidence, not a runtime result. New-game loading, early initialization and error branches are not covered.

Added a12-second menu/boot carousel with a private deterministic shuffle, persisted seed/cursor, text wrapping, hover hold and menu-only toggle. It does not consume the game's random stream. File-write failure downgrades to session-only persistence. No network requests, native state writes, save actions or added waiting gate exist in this feature.

No tests, syntax compilation, game launch, preview execution or native loading observation were run. The pure content generator was run to write data, not validate behavior. Translation merging/discovery, localization fallback, native tip width/contrast, menu layout at small/high-DPI sizes, hover behavior, clock changes, malformed/unwritable preferences, deck persistence, Lua resets and native-vs-menu repetition boundaries remain unverified. The future checker has compile-only new modules and a fixture stub, neither was run. All earlier unverified startup/mod-matching limits remain.

Copied revision0.0.8 to the standalone ZIP, private Workshop draft and existing owned Toolkit profile mod. PC-side Remote Desktop Commander readback showed0.0.8 metadata, the first native tip keys and final index entry120. Preserved the preceding archive and staged mod under ignored build/fast-load before replacement. No enabled-mod list, normal-profile mod installation, save or existing tip-deck preference file was changed. The mod will create its own deck file only when the carousel is first drawn later.

DOX pass: updated Fast Load's owning content, generator, persistence and presentation contracts. Root, camera and vehicle docs remain unchanged because those products and their existing rules are unaffected.

## Previous revision: 0.0.7, untested

Added the original Project Zomboid themed Knox County background and bounded rain/fog/reflection animation behind the native logo/menu, plus scene and reduced-motion toggles. Removed all29 whitespace warning translation files, restoring native pre-Lua warning text. No scene timer, save load, loading-state replacement or engine speedup is introduced.

No tests, syntax compilation, game launch or native scene observation were run. Boot visibility, terms ordering, menu legibility, aspect-ratio cropping, UI scaling, preference/reset lifecycle, native-option restoration, mod conflicts and frame cost are unverified. Read-only shipped-source/bytecode inspection is recorded in startup-art.md. The future checker has compile-only scene input and a stub; neither was run and neither proves native rendering. Existing0.0.6 mod-matching limitations remain.

Source files and the original generated background were copied into the standalone ZIP, private Workshop draft and existing owned Toolkit profile mod. Remote Desktop Commander readback confirmed PC-side0.0.7 metadata, image size and scene source. The previous archive and staged mod were backed up under ignored build/fast-load before replacement. Obsolete whitespace UI.json overrides were removed from source, draft and staged copies. No enabled-mod list, save or normal-profile installation was changed. The browser preview was generated but not executed.

DOX pass: the owning Fast Load instructions reflect artwork ownership, user branding preference and removal of warning suppression. Root, camera and vehicle docs remain unchanged because their scope/contracts did not change.

## Previous revision: 0.0.6, untested

## Crash investigation, 2026-10-18

The user reports a full application exit. The latest isolated console contains repeated right-click exceptions in the separate development vehicle hook `DSISliceAudit.lua`, caused by unavailable profile/version APIs. That hook was corrected and staged without running tests or launching the game. Details and preserved evidence are recorded in `build/stl-full-trace/slice-v03/native-test/crash-recovery.md`.

No Fast Load exception stack appears in that console. This is not proof that Fast Load is crash-free, and the full process-exit cause remains unresolved. No Fast Load release, enabled-mod list or save was changed during recovery. Revision0.0.6 remains untested.

## Revision status

No tests, automated checks, syntax compilation or game launch were run. No actual preset or save was changed during development. Packaging copies/zips source only.

Match startup mods now copies the selected save's enabled mod IDs and order, rather than requiring equal membership. New source paths cover addition/removal previews, missing/unavailable IDs and omitted dependency refusal, explicit empty lists and self-disabling Fast Load when absent from the chosen save. The pre-write backup and session Undo restore membership plus order; Undo still refuses later edits and now checks the original mods remain available.

All new paths are unverified, including dependency metadata, stale preview/missing-save cases, empty/vanilla saves, self-disable/re-enable, failed backup/persistence/rollback, external edits, Undo and next-launch reload avoidance. Map order, saved metadata and the loaded snapshot are not copied. Native saveModsFile still supplies no persistence result. The optional checker compiles the integration only and stubs its installation in the startup lifecycle fixture; it was not run and provides no new behavior coverage.

Root, camera and vehicle instructions stay unchanged because their existing boundaries apply; the changed Fast Load contract and docs were updated in their owning domain.

## Prior revisions

# Revision 0.0.5, untested

No automated checks, syntax compilation, game launch or runtime tests were run. Packaging only copies/zips source. No startup preset or save was modified during development.

Added a native Load-screen Match startup order button for the currently selected single-player save, guarded by exact mod-ID membership, with pre-write backup and session Undo. Changes use native default ActiveMods and saveModsFile only; map order, enabled IDs, saved metadata and loaded-mod snapshot are preserved. No Continue, ResetLua or automatic restart is invoked. Same-set matching is required before any write.

Future gates: Load-screen initialization, small/resized/high-DPI layout, keyboard/controller operation, selected/removed/old/multiplayer save handling, no-op and different membership, missing/duplicate IDs, backup and write failures, rollback and external edits before Undo, actual disk persistence and next-launch reset avoidance. Native saveModsFile discards the internal write result, so Lua pcall success alone is not persistence proof.

The optional checker was adapted but not run. It compiles StartupOrder.lua only; the old lifecycle fixture stubs the new integration. Thus it cannot establish reorder/Undo correctness even if executed later. The startup bypass and warning suppression retain their earlier unverified status. Root/camera/vehicle docs remain unchanged because their existing boundaries and standalone/no-auto-load/no-test requirements still apply.

## Prior revisions

# Revision 0.0.4, untested

No automated checks, syntax compilation, game launch or runtime tests were run. Read-only REA/archive/bytecode and translation-source inspection is not native execution. Source files were copied/zipped only.

New feature: eight whitespace-valued startup warning keys per bundled UI locale, loaded through the native translation mechanism before Lua. This should hide warning text; it cannot remove the black/loading frame, accelerate required initialization or make an uninitialized menu usable. It is unconditional while enabled, including when the later logo bypass is disabled. Native text suppression, merge precedence, locale coverage and mod conflicts remain unverified.

The ordinary-mod package still requests the native terms state at boot for a logo bypass and never calls Continue. All 0.0.3 bypass/lifecycle limitations remain. The remaining user objective of eliminating pre-menu engine loading is not achieved under the Workshop-only contract. Root and other product documentation remain unchanged because their existing standalone/no-save-auto-load/no-tests requirements still apply.

## Prior revisions

# Revision 0.0.3, untested

No automated checks, syntax compilation, game launch or runtime tests were run, per the user's instruction. Packaging only copied/zipped source. Read-only shipped-code inspection is not a passing test or native proof.

The candidate requests the native TermsOfServiceState at cold OnGameBoot through forceChangeState. Source ordering indicates the logo state exits before update/render, preserving native terms checks and the original menu queue. The earlier animation-speed boost/watchdog are removed. No save auto-load exists. Pre-Lua initialization/loading/warning display remain.

A replacement lifecycle fixture was written but not run. Future gates: constructor/global exposure in non-debug mode, actual logo absence, first-time/updated terms behavior including the duplicate queued terms entry, Escape and disabled preference, startup Lua resets, third-party transition conflicts, normal menu/game lifecycle and controlled startup timings. Existing reversible light-menu behavior also remains untested. No previous results establish 0.0.3 correctness. Workshop preview/uploader validation remains pending.

## Superseded 0.0.2

This revision removed auto-continue and added light-menu behavior, but only accelerated logos with GameTime. It was not tested. Version 0.0.3 replaces that approach rather than claiming those changes achieved a complete skip.

## Historical 0.0.1 results only


Run `python fast-load/check_fast_load.py --game C:/Games/ProjectZomboid`.

The installed game's Kahlua compiled and executed the actual runtime adapter against a controlled native-API fixture. Checked: no pre-boot resume, deadline, a single native Continue request, menu return without loops, Escape bypass, mod-selection ResetLua bypass, client exclusion, persisted-preference toggle, eligible Survivor-mode dispatch and Multiplayer-mode exclusion. The three-file independent package passed content and ZIP checks.

Additional checks cover exact base multiplier restoration with a non-one per-object modifier, the real-time watchdog, restoration before world loading, and the short-intro preference off path. These checks do not establish native event timing, UI button visibility, actual preference persistence, intro shortening or measured startup improvement.

Ownership tests also verify preservation of another startup mod's later multiplier change and best-effort recovery from an injected post-set read failure under the native boot modifier ofone. The final three-file ZIP was regenerated after those checks passed.

## Native test, 2026-10-18

Activated the independent mod in Toolkit's isolated profile and the existing save through the game's Mods UI. Both menu toggles appeared. The mod-selection Lua reset remained at the menu, without unexpected auto-resume. On a clean Toolkit launch, the mod automatically invoked the native Continue path and entered that save without menu navigation. Console logs confirm the startup logo boost was applied and restored, including the Lua reset during native Continue. The final Click to Start was still required.

Launch was recorded at 20:56:35 UTC. First Lua boot was 20:57:04.914 UTC, approximately 30 seconds later. The second Lua boot during Continue was 20:57:27.414; map load began at 20:57:28.681. The engine reported 31 seconds of world loading. Game-start event time includes a manual delay before acknowledging Click to Start and cannot measure loading readiness. There was no controlled baseline with the same enabled mods, so neither a logo-duration improvement nor a total speedup percentage is established. Earlier engine initialization precedes ordinary mod Lua and remains untouched.

Remaining native gates: Escape/click bypass, toggle persistence, invalid-save validation, return-to-menu without automatic reload and controlled phase timings with the same mod set/save. Repeat a normal non-debug launch before claiming normal-mode support. Keep engine/asset duration separate from actions and menu delay removed. ZIP and private Workshop upload draft are under ignored build/fast-load; preview/uploader validation and publication remain pending.

## Documentation scope

Updated the owning Fast Load contract and startup evidence. Root instructions and camera/vehicle documents remain unchanged because the existing standalone/no-auto-load/no-test contract already covers this work and no other product behavior changed.
