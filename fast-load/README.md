# Dead Signal Fast Load 0.0.8

**120 survival tips**, selected after [three research passes](survival-tips-research.md), cover combat, escapes, condition, loot, shelter, water, food, wounds, vehicles, crafting, power/fire and long-term planning. All text is original, bundled offline and currently English.

Existing-save loading gains these entries in the native rotating quick-tip pool. The game controls that picker's timing and randomness; stock tips/jokes remain, and repeats are possible. New-game loading and the earliest engine-initialization screen do not use this path.

The front-menu/boot-UI carousel rotates every12 seconds through a shuffled120-card deck before cycling. That is24 minutes of continuous card time per deck, not a loading-duration prediction. A mod-owned seed/cursor file resumes the deck across launches when writing succeeds. Hover to hold a card; the Survival cards toggle controls this carousel only. Native loading entries remain while the mod is enabled. The [browser preview](startup-preview.html) includes Next/Previous and pause controls for browsing the library; these are preview controls, not in-game buttons.

**Rainy Knox County:** original Project Zomboid themed artwork behind the game's own logo and menu, with moving rain, drifting fog and subtle wet-street reflections. No developer branding appears in the artwork. The menu remains available immediately; there is no new cinematic wait. Use **Rainy Knox County** to switch it off, or **Reduced motion** to keep the artwork still. No added audio or flashing effects.

This scene begins only after Workshop Lua is available, when the native state renders UI, and continues behind the front menu. It cannot replace the earlier engine-loading frame or the native world-loading screen. The former blank-warning overrides are removed, restoring native warning text on that earlier frame. See [artwork and integration](startup-art.md).

Open **Load**, choose a single-player save, then click **Match startup mods**. The action copies that save's exact enabled mod list and order into the startup preset. Restart manually, then choose and load the save yourself. Nothing auto-loads or restarts.

The row previews enable/disable counts; hover the button for the affected IDs. Startup-only mods are disabled, saved mods are enabled, and their saved order is preserved. A vanilla save with an explicitly empty mod list disables all startup mods. If the save excludes Fast Load, it will also be disabled next launch; the preview says so. It is deliberately not added back, because that would prevent an exact match.

Missing/unavailable mods, omitted dependencies, duplicate/invalid IDs, saves without stored mod metadata and unsupported save modes are refused before writing. The feature does not download mods, guess a legacy save's list or enable extra dependencies beyond the stored list. Map order, save files and the native loaded-mod snapshot stay unchanged. Matching can avoid the native second Lua-reset branch on a later launch; this is conditional and unmeasured.

**Backup and Undo:** each operation writes the preceding enabled list and order to DeadSignalFastLoad-startup-order-backup.txt under the game's Lua preferences directory before changing the preset. Undo restores the previous enabled list and order during the current Lua session, provided the preset has not subsequently changed and the original mods remain available. After restart, the backup is a manual Mods-restoration reference; Undo is session-only. Native preset saving logs disk failures internally and supplies no persistence result.

**Untested:** no checks, syntax compilation, game launch or runtime tests were run for0.0.8. Content generation and file packaging only. The future checker compiles the UI modules but its older lifecycle fixture stubs their integration, so it does not establish tips, scene rendering, matching or Undo correctness. No startup preset or save was changed during development.

The package remains independent and Workshop-format, with no external loader, installer, camera or Toolkit dependency. Output: build/fast-load/DeadSignalFastLoad.zip and its separate private Workshop upload draft. Nothing is published.

## Existing startup presentation features

Skip startup defaults on and requests native TermsOfServiceState at cold OnGameBoot to bypass the logo state before update/render. Native terms prompts remain when required. The queue may enter terms twice internally; the bypass is unverified. Escape or the Skip startup toggle leaves that later presentation native.

Warning-text suppression is removed in0.0.7. Removing text never skipped loading work.

Ready-menu delay/fade removal and the reversible light-menu background remain. Light menu uses the original background instead of video effects, restoring the captured option before Options reads it and before gameplay. Required pre-Lua initialization, asset/world loading and final Click to Start remain. No overall speedup is measured.
