# Native candidate loading route

## Cycle5 cargo native follow-up

The188,828-triangle cargo candidate was installed with16 payloads and Toolkit ownership verified; backup20261018T113458575409Z. Toolkit launched the no-save audit. The open cargo view still exposes a rear tire and the cabin remains black, contrary to fixed-lining source rays. Investigate native Interior model attachment/visibility before accepting the cavity correction. All three lighting snapshots report white ambient, no local lights, NoLighting=false. Evidence is under ignored `build/parity-cycle5/native-world-audit/`; exact temporary-hook cleanup is complete in `build/parity-cycle5/temporary-native-hooks.json`. Normal game exit and inspection latest-save pointer restoration completed. No normal save or normal mod was changed.

All sections remain open. The original read-only investigation below is retained as historical evidence, followed by its loading rationale.

## Current combined cycle4 loading state

The187,836-triangle combined candidate is now installed only in the isolated Toolkit profile. All16 payload hashes and the Toolkit marker were verified; the previous candidate is backed up outside mods. The PC-side car FBX hash agrees with the source package. Normal Toolkit UI launch reloaded the separate inspection save with both mods enabled. Base.Javelin73PC rendered the latest candidate in both side views, front, rear, top and underside. Selection again triggered a brief asynchronous skin-transform exception, then recovered unchanged. The editor lighting is flat and does not establish cup shading or interior likeness. Dark rear-corner regions and the simplified underside remain findings. A subsequent Toolkit-launched no-save world spawned this exact candidate and displayed closed, open-panel, lowered-window/open-door and restored-closed poses from one high rear-quarter angle. The open cargo cavity exposes a rear tire; paint reads flat, and the roof-occluded cabin does not establish Cardin visibility. These are corrective findings, not visual approval. Complete multi-angle motion, native interior review and vehicle persistence remain pending. Earlier six-view static native evidence belongs to167,134triangles, including its recovered transient model-readiness exception. Normal saves, the normal installed mod and distribution ZIP remain unpromoted.

The latest car FBX SHA-256 is `8c1a7f93bfa30924138610be194a65156b9e9a5413133d76888b0993d011ce5e`. Ignored `build/parity-cycle4/combined/deployment.json` records the backup and all payload hashes. The exact37-input source checkpoint and matching reports are under `build/parity-cycle4/combined/`.

## Temporary world audit

The later combined-cycle4 world inspection uses the existing repository visual audit, staged under ignored `build/parity-cycle4/native-visual-stage/`. Only its two development client hooks were temporarily copied into the owned Toolkit deployment after a normal game exit. The original16 runtime payloads and production source package remain unchanged. The audit launches a disposable no-save, no-zombie scenario and holds panel poses for60seconds. After all poses were observed, the game exited normally. Both exact hash-matching temporary hooks were removed and the separate inspection latest-save pointer restored. Completed cleanup is recorded in `build/parity-cycle4/temporary-native-hooks.json`; console markers are preserved in `build/parity-cycle4/native-world-audit/`. This is an inspection procedure, not a distributed mod dependency or an alternative launcher. Toolkit remains the launch route. Do not leave the temporary auto-start hook installed.

## Historical pre-deployment PC state

Remote Desktop Commander on APeX-2 confirmed:

- Game PID 60552 runs the installed `ProjectZomboid64.exe` with `-debug`,
  `-cachedir=%LOCALAPPDATA%/PZToolkit/game-profile` and `-modfolders mods`.
- The fresh MCP bridge reports Build `42.20.4 b0bbce05d5`, debug single-player,
  loaded player, god mode, native operations available and inline Lua unavailable.
- Both the isolated profile's `mods/default.txt` and the sole existing world's
  `Saves/Apocalypse/2026-10-17_21-30-32/mods.txt` list only `PZToolkitBridge`.
  Javelin73PC is present on disk but is not enabled by either configuration.
  The log search found no Javelin73PC loading record. This world is not evidence
  of the current candidate's appearance.
- The isolated `mods/Javelin73PC` has `.j73-install.json` with
  `mod_id: Javelin73PC`, and `.pztoolkit-owned` containing `pztoolkit-v1`.
  All 16 deployed payload hashes match its installer marker. The deployment
  is owned and unmodified relative to that marker.
