# Front longitudinal crown trial

Cycle 6 isolated scope: `build/front-crown-cycle6/`. Canonical tools, assets, package, specification and native installation are not edited by this work.

## Four fresh comparisons before modeling

1. Original `reference-2.png` against `build/front-envelope-cycle5/after-v2/target-frame2-estimate-paint.png`: lamp pockets and lower nose have depth, but upper fenders still flatten into a wide, plate-like front third. The target shoulders continue their rounded roll while falling around the lamp ends. Camera difference prevents a single-view height correction.
2. Original `reference-30.png` against `after-v2/target-frame30-estimate-clay.png`: target fender/hood shoulder volumes remain distinct into the forward run; candidate clay shows a broad nearly flat leading platform. Corrected corner trim alone does not resolve this underlying volume.
3. `build/six-pass2/druk-025.jpg` against `after-v2/fender-close-paint.png`: the photographed outboard fender turns continuously down and inward toward the nose. Candidate has a muscular axle region but loses its transverse crown well before the leading edge. Reflection brightness is not a measurement of missing height; shape must be checked in clay and profile.
4. `build/six-pass2/druk-005.jpg` and `druk-000.jpg` against `after-v2/side-clay.png` and the opposite front-quarter capture: the front-wheel shoulder should have a sustained rounded fore/aft run, not a narrow hump followed by a plane. Supplemental views support the local longitudinal form but do not authorize adopting their trim, tires or equipment. Preserve cowl/nose anchors, actual width, wheelbase and door seams.

## Diagnosis before trial

The current `front_fender_point` uses a narrow fourth-power longitudinal fullness centered at Y 1.43 with .45 m scale. Its effective crown collapses forward: sampled peak is Z .9132 at Y 1.78, .8568 at 1.96 and .8240 at 2.10. By Y 2.24 the highest point is almost the inner hood edge (X .7202, Z .7949), not a rounded outboard shoulder. This matches the visible flattened leading platform.

These are source-shape measurements, not recovered factory heights. A reversible trial will sustain a broader forward crown while preserving the exact cowl/nose endpoints, the .706 m fixed-wing inner edge, hood seam, shared tessellation/decal support and the existing 60 mm crest-above-hood-edge guard. Any hood/wing rise must be local with smooth zero endpoint deltas, not whole-car scaling. Compare multiple fixed perspective alternatives and orthographic profile before accepting the patch.

## DOX

Root, tools and assets contracts were re-read. Existing Blender/img2blender workflow applies. Root owns this document. Active contracts remain unchanged while the trial is isolated. No section acceptance or fidelity percentage is assigned.

## Baseline and proposed implementation

The actual build baseline is the parent's newly generated front-envelope plus cargo candidate, 193988 triangles. `baseline/Javelin73PC.blend` has SHA-256 `535800eb2340d3975c4046efe0c724561eb4a7535ed7174c79fe424fefd2e17c`. Its exact `build_mod.py` is retained in `baseline/`, and copied module hashes are recorded in `inputs.json`. This baseline includes the accepted cycle 5 front envelope and cargo returns.

`proposal.patch` changes only three localized functions in `tools/build_mod.py`:

- `side_top`: a broader front upper-side drop creates room for the same continuous transverse roll over more of the forward wing. The outer width function and wheel opening remain unchanged.
- `hood_base`: the local added term is `1.10*t**3*(1-t)**2`, with `t` clamped across Y .81..2.34. It has zero position/slope delta at both endpoints, raises support only in the intermediate run and falls to the original nose. It is an inferred shape trial, not a measured factory profile.
- `front_fender_point`: a broader fullness run centered at Y 1.55 sustains the round shoulder into the forward third. The cubic still meets the exact side skin tangentially and the shared .706 m hood edge. Both fender and graphic generation use the unchanged shared station/grid interface.

The first overweighted variant exceeded the existing 60 mm crest guard. It is preserved as `iteration1.blend` and `iteration1.patch`, not proposed. The selected variant redistributes support through the forward hood run and reduces the cubic rise rather than relaxing that guard.

Selected saved blend: `assets/Javelin73PC.blend` under the trial directory, SHA-256 `84acb79039c7278dbd9194de679b3d0f1bd220720a9578ff64551ea014a69ec7`, 193936 triangles. Only Body and Hood source meshes change. Lamp apertures, grille, trim, cargo returns, cabin, axle placement and door geometry are retained.

## Multiple fixed-camera comparisons

All paths in this section are beneath `build/front-crown-cycle6/`. Each before/after pair uses identical full framing, lights, projection, material mode and view transform. No independent silhouette alignment, image scaling or lighting adjustment was used.

