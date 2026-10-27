# Native form shading prototype

Experimental cycle6, not promoted or installed. Genuine same-part self-occlusion makes little useful difference to this car's broad paint surfaces. A restrained upper-hemisphere form multiplier modestly separates roof/fender tops from sides under flat ambient, but remains an artistic rest-pose shading bake, not AO. The narrow protected lookup bands also introduce a native mip/filter uncertainty. Neither variant is ready for automatic adoption.

Geometry/reference parity remains a separate requirement. No geometry, native normals, rig weights or panel registration changed in this experiment; adding colour contrast cannot establish that the current proportions match the original car.

## Frozen input and scope

- Input: the202,046-triangle backlight checkpoint at `build/parity-cycle5/backlight/checkpoint/`, copied into `build/native-form-shading-cycle6/frozen/`. Saved input blend SHA256 `9c3cb29712b94219c1a035c958f005adb185e96098e3f54997988a2cb140f8d5`.
- Variants: `baseline/`, `self-ao/` and `hemisphere/` beneath that experimental folder. Each has an editable saved blend, experimental FBX and textures. The202,046 input already includes cargo work, but omits later canonical dashboard/crown work and must not replace the current package.
- `tagged/tools/build_mod.py` is an isolated copy instrumented with a face-domain Boolean paint tag. It selects plain red exterior paint, excluding all decal/plate module calls and red beam/cylinder/ellipsoid details. RedLight/redDark artwork, letters, grille, glass, lamps, upholstery and interior UVs remain untouched.
- Only this document and the experimental build subtree were edited. No canonical generator, texture, profile, UI, game or save was changed. All prototype artwork and geometry come from this original project; no vanilla texture or model was copied.

## Native contract and lookup encoding

The installed `vehicle.frag` multiplies sampled Texture0 by ambient plus five normal-dependent local-light terms. Alpha255 preserves authored colour through its HSV branch, but does not disable lighting. It has no AO sampler. The recorded native snapshot has ambient1,1,1, no square local lights, all five vehicle lights zero and NoLighting=false, so the constant red swatch has little intrinsic form contrast. See `native-paint-shading-audit.md` for the shipped shader and bytecode evidence.

Scalar paint shading is encoded as a red ramp inside the existing32px semantic cell. Only a tagged paint loop's U coordinate changes to represent scalar0.78..1; V selects its protected ramp row. Every loop stays in its original semantic cell, the material count stays one, and mask/light/damage/rust files are byte-identical to the frozen package. Palette alpha remains255 everywhere.

Untouched red details already use part of these cells. Rather than moving their UVs or tinting their artwork, `prepare.py` reserves an unused three-pixel horizontal band outside all untouched red faces' UV Y bounds, with a two-pixel exclusion margin. Most bands use row16; the front-left guard cell needs row28. Palette bytes outside these bands stay unchanged. `prepare-report.json` records the protected ranges and selected rows. This preserves all nonpaint UVs exactly, rather than merely preserving their mask categories.

This is a base-level texture proof. Mip generation can mix the band with surrounding constant red pixels, weakening the intended contrast and potentially affecting nearby detail samples at distance. The three-pixel band is deliberately conservative about existing artwork, but it limits sampling robustness. An actual native filtering/distance A/B is required before adopting this layout. Do not claim this solves spatial texture authoring generally.

## Two accurately named shading methods

**Same-part self-AO:**24 deterministic cosine-weighted hemisphere rays from each unique sampled paint corner position/normal,0.16m radius and1.5mm outward bias. Distance-falloff obstruction gives multiplier `1 - 0.16 * mean(blockedFalloff)`. Each BVH contains only the current original part, so closed doors/hood/trunk cannot bake shadows onto neighbouring objects. This is bounded self-occlusion, not a complete physically calibrated scene AO solution.

Mean scalar over paint loops is0.9901 for Body,0.9978 for each door,0.9984 for Hood and0.9881 for Trunk. Rare tight regions reach about0.84; broad exposed surfaces remain nearly unchanged. Visual inspection of the fixed ambient views confirms that this does little to resolve the flat-car readability problem. Do not increase its strength merely to manufacture an improvement.

