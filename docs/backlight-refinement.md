# Backlight perimeter refinement, cycle 5

All sections remain open. This isolated trial addresses the backlight aperture and its adjoining local support surfaces. Coordinates are inferred from uncalibrated photographs. It does not establish a likeness percentage or native-game approval.

## Four fresh visual comparisons

1. Re-examined target `reference-2.png` and `reference-22.png` against canonical 188,828 source. Frame 2 shows the front/roof and frame 22 the tail panel/spoiler, so neither reveals the backlight perimeter. They constrain continued target identity, red body and separate moving trunk, but cannot supply glass corner radii. The target side image shows the continuous fastback roof/sail envelope; that envelope must remain unchanged for this localized correction.
2. Re-examined supplied `build/six-pass2/druk-002.jpg` against canonical rear-quarter/open-right source. The photographed upper glass corners have substantial rounded changes of direction, its sides bow rather than following one straight trapezoid edge, and the lower glass meets a shallow rolled painted return. Current source upper and lower corners meet abruptly. Vinyl covering and replacement trim are properties of this supplemental car, not instructions to reproduce its finish.
3. Re-examined `druk-004.jpg` from the opposite rear quarter against the same canonical source and latest clay. Both photographed sides show the same rounded upper aperture and continuous lower support construction. The current source's long straight edge and pointed lower corner dominate its rear view. A local aperture change is supported; moving the entire roof or altering the camera to conceal the corner is not supported.
4. Re-examined low close `druk-032.jpg`, then target-side and all three Druk photographs again against canonical clay/open rear source. The bright backlight surround flows into a narrow crown and a rounded upper corner; the surrounding sail has a broad continuous roll. Keep the shared cubic sail and original upper/lower attachment stations. Exact hidden flange thickness, corner radius, glass curvature and lens projection cannot be measured from these images. The target frames do not resolve the aperture, so the supplemental construction remains an inference rather than a recovered factory specification.

## Isolated construction proposal

The isolated copied `build_mod.py` now rounds the upper and lower aperture corners, bows the side edge by at most the inferred 18 mm shaping term, and preserves the existing outer roof/sail envelope. Upper corner radii use inferred 60 mm transverse/55 mm longitudinal values; lower radii use 50 mm/45 mm. These are reversible construction parameters, not measured factory dimensions. A painted filler connects the rounded upper corners to the unchanged Y=-.80 roof boundary. The lower apron starts from every actual curved glass point, returns through the existing (+/- .838,-1.72,.965) anchors, and ends at retained (+/- .85,-1.87,.940) anchors. A modest inferred 6 mm roll is shared by its side border. Chrome follows the same rounded perimeter.

The original 20 longitudinal intervals were retained. An intermediate 32 interval trial introduced extra visible sail shading strips through the shared station grid, so it was rejected before closeout. Denser transverse glass/support samples still increase roof tessellation, keeping its analytic positions unchanged. Nine other meshes are exactly unchanged; no camera compensation or global roof displacement was made.

Canonical source/tools/assets/spec/profile were untouched by this subtask. Root owns promotion. Isolated proposal files are `build/backlight-cycle5/tools/build_mod.py`, `tools/check_model_pose.py`, `tools/test_sail_surface.py`, and `backlight_guard.py` within that trial folder.

## Verification

Final source: `build/backlight-cycle5/assets/Javelin73PC.blend`, SHA-256 `c192fdb838c204181804563fc97c5e3b9b2ffc2d725ef73aab14bd7a46d961b3`, 196,886 triangles (+8,058 versus 188,828 baseline).

- `before/` and `after/` contain identical-camera paint/clay rear-quarter full frames from both sides, side full frame, backlight close and top. Camera/report hashes identify the exact sources. Backface culling is enabled. Clay glass is opaque. These are diagnostic views, not calibrated photograph matches. Visual review confirms rounded corners and matching support in the source, while overall whole-car likeness remains open.
- `backlight-guard.log` checks the actual saved boundary: 148 perimeter points, no disconnected or branched boundary loops, largest local direction change 22.33 degrees, maximum support distance 0.0001 mm, and 1,864 unobstructed interior-glass visibility rays. The same guard rejects canonical sharp corners at 96.26 degrees. This numerical corner test is a geometry regression check, not a likeness score.
- `scope-report.json` verifies exact coordinate/topology digests for all nine non-Body/non-RearGlass meshes. ASTs for eight existing roof/sail/side scaffold functions match the frozen canonical checkpoint. Glass/apron/roof-support tessellation changes are confined to Body and RearGlass.
- Full `pose.log` passes original seam, moving-panel, normals, axis, lamp, upholstery, cargo, wheel/rest/steering and ten-fraction panel-clearance checks. The local copied pose checker requires the same outward dot>.75 threshold for every nondegenerate RearGlass face, instead of selecting faces above 0.01 square metres. The old selector returned no faces after refinement, causing a false failure; final glass minimum dot is 0.9439. Other glass selectors and tolerances are unchanged.
- All 32 unit tests pass. The extracted apron test's local scope now imports math for the new roll; no expected seam tolerance changed. Two initial missing fixture dependencies were copied into the isolated trial. Static validation passes with 0 errors. Native importer resolves 11 meshes and 3 clips through the installed game's native importer.
- Native editor/world appearance and panel playback of this exact trial remain untested. No installation or desktop operation was performed by this subtask. Rounded corner dimensions and hidden support form remain inferred, and all sections remain open.

## DOX pass

Root owns this research record. Owning AGENTS documents intentionally unchanged because an unpromoted isolated trial introduces no durable project contract or ownership change.

## Root source promotion

Root inspected the same-camera before/after backlight clay close-ups and full rear-quarter paint against actualDruk002. The rounded perimeter and painted support are promoted on top of193,988front/cargo source, retaining the native interior callback. The updated orientation gate samples all nondegenerate RearGlass faces with the unchanged dot>.75 bound; the previous area>.01 subset became empty after subdivision. A new saved-mesh perimeter/support/visibility guard rejects the sharp-corner baseline. Canonical combined build and gates follow; native appearance of this exact glass revision remains pending.
