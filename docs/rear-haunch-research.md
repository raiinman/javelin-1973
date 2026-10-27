# Rear haunch, deck and tail rollover research

Research-only review of combined 220,498-triangle source, SHA-256 `7e147b7d6fd1cc57f32b7c62936376b7f87e906e1f2185380e5bd8b13d0f091c`. The current cycle8 body report identifies this saved blend. Blender/img2blender review guidance and root/tools/assets DOX were reread. No source, model, profile, camera or native UI edits were made. No trial model was built. All sections remain open.

## Four fresh full-frame comparison groups

Original reference and model images were reopened, including the complete photographic frames. The sheets retain those full inputs, fitted uniformly at independent display scales, without crop, image alignment or camera adjustment. `build/rear-haunch-research/visual-inputs.json` records their exact paths, sizes and hashes.

1. **Side contour:** Druk005 against current side paint/clay and sail-close clay. [Full-frame sheet](../build/rear-haunch-research/01-side-contour.png). The photographed haunch has a broad rise and a flowing fall into the tail. The model has a short high shelf near the aft end of the sail, above/behind the rear wheel, followed by a more abrupt change near the deck junction. This persists in clay, so it is not solely red-paint reflection. Druk005 is near side-on, not calibrated orthographic. Its vinyl boundary, wheels and equipment are supplemental evidence, not target instructions. `side_top` is a construction boundary, not a measured photographed crest.
2. **Quarter rollover:** full Druk002 and Druk004 against current rear-quarter paint/clay. [Full-frame sheet](../build/rear-haunch-research/02-quarter-rollover.png). Both photographic sides support a broad convex shoulder flowing from sail to quarter and rolling into the tail. The model's sail-close transition is concentrated into a narrow bright/dark strip near the deck, with an angular trailing corner. The photographs also have genuine creases and panel seams; the objective is not to erase every reflected line. Their differing camera angles do not establish exact rear width or overhang length.
3. **Low flank and reflection:** full Druk032 against current sail-close paint/clay and top clay. [Full-frame sheet](../build/rear-haunch-research/03-low-flank.png). The low photograph demonstrates real outboard depth and curved vertical tail return beneath the long sail sweep. Current clay retains a discrete ledge where the upper quarter changes construction. Paint amplifies it. Top clay does not show an overall width failure and does not justify widening the entire rear quarter. Reflected trees/sky in Druk032 are not a depth map; the photograph is close, low and uncalibrated.
4. **Tail composition and target limits:** full Druk040 and target `reference-22.png` against current rear-quarter paint/clay. [Full-frame sheet](../build/rear-haunch-research/04-tail-limits.png). They establish the target's red tail, substantial rolled bumper and rounded lamp pockets. Current tail composition still looks rectangular, but these cropped-at-capture views do not establish the full haunch silhouette, rear overhang or a factory tail radius. Target22 cannot validate the proposed shoulder location. Lamp/bumper proportions remain an additional review item; do not scale the entire tail to fit these close photographs.

The strongest reference conclusion is broad continuous rollover, not a recovered contour coordinate. The saved-mesh findings below are stronger evidence for a localized construction repair than photographs are for global proportion changes.

## Saved geometry: overlapping owners create the shelf's hard reflection boundary

`build/rear-haunch-research/analyze_saved.py` opens the exact saved blend, verifies its hash before/after, reads geometry, and writes only research JSON. `saved-diagnosis.json` records face indices, original face-facing attributes, normals, actual first/second intersections and shared-edge adjacency. It never saves or alters the model.

In `tools/build_mod.py`, the loop headed **Close the wing tops between hood/deck and the muscular outer fender line** generates a planar deck-wing field for `TRUNK_REAR < midpointY < -1.72`. The later sail loop also generates `rear_quarter_surface` through Y=-1.87. Therefore Y=-1.72..-1.87 has two painted owners covering the same strip, between the side seam and the inner deck/sail edge.

