# Roof hardware refinement

Canonical integration: root rebuilt the current quarter/manual-cabin source with the reviewed UV reacquisition, original hardware module and independent saved guard. Saved source is222,146triangles, SHA-256 `f13f3b43e1b4da9f5c8a88efec16cec8b5ff9e24deb920982ffb1aeddc318168`. Root36unit/static0/game5parser/native11mesh3clip/fullpose/roof gates pass, and all ten nonInterior saved field arrays exactly match the UV-fixed baseline. Current body/cabin captures and corrected69-input freeze are under `build/parity-cycle9/` (`roof-verified-inputs/` includes every local Python/Lua/Java verification dependency omitted from earlier freezes). Tools/assets contracts were updated; package/42 instructions and child indexes remain unchanged because gameplay interfaces and ownership did not change. The earlier native persistence stopline is cleared by the fresh220,498candidate reload; native inspection of this222,146roof revision is pending. All sections remain open.

Historical corrected62-input review candidate is the corrected pipeline trial `fixed-trial/assets/Javelin73PC.blend` (SHA-256 `3cffc0e51fe8ee4a8d4e6fa4b6592a47ca36ad261bcd1cf187f5bd6ef3ece6d8`). The original c14 trial and its roof-only patch are rejected because of unintended exterior corner-normal changes. Use the explicit pipeline patch and updated invariant proof below.

## Four fresh comparisons before modeling

Base is frozen220498 at `build/parity-cycle7/pedals/checkpoint`, SHA-256 `28cc299385332241a99c9b6195fc9ec2de5a0d99010e36c559785346c31dc62c`. Fresh baseline saved-source renders are in `build/roof-hardware-cycle8/before/`. Every source below was inspected full-size, and each of the four dedicated comparison sheets was also actually viewed before geometry changes.

1. `pre-comparison-1.png`: target47/53, exact220498 driver-eye and BaT048. Target crops show the manual knob/wheel and cloth, but no roof hardware. BaT048 visibly supplies two thin padded visors and a small rectangular mirror below the header. Current220498 has an uninterrupted upper windshield field without these silhouettes. No exact target visor pose or dimensions are recoverable.
2. `pre-comparison-2.png`: BaT048, exact headliner/open-door views and factory roof20-2. Factory text names sun visors and rear-view mirror as separate removable hardware. The current headliner and adjacent structure provide physical support candidates. Use original shallow padded panels with actual small support/pivot pieces, no modern roof console. Hidden fasteners and dimensions remain inferred.
3. `pre-comparison-3.png`: BaT062, Druk115, exact headliner and factory roof20-1. BaT dome is missing its lens, Druk shows the assembled shallow cream lens and bright rim. Preserve the model's assembled dome and Cardin ribbon surfaces. Druk's folded shoulder belt is visible but excluded from this slice. Neither image measures visor mounts.
4. `pre-comparison-4.png`: target47/53, exact whole cabin and BaT048, then full-size roof photographs rechecked. The current empty front ceiling is missing distinct small hardware. Add both visors neutral and stowed as explicitly authorized, retaining all surrounding cloth, dashboard, wheel/shifter and dome. BaT's uneven visor pose is not proof of the target's pose. Check whole-cabin scale and multiple viewpoints rather than reshaping to one estimate.

Source image URLs and factory page filenames are linked in `docs/manual-cabin-hardware-research.md`; this slice uses BaT048/062, Druk115, target47/53 and actual factory roof pages20-1/20-2. The hosted factory1973manual covers multiple AMC series. No dimensions are extracted from its generic illustrations. Capture cameras are fixed uncalibrated inspection views, not lens fits. A standalone origin wheel is hidden in these cabin captures because native wheel placement is separate; no saved geometry is changed by capture.


## Initial geometry trial, rejected for shading drift

Selected source: `build/roof-hardware-cycle8/assets/Javelin73PC.blend`,222146 triangles, SHA-256 `c14d6862c84d8630ddd4df840b65587dd4b579f01de7c93698a1c3424510c01c`. This adds1648 triangles to the frozen220498 base. Two small original stowed visors have rounded padded thickness, outer pivots, inner supports and roof-facing mounting plates. A separate rounded rectangular mirror has a shallow inset face, narrow dark frame, short metal stalk and small roof mount. There are no belts, modern console, new materials or unrelated cabin changes.

`tools/javelin_roof_hardware.py` is the only new generator module. The promotion patch adds one import and one call after the existing dome/steering build. The module receives the existing headliner surface/grid and seats its supports against those actual planar cells. Visor boards remain shallow planes with rolled edge thickness, rather than bending the cloth or adding raised patches to it. Both neutral stowed poses and all hidden support dimensions remain reconstruction choices.

