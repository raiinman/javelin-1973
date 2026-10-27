# Focused front-fender review

Current implementation checkpoint: canonical242911/b05b7b62 broadens the front outer roll while preserving the new SVG and all ten nonBody meshes. Four complete fresh comparisons and explicit bounded shading review are in `front-fender-form-cycle15.md`. The shape improvement is modest and the raised rail remains. The other chat finished its captures; all prior live states have recovery copies and the single retained Blender window visibly loads the current b05 source. Native visual review remains pending. Earlier research tables describe7985.

**Front fenders only.** Research/proposal on current 231,893-triangle canonical source, SHA-256 `7985de86a18e3e0df4b6d1ba0299487d8b27ba394173213a4d9998147e676167`. No geometry, model, profile or UI changes. Other areas remain paused. The proposal treats apparent breadth, height, fore-aft distribution and hood-to-fender graphic as one fender task, not a terminal-tip correction.

## Evidence and method

- **Target authority:** full `reference-2.png` and `reference-30.png`, frames of the supplied restored car. They establish its painted form and graphic identity, with uncalibrated perspective and strong studio reflections.
- **Supplemental construction/shape:** full `build/six-pass2/druk-000.jpg` and `druk-025.jpg`. Druk000 shows a front quarter; Druk025 exposes the hood seam, broad fender surface and pointed graphic return. Its vinyl roof, wheels, mirrors and equipment do not replace target identity. `reference-side.png` is an additional supplemental side photograph, not a target-video frame.
- **Actual current model:** `build/current-front-cycle11/body/report.json` identifies the exact current hash. Full fixed paint/clay frames cover both front quarters, side, top and fender close. Fresh `build/front-fender-focus/locked/` captures use the established frame2 balanced/contact-anchored and frame30 balanced cameras, including sensor36, HORIZONTAL fit, identical shift/roll equations and914x523 aspect. No camera was refitted.
- **Measured source:** `saved-fender-sections.json` contains eleven saved triangle-plane sections and actual decal support rays. Source functions identify crown triangles; all reported coordinates/heights come from loaded saved triangles, not sampling the analytic surface as a replacement. Coordinates are source metres, saved local Z plus .65.

Blender/img2blender plus explicitly installed `llm-blender-agent`, `cc-blender-toolkit` and `blender-studio` entrypoints were read, including vehicle-artist/proportion-blockout, multiview-fit-loop, backend and compatibility guidance. Their proportion, panel-flow and rigid-view comparison principles apply. No advertised Blender MCP was available; native background bpy was used. These are perspective photos, not calibrated orthographic templates. No bbox/IoU pass, recovered factory cross-section or numerical likeness score is claimed. Subsequent background calls use disable-autoexec. Earlier same-camera captures are retained as actual outputs, not rerun solely to change the command flag.

## Four complete fresh reviews

The initial four topical sheets were insufficient to count as four complete reviews. They are superseded by the following **four separately reopened full-frame sheets, each containing all four full references target2, target30, Druk000 and Druk025**. `complete-four-pass-inputs.json` records every file, size and hash. Each pass reviewed breadth, height, fore-aft shape and graphic together, without crops or registration.