**Upper-hemisphere form shading:** `0.78 + 0.22 * (0.5 + 0.5 * restCornerNormalZ)`. An upward surface stays unchanged, a vertical surface receives0.89 and a downward surface0.78. This is invariant to car yaw and contains no preferred compass-facing light direction. It is explicitly an artistic rest-normal form multiplier, not AO. The saved local corner normals themselves are unmodified.

Mean scalar is0.9511 for Body,0.8913 for doors,0.9988 for Hood and0.9009 for Trunk. The multiplier is encoded in source RGB bytes, so colour-space conversion/tonemapping affects the final perceived difference. It is not a recovered factory paint response or a measured game-lighting model.

## Actual comparisons

`render.py` produced24 fixed-camera views, recorded in `render-report.json`:

- `renders/ambient1/` in each variant: front/rear quarters, panels closed and open. Texture colour feeds emission at strength1 with no diffuse, AO or environment reflections. This isolates the verified constant-ambient factor; it is not a pixel-identical recreation of the complete native shader.
- `renders/local-light-sim/`: closed front and open rear, using ambient0.45 plus one normalized effective light direction with0.5 strength and the shipped ceil-to-thirds quantization. This approximates one effective local-light term, without claiming captured native uniforms, attenuation or GPU output.
- `renders/paint-studio/`: the same two views under the unchanged softboxes, controlled Principled roughness0.32, metallic0.05 and coat0.35 for all variants. This deliberately uses identical inspection material settings; the native shader does not implement those Principled controls.

Visual findings:

- Self-AO barely changes broad surfaces in the ambient1 closed/open views. It is unsuitable as the main cure for the observed flat red paint.
- Hemisphere shading gives modest fender-crown, sail and side differentiation. The car still reads as a simplified model under emission-only ambient. It does not repair silhouettes or component proportions.
- Open-panel views reveal no closed-neighbour contact-shadow ghosts. That is consistent with excluding other parts from the AO BVH. All source panels still move independently.
- Hemisphere shading follows the *rest* surface orientation. A raised hood remains relatively bright because its closed upper surface was upward; it does not become a dynamically relit hemisphere bake. This is an expected limitation to judge in native open-panel views, not evidence of correct physical illumination.
- The simulated local-light views retain red paint rather than crushing it to black; their quantized bands also emphasize existing mesh/normal changes. Strong studio highlights dominate some areas. Neither light simulation proves an acceptable native appearance at night or at distance.

The same camera and geometry are used across variants. No comparison is aligned, cropped or scored to imply a likeness percentage.

## Verification and recommendation

- `prepare-report.json` asserts one shared202,046-triangle position/topology hash across frozen input and all variants: `5419d318363ab448abc9d965eafb808c07413879cb124204b75c0662e911c490`.
- `normal-skin-proof.json` proves identical saved corner normals and skin weights across frozen input and all three saved variants. All eleven original mesh nodes retain one material.
- Both `import-self-ao.log` and `import-hemisphere.log` pass the installed native importer: eleven resolved meshes and the expected three named clips, including the separate animation FBX. The initial experimental re-export omitted the saved hidden wheel; export now temporarily unhides all eleven selected source meshes and restores their visibility afterward. The corrected native import checks pass.
- `pose-hemisphere.log` passes the full saved-model pose/ten-fraction clearance gate. `static-hemisphere.log` passes with0 errors. `payload-differences.json` records that only experimental FBXs and the palette change; masks and scripts do not.
- Blender5.2.1 background processes reopened the saved files for rendering/proof. Current official Blender BVHTree and corner-normal/attribute documentation was fetched through Context7 before the new probe implementation. Native shader/bytecode evidence came from the installed game, with REA skill/plugin limitations retained in the earlier audit.

Keep self-AO as a negative experiment. Hemisphere form shading is worth a reversible native A/B only if the parent wants to assess its small readability benefit against the lookup filtering and open-panel limitations. Do not ship or merge either result from studio evidence alone. Preserve the original unshaded package and compare identical car heading, camera, time, local lights, open/closed states and several distances. No native A/B or promotion was performed here.

