# Rear haunch construction refinement

Canonical integration: the working source now has223,722triangles, SHA-256 `241f5745fb6718cb4aa593f8d6d142cde64e90eac25bda94be477fe3da9bddc3`. Root applied only the reviewed rear geometry/guard/fixture changes, preserving newer roof hardware and runtime helpers. Root36unit/static0/game5parser/native11mesh3clip/fullpose+rear/roof gates pass; all ten nonBody field arrays exactly match the previous roof source. Current captures and70-input checkpoint are under `build/parity-cycle10/`. Tools/assets contracts were updated; package/42 contracts and child indexes remain unchanged because runtime interfaces/ownership did not change. This revision is not installed or natively inspected. The broad shelf, contour knees and diagonal apron tangency remain open. Earlier isolated statuses below are historical evidence.

Isolated scope: `build/rear-haunch-cycle9/`. Frozen baseline is cycle8 220,498 triangles, SHA-256 `7e147b7d6fd1cc57f32b7c62936376b7f87e906e1f2185380e5bd8b13d0f091c`. No canonical/profile/UI changes. All sections remain open; native promotion remains with parent and its persistence-audit stopline.

## Evidence before implementation

Reopened all four full-frame groups in `build/rear-haunch-research/`: Druk005 versus current side/sail clay; Druk002/004 versus current rear paint/clay; Druk032 versus sail paint/clay/top; Druk040 and target22 versus the current tail. The complete evidence, photographic limits and actual saved-mesh diagnosis are in `rear-haunch-research.md`. The photographs support broad rollover; target22 cannot establish the haunch contour. This trial repairs verified ownership/seam faults, not the separate Y=-1.65/-1.70 contour knees.

The old saved mesh has two outward red sheets 4.413..8.770 mm apart in Y=-1.72..-1.87; 24 triple-painted sharp outer edges; different apron/sail boundary functions; and differing forward-deck/aft-tail transverse profiles. The proposed slice removes the duplicate sheet, shares the apron/sail edge, reconciles the retained moving-lid front fit locally, and gives the deck/tail join one sampled cross-section. No global shape or width function change is proposed.

## Explicit normals pipeline prerequisite

The independent roof agent identified stale UV RNA after edit-mode welding in `Part.object`. Reacquire `mesh.uv_layers.active` after `mesh.update()` in the final Body branch before its semantic glass sharp-edge selector. This is an explicit separate `pipeline.patch`, not a hidden shading adjustment. Rebuild an unchanged baseline with this fix and compare coordinates, topology, UVs, weights, material slots/indices, sharp flags and per-corner normals. The geometry patch is recorded separately. NonBody invariants must include Interior/pedals and both doors/crests, not just a coordinate digest.

## DOX

Root/tools/assets DOX and Blender/img2blender guidance apply. Only ignored trial artifacts and this record change. Owning contracts remain unchanged until parent reviews/promotes an implementation. Native appearance and persistence checks remain separate from source verification.

## Pipeline isolation result

The independent UV-only rebuild matches all eleven saved-mesh invariants of parent's fixed baseline `fb54617c43be4066ef044ebe013c59eafd6f15b1c85398aadbf21b281f36e2d3`. Its own blend hash is `7c00e0f5d5b1d0c2d0faab32806a4d6fd144490e4a41541ce75ca14662dbb7f1`, reflecting a separately saved file. Relative to raw7e, only Body's 706 corner normals and 176 sharp bits change. Localization records 166 false-to-true flags on actual glass/paint boundary edges and 10 true-to-false flags between red faces. Changed normals are 332 glass corners and 374 painted corners, on face centres in Y=-.973747..-.467650. Actual semantic glass selection remains 88 faces. See `baseline-pipeline-check.json`, `pipeline-localization.json` and `baseline-check.log`.

The geometry before/after images use this same corrected pipeline on both sides. The window sharp-edge correction is not counted as a haunch geometry improvement. No shading exception or normal override was added to conceal the four joins.

## Selected implementation

Saved candidate: `build/rear-haunch-cycle9/assets/Javelin73PC.blend`, SHA-256 `6e527017f96befc980a2492a52444044c80ad4c4dcfcb0434c1de9fd61cb149f`, **222,074 triangles**. Body has 93,772 triangles. The proposed geometry is only `proposal.patch`; `pipeline.patch` and `verification.patch` are separate.

- The wing strip now starts at TRUNK_FRONT=-1.87 rather than -1.72, leaving the existing cubic sail as the single visible owner forward of it.
- `rear_wing_point` begins with the existing sail's transverse cubic and transitions through the fixed wing band to the existing aft crown profile. Its outer side point remains unchanged. The fixed inner seam reconciles the former 4 mm height mismatch at -1.87, fading that change to zero over the first 50 mm aft. This local reconciliation is inferred construction, not recovered factory thickness. The moving lid remains exact and the full hinge sweep passes.
- The shared transverse sampling includes the original sail subdivisions and its quarter-tip fraction. The same sampling is applied to the adjoining aft crown so TRUNK_REAR has actual shared edges instead of two noncoincident profiles. The aft crown's analytic profile remains unchanged.
- The aft apron uses the same `upper_sail_x` / `rear_roof_edge` boundary and the corresponding shared Y rows. Its lower-glass support and 20 backlight longitudinal intervals remain unchanged. Its upper, backing and perimeter geometry are regenerated together.

