# Spoiler height and deck audit

All sections remain open. This is a read-only diagnosis and parameter proposal, not an implemented correction, native inspection or numerical likeness assessment.

## Exact reviewed state

- Saved source: `assets/Javelin73PC.blend`, SHA256 `2cf24956ef2b112398a3788cf35802033686964bcdcf610b4735cd5e40616e2a`, 167134 triangles according to `build/parity-cycle3/body/report.json`.
- Rear generator: `tools/javelin_rear.py`, SHA256 `a650f244370243372f52c1492e6dac74eb91fa9ea2a6cd566e7bf9cf280999a5` at this review.
- Inspected diagnostic renders: cycle3 body `side-clay.png`, `sail-close-paint.png`, `rear-quarter-clay.png`, `top-clay.png`, plus `assets/javelin-perspective.png`.
- Read root and assets DOX, the tools contract for interpreting generator responsibilities, reconstruction spec/recent reviews, and Blender/img2blender skills including camera and visual-review guidance. No source, asset, package or spec was changed.

All dimensions below are source coordinates before the common -0.65m source-mesh Z offset. Differences are unaffected by that offset. They are authored dimensions, not measurements of the real car.

| Feature | Current source value | Implication |
| --- | --- | --- |
| Trunk front | Y=-1.87000 | Shared fixed/moving seam |
| Trunk rear | Y=-2.18092 | 310.92mm anchor separation; actual front edge at -1.876 gives304.92mm top-sheet run |
| Tail face | Y=-2.29492 | Rear return lies aft of this station |
| Ramp foot, centre | Y=-2.16592, Z=.895 | 15mm overlap forward of rear seam; 5mm above lid rear Z=.890 |
| Crest, centre | Y=-2.32692, Z=1.045 | 150mm rise over foot, 161mm horizontal run |
| Return bottom, centre | Z=.840 | 205mm total rear return |
| Lip radius | 10mm | Rounded crest, not a sharp top edge |
| Transverse crest | 1.045 minus .010*(X/.850)^2 and rounded end drop | Width1.700m; endpoints Z=.975, 70mm below centre |
| Latch cup | Centre Z=.945, half-height80mm, half-width67mm, depth48mm | Upper boundary1.025 leaves20mm below current centre crest |
| Lock | Z=.906 | Low in the cup, not at its centre |

The 119.08mm rear-overhang shortening is already included. Restoring or extending it would move fixed fascia, body, bumper and cargo stations, not merely soften the lip. The source-sheet run is about305mm, not a long horizontal deck. The short foot-to-crest run and150mm rise make a steep local kick even though the rear return itself can legitimately be tall.

## Four fresh comparisons

### 1. Target frame relevance and actual rear-face evidence

Viewed the complete supplied `reference-12.png`, `reference-16.png`, `reference-22.png` and `reference-26.png` against cycle3 rear and side renders. Frame12 is a grille-medallion detail. Frame16 is a door, crest and sidepipe detail. Neither contains the rear spoiler. Frame22 shows the target's red lamp panel, upper moving return, lower seam, pressed lock cup and badges, but cuts off the crest. Frame26 superimposes a front view over a rear-corner shot during a dissolve; its outer edge is not a reliable single silhouette.

The target confirms red rear paint, a distinct moving return above the lamps, and a low lock in a pressed cup. It does not directly support a metric crest height, a deck run, or a requirement to flatten the spoiler. Cycle3 retains these identifiers. Its rear quarter still reads as a high continuous wall and short ramp, which needs further comparison. Cropped upper boundaries must not be treated as observed crest landmarks.

### 2. Low-quarter construction versus apparent height

Viewed Druk `build/six-pass2/druk-032.jpg` and `druk-034.jpg` against cycle3 `side-clay.png`, `rear-quarter-clay.png` and `sail-close-paint.png`. These photographs show a substantial integrated return with solid end cheeks, a strong rising top, a narrow lower seam, and a rounded transition into the corner. The low camera makes the return imposing while hiding most of the deck. Neither establishes the ramp's side-profile slope independently of camera.