DOX pass: root owns `docs/` and this disposable experiment. No durable project contract or workflow changed, so root/tools/assets AGENTS.md remain unchanged. The experimental files are not distribution inputs.

## Matched214,322 staging for a future native A/B

Cycle7 now uses the exact current `build/parity-cycle6/checkpoint/` input, including cargo, dashboard, crown and the original Interior init callback. Frozen source SHA256 is `c9c25499d084ded7bfe8910375247a9be5568f0c3235bce57166656dc01216c8`. Only baseline and hemisphere were prepared; the negative AO experiment was not repeated.

- Baseline stage: `build/native-form-shading-cycle7/baseline/Javelin73PC/`. All17 payload files are byte-identical to the214,322 checkpoint.
- Hemisphere stage: `build/native-form-shading-cycle7/hemisphere/Javelin73PC/`. It contains exactly the same17 payload paths, with **only** `common/media/models_X/vehicles/J73_Car.fbx` and `common/media/textures/Vehicles/J73_Palette.png` changed. The separate animation FBX, all masks, model/vehicle scripts and `Javelin73PC_Visual.lua` init callback remain byte-identical. No diagnostic Lua, reports, source instructions or ownership markers were added to either payload.
- `build/native-form-shading-cycle7/deployment.json` records all17 hashes for each variant, their exact package paths, no extra payload files and the two-file difference. `checkpoint.json` freezes the experiment and its scripts. No deployment was performed.
- Both saved variants retain214,322 triangles and source position/topology hash `b01e553a1cfa6e39ae37c24dc7f12d8929bb5877a3e091ee3f62fe2f5bd7ae12`, with exact original corner normals and rig weights. All eleven nodes retain one material; every nonpaint UV is unchanged and palette alpha remains255.
- Both packages pass the native eleven-mesh/three-clip import gate. The hemisphere saved pose/ten-fraction clearance gate and static validator also pass. Logs and proofs are contained in the cycle7 folder.
- Four fresh matched ambient-only images are at `baseline/renders/ambient1/front-closed.png`, `baseline/renders/ambient1/rear-open.png` and their `hemisphere/` counterparts. `render-report.json` records the same cameras/poses and simplified emission-only material. The hemisphere variant's modest top/side separation remains visible on the current crown; the car still lacks complete reference form identity under flat ambient.

The intended next test is a controlled native comparison of these matched stages, not a comparison between the old202,046 experiment and the current214,322 game car. Existing cycle6 filtering, colour-space, rest-pose/open-panel and limited-benefit caveats remain applicable. Root owns installation, rollback and live-game testing. No canonical/profile/UI changes, native A/B or adoption were performed by this preparation.

## Read-only native comparison controls

`build/native-form-shading-cycle7/audit-control.lua` is a prepared, self-contained diagnostic for the parent's future audit. It defines `J73AuditControlSnapshot(car, label)` and includes the existing `J73LightingSnapshot` verbatim. Nothing invokes either function, registers events or changes vehicle, camera, lighting or time state. The caller supplies the exact spawned car. The shipped LuaCompiler accepted the complete file without executing it.

The control record contains vehicle ID/script, world XYZ, native Euler XYZ in degrees, native forward vector, horizontal heading from native positive X, player0 zoom, world-camera offsets, screen size, player position, time of day and world-age hours. It then records the existing interpolated square ambient, square cached result-light count, all five actual vehicle effect lights and `FBORenderChunk.NoLighting`. Failed reads print `UNAVAILABLE` rather than silently substituting values.

Installed-game bytecode verifies `BaseVehicle.getAngleX/Y/Z` converts quaternion Euler XYZ to degrees; `getForwardVector(out)` returns native basis column2, with native Y as up. The derived heading is explicitly `atan2(nativeZ, nativeX)`, not a claimed compass bearing. `Core.getZoom(int)`, screen dimensions, `IsoCamera.getOffX/getOffY(int)` and both GameTime getters exist. The Lua exposer registers IsoCamera and Vector3f; shipped Lua uses `getZoom(0)`, `Vector3f.new()` and `math.atan2`. These observations ground the prepared calls, but syntax acceptance alone does not prove every live reflection read succeeds.