`width`, `shoulder`, `side_top`, the roof/sail envelope and quarter controls are untouched. This does not smooth the separate longitudinal contour knees. Matching borders require more samples despite removing the duplicate strip. The actual saved-mesh triangle delta, including welding, is:

| Slice | Delta |
| --- | ---: |
| Removed duplicate wing strip | -48 |
| Remaining wing transverse subdivisions | +576 |
| Matching aft crown subdivisions | +168 |
| Apron upper shared rows | +432 |
| Apron backing/perimeter shared rows | +448 |
| Total | +1,576 |

`triangle-breakdown-saved.json` measures these families from the loaded meshes. Raw pre-weld grid counts are not substituted for saved triangle counts.

## Preservation and saved-surface guard

`invariants.json` verifies **all ten nonBody meshes are exact** against the pipeline-fixed baseline, including positions, polygon topology, loop vertices, UV layers, bone weights/group names, material slots/indices, sharp flags and per-corner normals. This includes the complete Interior/pedals, doors/crests, Hood, Trunk/spoiler, all four glass objects and Wheel. Body's changed face order makes an index-to-index corner-normal difference count inapplicable to locating Body changes; it is not presented as a body-wide shading change.

`tools/check_rear_haunch.py` provides the callable `check_rear_haunch_joins(atlas)`. It reads the currently loaded saved Body and has no file paths, writes, historical-baseline dependency or generator imports. It is wired next to the rear-corner guard in the isolated pose runner. Actual checks are:

- 24 fixed section probes, from both sides, require exactly one outward red sheet in the diagnosed overlap region.
- Outer seam edges require two painted neighbors and no sharp split from a redundant third face.
- Explicit nonempty shared-edge coverage checks the apron/sail edge and both front/rear transverse joins.

The old raw7e and UV-fixed baseline both reject. The selected candidate passes with shared-edge counts **outer12, apron12, front27, rear25 per side**, plus all 24 single-sheet rays. `guard.log` and `guard-report.json` retain the counterfactual and passing evidence. These are deliberate probes and complete expected edge-count coverage for this sampling, not a proof against every possible future arbitrary mesh defect.

## Visual review

Fresh before/after paint/clay captures use identical cameras, lights, framing and transforms. All 56 captures were inspected, including both front/rear quarters, full side/top, sail close, other diagnostic views and all six locked-camera alternatives. Eight full-frame sheets are retained:

- [Sail and both rear quarters, paint](../build/rear-haunch-cycle9/compare-sail-paint.png) and [clay](../build/rear-haunch-cycle9/compare-sail-clay.png).
- [Side/top and both front quarters, paint](../build/rear-haunch-cycle9/compare-silhouette-paint.png) and [clay](../build/rear-haunch-cycle9/compare-silhouette-clay.png).
- [Locked alternatives, paint](../build/rear-haunch-cycle9/compare-locked-paint.png) and [clay](../build/rear-haunch-cycle9/compare-locked-clay.png).
- [Other diagnostic views, paint](../build/rear-haunch-cycle9/compare-other-paint.png) and [clay](../build/rear-haunch-cycle9/compare-other-clay.png).

The rear-quarter/deck transition is visually cleaner in paint and clay, and the rear join no longer forms the same small broken termination. The side profile retains the broader shelf associated with the untouched longitudinal functions. A diagonal apron/sail reflection boundary remains because positional continuity alone does not establish transverse tangent continuity there. This trial does not claim to resolve the reference's complete rear haunch contour, roof identity, lamp/bumper proportions or native shading. It is a useful construction repair for independent review.

## Verification and promotion instructions

Passing: `pose-with-guard.log` (full saved pose, all ten hinge fractions, existing wheel/steering/lamp/cargo/backlight/crest/pedal/seat/headliner checks and the new join guard); `static.log` (zero errors against the installed game); `import.log` (eleven native mesh nodes and three clips); `unit-final36.log` (36 unit tests). Earlier intermediate unit logs contain the parent's then-unfixed iterator failure and the original fake-profile apron fixture error. They are superseded, not counted as passing evidence. The fixture now executes the real profile helpers and supplies its explicit sampling context, retaining its existing support-anchor assertions.

The parent's final runtime helper and regression were synchronized explicitly, with hashes in `runtime-inputs-final.json`: runtime_gameplay.lua `10191a65878ae90faffcc9d4b8c2c5b8e41c1498c1d49f23a9109e0675640856`; test_runtime_vehicle_set.py `993589ae71ef4f6673703f8cb76078280db98114a3f234e81f2a1db4b500f349`. They do not change this model's geometry.

