# Native paint shading audit

2026-10-18. Read-only investigation of the187,836-triangle candidate. No source, package, profile, game or UI changes were made. This report is the only intentional file write.

## Finding

The installed `vehicle` shader supports normal-based lighting without baked shading. The current body imports with finite, varied, unit-length normals through the shipped native importer. Uniform outdoor paint therefore does not establish a broken normal export. The inspected world renderer supplies uniform ambient colour plus up to five local square lights, with no separate fixed sunlight direction in this path. Without effective local lights, a constant-red atlas naturally provides little form shading beyond weak environment reflection.

Original baked ambient occlusion and restrained form shading may improve readability, but they are an art-direction choice to test after measuring actual native light inputs. They are not a shader prerequisite, and a baked directional sun would remain attached to the car as it turns.

## Exact scope and primary sources

- Workspace model SHA256: `8c1a7f93bfa30924138610be194a65156b9e9a5413133d76888b0993d011ce5e`.
- Saved Blender source SHA256: `363dfc71f833875a3c94f577bb094d19e52db2c9f2a1d82240629327871fccbf`.
- Installed game jar SHA256: `80e405a4bfc42f6072e75b3735f458a6514143da011d3226007ded305a442f44`.
- Installed `media/shaders/vehicle.frag` SHA256: `cf0c9bc62247b79e2db9ade670bcc237e479cc7fad5bd5c2dfd9f6ef95d24975`.
- Shipped shader text and JDK `javap -c -p` output were inspected directly. Bytecode is shipped implementation evidence, not original Java source.
- REA skill and plugin were consulted. The current session is target-free; the prior established limitation remains no configured Java class decompiler route/Ghidra installation. Shader source and JDK bytecode inspection answer this bounded question without modifying that setup. No REA Evidence ID was returned for the session status, so none is invented.

## Shader contract

`vehicle.frag:84` normalizes interpolated normals. Lines100-124 compute ambient plus five `max(dot(normal, normalize(LightNDirection)),0)` terms, quantized to thirds by the shipped `util/math.glsl` ceil-based helper, then clamp lighting to0..1. Line198 multiplies the surface colour by lighting and tint. This supports live lighting but can suppress subtle curvature through quantization or saturation.

Palette alpha255 only bypasses HSV recolouring at line167; it does not bypass line198 lighting. The shader has no AO, roughness, metallic or normal-map sampler. The Blender preview's Principled metallic/roughness settings do not constitute this native shader's material contract.

Lines169-176 distinguish glass by semantic mask. Glass mixes environment reflection with coefficient `0.1 + ReflectionParam.y*0.5`. Other surfaces mix `texRef/4` with coefficient `0.05 + ReflectionParam.z*0.3`. Glass can visibly reflect while paint remains subdued. This difference does not prove paint normals failed.

`vehicle_static.vert` transforms normal vectors with the object transform and passes them to the fragment shader. `vehicle.vert` applies the weighted bone matrix. The model scripts select `shader = vehicle` and retain static fixed parts and animated moving parts.

## World light setup

The installed implementation establishes this chain:

1. `VehicleModelInstance.UpdateLights` calls `ModelManager.getSquareLighting`.
2. `getSquareLighting` clears every EffectLight, returns if no current square, and otherwise fills entries from `square.lighting[player].resultLightCount()` and its ResultLight records. These have position, RGB and radius. No fixed sun light is injected in this method.
3. `ModelSlotRenderData.initModel` obtains one ambient RGB using the vehicle's square `interpolateLight`. The no-lighting debug option can force this ambient to white. Its vehicle initialization converts active positive-radius EffectLights to vehicle-local coordinates.
4. `Model.DrawVehicle` supplies these lights and ambient to the shader. It also supplies body/window reflection parameters from the vehicle model instance.

This is static control-flow evidence. The current world's actual resultLightCount, ambient RGB, light radii/colours, debug option and GPU uniforms were not read here. Ambient domination, absent point lights or clamping are hypotheses until those values are captured. There is no basis here to declare the native lighting globally broken.

## Actual native normal import

An isolated, read-only JShell probe imported the exact workspace FBX through the installed `jassimp64.dll` and `projectzomboid.jar`, using the same seven default postprocess flags as `FileTask_LoadMesh.loadFBX`: FIND_INSTANCES, MAKE_LEFT_HANDED, LIMIT_BONE_WEIGHTS, TRIANGULATE, OPTIMIZE_MESHES, REMOVE_REDUNDANT_MATERIALS and JOIN_IDENTICAL_VERTICES. No game/world/editor was launched or controlled. The probe used installed JDK26, not the game's bundled VM; no source/class file was written. A first custom-loader attempt failed JNI class-loader linkage, then a default-name attempt could not find `jassimp.dll`; the final same-class-loader load succeeded against `jassimp64.dll`.

| Imported mesh | Vertices | hasNormals | Distinct directions rounded to0.01 |
|---|---:|---|---:|
| Body |72617|true|14300|
| DoorLeft |3564|true|1163|
| DoorRight |3564|true|1163|
| Hood |756|true|296|
| Interior |42924|true|9663|
| Trunk |15934|true|4430|
| Wheel |11872|true|5351|
| WindowLeft |36|true|11|
| WindowRight |36|true|11|
| RearGlass |147|false|not applicable|
| Windshield |14|false|not applicable|