This captures the world camera, not the vehicle editor's private camera. A baseline/hemisphere claim requires matching the recorded transform, world camera, pose, time and lighting, with no missing required control values. No live invocation, installation or camera adjustment was performed by this subtask.

## Shipped texture filtering evidence and limit

Read-only `javap` inspection of the installed jar shows `BaseVehicle.LoadVehicleTexture(String)` passes flag256 plus optional compression flag4 to `Texture.getSharedTexture`. The ordinary one-argument shared-texture overload supplies only optional compression4. In `TextureID.generateHwId`, the usual non-depth branch selects linear magnification unless flag2 requests nearest; minification is linear unless flag1 requests nearest or the mip-enabled branch selects `LINEAR_MIPMAP_LINEAR` (9987). That mip branch requires flag64 and is disabled by flag16, with an additional method argument condition. Mip image levels are uploaded when enabled.

Consequently, the inspected ordinary loose vehicle-texture path does not itself request mipmaps. This narrows the earlier uncertainty, but does not establish this running palette's actual GPU state: shared textures are cached by path, other loading paths can supply flags, and debug filtering overrides can alter applied filters. No live TextureID or GL state was read. Linear sampling at the base level still requires adequate ramp-band margins; mip-enabled loading would additionally mix the narrow bands with surrounding red. Retain the controlled native near/far A/B before judging sampling stability.

DOX closeout for this addition: only the isolated control snippet and this evidence note changed. Root continues to own the disposable build experiment and `docs/`; no durable workflow, ownership or child index changed, so AGENTS.md files remain unchanged.

## First native comparison rejected: randomized debug spawn yaw

Parent native evidence recorded baseline horizontal heading -88.1911656degrees and hemisphere -80.32667degrees. Zoom0.75,1600x900 screen, world position, ambient1,1,1 and all five zero lights agreed, but the heading did not. These captures do not constitute a matched A/B and do not support adoption.

The installed jar explains this directly. In `LuaManager$GlobalObject.addVehicleDebug`, bytecode60..78 computes `dir.toAngle() + PI + Rand.Next(-0.2f,0.2f)`. Supplying `IsoDirections.N` avoids random direction selection, but does not avoid the subsequent random yaw offset, approximately +/-11.459degrees. The integer0 argument selects skin, not exact yaw. IsoDirections N is ordinal0 and `toAngle()` is ordinal times2PI/8, making its unjittered rotation PI about native Y.

The supported temporary correction is `car:setAngles(0,180,0)` immediately after the returned car is checked, before its panel cycle begins. `BaseVehicle.setAngles` accepts degrees, multiplies by0.017453292, calls Quaternionf.rotationXYZ, copies the existing native transform and changes its rotation before `setWorldTransform`. That method updates jniTransform and, in this single-player non-server path, calls Bullet.teleportVehicle with the preserved origin and new quaternion. BaseVehicle is registered by the Lua exposer, and shipped `media/lua/client/Vehicles/ISUI/ISVehicleAngles.lua:128` uses the same setter. A pure mathematical check with the shipped JOML class transforms forward(0,0,1) to(0,0,-1), producing the audit heading -90degrees. This check does not instantiate a game vehicle or prove live settling.

`stage_native_ab.py` now generates both baseline and hemisphere hooks from the identical frozen fixed-timer template, inserts that one setter and immediate forward-heading assertion (absolute error below0.01degree), and changes only the comparison label between stages. The original frozen hook remains intact; `deterministic-audit-preview.lua` preserves the generated baseline for inspection. The complete generated Lua passed the shipped LuaCompiler without execution. No physics freezing, repeated yaw correction, new gameplay or saving was added.

