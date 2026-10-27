# Front crown and nose research

Research-only review, 18 October 2026. No geometry, source, package, profile or UI changes. All sections remain open. This is a proposed local construction trial, not a likeness score or native inspection.

## Exact inputs and method

The target evidence is the supplied video's full `reference-2.png` and `reference-30.png`. Supplemental photographs are the full `build/six-pass2/druk-000.jpg` and `druk-025.jpg`, freshly reopened at original resolution. Druk is a different restored car: its wheels, roof treatment, mirrors, grille/auxiliary equipment and graphic details do not override the target. Its visible sheet-metal continuity provides supporting evidence only. Ref30's open door/person prevents a closed-door judgment.

Current comparison inputs are the twenty existing paint/clay captures in `build/parity-cycle8/body` (saved blend SHA256 `7e147b7d6fd1cc57f32b7c62936376b7f87e906e1f2185380e5bd8b13d0f091c`) and `build/current-uv-cycle9/body` (fixed-UV saved blend `fb54617c43be4066ef044ebe013c59eafd6f15b1c85398aadbf21b281f36e2d3`). The two report camera arrays compare exactly equal. No camera was refitted, reference warped, body scaled, or height measured from photo pixels. Target camera estimates remain explicitly uncalibrated. The saved geometry probe opens only the fixed-UV blend and does not save it.

Four complete fresh comparison groups are recorded below. Each sheet contains **all four full references**, then the selected 7e paint/clay and fixed-UV paint/clay pair. Original-resolution photos and the eight fixed-UV individual images were also inspected separately. The contact sheets preserve full frames with uniform fitting and padding. `build/front-nose-research/inputs.json` records all image hashes and both original camera reports; `compare.py` reproduces the sheets and source calculations. Source-station values are generator coordinates in metres. Saved Body coordinates subtract0.65m from source Z.

## Group1: target-frame2 estimate, complete evidence set

Sheet: [target-frame2-estimate-comparison.png](../build/front-nose-research/target-frame2-estimate-comparison.png).

Ref2 shows rounded shoulders flowing toward a curved upper outer-lamp surround, with a shallow rolled change into the front assembly rather than two distinct domes stopped behind a straight plate. Ref30 supports that reading from a second target frame despite changed framing and the open door. Druk000 provides a longer side-to-front context: the broad wheel shoulder continues into a substantial nose end. Druk025 resolves the painted sheet wrapping over the outboard headlamp corner, alongside the hood seam and stripe crossing.

Both saved variants still read as broad raised wings that run into a relatively straight, narrow leading platform. Paint makes the diagonal outboard graphic edge conspicuous, but opaque clay retains the flattening at the last wing run. The fixed-UV version does not resolve this front shape. Camera mismatch prevents an exact target crest height or nose depth deduction; this group establishes a continuity concern, not a dimension correction.

## Group2: target-frame30 estimate, complete evidence set

Sheet: [target-frame30-estimate-comparison.png](../build/front-nose-research/target-frame30-estimate-comparison.png).

Ref30 again has a full rounded lamp-end cap beneath the fender, and Ref2 prevents reading its near headlamp alone as a different overall width. Druk000 supports sustained front-wing fullness, while Druk025 shows the graphic riding an already rounded support rather than creating its shape. All four references were reviewed again against both source versions in this lower, more frontal estimate.

The model's broad crest is useful, but its final descent converges quickly into an almost straight front edge. In clay, the outer raised run loses identity before reaching the lamp-end surround. The same concern survives the different locked camera, so it is not justified to cure it by shortening the hood or raising the entire fender. The frontal estimate cannot distinguish a few millimetres of local height from perspective, and the target's lamp reflections are not direct body-normal measurements.

## Group3: full front quarter, complete evidence set

Sheet: [front-quarter-comparison.png](../build/front-nose-research/front-quarter-comparison.png).

Ref2/30 retain the target's black T graphic and auxiliary lamp/badge assembly as identity authority. Druk000 supplies the clearest broad front-flank progression in this set; its chrome bumper and wheel equipment differ. Druk025 confirms that the upper nose corner curves across the fender-to-front change. Compared again with the complete model quarter in paint and clay, both 7e and fixed-UV show a dome behind a comparatively thin terminal cap. Clay preserves the wing-to-nose mismatch even with the black graphic removed from the visual explanation.

This whole-car view is also the constraint against a local fix becoming a swollen front wing. The existing shoulder and forward hood run already have substantial volume. Preserve the cowl, axle, overall length/width and long hood identity. The reference and orthographic model have different perspective, so their apparent front overhangs cannot be compared as measured lengths.

## Group4: close fender support, complete evidence set

Sheet: [fender-close-comparison.png](../build/front-nose-research/fender-close-comparison.png).

Ref2 and Ref30 show the target front graphic turning around the nose/lamp-end assembly. Druk000 keeps that feature in whole-wing context; Druk025 exposes the near hood seam, narrow painted/trim margin and rolled outboard sheet at much greater resolution. All four were freshly reviewed against each model's close paint/clay image.

The close model confirms an outboard crown that narrows and folds inward near the graphic's front end; the leading support then becomes a short near-planar strip. The target and supplemental photographs support a smoother transition around the upper lamp end. They do not establish a factory radius. Reflections and paint graphics amplify the difference, but their absence in clay does not remove it. A new graphic alone would conceal rather than correct this remaining shape concern.

## Measured construction, separate from visual interpretation