For every normals-present mesh, all vertex normal lengths were finite and within0.99999985..1.00000016; no zero/near-zero normals were found. This disproves wholesale missing or identical Body normals at the native Assimp boundary. It does not prove every normal's orientation, smoothing quality, final GPU binding or light-space alignment.

A separate read-only binary FBX parse found finite unit normal arrays in all eleven source geometries, including the two glass meshes. Native Assimp reports no normals for the separate fixed RearGlass/Windshield, so this is a distinct importer observation to investigate. It cannot explain the Body paint result. Inspected `ImportedSkinnedMesh` bytecode copies native normals when present, and otherwise writes a constant `(0,1,0)` fallback. That class's fallback is not evidence that this exact static-glass runtime path used it.

## Interior and open-panel observations

The parent operator reports the latest candidate spawned in the world with open panels and lowered windows, uniform red paint, reflective glass, visible rear wheel through the cargo opening and black engine/cabin regions. These are operator observations; this investigator did not change the live test or independently capture those views.

The vehicle script declares `part J73Interior`, category nodisplay, model Default file `J73_Interior`. Its model script references `J73Mesh_Interior`, shader vehicle and static true. The exact FBX native-import Interior mesh has42,924 vertices and valid varied normals. These facts establish available mesh and script references, not that the runtime part is attached and rendered. No Cardin stripes visible from one roof-occluded doorway angle does not establish missing interior. Cargo-wheel exposure and black cavities remain independent visibility/geometry checks, not outcomes explained by flat paint.

## Minimal next diagnostic

After the active pose test finishes, capture read-only values for the current car's square resultLightCount, each vehicle EffectLight position/RGB/radius, ambient interpolation and `DebugOptions.fboRenderChunk.nolighting`. Also inspect runtime model/submodel presence for `J73Interior`. Preserve the unchanged candidate while collecting these values.

Then compare the unchanged car at two headings under a clearly effective local light in subdued ambient, plus the same camera under daylight. If live shading follows light and rotation, preserve the normal export and test an original AO/form-texture prototype on a disposable copy. If no response occurs despite effective unsaturated light, inspect static versus skinned normal binding and transform space before changing geometry or textures. A control vanilla car under the same conditions can distinguish engine lighting from candidate appearance without copying its assets.

The semantic atlas reuses small swatches across body regions; a spatially meaningful AO bake requires unique surface UV coverage or a deliberately designed original form-shading mapping. Painting an AO gradient into one shared red swatch would repeat it across unrelated faces. Do not claim a realistic bake is a one-cell colour tweak.

DOX pass: root AGENTS.md owns `docs/`; no child AGENTS.md exists here. No durable workflow or ownership changed, so the existing instructions remain unchanged.

## Prepared follow-up diagnostic

Ignored `build/native-lighting-cycle5/lighting_snapshot.lua` is an opt-in read-only snapshot with shipped-compiler syntax validation and bytecode-verified field/API notes. It has not executed. Scalar vertex AO could encode one value in a monotonic red ramp within existing semantic swatches without unique UV islands. This differs from richer spatial AO, which still needs suitable surface coverage. No AO or texture change is implemented; first measure actual native lighting.

## Cycle5 live snapshot

The opt-in diagnostic executed successfully on the Toolkit-launched188,828-triangle candidate after rendering in the disposable no-save world. Three samples at10/20/30seconds report `FBORenderChunk.NoLighting=false`, interpolated square ambient `(1,1,1)`, cached square light count0 and all five vehicle light radii/RGB zero. This establishes fully bright ambient with no active local vehicle lights at that location/time, supporting ambient-dominated flat paint rather than missing Body normals. It does not prove the final GPU uniforms or an effective point-light response. No AO/texture/lighting-setting change is adopted. Console evidence is retained after normal test exit under `build/parity-cycle5/native-world-audit/`.

## Interior activation root cause

Read-only shipped VehicleParts/BaseVehicle investigation found that an itemless custom part with only a model declaration never activates its model. `VehicleParts.initParts` invokes configured callbacks as `(vehicle,part)`, and `BaseVehicle.createPhysics` calls it outside the created-once branch before model-slot creation. The original shared `J73Vehicles.InitInterior(vehicle,part)` callback now enables the declared Default model for this script only. The native visibility operation is idempotent. This explains a likely source/runtime divergence; actual fresh-spawn and saved-vehicle reload confirmation remain required. Detailed shipped-bytecode evidence is retained under ignored `build/native-lighting-cycle5/interior-activation.md`.

## Fresh-spawn activation confirmed

Fresh Toolkit no-save spawn confirms the original init callback activates itemless J73Interior, with13 active model entries and a non-null J73_Interior model instance at10/20seconds. The open door visibly reveals Cardin cushion ribbons and dashboard trim; the cargo opening no longer exposes the rear tire from the inspected high rear-quarter angle. This resolves that fresh-spawn activation/visibility defect, not whole-cabin likeness or every viewing angle. Real saved-vehicle reload and multiplayer remain untested. The game exited normally, both hash-matching temporary audit hooks were removed, and the separate inspection latest-save pointer was restored. The permanent original shared callback remains in the mod. Evidence: ignored `build/parity-cycle5/interior-native-audit/audit-markers.txt` and completed `build/parity-cycle5/interior-temporary-hooks.json`.
