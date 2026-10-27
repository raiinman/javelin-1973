# Quarter-window perimeter trial

Isolated scope: `build/quarter-window-cycle8/`, exact frozen cycle7 blend `ee99eb2206df0c62ff121990f522f544c422105f10f3ff7848ae2bfceee76e75`, 218,034 triangles. Canonical source has since advanced independently; this trial uses the verified cycle7 checkpoint rather than live tools. Parent will compose any accepted minimal patch with later work. No canonical/UI/profile changes.

## Four fresh dedicated comparisons before editing

1. Reopened target `reference-2.png` and `reference-30.png` against cycle7 locked front paint/clay. The quarter opening is too oblique/occluded here to recover its aft radius or exact slope. These frames constrain retention of the target greenhouse and equipment, not the proposed perimeter dimensions. Local `reference-47.png` and `reference-53.png` are interior close views, not missing side-profile evidence. No useful additional target side video frame or local video was found.
2. Reopened the complete supplemental `reference-side.png` against cycle7 side paint/clay. This different car shows a distinct descending aft window edge with a rounded lower corner, rather than the model's oval cap. Retain this as supplemental form evidence; its wheels, pipes and spoiler are not target authority.
3. Reopened full Druk005 side photograph against the same side clay and sail-close clay. Its aft edge follows a relatively direct descent, while the lower border stays nearly at the beltline longer before turning into that descent. Model curvature is distributed across both borders, making the opening look teardrop-shaped. The photograph is not calibrated orthographic and cannot establish a factory coordinate.
4. Reopened complete Druk000 front quarter and Druk004 rear quarter against current front-quarter-opposite clay, rear-quarter clay and sail-close paint/clay. The same descending edge/lower-corner construction reads in both oblique photographic views. Current model's oval opening persists under opaque clay. Supplemental vinyl/reflections emphasize the boundary but are not instructions to add vinyl or move the whole roof.

## Proposed limited experiment

Retain the divider, upper/lower start anchors, quarter tip `(sourceY=-.95, sourceZ=1.025)`, shared cubic `rear_quarter_surface`, roof functions and all backlight longitudinal intervals. Change only intermediate upper/lower Z values in `quarter_controls`: upper run descends earlier, lower run stays near beltline longer, and its turn remains concentrated near the aft corner. Existing generation already shares these controls among glass, chrome and adjoining sail support. No new independent overlay or copied reference art is used.

Every intermediate value is an inferred reversible shape choice. This tests perimeter distribution within fixed anchors; it does not recover hidden structure or establish final window dimensions. Keep the original baseline, minimal patch, exact module hashes and before/after full views. All sections remain open.

## DOX

Root/tools/assets instructions and Blender/img2blender skills were reread. Only this record and ignored trial artifacts change; owning AGENTS contracts remain unchanged until parent promotion. Source checks and renders are distinct from native-game approval.

## Selected result and minimal promotion

The first variant is preserved as `iteration1.blend` / `iteration1.patch`. It began descending immediately after the divider and erased the reference's short upper run, producing an overly triangular opening. It is rejected. The selected second variant retains both first upper-control heights and adjusts only six intermediate Z values in the same two table lines. `proposal.patch` is the complete proposed canonical edit, not the isolated build wrapper or a replacement build_mod file.

Selected saved source: `build/quarter-window-cycle8/assets/Javelin73PC.blend`, SHA-256 `9d1ca0c1c1a5f40f59149e17639b39f950eacdafc184f30ef127e6a9a9821b26`, still 218,034 triangles. Expected triangle delta when composed with later pedal work is zero. The upper descent is clearer, the upper run remains, and the lower edge turns close to the retained tip. This is an incremental visual improvement suitable for parent review, not completion of the greenhouse.

The source still has the rear shoulder/deck shelf identified by the exterior audit. This patch does not attempt to repair that separate defect. Quarter-window exact aspect, corner radius and anchoring remain inferred because the useful side photos are supplemental, and camera projection is uncalibrated.

## Frozen inputs and preservation