`construction.json` evaluates the exact frozen fixed-UV source functions without running the generator. `probe_saved.py` independently reads the saved Body mesh; `saved-mesh.json` records its hash, actual stations, saved vertices and local face/corner normals. The first diagnostic invocation used the wrong object name and failed before measurement; the corrected probe uses `J73Mesh_Body` and exits successfully. No blend was written.

- The actual last crown stations are Y2.19083,2.25,2.29042,2.39. There is **no crown row at the hood's Y2.34 end**, so the moving hood and adjacent fixed wing use different longitudinal sampling near this junction.
- At the actual21 transverse samples, the saved crown maximum is approximately `(X.804516,Z.825178)` atY2.19083, `(.793560,.804476)` at2.25, `(.756851,.793254)` at2.29042, and `(.706000,.781566)` at2.39. Across the last99.58mm interval, the highest sampled point shifts50.85mm inward and becomes the inner endpoint. This is a measured collapse of the crown's transverse maximum, not a measured defect height relative to the real car.
- AtY2.39 the source side/top boundary isZ.751142 while the hood-side wing endpoint isZ.781566. The fullness expression fades exactly to zero there. The final section is consequently an inward-rising return instead of a sustained outer crown. The saved vertices agree with evaluated actual-row samples within3.8micrometres across the probed forward run, allowing for rounded Y station reporting.
- `front_fender_point` derives a transverse cubic from `side_top`, `side_x`, `hood_base`, a fixed inner endpointX.706 and a fullness fade. Its breadth term also fades out. This construction does not impose a shared longitudinal tangent with the upper lamp-end contour. Dense transverse sampling does not supply that missing end condition.
- The hood ends atY2.34 andX+/-.700. The fixed nose strip runs from that edge throughY2.385 to a straight line atY2.399,Z.790 across its entire width. AtX.7 its final hood chord slope is-.13010 and fixed-strip slope is+.01755, a chord-angle change of8.42degrees. AtX0 the change is only-.61degrees; this specifically implicates the outboard transition rather than the whole hood centre. These are source chord angles, not claimed custom-normal discontinuities or recovered real-car slopes.
- The front module separately bows its fascia depth as `2.447-.046*(abs(X)/.84)^2`, with real outer-lamp apertures centredX+/-.708,Z.641,radius.122. The wing, straight fixed upper strip and bowed lamp field therefore have independent constructions. Their existence alone does not prove a hole or collision; any revised connecting patch needs saved-mesh rays and clearance tests.
- The current-UV independent review already established that its706 changed corner normals and176 sharp bits are localized to the rear glass/paint classification. That fix does not move vertices, and the paired front captures show no new front correction. No evidence here establishes broken native front normals. The probe retains actual near-nose face/corner vectors for a future tangent comparison; it is not a complete edge-continuity certificate.

The **hypothesis** supported by these measurements and four visual groups is that forced end-fade and unrelated wing/upper-strip/lamp-end constraints make the final crown lose its broad identity too early. The photos do not determine a unique replacement radius, amount of height change or station position. A prescribed global height increase would exceed the evidence.

## Smallest next original slice

Prepare one isolated trial of the fixed front-wing terminal roll, approximately sourceY2.10..2.399 and both outboard sides, leaving the existing main crest and all geometry aft of the blend start unchanged. Begin with unchanged hood skin, seam anchorsX+/-.700/Y2.34, centre nose edge, lamps/aperture/recess/bezels, bumper, valance, axle and factory envelope. Fit the terminal wing with shared stations and longitudinal tangents into the existing upper lamp-end boundary, rather than allowing transverse fullness simply to vanish atY2.39. Add the hood-end station to the adjacent fixed wing sampling and evaluate whether redistributing the last roll is sufficient. Adding samples by itself is not a shape fix.

First keep the moving hood and central fixed nose strip unchanged to isolate the effect. If a coherent outboard roll cannot seat against the existing fixed strip, record that boundary conflict and propose a second bounded change to only the outboard strip; do not silently reshape the hood. Retain a visible panel seam rather than forcing tangent continuity across an intentional moving seam. Preserve both lamp apertures and their true recession, not just the outline seen from one camera.

Regenerate fender decals against the **actual revised support triangles** using the existing shared `FENDER_T`/station path and0.8mm seating. No independent graphic lift or old decal support can count as the shape repair. Preserve all original mask/material semantics and alpha. Do not adopt Druk equipment, expand global width, raise all fenders, shorten the hood, alter ride height or move the axle.

For acceptance, rerender these exact camera reports in paint and clay plus opposite quarter, side and top. Compare the full four-reference set again. Require saved front end rays on both sides, lamp aperture/recess guards, hood seam and ten-fraction motion clearance, decal actual-surface support, outward normals/positive axes, envelope/axle invariants, native11mesh/3clip import and the full current pose/static suite. Native both quarters/front/top under logged heading/camera/lighting remain required. Ambient1 with zero local lights can hide diffuse normal effects, so it cannot independently validate the proposed curvature. No current trial or gate closes the nose section.

## DOX closeout and limits

Written only this root-owned research record and ignored `build/front-nose-research` evidence/scripts. Root and tools contracts were reread. AGENTS files remain unchanged because this adds no accepted workflow, ownership, geometry or production behavior. Existing source/native results are identified as prior evidence; no native check was performed for this research-only review. The four groups are full evidence-set comparisons, not four topic labels standing in for four reviews.
