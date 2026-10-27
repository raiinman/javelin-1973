# Camera renderer evidence

Research date: 2026-10-18. Static findings are not native game tests.

## Skills located

The requested [raiinman/skill-library](https://github.com/raiinman/skill-library) was inspected through GitHub's tree and raw-file APIs at main revision `697672c69dcb87834cf5c75cdcd0cbd85082c6cf`.

- `skills/coding-workflow/spec-driven-development/SKILL.md`: requirements, consequential decisions and acceptance gates; installed through the raiinman agent skills plugin.
- `skills/programming/lua/SKILL.md`: applicable if verified Lua controls are used; already installed.
- `skills/game-development/game-development/3d-games/SKILL.md`: camera and rendering principles; already installed.
- `skills/reverse-engineering/reverse-engineer-anything/SKILL.md`: shipped-game investigation. The locally installed REA skill is newer than this library snapshot.
- `game-architecture` was inspected, but its browser-game workflow is not the native Java integration contract.

## Local target identity

- Toolkit doctor resolves the game and the isolated profile without modifying them.
- Remote Desktop Commander on APeX-2 independently verified the game archive SHA-256 as `80e405a4bfc42f6072e75b3735f458a6514143da011d3226007ded305a442f44`.
- The Toolkit profile's `version.txt` reports `42.20.4 b0bbce05d5`; the ordinary Zomboid profile has an older `42.20.0 a2947723ca` file. Do not confuse these cached histories with a new live run.
- Toolkit bridge status is not ready and Lua execution is unavailable. It returns the cached 42.20.4 identity; no native camera check has occurred.
- Local archive SHA-256 matches the PC archive, so the bounded local `javap` observations refer to those same game bytes.

## Native camera evidence

`javap` of the installed archive exposes offset/follow functions on `IsoCamera`, plus per-player offsets, zoom and projection/modelview matrices on `PlayerCamera`. Those matrices alone do not establish support for arbitrary world rotation.

Bounded bytecode inspection of `IsoUtils.XToScreen` and `YToScreen` shows fixed world-to-screen arithmetic, using the tile scale and 32/16/96 coefficients. This supports investigating an additional world renderer rather than presenting offset changes as full 3D.

The developer's [rendering explanation](https://projectzomboid.com/blog/news/2023/02/play-your-cardz-right/) describes isometric sprites with assigned depth. This historical description is corroborating context, not proof that no modern 3D renderer can be added.

REA opened and inventoried the exact archive. Root manifest `agm_25f8916ae4a24804547b697f2286321c5496f9335412df33c5f303986aa21309`; inspection Evidence `ev_599ee2b190cd19388401a582e410b34da99ab011c5c5f1af46f871b79d68ddd9`, linked inventory Evidence `ev_547b8084d3f0f9dac33f9ce59f5e13917018844dc66001ee47bf6c93454d461f`. REA establishes archive identity/inventory only. Camera methods and arithmetic were independently inspected with `javap`; no REA execution or native camera behavior is implied.

## Existing renderer candidates

### Open-source Head Tracking renderer

[Author source](https://github.com/itsloopyo/project-zomboid-headtracking), inspected revision `14a0dab59bdbe3be7644647ed431ee4bc89f09d7`, MIT license. The author README documents testing on 42.21.0 and a rebuilt 3D world, with buildings/furniture and terrain. These are author claims until locally validated.

- Java 25 source uses the Class-File API and a `cameraunlock-core` native submodule.
- Build configuration requires a native CMake/Visual Studio toolchain for the core DLL; the ordinary mod build uses signature stubs. Neither establishes compatibility with the installed game.
- `ViewCamera.java` defines eye, right/up/forward vectors and OpenGL matrices in game coordinates. World x/y are horizontal tiles; a floor level is mapped to approximately 2.44949 vertical tiles. Audit handedness at integration, including picking.
- `FirstPerson.java` contains an overhead camera path and first-person camera state. A rotating overhead mode would need consistent renderer, culling and interaction integration, not only a new yaw variable.
- This project also changes gameplay and vehicle/terrain behavior. Reusing it unchanged would exceed the camera-only scope. Determine whether camera/rendering can be integrated without enabling those changes.
- Source checkout is retained only as ignored development research. Its deployment and installer scripts have not been run.

### Project Viewpoint

[Author Workshop item](https://steamcommunity.com/sharedfiles/filedetails/?id=3809306528) declares a custom 3D renderer, first/third-person views and free camera, with ZombieBuddy required. It also exposes optional terrain relief.

This makes it a candidate renderer dependency, but the page alone does not establish an addon API, license for source reuse, exact 42.20.4 compatibility or working terrain collision. Its extracted page includes availability banners inconsistent with item description/subscriber data; confirm actual client availability before installation.

### PZ3D

[Author Workshop item](https://steamcommunity.com/workshop/filedetails/?id=3807334881) describes a separate 3D camera framework. It is not interchangeable with Viewpoint. No local install, compatible addon hook or license has been verified for this candidate.

## Decision and remaining gate

Current contract: full rotation and tilt in a standalone Workshop package with no Viewpoint or external installer. This supersedes the earlier existing-renderer choice. Existing renderer findings below remain research references only.

## Existing overhead camera found

[OldPoint author Workshop page](https://steamcommunity.com/sharedfiles/filedetails/?id=3815999052), reviewed 2026-10-18, identifies version 0.6.119 targeting Project Zomboid 42.21 / Viewpoint 0.1.6. It describes a rotating overhead camera, middle-drag rotation and smooth wheel zoom. It notes remaining complex-building, opening/curtain, shader and mod-combination issues. The page does not establish exact Sims control parity or a locally tested result.

Its required-items list includes ZombieBuddy, Viewpoint and the sour_kisel 3D model pack. Its installation text explicitly requires completing ZombieBuddy setup and approving OldPoint's Java code. The [ZombieBuddy author README](https://github.com/zed-0xff/ZombieBuddy) prescribes a Windows installer or manual agent setup. Therefore this existing close match is not a dependency-free, subscription-only solution.

## Actual-game source compile

The pinned open-source Head Tracking renderer and core Java source were compiled directly against the verified installed game archive, rather than signature stubs. The compile failed at `FineSkins.java:944`: the game lacks `TextureID(int,int,ByteBuffer)`. No compatibility patch was applied. This is a confirmed build mismatch, not proof the entire renderer is unusable on 42.20.4. The native CMake and Visual Studio C++ tools were located, but no native backend was built or installed.

The independent read-only review confirmed the main world-render hook and useful outside-camera frame methods. It also found unconditional upstream vehicle physics hooks and visual hills not known to the simulation, so wholesale backend adoption needs a scope audit. Research checkouts and compiler output remain under ignored `build/camera-research/`.

## Shipped Lua-only rendering route

Installed `media/lua/client/Vehicles/ISUI/ISUI3DScene.lua` creates `UI3DScene` through the ordinary Lua UI wrapper, implements pan with `fromLua2("dragView", dx, dy)` and zoom with `fromLua1("zoom", delta)`. Installed `DebugUIs/AnimationClipViewer.lua:321` uses `fromLua3("setViewRotation", rx, ry, rz)` for rotation.

`javap` of the verified installed archive corroborates scene creation and view rotation command dispatch, models, characters, vehicles, geometry primitives and coordinate conversion. The [official UI3DScene API](https://www.projectzomboid.com/modding/zombie/vehicles/UI3DScene.html) also documents the scene class and conversion methods. Context7 returned the third-party API index; use installed bytecode and the shipped Lua wrapper for command semantics because its generated `fromLua` description is misleading.

Observation: the shipped game has a Lua-accessible rotatable 3D scene renderer. Unknown: whether it can support a complete live-world camera at adequate coverage and frame times with correct picking, occlusion, animation and lighting. It does not by itself provide a drop-in arbitrary-angle replacement for the main world renderer. A real loaded-chunk proof, not a model viewer, is required before claiming standalone feasibility. No custom Java-loading mechanism or native test has been established under the Workshop-only contract.

## Live Toolkit connection and probe

After the user started Toolkit, a fresh bridge check returned ready=true, loaded debug single-player on 42.20.4 b0bbce05d5. Inline Lua capability remains false. A minimal read-only Lua request was rejected with "Lua compiler unavailable in this game build. Built-in god mode and editor commands remain available". No inline camera code ran, and the current world/session was preserved. The earlier not-ready result is historical, not the current connection state.

The ordinary-mod `DeadSignalCameraProbe` supplies an opt-in debug context-menu scene. It samples loaded nearby floor/collision flags rather than a disconnected scene, with a live player-position marker. Shapes are coarse proxies; walls are collision edges, not reconstructed visual assets. It does not yet display actual characters/vehicles, perform world interactions or pass the full native-chunk gate.

Checks run with the game's own Kahlua classes: bounded sampling, anchor coordinates, missing squares, invalid-radius rejection, and client Lua syntax. Direct API inspection caught and corrected `PropertyContainer:Is` to Build 42's `has` before packaging. Filled primitive drawing uses the verified nine-argument `addBox3D` command. These checks do not establish rendered appearance or runtime activation.

## Native probe result, 2026-10-18

The isolated save initially retained only the bridge and Javelin, despite the probe being enabled in the profile default list. After a clean exit and launch through Toolkit Connection, Load > More > Choose Mods enabled the probe for that save while preserving both existing mods. Remote Desktop Commander verified the save's resulting `mods.txt` contains all three IDs.

The running 42.20.4 game logged `Loaded... UI3DScene=table`. Opening the probe from the world context menu sampled 169 loaded tiles, 169 floors and zero collision edges at the road intersection. The visible scene contained the sampled floor grid and cyan position proxy. Horizontal mouse drags rotated the scene; an additional 700-pixel plus 200-pixel drag completed a full orbit at the source's 0.4 degrees/pixel and returned to the prior orientation. Vertical drags produced near-overhead and low-angle views. Wheel scrolling visibly enlarged the scene. No probe exception appeared in the final console tail. The game was left paused with the probe visible.

Result: ordinary Lua mod loading can drive native 3D viewport rotation, tilt and zoom with nearby-map proxies, without Viewpoint or a custom installer. This does not establish full standalone gameplay-camera feasibility. The real world behind the window retained its original isometric view. This road sample did not exercise walls, actual character/vehicle models, textured map objects, multi-floor visibility, interaction picking, streaming or frame-time performance. Pan was not tested. Primitive faces also show view-dependent visibility artifacts, so do not infer production rendering quality from this probe.

## Main-world renderer audit

Read-only installed-bytecode review found these separate boundaries:

- `Core.StartFrame(int,boolean)` calls `PlayerCamera.calculateModelViewProjection` at offset 46, then `SpriteRenderer.initFromIsoCamera` at 113. The matrix calculation hardcodes orthographic projection, 30-degree X and 135-degree Y rotation, plus a further 180-degree Y rotation. Changing a matrix once does not establish a persistent world camera.
- `LuaManager$Exposer.exposeAll` explicitly whitelists `IsoCamera` and `SpriteRenderer`, but not `PlayerCamera` or `Matrix4f`; `shouldExpose` uses exact membership. `getRenderer():getRenderingPlayerCamera(0)` returns a rendering-state copy. A Java public field or returned object alone does not prove usable Lua camera controls.
- `LuaManager.validateReflectionAccess` throws `Not in debug` outside debug mode. Field/function reflection helpers call it, and `Field`/`Method` exposure is debug-gated. Debug reflection would not establish normal Workshop support.
- Cached terrain presentation in `FBORenderChunk` independently calls fixed `IsoUtils.XToScreen` and `YToScreen` (offsets 256 and 288). Rotating only 3D character/vehicle model matrices would not rotate the whole world.
- `RenderOpaqueObjectsInWorld` is dispatched by `FBORenderCell.renderOpaqueObjectsEvent` after the terrain/puddle pass and before moving objects. `OnRenderTick` and `OnPostRender` occur after world rendering. Merely registering these events does not provide an earlier terrain-camera setter.

The complete bounded `UI3DScene` command dispatch creates editor scene objects, models, characters, vehicles and geometry. No inspected command accepts an existing `IsoWorld`, `IsoGridSquare` or `IsoObject` to render its live world. `setModelSpriteModel` accepts a `SpriteModel`, but `createModel` instantiates a separate scene object from a model script. That is a reconstruction route, not an existing-world camera binding. The shipped `spriteModels.txt` has 416 tile entries across 19 tilesets and no floor/terrain-named tilesets. This file count does not cover runtime-generated mappings or prove all loaded-world model coverage; the native census is needed.

REA archive identity/inventory was refreshed against the same SHA-256. Summary Evidence `ev_dfaf56c51c78afe478ae33e67cef1a5b36bae64f06c2d55e8f4c9f52c0925f36` retains the existing inspection/inventory IDs above. It establishes package bytes and inventory only. Method semantics here come from bounded `javap` inspection, not REA runtime observation. Context7's API index returned no complete live-world scene binding; absence from that search is not an impossibility proof.

The v0.0.2 diagnostic uses protected calls to inspect the returned camera, direct matrix/method access and native axis projection, count actual nearby objects and their `getSpriteModel()` coverage within 33 by 33 squares, then record one real `RenderOpaqueObjectsInWorld` callback. It does not alter the camera or use reflection. Sampling behavior, complete client Lua syntax and four-file standalone package checks pass.

## Native actual-world access result, 2026-10-18

After the user released the PC, v0.0.2 was staged with all four PC-side hashes verified. The isolated game saved and exited cleanly, then restarted through Toolkit Connection. The same save loaded and logged v0.0.2. The actual-world context-menu action ran at frame 748 on 42.20.4.

Observed results:

- `getRenderer():getRenderingPlayerCamera(0)` returned an actual `zombie.iso.PlayerCamera`.
- Calling `getOffX`, looking up `calculateModelViewProjection`, and reading `modelview` or `projection` each failed with `attempted index ... of non-table: zombie.iso.PlayerCamera`. These are native Lua exposure failures, not inferred from Java visibility.
- `IsoCamera.cameras` returned a Java array, but `Matrix4f` was absent as a Lua global. The array's presence alone supplies no usable yaw or pitch setter.
- The real world X-axis projected to a 64,32 screen delta at the current tile scale. This is a baseline, not an altered-camera comparison.
- All 1,089 squares in the bounded neighborhood loaded. Their object lists held 1,425 objects, of which 2 returned SpriteModels. None of the 1,089 floors did; model-query failures were zero. The census includes square objects, not moving characters/vehicles, and covers this location only. Installed `IsoObject.getSpriteModel` bytecode resolves explicit model names or sprite mappings, so this query is not merely a test for already rendered mesh buffers.
- At frame 749 the real `RenderOpaqueObjectsInWorld` callback fired with player 0 and an actual grid square. The world remained in its ordinary isometric view. No whole-world rotated rendering was achieved.

The debug build initially stopped on the expected protected access error. Break On Error was temporarily unchecked and execution resumed, allowing the remaining protected checks to report. The game was then paused, saved and closed cleanly, with `GameThread exited` and no game process remaining. The temporary debugger flag is process-local; `UIManager.setShowLuaDebuggerOnError` only writes its static boolean. A console restoration attempt produced no visible text and did not run code. Other agents' Blender and browser windows were left open.

The exact diagnostic lines are retained outside the package at ignored `build/camera-probe/native-world-access-2026-10-18.txt`.

Conclusion: the tested direct ordinary-Lua camera route cannot provide full world rotation on this build, and the current map cannot be completely reconstructed just by reusing its existing SpriteModels. A substantial original renderer with new world-surface/asset handling remains a possible research direction, but its Workshop-only execution, coverage, picking and performance are unproven. The proxy viewport test must not be described as a working standalone gameplay camera.

## Native usability direction

The user subsequently prioritized the most usable camera the supported game APIs allow. `SPEC.md` now owns a native isometric camera product; the original rotation/tilt scope is preserved in `SPEC-3d-research.md`.

Installed `IsoPlayer.update` invokes native camera update at offset 1035, then `OnPlayerUpdate` at 1141. The initial adapter applied raw offsets there, but native gameplay rejected this route: the render loop recenters again before taking its snapshot. Getter values include native right-click offsets. Copied `IsoCamera.playerOffsetX/Y` Lua fields do not write the corresponding Java static fields.

Zoom uses native `Core.doZoomScroll` transitions and configured levels. `getZoom`, `getMinZoom` and `getMaxZoom` include tile scaling; `getNextZoom` does not. Use `Core.getTileScale()` as a static Lua class function, as shipped building/moveable Lua does. Static functions are not exposed through `getCore()` instance lookup. Native auto-zoom preferences remain untouched.

Context7's Project Zomboid JavaDocs index corroborated setter signatures. The REA archive identity remains the same recorded SHA-256. Native evidence and remaining gates are in `verification.md`.

## Native 0.1.0 offset rejection

The isolated save enabled DeadSignalCamera while preserving Toolkit Bridge and Javelin and disabling the separate geometry probe. The game logged successful 0.1.0 loading. Repeated toolbar drags changed its label to Offset look but left the actual player/world centered. Wide zoom smoothly reached 200%; Normal returned to 100%. No mod exception appeared in the inspected console tail.

Follow-up bytecode isolated the missing render-time reset: `IngameState.renderInternal` sets the camera character to the real player at45, calls `Core.StartFrame` at54, which calls `MultiTextureFBO2.update` at14. Its `setCameraToCentre` call at384 invokes `PlayerCamera.center`, replacing raw offsets. Setting a detached camera character is also overwritten. `OnRenderUpdate` has no dispatch call site in the inspected archive; the known render callbacks are too late. No ordinary setter for deferred or right-click target offsets was found.

The native `PanCamera` action instead computes mouse-based right-click offsets that survive centering. It defaults unbound and must be configured through native key bindings. Candidate 0.1.1 removes ineffective scripted pan/hold/edge controls, retains zoom presets and displays the existing native pan binding. This is a usable native-control subset, not full Sims-style camera completion.

## Native workaround and textured-ground evidence

The renewed 2026-10-18 investigation established a different ordinary-mod pan path: an original screen vertex shader can transform the actual final world image, using reversible values carried through inactive search-mode visual channels. Native testing verified a persistent 200 by 40 pixel drag, a complete image-roll cycle and planar flattening to 80 degrees. Closing restored the native image without restarting. This bypasses raw-offset recentering, but does not change world geometry or original visibility. Uncovered areas retained stale framebuffer pixels, native picking stayed unchanged, and hold compensation has no movement proof. The separate transform probe remains experimental and is excluded from the product package.

An original floor-plane projection also drew 169 actual loaded floor textures through the ordinary UI texture-quad renderer. Native yaw completed a full cycle and pitch reached 5 and 85 degrees. Clicking the player marker reported floor coordinates within approximately 0.03 tile of the live player location. This proves real textured-ground projection and inverse floor-plane picking, beyond the earlier coarse proxy. It does not reconstruct buildings, characters, separate road-marking objects, lighting or streaming, and cannot establish full gameplay-camera completion.

Exact native observations and limitations are in verification.md. The console extract remains outside distributed files under ignored build/camera/native-research-2026-10-18.txt. Fast Load is a separate product under fast-load/, without a camera dependency.
