# Isolated manual pedal refinement

## Result and scope

A reviewable original manual foot-control assembly is saved at `build/manual-cabin-cycle7/assets/Javelin73PC.blend`. It adds only separate clutch, brake, accelerator and far-left parking controls, their physical backing, tread and suspended support strips. The target wheel, manual shifter, dashboard, seats, roof and all exterior geometry are preserved. No canonical source, package, spec, UI or profile was edited.

Base: frozen214322, SHA-256 `c9c25499d084ded7bfe8910375247a9be5568f0c3235bce57166656dc01216c8`. Trial:216786 triangles, SHA-256 `961264f01524c55c08d1e68358cf76828df760e5c4cbd8f39ba28b19a2cea1cd`. The2464 added triangles belong to the Interior. All ten other vehicle meshes match the frozen geometry exactly, and every existing Interior face is preserved. This is an isolated source result, not approval of the whole cabin or native game appearance.

## Evidence used before modeling

The four fresh actual comparison passes are recorded in `docs/manual-cabin-hardware-research.md` and `build/manual-cabin-research/comparison-1.png` through `comparison-4.png`. Before creating geometry I re-opened the full BaT048, BaT053 and factory clutch5-2 images, then applied these findings:

- Pass1 retained target47's white manual ball and existing wheel, without introducing the supplemental Hurst lever or changing any Cardin trim.
- Pass2 governed this slice: [BaT048](https://bringatrailer.com/wp-content/uploads/2022/08/20220626_145233-81419-scaled.jpg) supplies the left-to-right parking/clutch/brake/accelerator distinction. [BaT053](https://bringatrailer.com/wp-content/uploads/2022/08/1973_amc_javelin-amx_20220926_130154-14067-scaled.jpg) corroborates the compact grooved pad and suspended arms, with wheel occlusion. The wide automatic brake from Druk140 was rejected.
- Pass3 kept roof belts, visors and dome outside this pedal-only change. No speculative roof feature was added.
- Pass4 required physical supports beneath the actual dash and visibility from more than one view, rather than floating pads in the cutaway floor. Druk142 remains passenger footwell context, not pedal authority.

The [1973 factory clutch chapter](https://www.amcjavelin.nl/all/javelinfo/Man_07_AMC_Clutch.zip), pages5-1/5-2, supports a suspended clutch and upper pivot/linkage principle. Pad dimensions, exact hidden pivot positions, support brackets and accelerator support remain explicit original reconstruction choices. They are not recovered manufacturing dimensions. BaT's worn/bare brake finish was not copied.

## Construction and correction

`tools/javelin_pedals.py` in the isolated trial reuses the existing `rounded_plate`, `box`, `cylinder` and `face` helpers. A local transform tilts each foot face aft/up. Clutch and brake remain compact separate rubber pads, accelerator is tall and narrow with lengthwise tread, and parking control is smaller and farther left. Each has a closed bent rectangular support strip continuing to an upper support plate against the existing lower-dash underside. All geometry stays in the fixed Interior mesh, using existing neutral atlas colours and one material slot.

The first render exposed lower arm bends crossing the front of the pads. V2 moves these spans behind the backing plates. The selected V2 images were inspected full-size: all pad faces remain distinct, supports now enter from behind, the driver wheel naturally occludes part of the pedals, and the assembly remains below the dash. The inferred arm bends are still somewhat angular and the generic tread does not establish the target's exact groove pattern. These are visible remaining detail limits, not hidden precision claims.

## Before/after visual review

The before and after folders contain matching full unaligned frames, with fixed camera positions/lenses, backface culling and identical12W local inspection fill. `capture.json` records source hashes, settings and view limits. Fill makes source surfaces inspectable and is not saved into the model or used to compensate geometry.

| View | Evidence and finding |
| --- | --- |
| `before/driver-seated.png`, `after/driver-seated.png` | Estimated seated driver camera. Real dash and wheel retained; pads partially hidden by the wheel, as expected from the reference. No occupant mesh or shoe envelope is included. |
| `before/open-door.png`, `after/open-door.png` | Actual source body, doors posed open and cabin retained. Four controls read beneath the lower ledge without crossing the door/sill. This is a source pose, not a game render. |
| `before/driver-footwell.png`, `after/driver-footwell.png` | Lower diagnostic camera clearly shows compact manual pads, separate small parking pad and tall accelerator. Front tread and suspended arms are geometry. |
| `before/whole-cabin.png`, `after/whole-cabin.png` | Same unaligned whole-cabin cutaway. Roof faces hidden in memory only. Pedal backs/supports are seen from the forward view; wheel, shifter, seats and surrounding geometry are unchanged. |
| `open-door-comparison.png`, `footwell-comparison.png` | BaT048/053 against actual frozen and selected renders. These are layout comparisons, not calibrated lens matches or dimensional measurements. |

## Verification

All results below concern the selected saved source and isolated output, with no installed-mod changes:

- `unit-v2.log`:32 existing units pass. Initial run found the copied checkpoint omitted `runtime_gameplay.lua`, a read-only test fixture dependency. Copying that existing file into the isolated tools directory resolved the failure; no runtime preparation or launch occurred.
- `static.log`: standard package validator passes, zero errors.
- `import-v2.log`: native importer resolves all11 meshes and the expected three clips. This uses the installed loader without a game world; it does not verify visual appearance.
- `pose-v2.log`: saved-model gate passes, including outward surface/component checks, attachments, wheels/steering, ten intermediate panel fractions, door/window motion and fixed Interior registration.
- `pedal-check.json`:12 actual foot-face rays require aft/up normals at dot>.985, plus positive face/backing thickness. Eight additional rays require upper/lower suspended-arm spans, and four require mounting plates. The checks inspect saved geometry independently of the generator.
- The selected assembly clears the existing floor by24.563mm. Across sampled added vertices outside intentional mounts, the nearest existing cabin surface is23.660mm away. A baseline-versus-added triangle-BVH overlap check finds no unexpected intersections with the existing dash, column, floor or seats.16 overlaps are confined to the four intended upper mounting seats against the dash underside. Existing full panel sweep separately clears the new fixed cabin geometry against moving doors.
- `guard-negative.json`: the proposed saved guard rejects the frozen pedal-free cabin and rejects removal of the clutch upper arm in memory (five faces). No mutated scene is saved.

The source geometry gate verifies normals and fit, not anatomical ergonomics, pedal travel or a linkage simulation. There is no pedal animation, shoe/leg mesh, calibrated target footwell camera or native visual inspection. Exact target dimensions and hidden pivot coordinates remain uncertain.

## Promotion materials

- `build/manual-cabin-cycle7/proposal.patch`: adds the73-line original module, one import and one builder call. It does not overwrite the surrounding builder or touch other sections.
- `build/manual-cabin-cycle7/saved_pedal_guard.py`: independent guard proposal. Parent can integrate `check_saved_pedals()` into the saved-model placement gate. It imports no generator and checks fixed expected locations, real facing, thickness and suspended support. The broader baseline-preservation/intersection proof remains in `check_pedals.py` with its JSON report.
- `build/manual-cabin-cycle7/build_trial.py`: reproducible isolated build, with inspection rendering performed separately by `capture.py`.
- `input-hashes.json`, `final-inputs.json`: frozen copied inputs and selected isolated tool hashes. Model FBX/animation and manifest are under the trial's original folder layout.

Parent owns composition and promotion. The combined canonical build must rerun its current gates after applying this slice. This trial intentionally uses the frozen c9 base and does not claim the newer combined result has passed.

DOX closeout: root/tools/assets instructions and Blender/img2blender skills were re-read. Only the authorized isolated trial and this report were changed. Stable canonical ownership/contracts are unchanged, so AGENTS documents are intentionally unchanged; promotion will need its owning documentation pass. All sections remain open.
