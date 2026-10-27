# Vehicle import contract

The project uses original assets. Existing models were inspected read-only to understand the installed Build 42.20.0 pipeline; no donor mesh, texture, UV layout, animation or script text was copied into the package.

## Evidence and boundaries

- REA archive inspection `ev_1376cef60c07636f48c5d320ceea2311b59195ba558d263e5709bfa584b2bc99` identifies the shipped game JAR. Its SHA-256 is `e4661ca9cb168abc995d3cf59994fa17f66ba8a4e2c2899cbfa48f7eacea54b8`.
- REA inventories archive members. It did not analyze FBX geometry or execute the importer. The Java decompiler route was unavailable because the JEB MCP endpoint was not connected.
- `tools/InspectFbx.java` separately loaded reference FBX files through the installed game's `jassimp64.dll`, then invoked `ProcessedAiScene.findMesh` and `initMeshTransform`. A disposable Java probe also read imported bone weights and animation channels. These are native importer observations, not REA decompiler results.
- The probe now mirrors all seven Assimp flags used by shipped `FileTask_LoadMesh`, including `MAKE_LEFT_HANDED`. Earlier raw probes without those flags do not establish final game-space signs. This conversion maps the original source nose +Y through raw FBX -Z into native +Z; the corrected native probe puts the hood at +Z and trunk at -Z. Do not flip the vehicle's front/rear script axes based on raw FBX bounds.
- `javap` inspected the shipped `VehicleScript`, `ModelScript` and `BaseVehicle` bytecode for scale, animation and part contracts. Neither bytecode inspection nor import success proves in-game rendering, driving or compatibility of the old mod.
- Local raw probe outputs remain under ignored `build/import-comparison/`. Sources, screenshots and local installation paths are excluded from published assets.

## Comparative observations

| Property | Installed en72 reference | Shipped Martin vehicle |
| --- | --- | --- |
| FBX | `Vehicle_en72_Javelin.fbx` | `ModernCarWithDoors_Martin.fbx` |
| SHA-256 | `caa33bf0801172c37e260188d75208d40f8661d525d1da8fcaba234424ca04a1` | `e38980ce3beca8f25e7695895c841ca8eabf0efda70c418f1f74764e36d99463` |
| Imported inventory | 21 meshes, 1 animation | 8 meshes, 8 animations |
| Selected body lookup | `Body` resolved | `Vehicles_ModernCar_mesh` resolved |
| Selected panel lookup | Door, hood and front window resolved separately | Door, hood and rear window resolved separately |
| Body weights | No skin weights | Body vertices weighted to a vehicle bone, although the model definition is static |
| Moving parts | Dedicated door, hood, trunk and window weights | Dedicated door, hood, trunk and window weights |
| Imported animation names | `Armature|ArmatureAction` | Separate named door, hood, trunk and window clips, plus a take |
| Model definition scale | `0.004519`; vehicle scale `1.0` | `0.01`; vehicle scale `1.82` |
| Resolved node transform | Axis rotation and scale `100` | Axis rotation and scale `1` |

Static versus skeletal behavior is a script decision as well as a file property. Martin's model definitions explicitly select a static shell and skeletal panels. The old reference uses skeletal panel definitions and isolates their bone weights. Its front windows also use the native `ClosedToOpen` animation hook. This supports separating rolling windows from swinging doors, but does not establish that the old mod works on the current build.

The two files have different stored coordinate sizes and transforms. Therefore their numerical scale values cannot be copied between models. The imported en72 body spans approximately `384.96 x 238.25 x 973.98` before its model scale; Martin spans `91.53 x 62.94 x 232.43`. The second axis is vertical after the native transform in both sampled body meshes. These are importer-space bounds, not measured real-car dimensions.

## Original project export rules

- Export one atlas material per named object. Resolve every `file|mesh` selector with the native resolver after rebuilding; a valid FBX alone does not prove the requested submesh resolves.
- Author and save the editable source in metres. For export only, copy mesh and armature datablocks, apply `Scale(100) @ Rotation(-pi/2, X)`, scale animated location keys by 100, and export with `axis_forward='Y'`, `axis_up='Z'` and unit scale `0.01`. Restore source data and keys before saving the Blender project. Native mesh-node transforms must be identity; model-script scale `0.01` converts the baked centimetres to metres and vehicle-script scale remains `1.0`.
- `InspectFbx` reports importer-transformed bounds separately from render-effective bounds and a vertex anchor. The renderer transposes the imported node matrix before multiplying it. Comparing only symmetric bounds concealed an inverted export. The calibrated bake preserves the original shell's actual rendered vertex positions while removing the ambiguous external skeletal transform.
- Keep shell and fixed cabin parts static; moving panels and windows need weighted skeletal meshes. Use separate window bones beneath their corresponding door bones and independent rolling clips.
- Use the `vehicle` shader for all project meshes, including wheels and the fixed cabin. The shipped static wheel shader expects UVs at vertex attribute 3, while the project mesh layout supplies the coordinates used by `vehicle` at attribute 2. In-game testing showed flat pink wheels with `vehiclewheel` and correctly textured spokes and tires after selecting `vehicle`.
- Give exported actions explicit names. Inspect the actual imported animation names and verify each vehicle animation reference, rather than assuming the FBX filename names its clip. The old reference's raw imported name contains an armature prefix while its script uses the action suffix.
- Windows use `ClosedToOpen`, `animate=false`, `reverse=false` for this project's closed-to-lowered clips. Shipped `BaseVehicle` bytecode sets their track position to clip duration multiplied by the native window opening fraction.
- Door, hood and trunk tracks must retain ancestor transforms. Restrict only window tracks to their own window bone: native window models share the parent door's animation player, so the door track supplies the root and hinge transform while the window track supplies independent lowering.
- Native rendering culls backfaces. The trunk lid needs an outward top and a closed underside; both large side-window faces must point outward after mesh normal recalculation. The source pose check verifies those normals because a two-sided studio preview can hide the defect.
- Keep model-space wheel, seat, chassis and interaction positions consistent with the exported shell. Native vehicle loading applies the vehicle model scale to its physics coordinates; model asset scale and vehicle scale are separate factors.
- The vehicle model and centre-of-mass vertical offsets are zero. `VehicleScript.toBullet()` adds the model offset and suspension rest length to wheel connection height. A former 0.65 m offset placed the physics origin near ground level, where suspension compression made the native seat path target floor -1. Changing both offsets together raises the physics coordinate origin while retaining the settled body/wheel relationship. Keep a positive origin margin and verify native entry after physics edits.
- Native side interaction targets move inward by 30% of area width; front/rear service targets move inward by 30% of area height. Keep these targets beyond the navigation polygon's 0.15 m padding. This vehicle uses side centres at 1.45 m and longitudinal service centres at 3.0 m.

## Remaining runtime checks

Importer checks do not verify animation blending between a door and its child window, removal visibility, glass transparency, headlight appearance, passenger alignment, physics contact or save/reload behavior. Inspect the original car in the game vehicle editor and an isolated world before treating those behaviors as verified. The shipped Martin file provides a native pipeline comparison, not a substitute for testing this mod.
