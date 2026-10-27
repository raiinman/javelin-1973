# Cycle 3 fresh visual audit

Read-only geometry review, 2026-10-18. Four fresh comparisons of the current cycle 3 renders were performed with vision. The body and interior reports both identify saved source SHA-256 `2cf24956ef2b112398a3788cf35802033686964bcdcf610b4735cd5e40616e2a`. This is a visual audit of those actual images, not a source-count assessment or a native-game inspection. No fidelity percentage or section acceptance is assigned.

## Comparison 1: front fender and nose against target video frame 2

- Candidate: `build/parity-cycle3/body/fender-close-paint.png`, checked again in `target-frame2-estimate-paint.png`.
- Evidence: original supplied `reference-2.png`.
- Visible finding: the candidate front face reads as a shallow rectangular grille sheet with separate large lamp rings attached at its ends. The target has a rounded, recessed black outer lamp surround and a grille perimeter that curves into the lamps and lower chrome surround. The candidate's straight lower bumper face and large cuboid overriders dominate the nose; the target bumper is a narrower chrome contour that bows and wraps around the face.
- Visible finding: target front fender shoulders roll into the nose, with the outer lamp enclosure sitting within that transition. The candidate ends its shoulders in relatively abrupt hard corners above and beside the lamps. The crown exists, but its termination at the fascia still reads as joined separate shapes.
- Limits: the close render looks down more steeply than the video. Hood length, windshield height, and fender crown amplitude cannot be corrected from this comparison without a fitted camera. Gloss intensity and the gray headlight appearance are material/light issues, not proof of incorrect depth.

## Comparison 2: full front envelope against target video frame 30

- Candidate: `build/parity-cycle3/body/target-frame30-estimate-paint.png`, with `side-clay.png` as an independent silhouette diagnostic.
- Evidence: original supplied `reference-30.png`.
- Visible finding: the target has a substantial red lower valance below its chrome bumper, with a curved lower contour and visible central depth. The candidate leaves a shallow dark/red strip below a thick horizontal bumper. This is a major missing volume relationship in the front identity.
- Visible finding: the target grille's lower boundary bows and its surround continues smoothly around the outer lamps. The candidate boundary is nearly straight across most of the nose, and the lamp housings make conspicuous polygonal outer corners. This persists in both estimated target views, so it is more than a single close-render highlight.
- Diagnostic finding: side clay shows a very sharp upward tail/spoiler tip, a roof-to-rear-glass run made of visibly straight segments, and a broad almost level door-side band. These remain review concerns, not diagnosed dimensional errors from frame 30, which does not expose them adequately.
- Limits: the candidate view is only an estimate and has a different pitch/framing. The relative hood, cabin and wheelbase dimensions are unresolved here. An open reference door cannot establish the candidate closed-door fit. Do not shorten the hood or change cabin height based solely on these two frames.

## Comparison 3: rear quarter surface against Druk detail photograph

- Candidate: `build/parity-cycle3/body/sail-close-paint.png`, cross-checked with `side-clay.png`.
- Evidence: `build/six-pass2/druk-032.jpg`.
- Visible finding: the photograph shows a broad convex rear quarter rolling from its upper shoulder into the wheel opening and rear lamp panel. The candidate quarter has a pronounced diagonal highlight/crease-like transition behind the quarter window, a nearly flat side band, and a sharp rear termination. Smooth shading alone has not produced the same continuous sheet-metal volume.
- Visible finding: the photo's lamp recesses have substantial inset depth and rounded walls; the candidate tail lamps read as shallow rectangular trim frames. The photograph also shows a bumper with strong corner wrap, while the visible candidate end remains block-like.
- Candidate-only finding: rear-glass perimeter, sail shoulder, and trunk joint meet in conspicuous angular wedges. These deserve an off-axis clay review before further trim work.
- Limits: Druk 032 is a low rear-quarter close-up, not a side elevation. It cannot determine roof height, quarter-window shape or rear-glass dimensions. Its black/chrome upper-quarter trim is a photographed configuration difference; do not add it to the supplied-video target without target evidence. Candidate angularity is visible, but an exact sail correction still needs a comparable target rear-quarter view.

## Comparison 4: seat and cockpit volumes against Druk interior photographs

- Candidate: `build/parity-cycle3/interior/front-seats.png` and `cockpit.png`.
- Evidence: `build/six-pass2/druk-140.jpg`, `druk-141.jpg`, and `druk-142.jpg`.
- Visible finding: the candidate front seats are thick rounded rectangular blocks with broad flat back faces and cushion tops. Druk 141 shows a thinner padded cushion with a crowned top, softer front falloff, piping, and shaped seam channels. The candidate stripe paths identify the theme but do not replace the missing upholstered form. Druk 140 confirms this shaped cushion relationship at cabin scale.
- Visible finding: the candidate dash is two broad horizontal blocks with a largely planar silver instrument face. Druk 140 shows a deep sculpted driver surround, rounded dash crown, tall central shoulder with its own vent, and a passenger grab handle projecting from the lower face. The candidate shifter is a straight ball-topped rod, while the Druk car has a tall open chrome loop and sculpted console.
- Visible finding: Druk 142 shows a carpeted passenger footwell rising into a curved toe-board and side kick panel. Candidate cockpit exposes a flat floor and simple vertical/support surfaces, without the same enclosing volume.
- Limits: Druk describes another photographed car, not automatic proof of every restored-video option. Confirm its selector and console against target interior frames before replacing those details. Camera angle and upholstery lighting differ, so do not derive seat width, recline angle or exact purple/pink values from the current pair. Seat crown, edge falloff and dash depth are clear form discrepancies even with those limits.

