# Front fender form, cycle15 independent four-review audit

## Scope and inspected version
Read-only research. No model, art, game package or UI changes. Current canonical blend SHA256 independently verified as `a617d127cf5da6f09603500081b75191d4250a7b7a2d74cf49c626689113846a`, matching the actual `build/front-decal-cycle14/new-drawing/redraw-v03/captures-v03/report.json` and locked render source record. This is the243,156-triangle clean-sheet decal checkpoint. Geometry is the previously promoted broader fender form; new artwork does not establish fender likeness.

Applied installed img2blender reference-analysis and visual-review guidance. Read the root, tools and assets DOX chain. All four full reference images were reopened and visually reviewed in EACH review below, with current model renders. These are four complete comparisons, not four topic headings standing in for one image inspection.

Reference paths used in every review:
- `reference-2.png`, target low front quarter.
- `reference-30.png`, target more frontal view.
- `build/six-pass2/druk-000.jpg`, supplemental low front/side quarter.
- `build/six-pass2/druk-025.jpg`, supplemental upper front/hood quarter.

Current render root: `build/front-decal-cycle14/new-drawing/redraw-v03/`. Cameras are estimates and studio illumination differs from the photographs. No cross-photo millimetres or numerical likeness percentage is justified. Druk is another car, useful for construction, not authority to change the target equipment or dark companion stripe.

## Complete review1
Model evidence reopened: `locked-v03/frame2-balanced-clay.png`, `locked-v03/frame30-balanced-clay.png`.

- Targetframe2: the near fender reads as a rounded mass flowing around the outer headlamp and into the wheel region. Its upper silhouette is a broad swell, not a separate tall rail pasted beside the hood. The current locked clay shows a more concentrated shoulder ridge along the outside of the hood seam, with a quick outer drop.
- Targetframe30: the same mass remains present in the less oblique view; it does not depend only on the near-side perspective. The current opposite crest can read as a narrow raised run. Camera differences prevent a numerical crown-height conclusion.
- Druk000: the upper wing and side above the wheel opening are one substantial rounded envelope. Its long side-facing reflection field supports a broader shoulder-to-flank transition. The current clay has a comparatively distinct narrow rounded top above a quieter side field.
- Druk025: the hood seam is inside the shoulder mass; outboard of it, the graphic crosses a rolling fender rather than a nearly immediate vertical drop. The current model has that construction in principle, but bends into the side over a concentrated lateral distance.

Finding: preserve overall width and the actual hood seam. Investigate distribution of transverse curvature first. Evidence does not justify uniformly raising either fender.

## Complete review2
All four full references reopened. Model evidence reopened: `captures-v03/fender-close-clay.png`, `captures-v03/front-quarter-opposite-clay.png`.

- Targetframe2: front termination is rounded and broad around the lamp. The current close clay sustains a long crest but approaches the nose as a conspicuous tapered lane. It needs a gentler volume transition, not a larger bumper or changed headlamp location.
- Targetframe30: both crowns retain muscular width toward the nose. The model's raised bands still appear relatively separate from the hood field. The view cannot distinguish exact sheet-metal section heights.
- Druk000: the side plane above the wheel is subtly swollen, with a long convex upper transition. Current opposite-quarter clay confirms the narrow ridge/quiet-side reading is bilateral, not only a mirror or lighting error.
- Druk025: the nearest fender has a generous rolling area between hood seam and outer flank. Current close clay retains a visible shoulder, but most of the turn is concentrated near its outboard edge. This is the most actionable common finding across the references.

Finding: a broader outer turn should be tested while keeping the upper field convex and continuous. Do not flatten the whole crown into a shelf, which would remove the volume visible in both target frames.

## Complete review3
All four full references reopened. Model evidence reopened: `captures-v03/top-paint.png`, `captures-v03/side-paint.png`, `locked-v03/frame30-balanced-paint.png`.

- Targetframe2: the new T improves identification, but the fender still needs to carry the graphic over actual broad curvature. The target's highlights alone cannot be copied as geometry.
- Targetframe30: the graphic's two outer returns clarify the wing tops. Current front paint remains narrow in the crest/outer-turn reading even with the new decal. Thus replacing artwork did not resolve the underlying form finding.
- Druk000: the fender crest rises through the wheel region and lowers toward the front. Current side paint already has a sustained arching longitudinal silhouette. A blanket longitudinal lift would exaggerate its rail character. Preserve that silhouette for the first transverse test.
- Druk025: plan placement of the graphic is distinct from transverse shoulder volume. Current top view shows no evidence that a uniform global width scale is the appropriate repair. It would disturb the known width envelope and hood anchors without isolating the defect.

Finding: do not widen the whole car, raise the whole fender, or redraw the new SVG again to disguise surface shape. Change the wing cross-section within its current endpoints and reproject the same artwork.

## Complete review4
All four full references reopened. Model evidence reopened: `captures-v03/fender-close-paint.png`, `captures-v03/fender-close-clay.png`, `captures-v03/front-quarter-opposite-paint.png`.

