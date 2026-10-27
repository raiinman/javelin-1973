# Purpose
Cleanup of the user-supplied GPT Astra AMC 360-style engine V28 (model SHA-256 `bc73281f...6428`): removal of the front gloss "glob" shine, rebuilt fan blades and rebuilt exhaust manifolds, with before/after evidence.

# Ownership
- `DSI_Original_AMC360_Exterior_Engine_V28_ClaudeCleanup.blend`: the cleaned model (SHA-256 `d3ebb74b...2e29`). The original V28 file is the user's and is not stored or modified here.
- `compare/`: same-camera, same-lighting before/after sheets for every smoothing, shading or shape change.
- `verification/`: per-pass change logs plus per-object geometry/transform fingerprints of the original and the cleanup.
- Scripts: `../../tools/amc360_v28_cleanup/`.

# Local Contracts
- Keep scale, origin, fitting position and separate parts intact: all 199 objects keep identical world transforms, parents, scales and material slots. Root stays at the origin; the car fit applies (0, 1.35, -0.235).
- Only these mesh datablocks may differ from V28: `Fan_Blade_1..6` and `ExhaustManifold_{Left,Right}_CompleteCast`. Any further geometry change needs new before/after views.
- Never overwrite the user's V28; save cleanups as separately named files. Open supplied blends with scripts disabled.
- Changes: `Black_Enamel` to satin non-metallic (roughness 0.40), Bakelite roughness 0.50; angle-based sharp edges (36 degrees) on smooth parts; fan blades rebuilt from their own leading/trailing stations (9 spans by 4 chords, slight camber, softened tip, 2 mm thick); manifolds rebuilt as port pads seated on the ray-cast head face, four primaries sweeping 35 mm rearward into one boolean-fused, filleted log, and an outlet elbow from the log underside onto the existing outlet throat with an open bore.

# Work Guidance
- The manifolds touch only their heads (pad seats) and clear the alternator by a measured limit. A few tiny boolean slivers remain (5 right, 2 left) and two front junctions show a faint shading tick; neither is a gap or crossing.
- No car fit was rerun for the cleanup; the rebuilt manifolds stay within V28's original manifold envelope (|x| at most 0.395 m against 0.396 m).
- Total evaluated triangles: 46,490 (V28: 44,082). The increase is the denser blades and manifold fillets.

# Verification
- Run the passes in order with Blender 5.2.1 or the `bpy` module (`pass1_shading_materials.py`, `pass2_fan_blades.py`, `pass3_manifolds.py`, each taking `-- <in.blend> <out.blend> <log.json>`), then `compare_transforms.py`, `manifold_overlap.py` and `views.py`/`manifold_views.py` with `compose_before_after.py`.

# Child DOX Index
None.