| View | Before | After |
| --- | --- | --- |
| Frame 2 estimate, 50 mm, paint/clay | `before/target-frame2-estimate-{paint,clay}.png` | `after/target-frame2-estimate-{paint,clay}.png` |
| Frame 30 estimate, 50 mm, paint/clay | `before/target-frame30-estimate-{paint,clay}.png` | `after/target-frame30-estimate-{paint,clay}.png` |
| Lower 45 mm alternative, paint/clay | `before/alternative-low45-{paint,clay}.png` | `after/alternative-low45-{paint,clay}.png` |
| Longer 70 mm alternative, paint/clay | `before/alternative-long70-{paint,clay}.png` | `after/alternative-long70-{paint,clay}.png` |
| Front detail, paint/clay | `before/fender-close-{paint,clay}.png` | `after/fender-close-{paint,clay}.png` |
| Side profile, clay | `before/side-clay.png` | `after/side-clay.png` |
| Opposite front quarter, paint | `before/front-quarter-opposite-paint.png` | `after/front-quarter-opposite-paint.png` |

Perspective outputs preserve 914x523. `camera-alternatives.json` records the extra 45 mm/70 mm cameras; the ordinary reports record the established views and source hashes. The close wide estimate is an additional diagnostic and partly crops the bumper, so the uncropped frame 2/30 and camera-alternative images remain the full-frame evidence.

Vision review finds the shoulder now remains rounded farther toward the nose in both front perspectives and the oblique close-up. The low 45 mm clay alternative still shows that change, and the long 70 mm view retains it without relying on the close-camera exaggeration. The orthographic side silhouette shows a fuller forward run over the axle, returning to the existing nose and cowl rather than increasing the whole vehicle height.

Source samples describe the actual change, not fidelity:

| Source Y | Previous crown peak Z | Proposed crown peak Z |
| --- | --- | --- |
| 1.43 | .9448 m | .9688 m |
| 1.78 | .9132 m | .9510 m |
| 1.96 | .8568 m | .9097 m |
| 2.10 | .8240 m | .8602 m |
| 2.24 | .7949 m | .8077 m |

The target still has its own sculpted shoulder/hood and leading-edge curvature. The trial is a more substantial correction than corner trim alone, but exact crest location, falloff rate, hood bulge and whole-car proportions remain open. Neither estimated camera fit nor screenshot highlights establish those dimensions. Root should judge the full multi-view set before promotion; native source visibility remains a separate gate.

## Verification

- `unit.log`: all 32 copied unit tests pass, with existing tests unchanged.
- `pose-v2.log`: complete saved-model pose gate passes, including the current cargo requirement (163128 rays with zero leaks), normal and semantic lamp checks, registration/steering clearances, glass/body seams and ten moving-panel hinge fractions. No test exemption was added.
- Existing factory bounds remain valid: Body length 4.88342 m, width 1.91859 m and axle separation 2.79000 m. This is local volume redistribution within the existing envelope, not a wider car or moved axle.
- `crown-check.log`: 161 dense longitudinal sections retain the 60 mm crest guard; observed maximum is 56.584 mm. Nine unrelated meshes keep exact vertex coordinates and face topology. Closed hood cowl/nose anchors remain fixed.
- The same saved-mesh check samples 2760 fixed-fender graphic points and 948 forward hood graphic points against actual painted triangles. Support remains .799.. .801 mm on the fenders and .800 mm on the hood. Selection uses the explicit graphic-facing attribute, excluding lamp pockets and other black hardware. It does not substitute an analytic height for actual support.
- `import.log`: native FBX importer resolves all 11 meshes and the three named clips. This confirms the importer route, not native visual appearance.
- `build-v2.log`: successful build/save, followed by Blender's small unfreed-memory exit diagnostic. Fresh-process reopen, multiple captures and all stated gates succeed.

Reproduction within the prepared trial tree:

```powershell
python build/front-crown-cycle6/prepare.py
& 'C:/Program Files/Blender Foundation/Blender 5.2/blender.exe' --background --factory-startup --disable-autoexec --python-exit-code 1 --python build/front-crown-cycle6/build_trial.py
python build/front-crown-cycle6/tools/check_model_pose.py --blend build/front-crown-cycle6/assets/Javelin73PC.blend
python -m unittest discover -s build/front-crown-cycle6/tools -p 'test_*.py'
& 'C:/Program Files/Blender Foundation/Blender 5.2/blender.exe' --background --factory-startup --disable-autoexec --python-exit-code 1 --python build/front-crown-cycle6/check_crown.py
python tools/check_fbx_import.py --game C:/Games/ProjectZomboid --package build/front-crown-cycle6/Javelin73PC --manifest build/front-crown-cycle6/assets/model-manifest.json
```

No canonical files or native installation were changed. Root owns promotion and subsequent native inspection. All sections remain open.

## Root source promotion

Root reviewed before/after fender clay and the target comparisons. Independent review supports the sustained shoulder volume while flagging a still narrow strongest-curvature region, abrupt front termination and heavy graphic tongue. The three-function patch is promoted over the frozen214,374dashboard/backlight/front/cargo source; native interior activation is retained. Combined source gates are rerun and a new exact checkpoint follows. No whole-car match or section closure is claimed.
