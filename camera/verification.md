# Native camera verification

Candidate: DeadSignalCamera 0.1.1. Standalone native zoom controls and native-pan binding guidance, with fixed isometric orientation.

## Automated checks

python camera/check_camera.py --game C:/Games/ProjectZomboid passes:
- Actual client zoom adapter executed in game Kahlua against a controlled native API fixture.
- Native preset direction, static tile scale, completion at target and blocked text/split-screen behavior.
- Pause cancellation through an event that continues during pause.
- Switching Normal while displayed zoom is normal but the native pending target differs.
- Complete runtime Lua compilation, five-file package inspection and ZIP integrity.

The raw-offset math/controller checks still pass as research only. Their modules are outside the distributed package because the native adapter failed. No source fixture establishes actual engine rendering or physical input correctness.

## Native gameplay evidence, 2026-10-18

- Enabled DeadSignalCamera for the isolated Sandbox save, preserving Toolkit Bridge and Javelin; disabled the separate geometry probe.
- 0.1.0 loaded without a camera exception in the inspected tail. Repeated drag-pad input changed the UI mode but did not pan the world. Native Wide smoothly reached 200%, then Normal returned to 100%.
- Bytecode follow-up identified the missed render-time recenter after OnPlayerUpdate. The renderer also resets the followed camera character. No viable ordinary Lua raw-offset or detached-anchor route was established.
- Removed ineffective drag, follow/hold/recenter and edge controls from the candidate.
- Cleanly saved/exited and launched 0.1.1 through Toolkit Connection. Its compact toolbar rendered, reported PanCamera unbound, and Close reached the configured 25% extreme.
- Toolbar close hid it; the normal world context menu still appeared with a road tile coordinate report and Camera controls successfully reopened the toolbar. This confirms menu operation, not exhaustive picking validation.
- Review found pause cancellation and rapid preset-switching races. Both had failing regression checks before their fixes and now pass. Final PC-side source hashes were matched before relaunch.
- Final corrected 0.1.1 loaded and Wide reached 200%. A Close click while paused left it at 200%; unpausing did not queue that rejected request. Normal then returned to 100%. The game was left paused at normal zoom with the toolbar visible. The animation recorder was briefly toggled while attempting to close the overlapping console, then stopped, as confirmed by its log.

## Remaining gates

- Exact pause-mid-transition cancellation and rapid preset-switch timing remain fixture-tested rather than native-observed. Final native preset and paused-input tests passed as recorded above.
- Physical native PanCamera binding/input, F7 and preset rebinding, modifier and alternate bindings.
- Full world picking, vehicle/map/text/focus behavior, saved toolbar positioning, repeated reloads, death/character replacement, floors/stairs and performance.
- Controller, split-screen and multiplayer support are unverified.
- Workshop uploader metadata/preview validation and publication remain pending.

## Artifacts and environment

- build/camera/DeadSignalCamera.zip: five runtime files, no installer or renderer dependency.
- build/camera/Workshop/DeadSignalCamera: draft upload folder; preview/uploader validation pending.
- Only Toolkit's isolated profile was staged. Normal saves and the installed game were preserved.
- Development DOX, specification and task records were updated. Root instructions now record two independent products and index the fast-load domain. Vehicle documentation remains unchanged by camera work because it has separate ownership.

## Native research expansion, 2026-10-18

The ordinary-mod transform probe loaded its original screen vertex shader in the isolated 42.20.4 game. Enable, full roll cycle (0, 90, -180, -90, 0 degrees), 55 and 80 degree planar tilt, and a 200 by 40 pixel drag were visually verified. Pan persisted with unchanged player coordinates. Closing restored the native image without restarting. Hold compensation is not movement-tested. Uncovered areas retained old framebuffer pixels, original occlusion remained, and native gameplay picking was not remapped. This is an experimental image transform, not full 3D geometry rotation or a production feature.

The separate textured-ground panel sampled 169 loaded tiles, 169 floors and 169 actual textures, with none unavailable. Native rotation completed 45, 135, 225, 315, 45 degrees. Pitch presets at 5 and 85 degrees visibly flattened and opened the floor plane. Clicking the player marker at 85 degrees reported floor coordinates 11772.95, 6837.56 against player position approximately 11772.974, 6837.590. This establishes floor-plane inverse picking only. No native gameplay action was issued. Road markings that are separate objects, buildings, characters, lighting and streaming remain absent.

Research windows were closed and the game left paused at native 100% zoom. The isolated console extract is retained under ignored build/camera/native-research-2026-10-18.txt. All four camera/probe/Fast Load checks passed before native testing; packaging checks are repeated at closeout. Neither research probe is a camera product dependency.
