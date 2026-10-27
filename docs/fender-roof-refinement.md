# Open fender and roof refinement

All sections remain open. This is an iteration record, not a likeness percentage, section completion or native-game approval. The user rejected the first broader crown as still tall, narrow and oblong; the initial reviewer approval was too generous and is withdrawn.

## Evidence and method

Use the target video frames `reference-2.png` and `reference-30.png`, plus the four complete [six-source analyses](six-source-four-analyses.md). Druk057 and forum September front/rear quarters clarify transverse rolls; Hagerty's window/roof close-ups distinguish the real roof lip from faceted model joins. Supplemental equipment stays separate from the red target.

Three agents independently investigated front shape, comparison cameras and the roof/haunch ripple. The primary edits the generator and checks their findings against saved renders. Mouse and keyboard support is authorized; Blender's pre-existing dirty session was saved as `build/session-before-fender-refinement.blend` before loading rebuilt sources. Clean live builds then reload in the existing Blender window.

## Front fenders, open

- The first iteration widened the fixed wing by moving its inner seam to X +/-0.706, beside hood edges +/-0.700. Decals were refitted to the actual hood support. Upper arch fullness changed without widening the complete car beyond its dimensional tolerance.
- That left the side wall too tall: at the front wheel it reached about0.960m, and the cubic control rose another65mm before turning inward. A broad patch alone did not remove the narrow high crest.
- The reopened iteration lowers the upper-side/crown boundary locally by about36mm at the wheel, fading to unchanged nose and door anchors. Both side skin and crown use `side_top`. The cubic rise is shorter, the hood-edge profile rises locally by12mm, and central hood relief reduces15mm to avoid raising the whole hood.
- A further iteration concentrates crown fullness near the wheel, fades its vertical control toward both ends, and increases the upper-flank curvature. This addresses the capsule-like longitudinal rail and upcurled nose termination. It still requires inspection against the real hood stamping and front fascia.

Remaining concerns include exact longitudinal taper, the raised central hood contour, and the tall/flat front face. Existing overall dimensions cannot prove these local shapes.

## Roof, sail and rear haunch, open

- Denser compound roof and quarter-window sampling replaces visible short outline facets. Glass/paint share position but have separate reflection normals along the perimeter.
- Sail, side skin and backlight border use shared longitudinal stations. This removes the alternating shading wedges created by T junctions.
- Explicit exterior facing targets correct the rear quarter's inward normals found in backface-culling renders. Twenty-four saved-surface ray samples now check both shoulders.
- The backlight-border bow fades to zero at its upper/lower ends, closing the curved-border/apron corner opening found by the reviewer.
- A90mm lowered patch boundary created an artificial longitudinal trough. The reviewer measured about929/936/890/931/899mm along it. The corrected20mm drop retains endpoint positions/tangents while removing that introduced central valley. This correction must be judged visually, not accepted from its formula.
- Denser stations exposed a closed-door overlap. Blending the curved jamb through nearby side stations restored the moving-panel clearance.

The longitudinal sail-to-haunch transition remains under review. Preserve the real roof lip and waist crease while correcting the curvature. No interior, rear trim or other section is closed.

## Comparison cameras and verification

`tools/review_body_shape.py` captures fixed paint and opaque-clay diagnostics with backface culling. Its `report.json` records source SHA256 and cameras. The additional914x518 perspective pair uses the same side as the target video, unlike the older source preview. These50mm cameras and the closer40mm trial are estimates; windshield-to-front-face ratios still differ, so they do not support metric parity claims.

Evidence is under ignored `build/fender-roof-20261018/`, with before/after renders and exact source snapshots. The earlier `fender-checkpoint` is a recoverable iteration, not an accepted final section. Final verification results are recorded in `.img2blender/reviews.jsonl` and `verification.md`; failed intermediate rounds remain in their own logs.