All 60 files recorded by the cycle7 checkpoint were hash-verified before copying. Its build script includes the approved front breadth, rear-corner closure and door-crest modules. It also contains the callable rear/crest guards. It does not include the later pedal call. Required native Java/runtime verification auxiliaries absent that checkpoint were copied explicitly and recorded. Two unused later pedal modules were excluded from the trial. `inputs.json`, `final-inputs.json` and the new `checkpoint/checkpoint.json` distinguish old baseline input hashes from final trial inputs.

`quarter-check.json` verifies the ten other meshes are byte-exact in their coordinate, polygon-winding and UV data: both moving doors, both windows, Hood, Trunk, Windshield, RearGlass, Interior and Wheel. Body changes are confined to the quarter-aperture/support construction. Rebuilding Body introduces 94 nonlocal float-coordinate face-key variations, at most 0.0000001193 m, while preserving semantic assignment and cyclic winding within a 1-micrometre comparison tolerance. These are reported explicitly rather than claiming a completely identical Body outside the aperture.

Both quarter windows contain 44 semantic glass faces and a single unbranched 89-vertex perimeter. Every boundary vertex meets actual painted support exactly; actual chrome geometry lies within 6.468 mm of all boundary vertices (the authored rolled trim radius is 7 mm). All selected glass faces point outward. From the exposed glass interior, 300 actual saved-Body first-hit rays per side hit the selected outward glass. Samples within 14 mm of the perimeter are excluded because the rolled chrome intentionally covers that edge. These 600 rays do not claim to prove transparency/material behavior in the game.

## Render and verification evidence

Fresh before/after captures use the same framing, lights, projection and material mode. `before/body/` and `after/body/` contain 22 views each, including both front quarters, both rear quarters, side, top, sail close, fender close and the three existing estimated target views, in paint/clay. `before/camera-fit/` and `after/camera-fit/` add the same six balanced/contact-anchored locked-camera views. Camera parameters are retained in their source reports; no fit was changed. All 56 captures were visually inspected. Eight comparison sheets retain their complete render frames at display scale:

- [Side, top and both front quarters, paint](../build/quarter-window-cycle8/compare-silhouette-paint.png) and [clay](../build/quarter-window-cycle8/compare-silhouette-clay.png).
- [Sail close and both rear quarters, paint](../build/quarter-window-cycle8/compare-sail-paint.png) and [clay](../build/quarter-window-cycle8/compare-sail-clay.png).
- [Locked camera alternatives, paint](../build/quarter-window-cycle8/compare-locked-paint.png) and [clay](../build/quarter-window-cycle8/compare-locked-clay.png).
- [Remaining fixed diagnostic views, paint](../build/quarter-window-cycle8/compare-other-paint.png) and [clay](../build/quarter-window-cycle8/compare-other-clay.png).

The four research sheets retain full uncropped reference frames, including the borders in reference-side.png. They are comparison displays, not calibrated overlays. Source camera framing is unchanged between versions; opaque clay removes glass transparency and is interpreted accordingly.

Passing final checks: 33 unit tests (`unit.log`); static validator against the installed game, zero errors (`static.log`); native script/Lua parser (`syntax.log`); native FBX importer, eleven mesh nodes and three named clips (`import.log`); full saved-model pose (`pose-v2.log`); and dedicated aperture/support/scope verification (`quarter-check.log`). The pose run retains 4,182 rear-corner rays, 12,128 crest-support rays, 163,128 cargo visibility rays and 1,864 backlight visibility rays, with the existing lamp, seat, headliner, wheel/steering and ten-fraction moving-panel checks.

The source review covers seams, moving fits, normals/axes, intermediate clearance, underside/wheel-well preservation, seat/wheel/hinge registration, exposed surface visibility and reference shape/trim. Native alignment/playback remains untested for this trial; no source pass is labeled native visual approval. Parent must compose the minimal patch into the current source, rerun integrated gates and inspect native views before promoting acceptance. No canonical/profile/UI files were touched.
