# Interior reference audit

All interior sections remain open. No likeness percentage is assigned. These are four fresh reference/model comparisons, captured from the saved source before corrective work. They do not replace the four complete webpage reviews in `six-source-four-analyses.md`.

## Evidence and limits

- Target video: https://www.youtube.com/watch?v=ZpfnHMBiRvA. Local `reference-47.png` establishes slotted metal wheel spoke, padded horn boss and white manual shift ball. `reference-53.png` establishes raised cream, pink and burgundy Cardin seams.
- Supplemental construction: [Druk gallery](https://www.drukautosales.com/vehicles/880/1973-amc-amk-javelin-pierre-cardin), local photographs `build/six-pass2/druk-105.jpg`, `107`, `109`, `115`, `117`, `118`, `119`, `121` through `131`, `136`, `140`, `141` and `144`. Exact photo URLs are indexed by number in `build/six-pass2/druk-evidence.json`. This car's automatic shifter and rectangular mirrors differ from the target and must not be copied as target equipment.
- Supplemental Cardin cabin visibility: `build/six-pass2/hagerty-042.jpg` and `hagerty-044.jpg`. Painted sport mirrors on that car are not the target mirrors.
- Saved-source baseline and cameras: `build/parity-audit-interior/report.json`, source SHA256 recorded there. Diagnostic cutaways hide body or headliner geometry in memory only. Cameras are uncalibrated, so visible categorical differences are stronger evidence than dimensional estimates.
- The installed `img2blender` and `blender` skills were read. The current library Blender skill was also checked at https://raw.githubusercontent.com/raiinman/skill-library/main/skills/3d-and-web/blender/SKILL.md.

## Comparison 1: front seating and Cardin upholstery

Compared target frame 53 and Druk 136/141 against fresh `front-seats.png` and `rear-seats.png` in the diagnostic folder.

- Blocking: model cushion bands run across the car. The photographed front cushion bands run lengthwise from the backrest toward the leading cushion edge. Reorient the projected ribbons while retaining original geometry, palette and supported front seat positions.
- Blocking: the current seatback reads as a narrow rectangular pad with a nearly straight top. The actual high back is fuller at the shoulders, with a pronounced rounded top and a deeper padded hip junction. Correct large contours before adding stitching.
- Model ribbon colour boundaries are crisp, flat sheets. Target seams are padded, with cream cloth visibly rising along each stitched edge. Add restrained cloth relief and piping after the pattern layout is corrected.
- Model cushion has five uniformly spaced black stitch lines. The photograph has broader panel breaks and a shaped transition near the seatback. Replace the generic divisions with reference-supported seams.
- Fine fabric response is unresolved. Studio smooth shading alone cannot establish cloth matching.

## Comparison 2: dashboard, wheel and console

Compared target frame 47, Druk 107/109/117/118/119/140 against fresh `cockpit.png` and the earlier close `build/cockpit-review/instruments.png`.

- Blocking: thin round wheel spokes form an upward Y. The target has broad flat drilled/slotted metal spokes and a black padded horn centre around its bright badge. Rebuild the wheel hub/spokes and inspect front and oblique views.
- Blocking: the panel is a straight narrow bar with three small protruding circular pods. Druk shows a much deeper curved instrument surround, three rounded-square apertures, a sculpted padded dash and a defined lower control ledge. Preserve target manual controls while rebuilding the fascia silhouette.
- Visible dashboard identity is missing: central radio/vent forms, glovebox, end vent and control levers. These require original geometry/artwork rather than copied photo texture.
- Static dial artwork lacks numbers and has generic identical markings. Druk's three dials have different fuel/temperature, speedometer and clock identities. First confirm target instrument configuration, then author the matching faces.
- The white ball is supported by target frame 47, but the tall straight rod and plain rectangular console are provisional. Do not replace them with Druk's automatic selector.

## Comparison 3: door panels

Compared Druk 105/106/133/134/138/139 against fresh `door-card.png`.

- Blocking: the model card is a rectangular slab; its armrest is a smooth oval pill. The reference has a shaped upper surround, a long pleated padded horizontal pull and a lower forward curl. Rebuild the large armrest/card volumes and rounded perimeter.
- The separate window crank is absent. The model's small release lever beside the top inset is not a substitute. Add the crank below and forward of the release plate, with a small black handle.
- Cardin top insert lacks the open PC crest and thin bright rounded perimeter seen in Druk 106. Author the crest at the observed position, retaining original artwork provenance.
- A small patterned forward trim wedge and detailed latch hardware are absent. Their sizes remain inferred until a target door shot is matched.
- Inspect both moving cards and the entire door swing after correction. An isolated card render does not establish motion clearance.

## Comparison 4: rear seating, headliner and cargo

Compared Druk 115/121-131/144 against fresh `rear-seats.png` and `headliner.png`.

- Blocking: the model has two separate rear bucket seats. Druk 144 shows one broad rear bench and backrest with continuous nested Cardin loops across the full width. Replace the rear pair with a bench while retaining the two native rear passenger support regions.
- The rear cushion graphic is a broad rounded loop around a dark central field, not two copies of the front transverse stripe. It needs a separate pattern path projected onto the bench cushion.
- The headliner model has one simple U loop. Druk 115 shows long roof-side ribbon runs turning across the ends, plus a central dome lamp and shoulder belt hardware. Their layout and bends need a dedicated overhead comparison; the current simple U cannot be accepted from correct colours alone.
- Cargo is represented by smooth dark boxes. Druk 121-131 show pressed wheel-house intrusions, shallow floor relief, weatherstrip, hinge/underside stamping and a spare. Target equipment and removable cargo must be distinguished before adding these details.
- Belts, buckles, seat base shells, rear quarter trim and parcel shelf detail remain visibly absent or generic. Front seat access/folding is not established by the current rigid geometry.

## Correction order and re-audit gate

1. Correct rear bench topology and front cushion stripe direction.
2. Rebuild wheel identity and dashboard volumes.
3. Shape door cards, pull handles and cranks.
4. Reconstruct headliner layout, roof hardware, belts and cabin/cargo transitions.
5. Recapture the same source cameras, plus assembled open-door and in-game views. Re-audit every feature against the original photos as an unapproved model, even if the previous iteration felt close to the requested threshold.

Categorical blockers above individually prevent a credible 90% interior claim. Mathematical checks prove support, orientation or clearance only. All sections remain open.

## DOX pass

This report is owned by the existing root documentation scope. It introduces no new directory ownership or child index. Source contract changes from the bench correction are coordinated by the root agent in the existing tools/assets contracts.

## Seat correction and skeptical review

`tools/javelin_seats.py` now generates two original front buckets and one 1.24m continuous rear bench. Front positions and dimensions remain unchanged. Both native rear support regions remain beneath the bench. The front cushion bands run fore/aft. The rear backrest has one broad inverted U and its cushion one continuous rounded loop. Ribbons still project onto the authored support triangles through the existing single-atlas interface.

Inspected new `build/parity-audit-interior/new-seats-quarter.png`, `new-bench.png` and `new-seat-top.png` against Druk 141/144. `seats-review.json` records generator hash and fixed cameras. This isolated diagnostic uses the actual project Part class and saved original atlas without rebuilding or modifying the shared source blend. Python compilation passes; assembled/native verification belongs to the root build.

The categorical arrangement and stripe direction are corrected, but the seats remain unapproved. A fresh critical review still finds a rectangular front shoulder/top, shallow generic padded bases, overly uniform rear back padding, flat ribbons without stitched relief, missing side shells/adjustment hardware, belts and buckles. The rear bench's precise width, corner taper and cloth drape remain inferred. Its cream border must be compared in an assembled open-door view so the body cannot conceal an incorrect fit. These findings remain blocking for the overall interior target, rather than being averaged away by the corrected seating arrangement.

## Four fresh dashboard comparisons before correction

The updated saved-source baseline is captured under `build/parity-audit-interior/dashboard-before/`, separately from the earlier seat baseline. The original video frame47 remains equipment authority; Druk's automatic selector is excluded.

1. **Druk107 versus saved cockpit overview:** the real raised driver hood occupies roughly the left three-fifths of the dashboard, with a separate broad, padded passenger face. The model's full-width thin silver strip erases this division. Correct the two principal volumes first; retain the current windshield clearance and steering location.
2. **Druk109 versus saved driver region and target47:** the fascia wraps around three deep rounded-square instrument mouths, with controls on a lower ledge. The model has circular pods pasted onto a straight bar. Build recessed rounded-square tunnels, a shallow transverse fascia bow and a separate control ledge. Target47 supports the new slotted wheel and manual white ball; do not move them to imitate Druk's automatic cabin.
3. **Druk117/118 versus saved fascia:** the left dial is combined fuel/temperature, centre is speed, right is a clock on the supplemental car. Radio above a rectangular vent occupies the right of the metal instrument surround. The model has no radio/vent and identical small generic dials. Add original radio/vent forms and differentiate the first two static dials. The target right-dial configuration remains unresolved, so a detailed supplemental clock face is not automatically authoritative.
4. **Druk140 versus saved passenger side:** padded dash depth, passenger end vent, glovebox seam/handle and centre lower controls are visible. The model is essentially empty below the narrow bar. Add the padded passenger volume, recessed end vent, glovebox boundary and simple original lower control shapes. Fine grain, exact controls and lettering remain later gates rather than a reason to leave the major shapes generic.

All four comparisons identify categorical form differences; uncalibrated photographs do not establish manufacturing dimensions. The following geometry is an evidence-led correction, not an accepted dashboard or a percentage measurement.

## Dashboard correction and skeptical review

`tools/javelin_cockpit.py` adds `build_dashboard(inside)` for the root generator to call in place of its former thin full-width dashboard block. The root's `build_steering` function and manual white-ball/H artwork are preserved.

The corrected section has a bowed, crowned padded driver hood; a separate original metal fascia with actual openings, dark rounded-square gauge mouths and original restrained engine-turn scallops; larger static dial faces; radio and vent forms; a separate lower control ledge; a padded passenger dash/glovebox boundary and pull; an end vent and lower heater controls. The left dial now has two needles and the centre a small original odometer suggestion. The right dial stays generic because the supplemental clock configuration is not confirmed for the target. No photo texture, extra atlas, material or imported asset is introduced.

Inspected `build/parity-audit-interior/dashboard-new/dashboard-front.png`, `dashboard-quarter.png` and `dashboard-passenger.png`. Their isolated source renders use the actual project Part class, existing original atlas and a documented front softbox for cabin visibility. The shared blend is untouched by these diagnostics. `seats-review.json` in that folder records the cockpit generator hash and cameras. Python compilation passes. The root owns the assembled rebuild, native import and clearance gates.

A skeptical review still rejects dashboard closeout. Overall cap curvature and passenger transition remain too regular, the instruments need target-supported numbers and distinct bezels, radio/vent/control dimensions are inferred, the lower passenger structure is simplified, and the fascia scallops approximate engine-turned metal. Grille/defroster slots, fasteners, labels, pedal hardware and steering-column switches require later reference-led passes. Better feature coverage does not establish the requested threshold. All sections remain open.

## Integrated cycle 2 independent review

Inspected all five images in `build/parity-cycle2/interior/` against target47/53 and Druk107/109/115/117/118/140/141/144. Its report records saved-source SHA256 `c5bc8acf83c570c8a2fea61fed199ff347b4df42d3fe4209344cf3c60ae79ba1`. No visible regression was found in the longitudinal front bands, continuous rear bench, rear border arrangement or slotted wheel. The dashboard fascia, gauge mouths, radio and vent remain visible. The integrated pleated door pull, separate crank and central roof dome add reference-supported features.

All earlier shape blockers remain open. In particular, the front seat shoulders are boxy; rear padding and dash/passenger transitions remain overly regular; dials lack target text; the door pull lacks its lower forward curl and the insert its PC crest; the headliner is still a simplified U, with belts and roof hardware missing. These captures hide the exterior and the cockpit view clips the passenger outer edge, so they cannot establish dash/body fit or moving release clearance. The root's later tucked lower-ledge correction requires a fresh build and full-pose clearance gate independently of this visual review. No source changes were made during this review.