The fender/roof checkpoint has122,611 triangles. All32 unit checks, static validation, native FBX node/clip importing and the full saved-model pose/steering/ten-fraction clearance checks pass. Twenty checkpoint paint/clay captures are in `front-muscle-review/`. Both fenders, the quarter-window outline and rear backlight/haunch were visually inspected. These results do not verify native-game appearance or the real car's exact shape. No section is closed.

## Mirror correction, open

The subsequent mirror correction has121,875 triangles and preserves the body refinement. The former elliptical pods had reflective faces directed sideways along X. Both replacement round chrome pods have domed front shells, rolled lips, narrow seals, recessed rear reflective disks and short swept pedestals attached to their respective doors. Saved-mesh checks verify48 actual reflective triangles per side face source -Y with inward toe; the full door sweep,32 unit checks, static validation and native importing pass. The clean Blender live view reports the updated source loaded. Four front/rear close-ups are retained under `build/mirror-fix/`.

Reference photographs were also inspected directly: [BaT glazing/door view](https://bringatrailer.com/listing/1973-amc-javelin-amx-2/) (`build/six-pass2/bat-017.jpg`) shows a chrome housing with a separate mounting base and fasteners; [Druk close-up](https://www.drukautosales.com/vehicles/880/1973-amc-amk-javelin-pierre-cardin) (`druk-057.jpg`) shows chrome shell depth and pedestal placement; [Hagerty side view](https://www.hagerty.com/media/opinion/vellum-venom/vellum-venom-1972-amc-javelin-pierre-cardin/) (`hagerty-041.jpg`) shows a painted sport pod and shaped stem; [forum front quarter](https://theamcforum.com/FORUM/uploads/1385/SH100318.jpg) (`forum5local-024.png`, exact mapping retained in its manifest) shows a painted variant. Their construction relationships inform the original geometry. Their differing paint, housing outlines and bases are not silently adopted as the target specification. The target video remains authoritative for round chrome style. Exact size, toe angle and fine curvature remain inferred and open.

## DOX

Root and asset/tool instructions point to this record and preserve the user's all-sections-open requirement. `.img2blender/AGENTS.md` owns the new reconstruction-state boundary. The package instructions remain unchanged because runtime naming, mechanics and installation authority did not change. No installed mod, existing save or running game was altered in this refinement.

## Later cycle3 volume refinement

The167,134-triangle checkpoint supersedes the preceding sail residual and20mm boundary trial. Four fresh comparisons inspected target frames2 and30, the supplemental side photograph and Druk000 against baseline paint/clay before testing variantsB,C,D. Their fixed cameras and images are in ignored `build/front-volume-cycle3/`. The broaderD roll improved the upper-fender depth; the final source uses a115mm smoothly faded boundary drop and145mm rise coefficient. An initial165mm coefficient exceeded the existing60mm hood-relative crest guard; reducing the geometry restored the guard without changing its tolerance. Hood seam, nose endpoints, factory envelope and decal support stay shared.

The sail and quarter-light trial now uses a common cubic roof-to-flank surface with actual side-skin tangency and a longer aperture ending at sourceY=-.95. See [sail refinement](sail-tangent-refinement.md). Earlier frozen residual fades are historical implementation evidence, not present factory constraints.

Twenty body diagnostics and five cabin cutaways identify the exact source hash in `build/parity-cycle3/`. The37-input checkpoint preserves the build, modules, spec, artwork inputs and blend. All32 unit checks, static validation, native11mesh/3clip importing and the full hinge/placement gate pass. Six static native-editor views render the exact isolated deployment, with world spawning and moving-panel playback still pending. The independent [cycle3 audit](cycle3-visual-audit.md) still finds angular sail/haunch transitions, flat front relationships and block-like seat padding. This is incremental progress, with every section open.

The review helper now retains the actual914x523 reference aspect for future estimated-camera captures. Historical914x518 renders keep their original evidence labels; neither aspect correction nor fitted camera alternatives establish calibrated likeness. Owning asset/tool contracts were updated for current construction and capture behavior. Package runtime contracts remain unchanged.
