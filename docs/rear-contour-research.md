# Rear contour research after the shared-join repair

Research only, on canonical **223,722 triangles**, saved source SHA-256 `241f5745fb6718cb4aa593f8d6d142cde64e90eac25bda94be477fe3da9bddc3`. `build/parity-cycle10/body/report.json` identifies this exact source. Root/tools/assets DOX and Blender/img2blender guidance were reread. Only this document and ignored `build/rear-contour-research/` evidence were written. No geometry, camera, shader, profile or native UI changes were made. All sections remain open.

## Four fresh full reference/model comparisons

All listed complete frames were opened again, then reviewed together in four new sheets. The sheets preserve uncropped inputs at independently fitted display scales, without image registration or camera adjustment. `visual-inputs.json` records every actual input path, size and hash. These are visual comparisons, not calibrated overlays.

1. **Longitudinal distribution:** [Druk005 and supplemental reference-side versus current side paint/clay and sail clay](../build/rear-contour-research/01-side-distribution.png). Both photographs show a broad rear-quarter volume whose fall flows toward the tail, with a genuine raised shoulder above the arch. Current clay still has a short high shelf at the aft sail/deck junction and a distinct change into its descending rear portion. The source repair improved construction without changing this larger distribution. The photographed black vinyl boundary is equipment/trim, not an edge to cut into the red target. `reference-side.png` is supplemental, not a frame of the restored video car. Wheels, ride height, mirrors and exhaust differ; do not import them. Neither photograph is calibrated orthographic.
2. **Volume from both rear quarters:** [Druk002/004 versus current rear paint/clay, sail paint and top clay](../build/rear-contour-research/02-quarter-volume.png). The photos support a convex quarter that carries its fullness down the flank and turns into the tail. They do not support treating the sail-to-apron line as a sharp diagonal ridge. Current paint and clay retain a narrow diagonal transition beside the lower backlight, while the broader upper flank remains shelf-like. Top clay does not justify widening the whole rear body. Genuine deck seams, chrome and the Druk vinyl edge remain distinct from continuous painted sheet. Opposite photographic perspectives are useful qualitative checks, not recovered cross-section coordinates.
3. **Transverse roll and tail return:** [Druk032/040 versus current sail paint/clay, rear clay and top clay](../build/rear-contour-research/03-transverse-boundary.png). Druk032 shows a substantial outward quarter volume and curved upper-to-flank transition, with a real rear corner return. The model still concentrates a visible change along the apron/sail construction boundary. Reflected trees and sky are not depth measurements. Druk040 mainly constrains the rolled crest, latch cup, lamp pockets and bumper; it cannot independently locate a haunch crest. Do not smooth away real rear seams or turn this into a lamp/bumper scaling task.
4. **Target authority and visibility limits:** [Target22/26/2/30 versus the exact current rear paint/clay and existing target-frame estimates](../build/rear-contour-research/04-target-equipment-limits.png). Target22 establishes the red rear panel, rounded lamp pockets and substantial chrome bumper; it excludes most of the haunch. Target26 is a crossfade with overlapping front/rear images and is unsuitable for measuring rear curvature. Target2/30 establish the target's front equipment, red body and painted roof identity, but hide the useful rear-quarter contours. They therefore constrain what must be preserved rather than prove a rear shoulder coordinate. The current front estimates remain uncalibrated and were not refitted. Druk's vinyl, equipment and photographed stance must not replace the restored target's identity.

The reference conclusion is broader continuous rollover with real seams. Exact hidden sheet thickness, crest location and local curvature radii remain inferred. The following saved-mesh measurements distinguish separate causes without pretending the photographs provide factory coordinates.

## Measured saved sections and normals

`analyze_saved.py` opens the exact canonical blend, checks its hash before and after, and never saves it. `saved-sections.json` retains actual triangle-plane sections at fifteen Y stations, outward surface rays at six fixed heights, face adjacency, sharp flags, face normals and per-corner normals. Coordinates below are source metres, saved local Z plus .65. Source formulas are recorded separately from actual saved triangle intersections.