Cycle3's closed cheeks and rolled crest have the right construction category. Its side render exposes a very short, abrupt upward kick; the broad upper face is not itself evidence of a bad part. Keep the ramp foot, transverse crest and return height separate in any correction. Do not replace the integrated lip with a thin wing or remove the end cheeks. The Druk car has a dark rear-window surround and other trim/fit differences, so it corroborates construction rather than target finish or factory originality.

### 3. Straight-rear return, cup and lamp relationship

Viewed Druk `druk-040.jpg` alongside target22 and cycle3 `sail-close-paint.png`/`rear-quarter-clay.png`. Druk040 shows a broad, tall return and a pressed oval cup whose top leaves visible metal below the crest and whose lock sits near its bottom. Perspective, cropped ends and unknown lens prevent converting the image into a manufacturing dimension. Its tall return is counterevidence to simply shaving off a large fraction of the current face based on the side render alone.

The current cup is160mm high within a205mm return, leaving only20mm above its boundary. Lowering just the crest25mm puts that existing boundary5mm above the new top; lowering40mm would be worse. Therefore a crest reduction must also revise the cup or move its upper boundary. Preserve the target22 low-lock relationship and separate AMC/AMX badge supports. Re-run their projection onto the revised bowed face. A global Z scale of the complete trunk would also alter deck seating, seams and hinge registration and is unsuitable.

### 4. Whole-side proportions and camera sensitivity

Viewed supplemental `reference-side.png` against cycle3 `side-clay.png` and the full top/rear-quarter captures, then checked the low target front `reference-2.png` and `assets/javelin-perspective.png` for visibility limits. The side photograph shows a small curved kick relative to the roof/haunch fall, with the lip smoothly growing out of a relatively shallow aft surface. Cycle3 shows a more conspicuous vertical prong at the back of the short deck. This supports testing a less abrupt local rise, but this photograph is a different car, without the target sidepipes and with different wheels, so it cannot define the video car's exact spoiler height.

Cycle3 side is an orthographic diagnostic with camera(-8,0,.5) aimed at(0,0,0), about3.6degrees downward rather than perfectly horizontal. Its horizontal deck run is foreshortened by height coupling. The rear-quarter and sail cameras are much higher and expose more deck; the front perspective does not expose enough rear geometry to judge this section. A camera change can alter the apparent deck length and prominence of the crest, but cannot remove the actual150mm source rise. Fit a clean target rear/side camera before selecting final dimensions. Do not lower the roof or lengthen the complete body to conceal this local kick.

## Controlled proposal, not adopted geometry

Use independent variants against the exact saved baseline, with unchanged cameras, light, projection and framing. Retain full vehicle views as well as crops. These numbers are modest inferred sensitivity tests, not recovered factory or video dimensions.

1. **Height-only group:** test centre crest1.020m, a25mm reduction. Preserve the10mm rolled radius, transverse rounded ends, ramp foot, return bottom and deck seams. The rise becomes125mm and return180mm. Revise cup centre to .935 and half-height to .065, retaining current67mm half-width and lock Z=.906 initially. Its top becomes1.000, maintaining20mm crest margin; bottom.870 leaves30mm to the lower return edge. Verify that the lock and its radius still sit visibly inside the bowl. Sample the complete cup support rather than checking only its centre.
2. **Ramp-length-only group:** retain current crest and cup; move ramp foot40mm forward (+Y), from-2.16592 to-2.12592. Centre run becomes201mm instead of161mm. This consumes40mm of exposed lid and could make the short-deck impression worse from above, so it is a diagnostic alternative, not the preferred automatic correction. Preserve the original thin closed lid beneath the overlap and inspect for duplicate visible surfaces or intersections.
3. **Camera-only group:** preserve geometry and recapture a genuinely level side diagnostic, plus low rear-quarter and higher rear-quarter using the same frame bounds. Establish which shifts are camera-induced before choosing between the geometry groups.

