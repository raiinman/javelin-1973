# Dead Signal Camera, original 3D research scope

Status: native rotation, tilt and zoom verified for the geometry probe. Further native tests verified full yaw and 5 to 85 degree pitch on 169 actual floor textures, plus persistent actual-image pan, full image roll and 80 degree planar flattening. Reconstruction lacks world objects/characters; image transformation retains native occlusion/picking and has uncovered-frame artifacts. Full standalone gameplay rendering remains unproven. The actual-world audit rejects the tested direct Lua camera-access route and complete existing-model reuse.

The renewed investigation tests two additional ordinary-mod paths: projecting real loaded floor textures with an original orbit projection, and an opt-in original screen vertex shader for dynamic image pan, roll and planar foreshortening. Record their native evidence separately. Image transformation preserves original visibility/occlusion and native picking; textured-ground reconstruction does not yet render buildings or characters.

## Objective

Provide a playable Sims-style camera inside Project Zomboid, with freely rotating and tilting views of the actual world. Require a standalone Steam Workshop package with no Viewpoint dependency, external installer or engine file replacement. This supersedes the earlier existing-renderer choice. Feasibility is unproven.

The Sims is the interaction reference. No Sims assets or code are required. Working default proposal: an overhead orbit camera with an isometric preset, adjustable perspective and focus on the player or a point in the world.

## Capabilities and order

| Module | Responsibility | Depends on |
| --- | --- | --- |
| world-renderer | Reconstruct and draw live world data through verified shipped rendering APIs; visibility and picking | Built-in game APIs |
| orbit-camera | Focus, yaw, pitch, distance, camera pose, smoothing, pan and zoom | Built-in renderer coordinate contract |
| game-controls | Mouse/keyboard routing, menus, reset, player follow and saved preferences | Both modules |

Build order: prove a live-world chunk can be rendered, rotated, tilted and selected through ordinary mod loading; establish model/sprite coverage and timing; connect the camera controller; implement and verify controls and lifecycle. A model viewer or disconnected demo does not pass the first gate.

## Behavior and acceptance

- Orbit 360 degrees around a focus point. Optional 90-degree snap turns preserve the focus.
- Tilt from a low oblique view to near top-down, with bounds preventing inversion.
- Smooth zoom and camera-relative pan. Camera motion uses elapsed real time, independent of game speed and frame rate.
- Provide free pan, player follow and return-to-player/reset controls. Panning does not move the character.
- Proposed bindings: middle-drag pan; modified middle-drag orbit/tilt; wheel zoom; explicit rebindable reset and snap turns. Resolve collisions with the renderer and game before finalizing.
- Capture camera input only while the game world owns focus. Inventory, text entry, pause menus and lost window focus release input.
- Rotate and tilt real world geometry. World selection, doors, containers and movement targets remain aligned with visible objects.
- Buildings, floors, roofs, characters, vehicles and terrain remain visible from the supported angles. Report missing renderer model coverage explicitly.
- Preserve native terrain collision and navigation. Visual terrain relief is separate from physical hills and must remain aligned with movement and picking.
- Handle entering/leaving buildings, stairs, vehicles, loading, death/respawn, returning to menu and three repeated enable/disable cycles.
- Retain a one-action return to the ordinary game view.
- Native single-player is the first verification target. Multiplayer and split-screen require their own checks before support is claimed.
- Record same-scene frame timings for the renderer baseline and camera mode, using the PC's actual settings. Set a performance target after measurement.

## Stack and structure

- Runtime candidate: original Lua using the shipped `ISUI3DScene` / `UI3DScene` interfaces. Arbitrary scene rotation is exposed; complete live-world rendering and interaction remain unproven.
- External 3D renderers remain research references, not runtime dependencies.
- Installed JDK 25 is available for development-only bytecode inspection and Lua checks; users must not need it.
- `src/`: original controller and renderer adapter. `tests/`: executable behavior tests. `research.md`: evidence and limitations. `tasks/`: plan and status.
- Compiled outputs and dependency source checkouts: root `build/`, outside distributed artifacts.

## Commands

Existing read-only API verification:

```powershell
javap -classpath C:/Games/ProjectZomboid/projectzomboid.jar zombie.iso.IsoCamera zombie.iso.PlayerCamera zombie.iso.IsoUtils
```

Development probe check and ZIP packaging:

```powershell
python camera/check_probe.py --game C:/Games/ProjectZomboid
```

The probe uses ordinary mod loading. It samples a 13 by 13 neighborhood on the player's floor, draws colored proxy boxes for existing floors and north/west collision edges, and shows a live player position marker. The user can orbit/tilt/pan/zoom the scene. Map geometry is a snapshot refreshed explicitly. This lacks complete object, texture, animation, picking, lighting and streaming coverage and does not satisfy the gameplay-camera gate.

## Code style

Use named world coordinates and radians, with screen input converted at the adapter boundary. Keep original controller math independent of game classes for reproducible tests.

```lua
camera:orbit(yaw_delta_radians, pitch_delta_radians)
camera:update(elapsed_seconds)
```

## Verification strategy

1. Behavior tests: orbit wrap, pitch limits, zoom bounds, pan relative to yaw, frame-rate independent smoothing, reset and invalid input handling.
2. Compile packaged Lua with the game's compiler; inspect APIs in the actual installed game. Syntax and API checks alone are insufficient.
3. Native live-world rendering through ordinary mod loading in an isolated world, then the same world with camera controls enabled.
4. Native world selection, occlusion, floor changes, driving and lifecycle checks at multiple orientations.
5. Packaging and license checks; no game files distributed.

## Boundaries

- Always: preserve existing saves and unrelated work; distinguish static checks from native execution; preserve dependency licenses.
- Resolve before proceeding: insufficient built-in rendering access, unusable live-world model coverage/picking/performance, installation outside the isolated test workflow.
- Never: claim completion from camera math or a separate scene demo; silently replace the game installation; publish game binaries or third-party assets without distribution rights.

## Open questions for investigation

- Can shipped `UI3DScene` rendering represent a real loaded chunk, including player, zombies and vehicles, at playable frame times?
- Can sprite-backed buildings and objects be reconstructed with sufficient coverage at arbitrary yaw/pitch without engine changes?
- Can visibility, lighting, world picking and native interaction stay consistent with that scene?
- Which terrain representations remain correctly aligned with native collision at every supported angle?