- The PC workspace candidate and execution workspace have the same current
  car FBX hash. Three candidate payloads differ from the isolated deployment;
  the other 13 files match.

| Payload | Isolated deployed SHA-256 | Current candidate SHA-256 |
| --- | --- | --- |
| `common/media/models_X/vehicles/J73_Car.fbx` | `fef129ef751048e98630b094b00588409670eeeb0ac38f54d4831bd440f51e04` | `6513b4f5e48a7f3a03fb03428e517faeb284d0861a65d9e991faeb9be73991f5` |
| `common/media/anims_X/vehicles/J73_Panels.fbx` | `60e0b2ee1b58b0886022d151029ff335b9b063563b8c4e2ed4eda2953e8e19f1` | `202986a37c47452dea77f200d71c1c5024456f734fc94bc48124b6d5d1728695` |
| `common/media/textures/Vehicles/J73_Palette.png` | `8c8f03b1ce7418f8ad2332d027785dc7f766b49a9ee0430901209be328d18ea6` | `1806230b63c873d7cd121903785ccb56df00c79f23c9b3e93809e92375324736` |

Hashes identify this snapshot, not any later rebuilt candidate. Recompare all
payload files immediately before installation and native review.

## Loading procedure (cycle3 reached static editor inspection)

1. Exit the built-in vehicle editor with **Exit**, without **Save**. Use the
   game's normal pause-menu **Quit to Desktop** and confirmation. Wait for
   the verified isolated game process to finish. Do not force terminate it.
   The normal quit path can save this isolated world; do not claim a no-save exit.
2. Validate the exact current source and use the existing repository installer
   with `--game <installed-game> --destination
   <isolated-profile>/mods/Javelin73PC --update`. This is a repository development
   operation, not a Toolkit mod-management feature. The installer stages hashes,
   backs up the existing owned directory in the profile's `Javelin73PC-backups`,
   then swaps the stage into place. It refuses an unowned destination.
3. Account for the extra Toolkit ownership marker: the installer copies only
   `42`, `common` and its own marker. It does not carry `.pztoolkit-owned` into
   the new stage. Its previous contents remain in the backup. Preserve that
   ownership contract explicitly when performing the later deployment, and
   verify through Remote Desktop Commander before relying on PC files.
4. Relaunch only through **Toolkit Connection > Launch Project Zomboid (test
   profile)**. In the game's Mods screen enable the existing Javelin73PC and
   PZToolkitBridge. Create a disposable test world with both enabled, or use
   the game's save-specific mod management before loading an existing disposable
   world. Merely changing `default.txt` does not prove that the existing world's
   separate mod list changed. No normal saves or other mods need modification.
5. Confirm a fresh loaded-world bridge and native logs naming the candidate's
   vehicle scripts. Use the native vehicle spawn/debug controls to instantiate
   `Base.Javelin73PC`, then inspect the vehicle editor and world. Recheck deployed
   hashes against the frozen candidate. Record six-view alignment, moving panels,
   surface visibility and reference comparisons separately from importer checks.

The checked Toolkit MCP interface has no graceful quit operation. Inline Lua
cannot supply one in this session. Desktop interaction is required for the normal
quit and mod-enable steps; none was attempted here.

## What Reload All actually establishes

REA opened the installed `projectzomboid.jar` as a ZIP and identified SHA-256
`80e405a4bfc42f6072e75b3735f458a6514143da011d3226007ded305a442f44`.
Remote PC hashing independently matched. Current REA tools expose no Java
class disassembly operation, so the existing JDK's read-only `javap -c -p`
provided focused bytecode evidence from this same JAR. No REA setup/router
scripts or target code were executed.

- Shipped `media/lua/client/Vehicles/ISUI/EditVehicleState.lua`,
  `EditVehicleUI:onReload`, invokes `reloadVehicles()` then `setScript(scriptName)`.
- `zombie.Lua.LuaManager$GlobalObject.reloadVehicles`, bytecode offsets 0-15,
  reloads only `ScriptType.Vehicle` and `VehicleTemplate`; offset 15 loads vehicle
  textures; offsets 18-56 visit current-cell vehicles and call `scriptReloaded()`.