1. [Complete pass1](../build/front-fender-focus/complete-pass1.png), all four references against fresh locked frame2/frame30 paint and clay. Target2/30 show broad raised shoulders continuing into the nose, rather than narrow separate rails above an otherwise broad hood plate. Druk000 confirms substantial outer quarter depth; Druk025 shows the graphic crossing the seam and ending in an extended outboard aft point. Current paint reads as two elevated bands around the hood, and clay retains their steep outer turn. The current black field reaches the fixed fenders but its short outboard return does not reproduce that longer pointed sweep. A total-body width change cannot be inferred from these different perspectives. Reflections amplify the defect but clay prevents treating it solely as paint.
2. [Complete pass2](../build/front-fender-focus/complete-pass2.png), all four references against both current front quarters in paint/clay. Rechecking target2/30 against Druk000/025 preserves the same combined conclusion: a broad shoulder with distributed rollover, a restrained high crown and a graphic that visually joins hood and fender. Both current sides carry the raised narrow-band reading through the middle/forward run; it is not just one terminal corner or one bad handed face. Druk's lower camera and different tires affect apparent stance and side depth, so this pass does not establish an absolute fender width or demand global height reduction. The seam and graphic must follow the corrected surface together.
3. [Complete pass3](../build/front-fender-focus/complete-pass3.png), all four references against current fender-close and top paint/clay. Target2/30 still require a strong shoulder, so flattening away the whole fender would lose identity. Druk000 supports its outer mass; Druk025 makes the long pointed black/fine-border return particularly clear. Current top clay shows a real transverse patch, not a literally millimetre-wide rail, while close clay shows how its high region turns steeply into the side. Current paint emphasizes hood-contained red fields and a blunted fixed-fender black return. This separates insufficient *apparent usable shoulder breadth* from simply insufficient total body width. Druk025 is uncalibrated and close; its point supports a silhouette/footprint correction, not an exact new XY coordinate.
4. [Complete pass4](../build/front-fender-focus/complete-pass4.png), all four references against the established contact-anchored frame2 alternative and full current side paint/clay, plus supplemental side reference. Changing between the two already locked frame2 solutions changes the severity of apparent breadth but leaves the high-band/steep-flank reading and short graphic return. Rechecking target30 and Druk000/025 still supports correcting the whole front run. Side clay shows that lowering the whole car, changing tires or editing only the extreme tip would not redistribute the measured transverse crown. Supplemental side stance and equipment differ and cannot authorize wheel/ride-height changes. Exact longitudinal crest heights remain inferred from photos.

## Actual saved crest, breadth and roll

[Actual transverse sections at fixed equal scales](../build/front-fender-focus/actual-transverse-sections.png) distinguish the full patch from its high region. Measurements below are **current model dimensions**, not factory target values. Hood edge is actual X=.700; fixed fender begins at X=.706. Peak breadth means the saved transverse span within the stated vertical distance below its own maximum, not the whole wing width.

| Y | Full crown patch width mm | Crest X m | Crest above hood edge mm | Breadth within10 /20mm of peak | Crest-to-outer-roll vertical drop mm |
| --- | ---: | ---: | ---: | ---: | ---: |
| .94 | 186.6 | .8643 | 30.8 | 99.7 /139.8 | 17.8 |
| 1.10 | 201.8 | .8509 | 47.7 | 105.3 /140.3 | 50.8 |
| 1.23 | 217.1 | .8337 | 48.0 | 119.0 /151.6 | 85.5 |
| 1.43 | 233.6 | .8151 | 41.8 | 134.0 /165.5 | 131.0 |
| 1.60 | 227.9 | .8135 | 43.6 | 130.3 /160.3 | 136.1 |
| 1.78 | 201.3 | .8170 | 52.9 | 109.6 /137.3 | 112.6 |
| 1.98 | 169.5 | .8156 | 46.5 | 90.8 /117.9 | 72.8 |
| 2.10 | 154.2 | .8178 | 30.3 | 90.1 /120.7 | 45.9 |
| 2.24 | 140.4 | .8021 | 13.1 | 107.0 /138.5 | 29.4 |
| 2.30 | 135.6 | .7814 | 4.3 | 126.9 /134.2 | 26.5 |
| 2.34 | 132.6 | .7560 | -.6 | 120.0 /131.0 | 25.7 |

At Y1.43 the crest is115mm outboard of the hood edge; the outer side boundary is X=.9396. Its131mm vertical fall occurs over about124mm lateral run. At Y1.60 the fall is136mm over120mm. The transition thus carries substantial vertical drop, while the upper surface rises42..53mm above the adjacent hood through the middle/forward run. This supports redistributing and modestly lowering the local upper section, not merely adding width to a tiny peak. The overall patch already has217..234mm of width around the axle region.