Timing limits remain material. `addVehicleDebug` has already called addToWorld/createPhysics when it returns, so this is a live native transform correction rather than a pre-physics seed. The setter preserves position and does not explicitly clear velocity or guarantee subsequent suspension/collision settling. It also has a coarse existing-Euler early-return check; this patch makes one initial correction and verifies the actual forward vector rather than assuming subdegree setter precision. Existing ten-second controls continue for eighty seconds, while the panel cycle accumulates only bounded active-tick time. Editor pauses can therefore move controls relative to the visible poses. Verify actual world position, heading, full orientation, camera, pose and lighting at each captured comparison; an initial FIXED_SPAWN line alone is insufficient. If those controls drift, reject that pair and investigate before adding more state changes.

At12:44UTC the parent-authorized baseline-first stage passed the absent-process, exact17-file payload, two-hook ownership and Toolkit-marker gates. The new baseline cleanup manifest is active. Root retains responsibility for Remote Desktop Commander PC verification, Toolkit launch and visual review; this preparation makes no new native matching or adoption claim. The previous hemisphere test was restored to the frozen baseline by root before this stage. New canonical218,034 geometry remains separate from this214,322 A/B.

REA skill and plugin were consulted again. Its session reported no configured Ghidra provider and no active target; this bounded Java investigation used the installed JDK's read-only javap and the shipped Lua/JOML/LuaCompiler instead. No tool configuration, canonical assets or UI was changed. DOX ownership and indexes remain unchanged.

## Fixed native pair: modest closed-pose benefit, incomplete adoption evidence

The subsequent fixed pair produced eight matching control samples. Both cars stayed at10605,8834,0 with heading approximately-90degrees; maximum paired heading difference was1.72e-11degrees and maximum wrapped Euler difference1.71e-11degrees. Both had native Euler X=-179.94241333007812, Y approximately0 and equivalent Z+/-180, with forward-vector component differences below6.64e-9. Both camera schedules matched: sample1 zoom1/offset112288,621446, then samples2..8 zoom0.75/offset112488,621558,1600x900 screen and player10601.5,8834.5,0. Ambient1,1,1, no square lights, five zero light radii/RGB and NoLighting=false matched throughout. Paired time/world-age differences stayed below0.038game seconds. Pose markers occurred at identical frames60/1260/2460/3660.

The raw parsed samples, deltas and source-log hashes are `build/native-form-shading-cycle7/fixed-native-controls.json`, reproduced by the read-only `compare_native_controls.py`; the analyzed hemisphere log is preserved alongside it. This establishes practically matched recorded controls, not identical whole-world state or screenshot-exact sampling. The random player appearance differs. The +180/-180 Euler representation is equivalent, not a rotation mismatch.

Actual initial closed and restored-closed screenshots for both stages were opened and inspected. Hemisphere shading modestly separates rear sail/quarter shoulder and fender roll from the sides. The baseline merges more of these surfaces into flat red. Paint remains red with no obvious lookup-band seam, black crush or contact-shadow blotch at this camera distance, while the whole car still reads as a simplified model. Glass reflection differences are excluded from the paint judgment. No numerical likeness gain is inferred.

The fixed hemisphere run did not capture its intermediate open/lowered poses. Matching pose logs do not fill that visual gap, and the baseline-only lowered screenshot cannot establish an A/B. Only one rear-quarter direction/distance is covered. Rest-pose raised-panel brightness, near/far sampling and local/night lighting remain unverified natively. Parent normally exited and restored the frozen baseline at12:54UTC; this read-only comparison made no profile or UI changes.

The benefit supports a guarded current-source candidate, not promotion. `build/native-form-shading-cycle7/PRODUCTION-MODULE-PROPOSAL.md` specifies a small default-disabled generator helper with explicit original face-intent tags, protected semantic lookup bands and geometry/normal/weight/nonpaint invariants. It replaces experimental call-stack selection with deliberate source guards. No canonical implementation was made. Regenerate and test current220,498 geometry if pursuing it; never install this old214,322 FBX over newer form work. `FIXED-NATIVE-COMPARISON.md` records the complete comparison limits. Geometry likeness remains a separate open requirement.