Start with the25mm height trial if a local geometry experiment is needed. Consider a40mm reduction only after reviewing that trial against a clean target crest. It requires another cup adjustment and fresh badge/lock support checks. Do not combine height, ramp run, deck length and roof changes in one test; improvement would become untraceable. No test render or patch was produced during this read-only audit.

## Required checks before adoption

- Preserve red target tail paint, four recessed lamps with inner reverse inserts, moving badges/lock, thin lid and fixed apron seams, rounded crest/ends, and closed cheeks.
- Inspect source clay from both sides, front/rear/top and close rear quarters. Compare roof/backlight fall, exposed deck run, lip rise and rear-face area separately.
- Re-run saved-mesh seam, winding/normals, surface visibility, cup/badge support and all ten hinge-fraction clearances, including the fixed fascia and corner trim.
- Rebuild and reopen only after selecting a supported correction; review native game alignment and trunk playback separately. Existing cycle3 native-static evidence does not test a proposed spoiler change.

DOX pass: root owns this development evidence document. Root, tools and assets instructions were intentionally unchanged because this audit adds no durable structure, generator responsibility, interface or accepted geometry contract. Existing `trunk-spoiler-refinement.md` describes its older iteration; its former restored205mm preference is context, not an accepted present-day likeness gate. All sections remain open.

## Isolated A/B follow-up

Executed the proposed sensitivity study under ignored `build/spoiler-height-cycle4/`, using hash-verified files from the167134-triangle frozen checkpoint. The authoritative blend and `tools/javelin_rear.py` retained the exact hashes above. `provenance.json` stores the checkpoint manifest; `height.patch` and `ramp.patch` contain only each proposed rear-generator edit. The isolated build scripts suppress normal preview renders; source generation, rigs and export execute inside their own copied project roots. No candidate was promoted.

`review.py` captures baseline, height and ramp variants at identical880x640 framing, camera coordinates, staging, backface culling and Eevee renderer. Every variant has `side-clay.png`, `rear-quarter-paint.png` and `close-paint.png`. Baseline also has `level-side-clay.png`, changing only the camera's elevation to the target's Z. `render-report.json` records each saved blend hash and capture camera. These controlled renders supersede casual comparisons between different cameras or resolutions; they are still uncalibrated diagnostics.

- **Height:** the25mm lower crest visibly reduces the side-view prong while retaining the integrated curved rise and broad return. It is a modest useful direction, not a solved silhouette. In the rear-quarter and close paint views the cup becomes noticeably squatter: its130mm height versus134mm width approaches round, whereas target22 and Druk040 show a vertically oval recess. The AMX badge also has less headroom. Existing mesh checks do not judge those likeness defects. Do not promote this exact patch. A next local trial should preserve the cup's vertical aspect, for example reduce its half-width from67mm to roughly54mm along with the tested65mm half-height, then independently review cup depth and lock registration. That54mm width is an untested inference, not an adopted dimension.
- **Ramp:** the40mm forward foot retains the same crest height and makes a broader wedge from the side; high views consume more of the already short exposed deck. It does not resolve the conspicuous high tip, so reject this variant as the present fix. Its mechanical clearance was not selected for acceptance testing.
- **Camera control:** level side changes the deck/haunch overlap and apparent roof slope, but the upright kick remains visible. Geometry contributes to the issue. The high close view exposes much more deck than a low rear-quarter photograph; avoid mistaking that change for a part correction.

The height candidate remains mechanically viable for further visual work: `height/pose.log` passes the complete saved-model pose/registration/orientation suite, including all ten hood/trunk/door hinge fractions, closed seam checks, panel/fixed body/glass clearances, dimensions, wheels and seat/headliner support. Native game appearance and playback were not tested for either candidate. Neither reference parity nor closure of the spoiler section is claimed.

The follow-up changes only this root-owned evidence document and ignored experiments. Owning DOX contracts remain unchanged for the same reason as the initial pass.

## Oval cup and pressed backing trial

