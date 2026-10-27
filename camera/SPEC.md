# Dead Signal Camera

Build the most usable camera the supported game APIs allow as one ordinary Steam Workshop mod, without Viewpoint, Java loading, an installer or engine replacement. Target installed 42.20.4 first.

## Verified boundary

The current product uses the native isometric view. The 0.1.0 gameplay test rejected scripted raw-offset pan: the render loop recenters after OnPlayerUpdate. It also resets the camera character immediately before that recenter. No supported later pre-world Lua hook or persistent offset setter was found. Do not ship drag, hold, follow/recenter or edge controls that only change Lua state.

Full world rotation/tilt remains separate unproven research in SPEC-3d-research.md and research.md.

## Current candidate

- Native smooth zoom buttons and Close, Normal and Wide presets use configured zoom levels.
- Compact movable toolbar displays actual zoom, native auto-zoom state and the existing PanCamera binding.
- Native pan uses the game's physical PanCamera action. Explain how to bind it; never overwrite the player's bindings automatically.
- F7 and the world context menu hide/reopen controls. Optional zoom preset shortcuts default unbound in native key bindings.
- Save only toolbar position in character mod data.
- Cancel unfinished zoom jobs on pause, text entry, menu return or unsupported player count.
- Preserve native world rendering, selection, simulation, zoom range and auto-zoom preferences.

## Verification

Run python camera/check_camera.py --game C:/Games/ProjectZomboid.
The actual zoom adapter runs against a controlled Kahlua API fixture. Rejected pan controller/bridge modules remain under tests as research, outside the distributed package. Passing those math tests does not establish a working camera adapter.

Native gates: zoom extremes and presets, pan binding/physical input, world selection, toolbar reopening/position persistence, pause/text/menu behavior, reload and performance. No controller, multiplayer, full rotation/tilt or release claim without dedicated native evidence. Workshop uploader validation and publication are separate steps.
