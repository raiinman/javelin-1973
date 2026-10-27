# Front envelope continuity trial

Isolated cycle 5 work from the frozen 187836-triangle combined candidate, source SHA-256 `363dfc71f833875a3c94f577bb094d19e52db2c9f2a1d82240629327871fccbf`. Canonical source, package, specification and Blender assets remain untouched. Root promotion review is required.

## Four fresh comparisons before modeling

1. Original `reference-2.png` against `build/parity-cycle4/combined/body/fender-close-clay.png`: the target nose rolls around the outer lamp enclosures; the candidate corners remain abruptly faceted despite the new recessed lenses. Clay confirms a shape boundary, but the higher candidate camera prevents an exact fender-height correction.
2. Original `reference-30.png` against `body/target-frame30-estimate-paint.png`: target has a curved red lower valance visibly extending below the narrow chrome contour. Candidate has a shallow visible red strip and a rail-like bumper. The estimated camera is uncalibrated, so retain body length/height and inspect a reversible local rearward-roll change instead of scaling the entire nose.
3. `build/six-pass2/druk-025.jpg` against `body/fender-close-paint.png`: the photographed sheet metal turns around the outer lamp beside a smoothly rolled bumper return. Candidate perimeter/bumper cross-section has visible polygonal corners. Secondary photograph supports local corner construction, not adoption of its wheels, trim or color.
4. `build/six-pass2/druk-000.jpg` against `body/front-quarter-opposite-paint.png`: full unaligned frames confirm that the front corner and lower bumper/valance relationship affects whole-car identity. The candidate's broad crowns exist; lowering or widening the entire fender without a fitted camera would be speculative. Retain crown/hood/decal support and concentrate the first trial on perimeter continuity and lower nose construction.

## Initial trial scope

Under `build/front-envelope-cycle5`, copy frozen generator inputs and make a reviewable patch. Preserve actual headlamp apertures, lens support and semantic atlas, central insert/rally trim, crown and hood geometry, decal projection topology, door seams, native bounds and factory dimension checks. Smooth existing outer fascia corners, roll the bumper section without changing its envelope, and test a shallower lower-valance rearward roll with matching side corners. Do not change render lighting or compensate for flat native editor lighting.

The camera is kept identical between before/after full frames and clay. It remains an estimate, so this trial does not claim to recover manufacturing dimensions or establish likeness.

## DOX

Root, tools and assets instructions and Blender/img2blender skills were re-read. Root owns this document. Active contracts remain unchanged while the proposal is isolated; promotion must record any adopted geometry contract in the owning tools/assets docs.

## Reviewed proposal

- Source patch: `build/front-envelope-cycle5/proposal.patch`, localized hunks in `tools/javelin_front.py` and `tools/build_mod.py`. Apply hunks to the current source, not whole-file replacement, because the separate rear cargo work has advanced since the frozen baseline.
- Isolated source: `build/front-envelope-cycle5/tools/`; reproducible preparation is `prepare.py`, and `build_trial.py` executes that trial source with automatic preview render calls suppressed. All generated files resolve inside the trial tree.
- Proposed saved blend: `build/front-envelope-cycle5/assets/Javelin73PC.blend`, SHA-256 `64e7f7cfaa258980c9015e281ccd8e8640c67d485e00f363b39cd1c63c126311`, 192996 triangles.

The proposal rounds the existing outer fascia path with short quadratic corner transitions. It does not move the lamp centers, apertures, rim/reflector/lens registration, central grille insert or badges. Front/back field columns are restricted to the rounded outline's actual X range, avoiding attempts to evaluate the former polygon's extrema outside the new boundary.

The front bumper retains its centerline, end wrap and cross-section envelope. A sampled rolled rectangular section replaces the eight-edge chamfer; denser longitudinal stations remove the visible angular changes at the returns. Rubber overriders remain in place.

`valance_point` is shared by the closed lower nose and its new side returns. The lower rearward roll changes from 180 mm to 140 mm, exposing more red below the chrome without lowering the car. The lower valance corners rise 35 mm with a continuous transverse curve. The front lower side/arch trim rises to that corner over the last 290 mm, and the side rollback changes correspondingly. Those are reversible inferred shape parameters guided by the images, not measured factory values.

Iteration 1 is preserved as `iteration1.blend`, `iteration1.patch` and `after/`. It was not selected: its round bumper looked too tubular and its flat valance bottom introduced an overly straight lower edge. Iteration 2 uses the rolled rectangular section, a less aggressive rollback change and curved lower corners. Its relevant captures are in `after-v2/`.

## Before/after review

All capture paths below are inside `build/front-envelope-cycle5`:

| Comparison | Frozen before | Proposed after |
| --- | --- | --- |
| Full unaligned target frame 2 estimate, paint/clay | `before/target-frame2-estimate-{paint,clay}.png` | `after-v2/target-frame2-estimate-{paint,clay}.png` |
| Full unaligned target frame 30 estimate, paint/clay | `before/target-frame30-estimate-{paint,clay}.png` | `after-v2/target-frame30-estimate-{paint,clay}.png` |
| Front detail, paint/clay | `before/fender-close-{paint,clay}.png` | `after-v2/fender-close-{paint,clay}.png` |
| Opposite front quarter, clay | `before/front-quarter-opposite-clay.png` | `after-v2/front-quarter-opposite-clay.png` |
| Side and top silhouette, clay | `before/{side,top}-clay.png` | `after-v2/{side,top}-clay.png` |

Each pair retains the same camera, full framing, renderer, lights and view transform. Target estimates retain the original 914x523 aspect. Both report files identify source hashes. No independent silhouette resizing or crop alignment was used to conceal placement changes.

Vision review of the full target estimates and close clay shows a softer black outer corner and bumper return, with a deeper visible red valance and a less abrupt lower corner. The altered volume remains visible in clay, so the finding does not depend on paint reflection or native editor lighting. Side/top checks retain the existing long hood, wheelbase, crown and cabin silhouettes apart from the intended lower front corner.

The improvement is local. **The fender/hood longitudinal shoulders still flatten into a broad front plate compared with the target's flowing downward nose.** The existing crown shape was retained to preserve evidence and exact decal support rather than making an uncalibrated global correction. This remains the next substantial front-body study. The central insert shape, bumper-to-grille proportions and lower corner trim endpoints also remain open to target-camera and native review. The proposed bumper roll does not establish a final stamped bumper profile.

## Verification and limits

- `unit-v2.log`: 32 frozen-baseline unit tests pass.
- `frozen-pose-v2.log`: the complete frozen 187836 pose gate passes, including outward sheets/closed-component winding, seat support, exact seams, attachment/steering registration, factory envelope and ten hinge fractions. Front lamp rays retain 9.830..17.029 mm recession with no spanning shadow caps. Saved Body length is 4.88342 m, width 1.91859 m, axle separation 2.79000 m, all within existing tolerances.
- `import-v2.log`: native importer resolves all 11 meshes and three named clips.
- `preservation.log` and `preservation.json`: the ten non-Body meshes have exactly the frozen baseline's vertex coordinates and face topology. Fifteen saved lower-valance rays hit outward surfaces, match the authored curved support within 3 mm, and align with the support normals (dot greater than .97). This custom check initially used an unjustified Y>.65 normal threshold; a valid steep outer roll gave .644. It now tests actual support orientation and position instead of treating a curved surface as nearly planar.
- `pose.log` records an attempted current canonical gate. It fails the newly added cargo visibility requirement because this trial intentionally retains the frozen baseline's pre-tub cargo. That failure belongs to the separate cargo composition. **The isolated proposal does not pass the current combined cargo gate.** Root must apply only the front hunks over its cargo candidate and rerun that complete current gate.
- The generation log reports successful save/build followed by Blender's small unfreed-memory diagnostic on exit. Fresh-process reopen, capture, frozen pose checks and native importer all succeed. This is retained as a tool diagnostic, not treated as a likeness or geometry failure.
- No trial install, game launch, live editor control or native appearance verification was performed. Native surface visibility, bumper/valance appearance, lower trim endpoints and moving hood views remain root's post-composition gates.

Reproduce with the trial tree already prepared:

```powershell
python build/front-envelope-cycle5/prepare.py
& 'C:/Program Files/Blender Foundation/Blender 5.2/blender.exe' --background --factory-startup --disable-autoexec --python-exit-code 1 --python build/front-envelope-cycle5/build_trial.py
python build/front-envelope-cycle5/tools/check_model_pose.py --blend build/front-envelope-cycle5/assets/Javelin73PC.blend
python -m unittest discover -s build/front-envelope-cycle5/tools -p 'test_*.py'
python tools/check_fbx_import.py --game C:/Games/ProjectZomboid --package build/front-envelope-cycle5/Javelin73PC --manifest build/front-envelope-cycle5/assets/model-manifest.json
& 'C:/Program Files/Blender Foundation/Blender 5.2/blender.exe' --background --factory-startup --disable-autoexec --python-exit-code 1 --python build/front-envelope-cycle5/check_preservation.py
```

Canonical files were not modified by this work. Root's independent cargo edits are not part of this proposal. No percentage or section acceptance is assigned.

## Root source promotion

Root reviewed the same-camera before/after target-front paint view plus the new fender-close clay and side clay. The rounded fascia/bumper contour and fuller visible lower valance are incremental improvements. The broader hood/fender longitudinal plate, approximate bumper detail and whole-car identity remain open. The localized patch is promoted on top of the frozen188,828cargo source; full combined gates are rerun by root. This does not promote the isolated whole build or replace the cargo guard.