The subsequent `height-oval/` trial retains the25mm crest reduction, cup centre.935, half-height.065 and lockZ=.906/radius.012, but sets cup half-width to `.067*(.065/.080)=.0544375m`. Its height-to-width aspect is1.19403, exactly the authored baseline's aspect. This is an inferred preservation of the existing shape, not proof that its absolute size matches the target.

Targeted saved-mesh testing then found an inherited defect that the general pose gate had missed: the flat inner return atY=-2.32192 rose toZ=.887 and crossed the lower cup depression. The frozen baseline has10 failures among161 sampled exterior cup rays. One oval trial sample atZ=.88625 hit that inward-facing return17.2mm before the intended cup surface. General component winding checks do not detect this same-component overlap. That discovery supersedes the earlier suggestion that a passing general pose suite alone made the candidate mechanically ready.

The trial now replaces that straight inner return with a17-station pressed backing following the actual rear cup surface plus5mm inY, up to the original stepped underside height. It retains the closed lower5mm fold, end cheeks, moving rear seam and original foot attachment. This adds4170triangles, giving171304 in the isolated build. Both the cup and its backing remain part of the moving trunk.

Final evidence is `cup-saved-mesh-audit.json` and its log, `height-oval/pose-backing.log`, `height-oval-render-report.json`, `cup-camera-report.json`, and `height-oval.patch`. Earlier diagnostic support files/logs record the failed intermediate experiments; they are not the final gate.

- All161 sampled cup positions have nearby saved red geometry, correct rear-ray depth and outward visible normals, with zero visibility failures.
- All102 paired exterior/interior backing rays have positive thickness and opposing outward normals; the finite sample grid checks for the prior crossing independently of global winding.
- All33 AMC/AMX faces have outward normals and supporting red geometry within2mm.
- The parameter-derived cup upper/lower boundaries are1.000/.870m, with20mm crest margin and30mm lower seam margin. Lock centre and radius are retained. These margins are inferred design geometry, not photographic measurements.
- The complete saved-model pose suite and all ten hinge fractions pass after the backing change. No native-game culling or playback was performed for this candidate.

Fresh matched side, rear-quarter and high-close captures retain the modestly lower kick. New `baseline/rear-cup-paint.png` and `height-oval/rear-cup-paint.png` expose the change under native-style backface culling: the baseline bowl has a horizontal folded shelf at its bottom; the corrected trial has a continuous lower bowl with a visibly low lock. `height-oval/rear-cup-clay.png` confirms the recess without relying on paint. Against Druk040 the trial preserves a vertically oval pressed opening, rounded top and lower lock. The smaller absolute opening may still be undersized; target22's cropped top prevents settling that dimension. Roof-to-deck length, transverse crest contour and remaining rear trim likeness are still open.

The final patch is suitable for root review as a bounded candidate. It is not promoted or visually accepted. Only ignored trial roots and this evidence document were edited by this audit; authoritative rear source remained at the recorded hash. Other concurrent project builds must be evaluated separately from this frozen-base rear experiment.

## Promoted after root review

The earlier isolated-only statements above describe proposal history. Root inspected the saved comparisons and promoted this proposal into the187,836-triangle combined cycle4 source, SHA-256 `363dfc71f833875a3c94f577bb094d19e52db2c9f2a1d82240629327871fccbf`. The169,766-triangle front-only source was frozen first. Fresh integrated evidence is under ignored `build/parity-cycle4/combined/`; all32 unit checks, static validation, native11mesh/3clip importing and the full saved-model pose/ten-fraction gate pass. The clean live Blender source is current. The installed/native-inspected candidate remains167,134 triangles; this combined geometry has not been installed or natively reviewed. All sections remain open, with no likeness percentage assigned.

The25mm height change, authored cup aspect and low lock were promoted together with the pressed backing, not the rejected ramp-only or squatter-cup variants. The integrated102 paired cup rays require positive3.5..6.5mm backing thickness and opposing outward normals. `counterfactual.log` rejects the inherited intersecting backing. Exact cup size, crest likeness and remaining rear trim remain inferred/open; native trunk playback remains pending.