The full Body width including trim is1.918588m, about6mm over the dealer75.3in/1.91262m envelope and within the existing10mm regression. This is a factory overall-envelope check, not evidence that local curvature matches. Current hood top width is1.400m; neither the photos nor these sections establishes a factory hood width. Initial correction should retain hood edges and explore the available fender band before changing hood proportion. Source native-preview wheels remain at X±.77, front Y1.43, localZ-.32, unit scale. Their tire/equipment differences and perspective affect apparent mass but do not remove the measured crown-to-flank section. No wheel or global-height change is proposed.

The saved crown mirror check records actual right vertices and nearest reflected left vertices. Section measurements are not inferred from one flattering image.

## Decal span versus actual support

The fixed-fender graphic is present on both sides, with2,016 selected black faces and8,304 sampled centres/near-corners. All samples hit the actual red support. Vertical separation is.798..802mm and face/support normal dot is at least.999998. Hood graphic, after excluding the six raised vent tops, has154 selected faces and731 supported samples at.7999..8001mm vertical separation. These exclude unrelated black hardware and do not equate support with the correct outline.

The fixed-fender footprint spans |X|=.706..8661 and Y=2.0525..2.3760, including the fine border. Its current trailing boundary is a smooth short run, `2.08+.105*t+.015*sin(pi*t)`. Druk025 visibly has a longer, sharper outboard aft return continuous with the hood crossbar/fine border. The current supported artwork is therefore a footprint/design mismatch, not a missing decal or generally buried graphic. It should be evaluated across hood seam, crown and outer roll, not corrected only at the last few millimetres of the nose.

A small additional support limit matters during re-projection: the fixed +Z offset gives only.033mm perpendicular separation at the steepest sampled front-facing support. It remains positive. Preserve actual triangle seating and inspect those steep portions; do not assume .8mm vertical offset means .8mm normal clearance everywhere. This is secondary to the broad form/graphic correction, not a new unrelated task.

## Compact reference-gap table

| Fender feature | Current evidence | Required correction / limit |
| --- | --- | --- |
| Broad shoulder versus rail | All four full reference reviews; saved217..234mm patch but high band and86..136mm outer roll drop atY1.23..1.60 | Redistribute upper section and outer roll across the whole mid run; keep total envelope |
| Crown height relative to hood | Actual42..53mm excess atY1.43..1.78; narrow raised reading in both locked alternatives/clay | Lower excess local lift while sustaining broad shoulder identity; no global scaling |
| Fore-aft flow | Middle/forward raised run persists in profile and both quarters | Smooth supported changes along .79..2.34, not a tip-only patch |
| Hood-to-fender graphic | Correct triangle support, short/blunted outboard aft return versusDruk025 | Redesign continuous crossbar, fine border and pointed return on corrected support |
| Absolute photographed width/height | Perspective, wheel/stance/reflection differences | No claimed factory section recovery or camera-refitted pass |

## Prioritized fender-only trial proposal

The evidence supports the parent's planned **lower, broader upper-section trial plus its full hood-to-fender graphic correction**, as one focused area. First compare the form in clay with the existing graphic retained; then re-project a revised pointed return onto those same actual triangles. Review the resulting combined area before moving elsewhere.