Twenty-four saved-Body rays, from both outboard sides at four Y sections and three interior heights, each hit two red exterior-facing sheets. The first is the cubic sail (`J73SheetFacing=(side,0,1)`), the second is the older planar wing strip (zero authored target). Their measured lateral separation is **4.413..8.770 mm**. Example at Y=-1.80, sourceZ=0.927885 on the left: first hit X=-0.883647, face7965; second X=-0.877397, face4453. These are actual loaded-mesh hits, not only predicted analytic boundaries.

The redundant strip joins the same outer lower seam as the side and sail. The saved mesh has **24 triple-painted edges** there, all marked sharp. Actual side-versus-sail face angles are only **3.34..8.10 degrees**, consistent with their intended tangent roll. The extra planar face makes **38.58..58.13 degrees** against the side and **35.29..50.04 degrees** against the sail. The builder's `mesh.set_sharp_from_angle(35 degrees)` consequently encounters this three-face construction instead of an ordinary two-face tangent continuation. This is a concrete cause for a hard reflection line despite the cubic's analytic lower tangency.

This is not evidence of reversed normals: the sampled exterior hits face outward and use the same red semantic field. The shader and light direction change the prominence of the boundary, but do not create the two sheets or the triple edges. Disabling sharp edges or forcing custom normals would conceal the construction defect without repairing it.

## Additional geometric joins at the ends of the strip

The current fields do not use one exact upper boundary throughout the aft apron:

- Sail upper edge uses `upper_sail_x(y)` and `rear_roof_edge(y)`.
- The aft apron uses linear interpolation from `(X=.838,Y=-1.72,Z=.965)` to `(.850,-1.87,.940)`.
- The planar wing's inner `deck_edge` uses the same linear X progression but ends at **Z=.936**, not .940.

For example at Y=-1.80, sail upper edge is X=.8447005/Z=.9506730, while the apron linear edge is X=.8444000/Z=.9516667. Their roughly 1 mm discrepancy is small but not an exact shared seam. At Y=-1.87 the sail/apron anchor is Z=.940 and outgoing deck-wing inner anchor is Z=.936, a 4 mm height difference. Preserve the moving trunk's existing front seam rather than casually moving either boundary until they coincide.

There is a separate transverse mismatch at **TRUNK_REAR=-2.18092**. The forward deck-wing strip has a linear cross-section between side and inner lid-seam anchors. The aft tail `crown` resumes with an added `+.010*sin(pi*t)` vertical bow. Their endpoints agree, but intermediate profiles do not. Saved vertices at t=.25/.55/.80 match that aft crown exactly. Vertical differences from the forward profile are **7.071/9.877/5.878 mm**; nearest distances to the actual forward deck surface are **1.911/2.670/1.589 mm** on both sides. The smaller surface-normal distances matter because this is a steep transverse strip. Do not describe this as a 10 mm perpendicular hole. It is a confirmed noncoincident seam profile; actual sightline leakage through that seam was not tested here.

This explains why merely rounding the tail silhouette or changing roof height would leave an angular local join. A future single shared cross-section must be used by both adjoining surface owners, preserving the inner seam and exterior anchors.

## Genuine longitudinal contour knees, separate from the overlap

Two analytic functions contain hard longitudinal slope changes:

| Function and location | dFunction/dY, rear side | dFunction/dY, front side | Cause |
| --- | ---: | ---: | --- |
| `shoulder`, Y=-1.70 | .315209 | .134654 | `-.130*max(0,(abs(y)-1.70)/.72)` |
| `side_top`, Y=-1.70 | .121172 | -.059385 | Inherits shoulder knee while rear-drop term is smooth |
| `width`, Y=-1.65 | .152071 | .094379 | `-.045*max(0,(abs(y)-1.65)/.78)` |