- Targetframe2: muscular fullness survives an oblique low view; a local tall crest alone is insufficient. Current paint gives a strong thin highlight at the shoulder, while clay shows that this is not purely an artwork boundary.
- Targetframe30: the near and far masses must be judged together. Current bilateral quarter captures indicate a symmetric form issue, not a one-side placement failure.
- Druk000: the broad upper-side transition connects visually with wheel-arch volume. Current arch lip is present and not the first feature to rescale, but the upper wing reads more like a narrow cap over a comparatively planar flank. Altering wheel size or ride height would not isolate this relationship.
- Druk025: the pointed return remains on a rolling sheet; the new longer return is useful as a curvature witness. Keep its XY drawing unchanged during the cross-section test so the effect comes from geometry. Current paint/clay pairs show smooth shading, so the next correction should not be another normals-only patch.

Counter-evidence and limit: the existing wing is no longer a flat rectangular panel. It has a sustained convex field, smooth crest and a formed nose. The recommendation is a bounded redistribution experiment, not a claim that these photographs recover the exact section or that every apparent narrowness is geometric. Camera fit remains a source of uncertainty.

## One recommended next geometry correction
Test a broader transverse outer roll, first preserving crown height and longitudinal silhouette. In `tools/javelin_fender_artist.py`, the current full-blend join is `inner + .72 * span`, leaving only .28 of the available wing span for the outer turn. This is source construction, not a measurement from the photographs.

For one isolated candidate:
- Change the available-span allocation `run` from `.72 * span` to approximately `.62 * span`, bounded to `.60..64` for this experiment. This moves the upper-field/outer-roll join modestly inboard and gives the outer turn more physical room without increasing maximum width.
- Retain `high=max(hood_z+.032, side_z+.012)`, current hood anchors, side endpoint/tangent, nose/cowl anchors and longitudinal endpoint fades initially. Do not combine a height change and width redistribution before seeing which change caused the result.
- Retain the existing C1 construction. If parameter reallocation is needed to sample the larger outer turn, start `cut` near `.40` rather than treating a sample-count change as the shape correction. Verify monotonic X, convex upper field and no overshoot into the hood or beyond the fixed outer endpoint.
- Keep the new SVG byte-identical. Regenerate its projection from the changed actual support triangles and transfer normals from the corresponding red support. Keep moving Hood ownership and its existing seam clearance.

This is a hypothesis to render and test, not an approved model change. A lower peak is not independently justified until the redistributed section is compared in the same locked clay and paint views. If the broader turn merely creates a bulb or weakens the muscle, reject it and retaina617.

## Candidate acceptance gates
Require a visibly broader shoulder-to-flank turn in both front quarters and close clay, while retaining the current front silhouette and smooth terminal taper. Reject a new flat shelf, a sharper ridge, detached hood rail, outer bulge beyond the factory envelope or lost arch clearance. Check actual wing section extrema and shared endpoints, saved-model artwork visibility/support, native mesh import and the existing hood/wheel/panel pose gates. Reuse fixed cameras and compare the full reference images again. A source check or nice decal does not close the fender section.

## DOX pass
Only this research record was added. Existing root/tools/assets instructions already require bounded front-fender work, preserved anchors/envelope, the new SVG and reference-first review. No stable ownership, workflow or child index changed, so AGENTS.md files are intentionally unchanged. All car sections remain open. No native-game appearance was inspected here.

## Implemented candidate and explicit review decision

Canonical source is242911triangles, SHA256 `b05b7b62a7146e494c5fc8b8c17157593e7dfdac92ac00620a8be01e4ff92572`. Four complete fresh reference comparisons led to one change: the upper-field allocation moves from.72 to.62 of available front-wing span, broadening the outer turn without enlarging overall width. The new SVG and all ten nonBody meshes, including Hood and its Javelin badge, remain exact. Actual saved sections show the main crest18..19mm inboard and approximately0.22..0.24mm lower. This is a small improvement; the long raised reading and terminal/arch fullness remain open.

The82-input frozen source at `build/front-fender-form-cycle15/verified-candidate-checkpoint/` passes42 tests, static validation, five native parsers,11mesh/3clip import, full saved pose, graphic/badge support and visibility, and15 artwork landmarks. Strict outside-front shading preservation FAILED and remains reported:518 corners belong to the mapped front terminal, while464 unrelated trim/cowl corners differ by at most0.004889degrees with coordinate drift below0.239micrometres. An unchanged control reproduces all eleven meshes exactly, so random rebuild noise is not established. Root explicitly accepted this hash-specific bounded difference after actual same-camera rear/front paint and clay review; no threshold was relaxed. See `build/front-fender-form-cycle15/acceptance-decision.json`.

Source/runtime promotion is recorded with backups in `build/front-fender-form-cycle15/promotion.json`. Game installation and native visual review remain pending. The other authorized chat completed its captures. At the user's request, all three live Blender states were saved as recovery copies under `build/window-cleanup-cycle15/`; redundant windows were closed and the single retained working window now visibly loads the checked b05 source. The authorized alignment chat froze a617 and keeps its separate STL inspection in ignored files; no donor geometry is included. All sections remain open and no numerical parity is claimed.

DOX closeout: controls changed within the existing Tools/Assets ownership and front-fender workflow. No new instruction boundary, gameplay contract or child index changed, so AGENTS.md files remain unchanged. Current reconstruction and verification records were updated.