1. Retain the actual hood edge, outer side join, total-width envelope, wheel arch, cowl/door joins and the accepted shared Y2.34 terminal profile. Apply a smooth compact longitudinal form weight over .79..2.34 with zero value and first derivative at both ends. Change the interior cross-section through Y1.10..2.10, especially1.23..1.78, rather than increasing global width or editing only the nose.
2. As **inferred trial controls, not recovered factory coordinates**, test reducing the cubic rise coefficient from .185 toward .130 at maximum weight, moving its inner upper control X from .755 toward .815, reducing that control's lift above hood from .050 toward .020, and increasing the breadth factor from .80 toward .90. These jointly lower excess lift and push the supported high surface outboard while preserving the seam and outer tangent. The intended10..25mm local lowering is a trial expectation; measure the actual result and reject new hollows, humps, rail edges or lost fullness.
3. Regenerate the fender surface, shared triangulation and graphic support together. Redesign the hood/fender crossbar and fine border to flow continuously across the fixed/moving seam into a sharper extended outboard aft return. Keep the central T identity, front red rim, native lamp apertures and hood clearance. The exact aft-point coordinate is inferred and must be checked against all four references, both sides and top, not copied from one perspective.
4. Compare saved crest X, height above the actual hood, full patch width,10/20mm breadth and complete transverse curves at the same eleven stations. Relative peak-width metrics alone can increase simply because a peak was lowered, so they are diagnostics, not acceptance. Retain the exact locked cameras and full unaligned frames. Accept only a visibly broader, lower coherent shoulder with the intended graphic span in target2/30, both quarters, top and side.

Preserve unrelated source/mesh arrays and all current runtime inputs. A shape-only Body trial should keep all ten nonBody full arrays exact; if graphic redesign requires hood artwork changes, separate that explicit semantic artwork delta from the unchanged hood support/rig and preserve its seam/sweep. Run actual saved support/normal checks, full pose/hood clearances, current unit/static/parser/import gates and independent visual review. Native appearance remains a separate parent-owned check. No passing script or earlier terminal repair closes the fender.

## DOX and limits

Only this document and ignored focused evidence were written. Owning AGENTS files already record front-fenders-only scope and need no additional contract/index change for this research. No reconstruction spec, model, package, camera-fit input, profile or UI was edited. Original source and all reference hashes were rechecked. All car sections remain open; work stays on the front fenders until the user is satisfied.

## Independent V01 form review

The parent supplied isolated V01, saved SHA-256 `ff4c656fbc7b0e7caddb80f1bf9b0d83e901ce4478724992694d681f3c9d3408`,231,893triangles. It is not canonical. [Fresh full-reference/V01 review](../build/front-fender-focus/v01-all-four-reference-review.png) reopens all four complete target2/30 and Druk000/025 images together with actual V01 locked frame2/frame30 paint/clay, fender-close paint/clay, side clay and top paint. `v01-review-inputs.json` retains the actual image hashes. The parent's full before/after `form-v01-comparison.png` was also viewed.

**Verdict: retain as a useful direction study; reject promotion as the resolved broad, muscular fender.** The outboard/breadth direction reduces the earlier narrow raised-rail reading. However, in locked clay and close clay the middle axle-region surface now reads too close to a flat extension of the hood while the run nearer the cowl retains a higher rounded hump. The result is uneven fore-aft suppression, rather than a uniformly strong broad shoulder. Target2/30 and Druk000/025 still support a sustained convex fender mass. Reducing a thin high rail must not remove that mass.

The parent's saved V01 sections quantify the concern: crest over hood drops from42/44mm to15/14mm atY1.43/1.60, whileY1.10/1.23 remains about42/34mm. Peak-relative10mm breadth grows134/130mm to164/161mm at the middle stations, but that metric improvement alone does not establish the right muscular volume. It is consistent with lowering a crest toward the hood plane. This review does not treat those numbers as recovered photographic target heights.

For the next form candidate, retain the broader outboard high-surface direction but moderate the middle lowering and smooth its strength along the fore-aft run. Do not restore a tall narrow crest, globally widen the body, or solve the imbalance with a flattering camera. Review the same complete sections and locked/full-quarter views for one sustained broad convex shoulder. The unchanged graphic remains short/blunted at the outboard aft return versusDruk025; it is still a required part of the focused combined correction after form selection. Its unchanged state is not by itself grounds to discard the geometric experiment.

This is an independent visual verdict only. Parent-owned source/pose/import/freeze results remain separate evidence. No V01 geometry or any canonical file was edited by this review; current visible canonical7985 remains untouched.
