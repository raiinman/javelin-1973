# Purpose

- Own the separate Dead Signal standalone Workshop camera mod and its rendering feasibility investigation.

# Ownership

- `SPEC.md` owns requirements and acceptance gates.
- `SPEC-3d-research.md` preserves the original full-3D research scope; it does not block native-camera delivery.
- `research.md` owns renderer evidence, compatibility findings and remaining unknowns.
- `verification.md` owns the current native-camera verification status and remaining gameplay gates.
- `DeadSignalCamera/` owns the standalone native zoom controls and pan-binding guidance. `tests/` owns executable checks and rejected offset-controller research outside the runtime. `check_camera.py` checks and packages it under ignored `build/camera/`.
- `DeadSignalCameraProbe/` is the ordinary mod-format development probe. It contains only runtime Lua, descriptor and brief instructions. `check_probe.py` checks and packages it under ignored `build/camera-probe/`.
- `DeadSignalCameraTransformProbe/` owns opt-in actual-world image pan/roll/planar-tilt research, including an original screen vertex shader and reversible visual-uniform transport. `check_transform_probe.py` verifies its Lua/transport and packages it under ignored `build/camera-transform-probe/`.
- `tasks/` owns the implementation plan and task state.
- Third-party checkouts and generated outputs stay under the root ignored `build/` directory.

# Local Contracts

- Prioritize usable native camera controls through ordinary Steam Workshop mod loading, without Viewpoint, external installers or engine file replacement. The latest user request authorizes native isometric controls within verified game limits. Preserve full 3D rotation/tilt findings as research, not a claimed feature or a gate blocking native controls.
- Keep camera work separate from Javelin geometry, textures and scripts.
- Preserve the installed game and existing saves. Develop and compile locally before any isolated-profile integration.
- Establish supported built-in rendering and Lua access before implementation. Cached version files and static checks do not prove a live functioning world renderer.
- Preserve upstream licenses and required notices for reused code. Keep reference research out of runtime packages.
- Treat unit checks, source compatibility and native game validation as separate gates. A camera controller alone is not a functioning game mod.

# Work Guidance

- Read `SPEC.md` and `research.md` before changing camera behavior or renderer integration.
- Use native camera offsets and native zoom for the production mod. Keep `UI3DScene` geometry probes separate. Custom Java/native loading remains outside the standalone installation contract unless a supported subscription-only mechanism is established.
- Prefer camera-only integration; retain the game's gameplay and terrain collision behavior.
- Pursue workarounds for rejected drag/hold and prove the strongest attainable rotation/tilt. Separate native world geometry, reconstructed real terrain, framebuffer image transforms and coarse proxies in every result.
- Minimize repeated startup interaction. The independent fast-loading product is owned by `../fast-load/AGENTS.md`; use it and safe explicit script reloads where verified. Shader changes still need a clean reload when the engine caches them.

# Verification

- Existing game bytecode can be inspected with the installed JDK `javap` against `projectzomboid.jar`.
- Use Toolkit's isolated debug profile for native game verification.
- Run `python camera/check_probe.py --game C:/Games/ProjectZomboid` for Kahlua sampling behavior tests, UI syntax and runtime package checks. This does not test native UI rendering.
- Run `python camera/check_camera.py --game C:/Games/ProjectZomboid` for controller, offset bridge and actual adapter lifecycle tests against a controlled native API fixture, plus complete runtime Lua compilation and package generation. Native pan, picking, zoom, input and lifecycle still require gameplay checks.
- Native 0.1.0 gameplay rejected raw-offset pan: render-time `MultiTextureFBO2.update` recenters after `OnPlayerUpdate`, and `IngameState.renderInternal` resets the followed character immediately before it. Do not ship scripted drag/hold/edge pan from the rejected adapter or treat its controlled fixture as engine validation.
- Use native `PanCamera` physical input for world pan and expose its existing binding without changing it. Zoom uses native transitions and configured levels; preserve auto-zoom preferences. Cancel unfinished presets in blocked contexts.
- Stage the probe only in Toolkit's isolated profile. Activate it through the game's Mods screen, including Load > More > Choose Mods for an existing save. Preserve existing enabled mods and save cleanly before a reload.
- Native probe rotation and tilt are verified on 42.20.4 for coarse nearby-map proxies. This does not establish a replacement gameplay renderer; keep that acceptance gate open.
- Native 42.20.4 research verified a full yaw cycle and 5 to 85 degree pitch for 169 real floor textures in the reconstruction panel. Actual-world image transforms verified a full roll cycle, 80 degree flattening and persistent drag pan. These do not establish a full gameplay renderer: reconstruction lacks buildings/characters, and image transforms retain native occlusion/picking and leave stale pixels outside their quad. Keep both outside the product package. The latter borrows only inactive search-mode visual channels and must restore them on close, blocking, search activation, resolution change or menu return.
- Native v0.0.2 world-access audit on 42.20.4 confirms the returned `PlayerCamera` cannot be directly indexed for its methods or matrices. A live world-render callback fired; the sampled 33 by 33 neighborhood had 2 SpriteModels among 1,425 objects and none for its 1,089 floors. These results reject the tested direct-camera and complete existing-model reuse routes, not every possible original renderer. Debug-only reflection cannot satisfy ordinary Workshop runtime support.

# Child DOX Index

- None.