The first version's open-ended helper tubes caused the existing headliner sheet selector to classify them as open roof sheets. The final version closes both ends of each support/stalk tube; the original headliner guard then passes unchanged. Mounts are seated1.5mm below the base fabric, preserving at least0.5mm to existing1mm-offset ribbons. The model's Cardin ribbons and assembled dome are preserved.

## Actual visual inspection

Final paint captures were inspected full-size in all four views, followed by neutral clay headliner and driver-eye views. `before/` and `after/` use identical fixed uncalibrated cameras and inspection fill. `capture.json` records the source hash and settings. The fill and material overrides are temporary capture state, never saved into the asset.

- `headliner-close.png`: two distinct dark padded panels occupy only the forward corners, with separate small mount/pivot silhouettes. The central lamp and long Cardin U remain clear. The tiny pale horizontal arcs higher in this upward full-cabin view are pre-existing seat-edge occlusion, also present in the baseline; they are not new roof parts.
- `driver-eye.png`: the mirror presents its rectangular face toward the driver, with its short stalk visible and a modest inward toe. Both stowed visor undersides remain above the windshield view. This is an estimated seated viewpoint, not an occupant ergonomic proof.
- `open-door.png`: source body/glass retained, both doors posed open. Visors stay beneath the header and mirror remains separate from pillar, glass, wheel and dashboard. This is a source pose, not native gameplay.
- `whole-cabin.png`: interior-only unaligned overview retains roof, dome, padding, manual pedals, wheel and shifter. The new hardware reads as small roof attachments. This view looks at the mirror's back, correctly distinct from its driver-facing inset.
- `headliner-close-clay.png` and `driver-eye-clay.png`: padding thickness, rounded outline, mirror rim and support gaps remain real volume without palette cues. Other clay views are also captured, but no unviewed image is represented as visual approval.

`visor-mirror-comparison.png` and `headliner-comparison.png` place actual frozen/selected full frames beside the supplemental photographs without alignment warps. The selected visors are evenly stowed per scope; BaT's asymmetric deployed angle is not copied. Visor outline, trim grain, fastener detail, exact mirror aspect/height and hidden pivots remain approximate. The mirror uses the existing neutral atlas metal colour as an original surface, not a promise of live reflected scenery in game.

## Saved geometry and clearance proof

`check_roof.py` reopens both saved files without rebuilding or saving. Its `roof-check.json` reports:

- All ten other vehicle meshes preserve exact rounded geometry and UV fingerprints. All47223 old Interior faces are retained within2micrometres. Four tiny rear-seat stitch faces differ by1micrometre in regenerated coordinate rounding, documented in `debug-compare.json`; there is no source edit to that section or visible reshaping. Do not describe the full Interior as bit-identical.
-728 added faces/866 added vertices, zero triangle intersections against the old Interior (including roof cloth/dome).
- Minimum actual new-vertex proximity to windshield54.688mm, each side window124.500mm and rear glass870.277mm. Current full pose gate separately clears moving doors and raised glass through ten hinge fractions.
- Ten visor sample rays require actual downward dark padding,12..21mm positive thickness and6..23mm ceiling gap above the board. Four mounting-plate rays require physical supports within6..9mm of the actual roof fabric. Four further span rays require the physical visor pivot/support rods between mounts and boards. Separate rays require the cabin-facing mirror surface and short stalk.

`guard-negative.json` verifies that the independent proposed guard rejects the frozen empty front ceiling and rejects removal of12 stalk faces in memory. No modified negative-test scene is saved. `saved_roof_guard.py` contains `check_saved_roof_hardware(atlas)` without any generator import, ready for the parent to integrate into the source placement gate. The guard checks meaningful surfaces, thickness and mounting features, not just triangle count.

## Current gate results

- `unit-v3.log`:33 current tests pass.
- `static-v3.log`: standard package check passes, zero errors.
- `import-v3.log`: installed native importer resolves11 meshes and three named clips; no game world is launched.
- `pose-v3.log`: full current frozen62-input saved-source gate passes unchanged, including308 closed-component windings, pedal support, rear corners, both door crests, front/rear lamp apertures, cargo lining, trunk backing, seat support, native attachment registration, wheel/steering clearance and ten moving-panel fractions.
- The existing headliner guard passes1584 cabin-side support rays at1mm and preserves all234 downward roof sheet faces. New hardware solids are not exempted from the general outward-volume checks.

No native visual inspection, visor movement, occupant head/leg clearance simulation or section closure is claimed. No model changes were made to compensate game lighting. These remain small original inferred attachments pending the parent's visual review and combined native inspection.

## Review and promotion files