[Equal-scale saved transverse sections](../build/rear-contour-research/saved-transverse-sections.png) show the shrinking roll band. Gaps in the forward diagrams omit untagged backlight-border faces; they are not diagnosed holes. [Longitudinal saved ray sections](../build/rear-contour-research/saved-longitudinal-sections.png) show the exterior at fixed heights, which can cross from one construction region into another. The Z=.98 samples include the backlight border, so their steep run is not a pure sail-curvature measurement.

| Y | Saved lower sail point X/Z | Saved upper sail point X/Z | Transverse span X / height Z |
| --- | --- | --- | --- |
| -1.52 | .921673 / .910767 | .809358 / 1.030000 | .112315 / .119233 |
| -1.65 | .910224 / .932232 | .829893 / .984172 | .080330 / .051939 |
| -1.70 | .903150 / .936170 | .835935 / .969737 | .067215 / .033567 |
| -1.80 | .890130 / .918556 | .844697 / .950685 | .045433 / .032130 |
| -1.85 | .883892 / .905018 | .848441 / .943128 | .035451 / .038110 |
| -1.87 | .881471 / .898732 | .850000 / .940000 | .031471 / .041268 |

These are model dimensions, not reference measurements. The roll onset rises aft while the roof/sail upper edge descends, pinching the vertical band around -1.70. Farther aft its transverse width keeps contracting. A broad curvature-distribution problem remains even if the two analytic knees are rounded.

### Outer join now behaves as intended

In Y=-1.50..-1.87, **66 actual outer sail/side shared edges** have exactly two incident faces. Face dihedral is **3.34..8.11 degrees**, sharp flags are zero, and corresponding corner normals agree (zero angular difference). The earlier duplicate outward strip is not the present explanation for the residual diagonal apron line. This measurement covers the identified region, not every Body edge.

### Apron/sail edge is positional continuity with a real transverse angle and backing branch

All **24 shared apron/sail edges**, twelve per side in Y=-1.72..-1.87, have **three total incident faces**: red sail, red apron, and the apron `redDark` perimeter return. The repair's guard deliberately requires two red neighbors and checks shared-edge coverage; it does not test total manifold adjacency or transverse tangency. Its passing result is valid within that narrower contract.

- Actual face dihedral: **22.71..45.43 degrees**.
- X/Z-projected transverse normal angle: **22.92..45.39 degrees**.
- Six sharp flags, in the aft rows from approximately Y=-1.8125 to -1.87.
- Actual corresponding corner-normal discontinuity: **22.85..46.60 degrees**, present even on the unflagged seam edges.

The extra backing return creates a nonmanifold exterior branch, consistent with persistent split normals even below the 35-degree sharp threshold. The angle between the actual red sheets is a separate geometric discontinuity. Turning off six flags or forcing averaged normals would leave both the angled cross-section and the three-face branch. The analysis does not claim a shader-only root cause or run a normal-override experiment.

The current apron aft of -1.72 is transversely flat, while `rear_quarter_surface` reaches its upper anchor with a finite sloping tangent. The current cubic solves X as a function of Z; matching a flat apron tangent requires a parametric section or a wider shared surface, not simply the old X(Z) derivative with a changed scalar. The shared upper anchor is an internal construction boundary, not established physical styling trim.

### Analytic knees are real but narrower findings

| Function / Y | Rear-side derivative | Front-side derivative |
| --- | ---: | ---: |
| `width`, -1.65 | .152071 | .094379 |
| `shoulder`, -1.70 | .315209 | .134654 |
| `side_top`, -1.70 | .121172 | -.059385 |

The `max` terms cause these discontinuities. In `side_top`, the sign reversal helps form a local high onset near -1.70. Saved tessellation spreads the effect over neighboring intervals; there is no exact factory-style crease at an authoritative -1.65 coordinate. Replacing only these terms with smooth ramps would leave the measured transverse apron angle, backing branch and pinched roll distribution. Conversely, repairing apron tangency would not settle the broader fore-aft shelf.

