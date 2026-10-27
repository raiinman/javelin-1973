# Native editor skin readiness investigation

2026-10-18, installed game reported as Build42.20.4. Read-only investigation of the exact167,134-triangle candidate. No package, source, game, profile or UI changes were made by this investigation.

## Result

The blank vehicle editor coincided with a short burst of native renderer exceptions while animated part skin data was unavailable. The parent operator subsequently observed the unchanged candidate render successfully in the editor. The evidence supports an asynchronous readiness race in the shipped editor, rather than a permanent mesh import or script failure. Do not change the FBX or disable its animated parts on this evidence.

## Observations

- Isolated-profile model SHA256: `7b019c34b6ccb780029df367360b117d852f23a73823d095a93c5b55c4a0fd0b`, matching the assigned candidate. Existing native import evidence reports11 meshes and3 clips; that is an import gate, not proof of runtime readiness or motion.
- Full console prefix before the first exception was reviewed, not just the tail. The mod loads at line175. No preceding Java exception or candidate mesh/animation failure appears before line787. Vanilla Lua require warnings and general game-content warnings do appear; this is a bounded log observation, not a claim that every warning is harmless.
- Line787 warns `skinningData is null, matrixPalette may be invalid`. Line790 starts `NullPointerException: Cannot read the array length because "skinTransforms" is null`, at `UI3DScene$VehicleRenderData.initPartModel`, line2811.
- There are117 occurrences of this NullPointerException. Their first and last timestamps are03:34:47 and03:34:49 local time. Remote Desktop Commander on APeX-2 independently confirmed console size202,901 bytes and last write03:34:49 in two reads separated by investigation work. No continuing log growth was observed.
- The parent operator reported that after Escape and waiting, the latest long-quarter-glass candidate rendered in the native editor. This is operator runtime evidence, not a new screenshot captured by this investigator. Panel animation and other angles remain separate gates.
- The package declares the body, fixed glass, interior and wheel static. Doors, hood, trunk and windows are animated; the windows declare their bone weights. Vehicle part animations reference `J73_Panels`, `J73_WindowLeft` and `J73_WindowRight`. These declarations do not justify forcing the moving parts static.

## Shipped bytecode path

Read-only `javap -c -p` inspection used the installed `projectzomboid.jar`, SHA256 `80e405a4bfc42f6072e75b3735f458a6514143da011d3226007ded305a442f44`. Bytecode is shipped implementation evidence, not recovered original source.

1. `UI3DScene$VehicleRenderData.initPartModel` returns if the model is null, but proceeds without checking its readiness. For a non-static model it acquires an animation player, calls `updateAnimationPlayer`, reads `Model.tag` as SkinningData, and only warns when that tag is null.
2. `SceneVehicleModelInfo.updateAnimationPlayer` checks `AnimationPlayer.isReady()` and returns early when false. Its caller does not receive a readiness result and continues regardless.
3. `AnimationPlayer.initSkinningData` returns while the model is unready or its tag is null. Allocation of `modelTransforms` occurs only after valid skinning data is available.
4. `AnimationPlayer.getSkinTransforms(null)` returns `modelTransforms` directly. The editor caller then dereferences the returned array length to size its matrix palette. This exactly explains the observed warning and exception while initialization is incomplete.

## Minimal response and limits

Keep the current candidate. Let loading finish, reopen/select the editor vehicle if needed, and verify that the log remains stable before judging rendering. Reproduce on a fresh launch before proposing an application workaround. If a bridge-level workaround becomes necessary, defer candidate editor selection until the required animated models and their animation players report readiness. A robust upstream fix would skip rendering an animated part until both its skinning data and transform array are available. Neither fix was implemented here.

The exact slow-loading part and load duration were not captured. The static path explains the failure mechanism; recovered runtime rendering and the stopped two-second exception burst support the transient diagnosis. They do not prove all animated parts are correct or establish visual likeness.

REA skill and plugin were consulted. REA6.5.0 `binary_session` reported no active target, no configured Ghidra installation, and no Java class decompiler route suitable for this jar. No unsupported native decompilation was attempted; available JDK bytecode inspection supplied the bounded implementation evidence. The session response did not supply an Evidence ID, so none is invented.

DOX pass: only this investigation record was added. Root AGENTS.md remains unchanged because no durable ownership, workflow or behavior contract changed; root already owns `docs/`. No child AGENTS.md exists under `docs/`.