- `build/roof-hardware-cycle8/proposal.patch`: the new module plus minimal import/call patch, no old dashboard replacement.
- `build/roof-hardware-cycle8/saved_roof_guard.py`: independent saved-mesh guard proposal.
- `build/roof-hardware-cycle8/assets/Javelin73PC.blend`: selected source; the matching FBX/animation/manifest remain in the trial's original folder layout.
- `build/roof-hardware-cycle8/build_trial.py`, `capture.py`, `input-hashes.json`, `final-inputs.json`: reproducible isolated build/capture and copied frozen input ledger.

Exact supplemental image sources: [BaT048 visor/mirror view](https://bringatrailer.com/wp-content/uploads/2022/08/20220626_145233-81419-scaled.jpg), [BaT062 headliner](https://bringatrailer.com/wp-content/uploads/2022/08/20220626_145814-81505-scaled.jpg), [Druk115 assembled dome/roof](https://cdn.dealeraccelerate.com/druk/1/890/152901/1920x1440/w/1973-amc-amk-javelin-pierre-cardin). Factory scans are pages20-1/20-2 of the [1973 roof chapter](https://www.amcjavelin.nl/all/javelinfo/Man_23_AMC_Domelight_Headlining_Vinylcovered_roof_Exterior_Decals.zip), not measured drawings of the target. Original video frames47/53 remain [target evidence](https://www.youtube.com/watch?v=ZpfnHMBiRvA) with the visibility limits stated above.

DOX closeout: root/tools/assets instructions and Blender/img2blender skills were re-read before editing. Only the authorized isolated folder and this report were changed. Canonical ownership/contracts remain unchanged, so AGENTS documents are intentionally unchanged; parent owns the promotion documentation pass. All sections remain open.


## Corner-normal blocker diagnosis and corrected pipeline

The independent review correctly blocked the c14 result. The original per-face geometry/UV fingerprint omitted corner normals and sharp-edge flags; its passing result was too narrow to establish unchanged exterior shading. Exact saved-data comparison reproduces722 changed Body corner normals (max component delta0.25936833024024963) and180 changed sharp-edge bits, while positions, topology, UVs, weights and material slots remain unchanged. Nine other non-Interior meshes are exact. This was not authorized exterior refinement.

The debugging-and-error-recovery skill was read and applied: preserve the rejected source, reproduce the failure, localize the cause, then add a meaningful regression before fixing. Blender's official [mode-switch memory-access documentation](https://docs.blender.org/api/current/info_gotchas_crashes.html), fetched through Context7, states mesh sub-data references including UV layers must be reacquired after edit-mode switches because the storage is reallocated.

`Part.object` created `uv` before edit-mode welding and used that cached RNA reference later to identify Body glass faces for sharp paint/glass boundaries. `stale-probe.py` preserves this path and stops immediately after selection. The stale selection contains88 faces, and the actual current UV layer also identifies88, but their symmetric difference is176 faces. Equal counts concealed completely different membership. `fresh-probe.py` reacquires the live layer after `mesh.update()` and reports88/88 with zero membership difference. The legacy baseline rebuild happened to match frozen shading in this run, confirming the stale reference's state-dependent behavior rather than proving that path safe.

The minimal explicit pipeline proposal, `pipeline-fix.patch`, adds only a comment, `mesh.update()` and `uv=mesh.uv_layers.active` inside the Body branch before reading UVs. This pipeline change is separate from the attachment module and import/call. It is proposed for parent review, not silently applied outside the isolated scope. `proposal-with-pipeline-fix.patch` contains both reviewed hunks plus the unchanged original roof module. The canonical tools remain untouched.

Both baseline and roof candidate were regenerated with this same fixed pipeline:

| Saved source | SHA-256 | Geometry |
| --- | --- | --- |
| `fixed-baseline/assets/Javelin73PC.blend` | `475004b4f6426df17369d27b9261f58024fac1f25c0361e35e3d69d1d504d1cf` |220498 triangles, no roof attachments |
| `fixed-trial/assets/Javelin73PC.blend` | `3cffc0e51fe8ee4a8d4e6fa4b6592a47ca36ad261bcd1cf187f5bd6ef3ece6d8` |222146 triangles, original attachments preserved |

`check_pipeline_invariants.py` and `pipeline-invariants.json` compare exact saved arrays, with no normal tolerance, across every non-Interior mesh: positions, ordered topology, loop vertex indices, every UV layer, skin weights and group names, material slots/indices, CORNER_NORMALS and sharp flags. Frozen28cc versus fixed-baseline has zero differing fields. Fixed-baseline versus fixed-trial also has zero differing fields. Thus this particular frozen base needs no accepted exterior-normal change to take the safe pipeline fix. The rejected c14 comparison remains a recorded failing regression rather than being replaced by the new result.

This proof applies only to the frozen62-input base. It does not generalize to a later quarter-window63-input source. Composition must first compare that exact current source to a fixed-UV-only rebuild of the same inputs, explicitly reporting any old shading changes; only then compare that fixed current baseline to the roof composition.

`pose-fixed.log` passes every existing current source gate unchanged; `import-fixed.log` passes native11mesh/three-clip import; `static-fixed.log` passes package validation (the redirected build generates common assets only, so the unchanged frozen42script/metadata tree was copied into the isolated package before validation); `roof-check-fixed.json` reruns the independent support, normals, thickness and glass clearance checks against the corrected saved candidate. Existing33unit success remains in `unit-v3.log`, and the new exact normal regression supplies the additional pipeline-specific proof.

Fresh corrected captures are in `fixed-after/`, with source hash in its capture manifest. The corrected driver-eye paint and headliner clay were inspected full-size; parent also reviewed these against full BaT048. The hardware design and original inferred pose limits remain unchanged. The original `after/` captures refer to rejected c14 and must not be used as evidence of fixed exterior shading.

DOX re-check: this diagnosis adds only authorized isolated build evidence/patches and updates this report. No canonical source, package, UI, profile, spec or owning AGENTS file was edited. Parent owns current-source composition and promotion. No native visual approval or section closure is claimed.


## Current64-input composition, cycle9

This isolated composition uses `build/parity-cycle9/runtime-checkpoint`, preserving its current quarter-window outline and new runtime helpers/tests. It applies only the reviewed UV reacquisition fix, unchanged original roof module/import/call, and independent roof guard/call. The canonical model, scripts, profile and UI were not edited. The earlier28cc baseline is not the authority for this composition.

| Role | Saved SHA-256 |
| --- | --- |
| Current7e source in runtime checkpoint | `7e147b7d6fd1cc57f32b7c62936376b7f87e906e1f2185380e5bd8b13d0f091c` |
| Parent-reviewed current UV-only baseline | `fb54617c43be4066ef044ebe013c59eafd6f15b1c85398aadbf21b281f36e2d3` |
| Composed roof source,222146 triangles | `6525b02c71decebb42e9199ee56c667b8c5a9ecffd21baf065794f12c6036217` |

The parent independently identified706 changed Body normals/176 sharp-edge bits in current7e versus its UV-only baseline, localized to the quarter glass/paint boundary. This composition compares to that explicitly reviewed current UV-only baseline, rather than disguising the pipeline repair as a roof-only change to7e.

`build/current-roof-cycle9/check_invariants.py` and `invariants.json` require identical explicit11vehicle object sets and exactly ten non-Interior entries. Every tested field carries its exact array length plus byte hash, including positions, ordered topology, loop indices, every UV layer, skin weights, material assignments, CORNER_NORMALS and sharp flags. Group/slot names and counts are compared directly. There is no zip truncation, normal tolerance or omitted Body exception. All ten non-Interior meshes match the current UV-only baseline exactly. `runtime-preservation.json` separately proves the checkpoint's prepare helper, three runtime test modules and Java test runner are byte-identical after composition.

Current results under `build/current-roof-cycle9/`:

- `unit.log`:36 tests pass, including new runtime helper tests.
- `static.log`: zero errors.
- `import.log`:11meshes/three named clips resolve through the installed native importer.
- `pose.log`: full current source pose gate passes, now also calling `check_saved_roof_hardware(atlas)`.
- `roof-check.json`:10visor surface/thickness/gap samples, four mounts, four pivot spans, mirror face/stalk, zero old-Interior intersections and unchanged54.688mm windshield/124.500mm side-glass new-vertex clearances. Four existing microscopic seat-stitch faces retain the documented1micrometre regeneration difference, not an exact Interior identity claim.
- `capture.log`, `before/`, `after/`: fresh identical-camera paint/clay headliner, driver-eye, open-door and whole-cabin captures against the actual current UV-only baseline. Final headliner/driver/open-door paint and clay plus whole-cabin paint were inspected full-size. Both original stowed visor boards and mirror remain physical, roof/dome/Cardin support is preserved, and no new obstruction or shape correction was introduced. Exact dimensions/poses and native appearance remain unresolved.

Promotion materials are split for review: `pipeline-fix.patch`, `roof-module-call.patch` and `guard.patch`. `roof-and-guard.patch` combines only the attachment/guard hunks after the UV fix. No whole old builder/dashboard replacement is required. Source outputs, matching FBX/animation and manifest are under this trial's original folder layout. `input-hashes.json` and `final-inputs.json` retain the checkpoint and trial input hashes.

Parent retains promotion authority and is waiting for its fresh native runtime-helper replay. Passing these isolated source gates does not complete that native test, establish occupant head clearance, provide live mirror reflection or close any roof/car section. DOX re-check finds no canonical ownership/contract change; nearest AGENTS files remain unchanged because this is still an isolated proposal and evidence update.