- `zombie.vehicles.BaseVehicle.scriptReloaded(boolean)`, offsets 0-74, removes
  physics/model instances, then offsets 79-127 clear part inventory references,
  reset created flags, set the script and recreate physics. Therefore Reload All
  is a world-affecting operation, not a harmless viewport refresh.
- `zombie.core.skinnedmodel.ModelManager.reloadModelsMatching(String)`, offsets
  0-49, searches loaded model-map keys by substring, and offsets 96-184 construct
  mesh parameters and invoke `MeshAssetManager.reload`. This is a distinct mesh
  reloading mechanism. No reference to it was found in the shipped Lua tree.

The editor's Reload All path does not explicitly request model FBX or animation
FBX reload. These observations do not establish that every downstream cache or
file watcher is inert. They also do not establish a supported GUI route for
reloading the changed car, panel animations and palette together. Since the
pre-deployment world did not enable this mod, a clean Toolkit restart after owned
deployment and game-side enablement is the reviewable route here. No hot reload
or latest-geometry native rendering was claimed or tested.

The normal quit UI is evidenced by shipped `MainScreen.lua`:
`QUIT_TO_DESKTOP` invokes `quitToDesktopFunc`, confirmation invokes
`quitToDesktop`, and that calls `getCore():quitToDesktop()` after resetting game
speed and pausing sound. The initial investigation did not execute that path. The later cycle3 loading work used normal quit and Toolkit restart.

## DOX and evidence boundary

Root AGENTS.md owns `docs/`; no child AGENTS.md exists on this path. The root
contract was reread. This report adds findings within the existing Toolkit,
installation and evidence contracts, so root instructions and child indexes
were intentionally unchanged. Earlier `docs/verification.md` statements about
a stale MCP connection are historical; the fresh pre-restart heartbeat above does not establish a loaded cycle3 world.
No source or native appearance gate was promoted by this investigation.

## Fresh-spawn activation confirmed

Fresh Toolkit no-save spawn confirms the original init callback activates itemless J73Interior, with13 active model entries and a non-null J73_Interior model instance at10/20seconds. The open door visibly reveals Cardin cushion ribbons and dashboard trim; the cargo opening no longer exposes the rear tire from the inspected high rear-quarter angle. This resolves that fresh-spawn activation/visibility defect, not whole-cabin likeness or every viewing angle. Real saved-vehicle reload and multiplayer remain untested. The game exited normally, both hash-matching temporary audit hooks were removed, and the separate inspection latest-save pointer was restored. The permanent original shared callback remains in the mod. Evidence: ignored `build/parity-cycle5/interior-native-audit/audit-markers.txt` and completed `build/parity-cycle5/interior-temporary-hooks.json`.

## Cycle6 static inspection and audit clock correction

The214,322candidate was installed with17verifiedpayloads and Toolkit marker retained; native FBX SHA256 `75040f3660f1668d93337a90ed237941b6e7ec0f38115b83db92137aba6f927a`. Toolkit-launched42.20.4 spawned the target. The native vehicle editor rendered both sides, settled top/underside, front and rear. Rear corner holes and a simplified underside remain actual findings. Editor Exit was used without Save. The editor suspended world ticks while the audit wall clock advanced, so returning skipped directly to restored-closed; this run does not verify intermediate panel poses. Normal game exit, two matching-hook removal and inspection latest-pointer restoration completed (`build/parity-cycle6/temporary-native-hooks.json`).

The audit now accumulates tick deltas capped at100ms rather than time spent in suspended editor states. A separate active-cycle guard prevents combined gameplay checks starting before successful pose completion. The actual Lua scheduler, executed in the shipped Kahlua VM with fake parts/clock, failed before each fix and passes afterward through a three-minute pause, all four poses, callback cleanup and suite gating.33unit tests pass. First harness attempts lacked the shipped stdlib working directory and VM owner-thread setup; those were corrected before the meaningful red/green runs. A real editor-pause retest remains pending. This changes development auditing only, with no production startup hook.