## Proposed next local slice

The next useful trial is a **jointly owned upper quarter/apron roll band**, with a separate knee-only control rebuild for diagnosis. Neither trial is implemented here.

1. Start with the current repaired source and preserve single painted ownership. Replace the apron/sail external branch with one continuous exterior patch. Route the apron underside into an inward backing network across the replacement band; do not retain a third wall attached at the visible shared edge, delete backing blindly, or hide a second overlapping exterior sheet. True openings and end closures still need positive thickness and culling coverage. A saved-edge guard must count *all* incident faces at this internal exterior join.
2. Use a parametric transverse X/Z curve, shared by both owners, or one shared patch from an unchanged lower flank attachment into an inboard apron attachment. Match position and first derivative at both ends and distribute curvature across the available band. The former `upper_sail_x` line can remain a sampling guide, but must not impose a visible kink. Preserve lower-glass perimeter and its exact supported points; changes beside the backlight must update its painted border coherently without moving the aperture.
3. Bound initial work to the upper rear flank/deck, approximately Y=-1.52 through TRUNK_REAR=-2.18092, with zero position and first-derivative delta at retained front/rear boundaries. Transition continuously through TRUNK_FRONT=-1.87. This span is an inferred trial boundary, not a factory station. Keep the side below the upper roll unchanged, including actual arch vertices. Do not widen the body or raise the roof to make the roll appear stronger.
4. Compare a knee-only rear-local fairing with the full roll-band trial using identical cameras. Apply a knee-only control as a height-localized upper-body delta that fades to zero above the arch lip, rather than changing `width()` at every height and moving the arch. Any smoothing of the upper width/shoulder traces must have compact support and leave their front functions exact. Judge whether longitudinal sections distribute the turn more evenly over -1.52..-1.87, rather than merely removing a slope jump at two values. Preserve the existing envelopes at the band boundaries; photographs do not establish a justified fixed millimetre displacement for its interior controls.

Hard boundaries for that trial:

- Factory Body length/width and native axle separation remain within existing regressions. Preserve wheel-arch lip and trim vertices, markers, 6mm door seam, rear jamb, quarter-glass controls/tip/divider, roof silhouette, backlight aperture and all twenty longitudinal intervals.
- Preserve TRUNK_FRONT=-1.87, TRUNK_REAR=-2.18092, TAIL_FACE=-2.29492 and the moving lid/spoiler's complete mesh. Internal fairing must respect both closed-lid seam anchors and the full hinge sweep.
- Preserve lamp apertures, lenses, bezels, lower rear corners, bumper, cargo liners and current roof/pedal/crest hardware. The tail composition discrepancies remain separate.
- Require explicit unchanged eleven-object set and all ten nonBody full arrays, including Interior, UVs, weights, material slots, corner normals and sharp flags. Retain all current frozen inputs and runtime helpers.
- Extend saved-mesh verification with nonempty both-side exterior two-face adjacency, actual triangle tangent/normal comparisons along the new join, outward single-sheet rays, positive backing separation and cavity/culling checks. Retain current rear, roof, headliner, glass, wheel and pose gates. Set a tangent tolerance from the chosen sampling, report its achieved maximum and inspect its convergence; do not substitute an invented likeness score.
- Reuse full side, both rear quarters, top, sail-close and existing locked camera alternatives in paint/clay, without per-trial camera fitting or lighting compensation. Run full current unit/static/parser/import/pose checks. Native rear/side and opening-trunk inspection remains a separate parent-owned gate.

The strongest immediate target is the diagnosed transverse angle/backing branch. A broader haunch trial must also demonstrate improved fore-aft distribution; fixing that join or smoothing the knees alone cannot be presented as resolving the complete rear contour.

## Limits and DOX

No trial build, source change or native game review was performed. The source hash remained exact after read-only measurement. This record adds research and a proposal, so owning AGENTS files and their indexes remain unchanged. Original source inputs, references and measurements are preserved under ignored research artifacts. Native current geometry remains pending with the parent. All sections remain open.