After independent review, parent can apply `pipeline.patch` once if not already integrated, then `proposal.patch`, add `tools/check_rear_haunch.py`, and apply the two small verification call/fixture edits from `verification.patch`. Do not copy the whole trial build script or wrapper. Keep the parent's newer runtime changes. Rerun integrated gates, update nearest owning DOX and frozen inputs, then perform native rear/side and open-trunk review when the parent's persistence stopline is cleared. This trial does not authorize installation or bypass that stopline.

No canonical source/model/profile/UI mutations occurred. A read-only pose command was briefly launched from the wrong working directory; its newly created root log was immediately moved into this trial as `accidental-canonical-read-pose.log`, then the correct isolated runner was executed. It is not used as trial verification evidence. All sections remain open and no numerical parity is assigned.

## Current roof/runtime composition, cycle10

The reviewed rear construction repair is composed in isolation onto the canonical roof model, retaining the already integrated UV selector correction. Baseline is the corrected **69-input** `build/parity-cycle9/roof-verified-inputs/checkpoint.json`, blend SHA-256 `f13f3b43e1b4da9f5c8a88efec16cec8b5ff9e24deb920982ffb1aeddc318168`, 222,146 triangles. The completed isolated source is `build/current-rear-cycle10/assets/Javelin73PC.blend`, SHA-256 **`e9030e1d2100c669fdd110eb8eeb42df860c282c000847e8b502a5704c990f6d`**, **223,722 triangles**, the expected additive 1,576.

Only the reviewed rear geometry, new saved-mesh guard and its pose call, and the real-profile test fixture change are added. Existing roof hardware, quarter geometry, UV fix and runtime helpers remain present. `promotion.patch` contains exactly these four tool changes, with context regenerated against the verified current baseline. It does not include the earlier UV patch or replace the whole builder. The older verification patch required its fixture hunk to be applied to the newer `**kwargs` fixture context; the actual change remains loading real profiles and the explicit apron sampling rows.

`invariants.json` and `check_invariants.py` explicitly require the same complete eleven-object vehicle set and exactly ten nonBody objects. They compare every array length and hash, including positions, topology, loop vertices, every UV layer, vertex weights/group names, material slots/indices, corner normals and sharp bits. All ten nonBody objects are exact against the canonical roof baseline. This includes the entire Interior with visors, mirror, pedals and headliner, plus moving Trunk and Hood. This is current f13 preservation evidence, not an extrapolation from the earlier 28cc cabin baseline.

The corrected auxiliary files are present before the final test reruns: `runtime_gameplay.lua`, `InspectFbx.java` and `GameSyntaxCheck.java`. Their hashes match the parent's verified 69-input checkpoint in `verified-aux-inputs.json`. `verified69-differences.json` records only the three intended tool edits, source blend and three regenerated model outputs; all other baseline files are unchanged. `checkpoint/checkpoint.json` freezes all **70 inputs**, the verified 69 plus `tools/check_rear_haunch.py`, with their current hashes. All live input hashes were checked again after freezing.

Passing isolated logs under `build/current-rear-cycle10/`:

- `pose.log`: complete saved pose and intermediate hinge sweep, current roof guard, rear single-sheet/shared-edge guard, existing attachment/clearance checks. Rear coverage remains outer12/apron12/front27/rear25 per side and 24 single-sheet rays.
- `unit-final.log`: 36 tests pass after the auxiliary input hash record.
- `static.log`: zero errors.
- `import-final.log`: eleven mesh nodes and three named clips resolve through the installed native FBX importer.
- `syntax-final.log`: all five Lua/vehicle/model files parse through installed game classes. This is syntax evidence, not runtime behavior.
- `invariants.log`: ten exact nonBody meshes including corner normals and sharp flags, with explicit object sets and lengths.

Fresh full-frame before/after captures use the same canonical roof baseline and composed source, identical lighting/cameras and no refitting. All 56 actual frames were reviewed across the eight current comparison sheets: `compare-sail-paint.png`, `compare-sail-clay.png`, `compare-silhouette-paint.png`, `compare-silhouette-clay.png`, `compare-locked-paint.png`, `compare-locked-clay.png`, `compare-other-paint.png`, and `compare-other-clay.png`. Individual frames remain in `before/` and `after/`. Locked frame2 balanced/contact-anchored and frame30 balanced alternatives retain their established parameters and 914 by 523 framing.

The repaired rear join remains cleaner from both quarters and the sail close view. The broad side shelf and longitudinal contour knees remain; the diagonal apron/sail reflection boundary is still visible in paint and clay. Full side/top and front views show no new visible silhouette or trim displacement. This composition establishes preservation and the reviewed construction change, not complete haunch likeness or transverse tangent continuity.

No canonical source, package, profile or UI changes occurred. Native roof/rear appearance and animation inspection remain pending with the parent; importer success is not native scene review. Root owns promotion, integration DOX and native review. The DOX pass leaves owning AGENTS files unchanged because this isolated evidence adds no durable workflow boundary or contract. All sections remain open.
