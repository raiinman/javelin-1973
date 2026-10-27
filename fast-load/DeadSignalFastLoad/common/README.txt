Dead Signal Fast Load 0.0.8

Standalone Workshop-format mod. No external installer or camera dependency.
Never auto-loads a save. Always leaves game selection to you.

120 survival tips:
Original offline tips cover combat, escape, condition, looting, shelter,
water, food, wounds, vehicles, crafting, power/fire and long-term survival.
Advice was curated through three research passes for Build 42.20.4.
Settings, updates and mods can change the right tactic. Current text is English.

Existing-save loading adds these entries to the native rotating quick-tip
pool. Native timing, stock tips/jokes and random repeats remain. New-game
loading, error screens and the earliest engine initialization are not covered.

Menu cards rotate every 12 seconds through a shuffled 120-card deck before
cycling, about 24 minutes of continuous card time. This is not a loading time
claim. Hover over a card to hold it. Survival cards switches this menu/boot
carousel off; it does not remove native loading-pool entries.
Deck seed and next position use DeadSignalFastLoad-tip-deck.txt in the game's
Lua preferences. Failed writing leaves order session-only. No save is changed,
and the game's random stream is not used. No internet requests are made.

Rainy Knox County:
Original Project Zomboid themed street artwork behind the game's native logo
and front menu, with moving rain, slow fog and subdued road reflections.
No developer branding in the scene. No added wait, sound or flashing effects.
Rainy Knox County switches the scene off. Reduced motion freezes animation
and removes rain. The native menu controls and required terms remain.
Artwork uses a single cached image with native UI draws, not a video player.

The scene can begin only after Workshop Lua loads and when native states draw
UI. It continues behind the front menu, not submenus or the in-game pause menu.
Pre-Lua engine initialization and normal world-loading screens remain native.
The former blank warning-text overrides are removed. Native warnings return.
No measured loading-speed improvement or successful bypass is claimed.

Skip startup requests the native terms-check state at cold application boot.
The queued terms state may run again. Hold Escape at boot or switch Skip
startup OFF for the next launch to retain the native logo sequence.
Required first-time or updated terms remain under native control.
No GameTime changes. No extra cinematic or minimum display duration.

Ready-menu input delay and fade are removed once per menu instance.
Light menu borrows the native video-effects option, restoring it before
Options reads the value and before world loading. Native options are not saved.
Preferences: DeadSignalFastLoad.ini, skipStartup, lightweightMenu,
animatedScene and reducedMotion. Legacy autoContinue is ignored.
survivalTips controls menu cards only. Native loading tips are data entries.

Match startup mods:
Open Load, select a single-player save, review the enable/disable counts and
hover the button for affected IDs. Click Match startup mods, then restart
manually and load the save yourself. No automatic restart or save loading.
The chosen save's exact enabled IDs AND order replace the startup preset.
Missing mods, omitted dependencies and invalid/missing lists are refused.
An explicitly empty saved list disables all startup mods. If the save omits
Fast Load it is disabled next launch too. No extra mod is silently retained.
Map order, saves and loaded-state metadata are unchanged.

Backup and Undo:
Before each action, the preceding list is written to
DeadSignalFastLoad-startup-order-backup.txt in the game's Lua preferences.
Session Undo restores it unless intervening edits occurred or original mods
became unavailable. After restart the backup is a manual restoration reference.
Native preset persistence provides no success result and logs disk errors.

Version 0.0.8 is untested at the user's request. No tests, syntax compilation
or game launch were run. Native artwork, lifecycle, layout, performance,
bypass, preset matching and Undo remain unverified.
Tip discovery, rotation, persistence, text fit and localization are unverified.