These are finite differences of the actual read-only source functions at 1-micrometre Y offsets. They are not photographed dimensions. `side_top` switches from rising to falling at its constructed Y=-1.70 peak. The cubic sail inherits its nonsmooth lower boundary and changing vertical control span. The span between sail top and `side_top` contracts from **75.6 mm at Y=-1.60** to **31.1 mm at -1.72**, then grows to **41.3 mm at -1.87**. This concentrates the transverse roll near the shelf. Simply adding stations cannot remove the underlying slope knee.

These real contour candidates should be reconsidered after the duplicate-sheet/sharp-boundary repair. The present bright shelf combines construction, sharp-edge splitting and profile distribution. It would be premature to attribute its entire appearance to a factory-shape error or to smooth all of `shoulder()` globally, which would also change the front.

## Strongest next isolated slice and exact constraints

The most defensible next slice is **one owned fixed rear-quarter/deck strip with exact shared boundaries**, before changing the overall haunch envelope:

1. Remove the redundant planar deck-wing coverage only in Y=-1.72..-1.87; keep the existing cubic sail there as the visible owner. Do not delete the required wing strip aft of -1.87 or the apron itself.
2. Make the aft apron's outer edge and this cubic sail use one sampled boundary. Keep lower-glass geometry, its supported perimeter, the 20 backlight longitudinal intervals and both end anchors. Any approximately 1 mm reconciliation must propagate to the apron underside/perimeter closure, not leave a second old surface.
3. Account explicitly for the 4 mm transition at Y=-1.87 while preserving trunk-front fit. Use a narrow local return or a shared transition surface after inspecting the saved hinge sweep. Deleting the duplicate alone is not a complete seam solution.
4. Reuse one transverse profile on both sides of TRUNK_REAR before reshaping its rearward continuation. Preserve its inner/outer anchors and the existing moving trunk/spoiler. A localized shared-profile connection is required; a pasted cover over the mismatched edges is not.

This is a proposal, not implemented geometry. Keep it distinct from a subsequent reference-driven local smoothing of the Y=-1.65/-1.70 knees. That later change must have zero position/derivative delta outside an explicitly bounded rear-only region; preserve factory bounds, wheel arches and all front functions. Photographs support broad rollover, not a specific added width or height. Do not use a more flattering camera, globally move the roof or rescale the rear overhang.

Required constraints for the future trial:

- Retain the approved quarter-window controls, all glass/divider/tip anchors, shared cubic and backlight support; preserve roof/cabin silhouette.
- Retain TAIL_SHORTEN=.11908, TRUNK_FRONT=-1.87, TRUNK_REAR=-2.18092, TAIL_FACE=-2.29492, native axle locations, body dimension bounds, door seams and cargo geometry.
- Preserve the front/rear moving lid seam anchors and positive trunk/spoiler thickness, all ten hinge fractions and wheel/steering clearances.
- Preserve lamp apertures, bezels, bumper and newly closed lower fascia corners. The current lower rear repair is separate from this upper-quarter defect.
- Preserve all ten nonBody mesh coordinate/topology/UV digests in a geometry-only Body trial. Retain the pedal/crest modules and all saved-mesh guards in the frozen source.
- Add a read-only saved-mesh guard that rejects the present double outward sheet and three-face outer seam, checks exact sampled apron/sail and deck/tail joins, and passes the replacement. Use actual ray hits/edge adjacency, nonempty sample counts and both sides. Preserve current lamp, cargo, crest, pedal, seat/headliner/backlight and wheel guards.
- Capture identical full side, both rear quarters, top, sail-close and locked target views in paint/clay, then run unit/static/native import/full pose. Native rear/side and moving-panel inspection remains a separate gate.

## Limits and DOX

Only this document and ignored research sheets/scripts/JSON/logs were written. Owning AGENTS files were intentionally left unchanged because this adds no durable contract or accepted model behavior. No new trial build, native inspection or shader experiment was performed. The geometry measurements establish construction defects, not final reference parity. All sections remain open.