## Recommended next geometric section

Prioritize the **front fascia, lower valance and leading fender transition** as one connected section. It is strongly exposed in two original target frames, carries vehicle identity, and has visible volume defects that cannot be resolved with badges or paint.

1. Fit and record a target-frame camera using outer lamp centers, grille corners, hood leading edge, windshield corners and front tire contact points. Retain the full frame.
2. Rebuild the curved grille perimeter and recessed outer lamp pockets, the narrower wrapping bumper contour, and the red valance depth below it. Blend the leading fender shoulders into that front envelope.
3. Re-render fixed-camera clay and paint plus side and opposite front-quarter views. Check panel seams, mirrored surfaces, wheel opening registration and moving hood clearance after the shape change.
4. Preserve the seat, dash and rear-quarter findings as open work. A successful fascia pass must not imply those sections are resolved. Native alignment and surface visibility still require the separate game inspection.

## DOX pass

Root `AGENTS.md` owns this development evidence document. No `docs/AGENTS.md` exists. Root instructions were read before writing. Root and child instructions are intentionally unchanged because this records an audit under existing contracts and adds no workflow, ownership or structure boundary.

## Read-only implementation proposal after the four comparisons

Inspected `tools/javelin_front.py` and the front bumper/fender construction in `tools/build_mod.py`, under `tools/AGENTS.md`. No implementation changed.

- **Existing geometry matters:** `build_valance` already generates a closed curved lower nose from Z .280 to .520. The bumper already has a swept eight-point cross-section, about52mm high after scaling, and135mm rearward wrap at its extreme ends. `depth(x)` already bows the front46mm from center to X .84. The audit concerns their rendered relationships, not missing generator functions or zero curvature. Do not simply add another overlapping valance or bumper.
- **Remove occluding full-face caps locally:** `build_front` currently emits a single `body.face(front, 'shadow')` across the entire outer outline, a corresponding rear cap at Y2.345, and side returns. Both caps span the lamp positions. The black cylinders under the outer lamps are capped solids, not open recessed pockets. Replace the broad front field with explicit strips/cells that exclude both outer lamp apertures. Also exclude those aperture footprints from any rear field that would cut through the intended pocket. Build a connected recess wall around each opening and terminate it at its intended reflector/lens support. Do not leave a hidden coplanar full-face polygon behind the new detail.
- **Keep the lamp assembly as an assembly:** retain the existing rolled chrome profiles, then seat their outer perimeter at the new aperture mouth and their inner return against the recess. The outer headlamp centers are currently X +/-.708, Z .641. Lens crown Y2.457 is forward of the surrounding field near the lamp, not deeply recessed. Determine mouth, bezel, reflector and lens planes together from a fitted target comparison; do not push only the lens rearward until it vanishes behind the existing cylinder cap. Preserve separate `headlamp` semantic faces and their outward +Y orientation.
- **Use one sampled front surface:** promote the current scalar `depth(x)` into a common surface relation for the surround, central insert, rim returns, lamp mouths and bumper registration. The insert has an existing downward center at Z .500 versus its lower-side corners at Z .520, while the outer surround has its own independent lower contour. Fit those two boundary curves to the target rather than applying an arbitrary stronger bow. Tessellate the field and boundaries explicitly so their evaluated depth follows the chosen curve. Preserve original grille artwork, atlas UV continuity and the single material contract.
- **Blend the leading fender junction:** retain the current .706 hood-edge interface and existing crown away from the nose. Add shared nose stations between the front fascia's upper/outer contour and the last fender samples. Derive their joins from the same boundary points, with tangent continuity where the target shows a smooth roll. Keep the hood seam distinct and preserve its physical clearance and decal support. A whole-body width increase would violate the established factory envelope and would not solve the local termination.
- **Refine the existing bumper and valance together:** increase section sampling around the corner roll before changing its size. Fit the upper/lower chrome outlines and rubber overrider height/width against the fixed reference camera. Then alter the existing valance surface so the red area below the bumper has the visible target depth and lower curvature. Its present lower portion rolls rearward180mm, which can hide substantial surface behind the bumper from a low frontal camera. A visibility problem may require changing that roll, the bumper placement, or both, not increasing the valance height blindly.
- **Meaningful verification:** add saved-mesh ray checks through both outer lamp apertures, analogous in purpose to the existing rear-lamp gate. Rays through the visible lens region should reach the intended semantic lamp surface without first hitting the broad shadow field or an unrelated backing cap. Sample aperture rim/mouth continuity separately. Re-run factory bounds, normal orientation, hood sweep, native import and saved-model pose checks, then fixed-camera and off-axis clay/paint captures. Native game visibility remains required after export.

The source inspection narrows the first implementation slice to real outer lamp apertures and their shared surround. Freeze the current candidate before that edit; re-render it before adjusting the lower valance or fender crown, so a changed depth relationship remains attributable.
