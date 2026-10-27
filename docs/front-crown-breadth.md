# Front crest breadth trial

Isolated cycle 7 scope: `build/front-crown-cycle7/`, based on the exact frozen 214322-triangle source, SHA-256 `c9c25499d084ded7bfe8910375247a9be5568f0c3235bce57166656dc01216c8`. Canonical source, profile, specification, native installation and UI are untouched.

## Four fresh comparisons before modeling

1. Original `reference-2.png` against exact-source `build/parity-cycle6/camera-fit/frame2-balanced-paint.png` and `frame2-contact-anchored-paint.png`, checked against the newly recaptured exact-source 45/70 mm alternatives under `build/front-crown-cycle7/before/`. The candidate now has shoulder height, but its bright outer roll is concentrated into a narrow rail, while the target shows a wider shoulder top turning down into the outer side. The same narrow roll persists under both locked solutions and sensitivity cameras. This supports a breadth trial rather than another height increase.
2. Original `reference-30.png` against `build/parity-cycle6/camera-fit/frame30-balanced-clay.png` and `body/target-frame30-estimate-paint.png`. Candidate crest is prominent but falls across a relatively short transverse band, leaving the upper mass tube-like. The target has a broader sculpted transition. The different projections limit exact width recovery; the existing locked cameras must remain fixed while testing geometry.
3. `build/six-pass2/druk-000.jpg` against exact-source opposite front quarter and the recaptured 70 mm sensitivity view. Supplemental car also shows a broad upper fender face flowing into the hood-side shoulder, rather than a narrow raised runner. Equipment differences remain excluded. This supports testing a flatter crest area within the current outer envelope, not widening the vehicle.
4. `build/six-pass2/druk-025.jpg` against exact-source `body/fender-close-clay.png`, checked with the recaptured low 45 mm clay view. The photographed outer shoulder rolls down over a substantial cross-section and carries a broad upper surface. Candidate curvature concentrates near its highest point. Graphic/nose boundary remains abrupt, but that decal shape is a separate finding unless actual support rays reveal geometric discontinuity.

## Trial rationale

Keep the current longitudinal crown, hood height, overall width, side endpoints and inner hood-edge anchors. The reversible trial redistributes existing transverse height toward the crest across a broad smooth window, bounded by the existing section maximum. It must neither increase that maximum nor alter endpoint position/tangent. Existing shared triangles regenerate both paint and graphic support. Compare identical locked 22 mm/36 mm cameras and the existing fixed sensitivity cameras without fitting either again.

## DOX

Root, tools and assets contracts were re-read, along with the relevant Blender/img2blender instructions. Root owns this evidence document. No active owning contract changes while the geometry remains an isolated proposal. No percentage or section acceptance is assigned.

## Proposal and exact source

`build/front-crown-cycle7/proposal.patch` changes only `front_fender_point` in `tools/build_mod.py`. The original cubic remains the scaffold. The function solves its vertical derivative to find the existing section maximum, then blends lower portions toward that maximum using a broad smooth window, `.80*fullness*16*t*t*(1-t)*(1-t)`.

Because the window is bounded below one, the result cannot exceed the existing maximum. Its value and derivative vanish at both transverse endpoints. All X/Y coordinates remain unchanged, and the original longitudinal endpoint fullness removes the correction at cowl/nose sections. No further hood rise, global scaling, widening, axle movement or camera change is introduced.

Exact copied checkpoint inputs remain in `baseline/` and `tools/`, with module hashes in `inputs.json`. The proposed saved source is `build/front-crown-cycle7/assets/Javelin73PC.blend`, SHA-256 `30dc178cd714ae5e8539e4398ced03a7fe9f60d5278f7e70329ba3d4cd92879d`. It retains 214322 triangles. Only the Body mesh's local wing/graphic geometry changes; the other ten meshes, including the complete Hood, remain exact.

This is an inferred shape experiment, not a factory cross-section. Its support is the repeated broad-shoulder finding across four fresh comparisons. Root review remains the promotion gate.

## Locked before/after evidence

All paths here are beneath `build/front-crown-cycle7/`. Full frames are retained without silhouette alignment or independent scaling.

| View | Before | After |
| --- | --- | --- |
| Locked frame 2 balanced, approximately 22 mm, paint/clay | `before/camera-fit/frame2-balanced-{paint,clay}.png` | `after/camera-fit/frame2-balanced-{paint,clay}.png` |
| Locked frame 2 contact-anchored, approximately 36 mm, paint/clay | `before/camera-fit/frame2-contact-anchored-{paint,clay}.png` | `after/camera-fit/frame2-contact-anchored-{paint,clay}.png` |
| Locked frame 30 balanced, paint/clay | `before/camera-fit/frame30-balanced-{paint,clay}.png` | `after/camera-fit/frame30-balanced-{paint,clay}.png` |
| Fixed 45 mm sensitivity, paint/clay | `before/alternative-low45-{paint,clay}.png` | `after/alternative-low45-{paint,clay}.png` |
| Fixed 70 mm sensitivity, paint/clay | `before/alternative-long70-{paint,clay}.png` | `after/alternative-long70-{paint,clay}.png` |
| Established 50 mm sensitivity, paint/clay | `before/body/target-frame2-estimate-{paint,clay}.png` | `after/body/target-frame2-estimate-{paint,clay}.png` |
| Front close-up, paint/clay | `before/body/fender-close-{paint,clay}.png` | `after/body/fender-close-{paint,clay}.png` |
| Profile | `before/body/side-clay.png` | `after/body/side-clay.png` |

`locked_cameras.py` reuses the exact `build/parity-camera/fit.json` and `contact-fit.json` parameters and the parent's render equations: 36 mm sensor, horizontal fit, principal shift and roll. Those input JSONs are read only. Their values are copied into each capture's `source.json`. Sensitivity settings are retained in `camera_alternatives.py`. No camera was optimized or refitted for this trial. The copied `before/body/` captures identify the same frozen source hash; locked and 45/70 mm before images were freshly recaptured from the frozen blend.

Vision review finds a broader and flatter crest transition in close clay and paint. The difference is modest at full-car scale, but remains visible under both locked cameras and the long-lens sensitivity pair. Profile peak height remains the same, consistent with breadth redistribution rather than increased fender height. The result still has a stylized smooth shoulder; it is not a recovered stamped-metal profile or whole-vehicle likeness approval.

The **abrupt graphic-to-nose boundary remains a separate open finding**. Graphic paths were not redrawn, shortened or extended to flatter the render. Actual support checks below show that the existing paths continue to seat on the changed wing triangles. The residual visible change of direction must be reviewed against target graphic/nose evidence rather than labeled fixed by broader geometry.

## Geometric evidence and verification

The following band widths describe the generated cross-section lying within 5 mm of its own maximum. They are diagnostic geometry dimensions, not likeness scores or measured reference dimensions:

| Source Y | Previous crest band | Proposed crest band |
| --- | --- | --- |
| 1.23 | 67.0 mm | 91.1 mm |
| 1.43 | 72.6 mm | 107.5 mm |
| 1.60 | 68.8 mm | 105.4 mm |
| 1.78 | 58.1 mm | 87.5 mm |
| 1.96 | 52.2 mm | 69.8 mm |

- `breadth-check.log` / `breadth-check.json`: six densely sampled sections keep identical X/Y and crest height within 0.01 mm while widening the band. Across 161 longitudinal stations the existing 60 mm guard remains unchanged, with observed maximum 56.585 mm. Endpoint/tangent unit tests pass.
- Saved-mesh preservation: ten unrelated meshes retain exact vertex coordinates and face topology, including Hood. Closed hood cowl/nose anchors remain fixed.
- Saved support rays: 2760 fixed-fender graphic samples retain .799.. .801 mm clearance over actual painted triangles; 948 forward hood samples retain .800 mm. No analytic curve is substituted for triangle support.
- `unit.log`: all 32 tests pass, unchanged.
- `pose.log`: full copied current saved-model pose gate passes, including cargo visibility, outward normals and actual lamp apertures, factory envelope, seat/steering registration, glass and moving-panel seams and ten hinge fractions.
- `import.log`: native importer resolves all 11 meshes and three named clips. This is importer evidence, not native appearance.
- `build.log`: successful generation/save followed by Blender's small unfreed-memory exit diagnostic. Fresh-process reopening, captures and checks succeed.

Reproduce the prepared isolated source:

```powershell
python build/front-crown-cycle7/prepare.py
& 'C:/Program Files/Blender Foundation/Blender 5.2/blender.exe' --background --factory-startup --disable-autoexec --python-exit-code 1 --python build/front-crown-cycle7/build_trial.py
python build/front-crown-cycle7/tools/check_model_pose.py --blend build/front-crown-cycle7/assets/Javelin73PC.blend
python -m unittest discover -s build/front-crown-cycle7/tools -p 'test_*.py'
& 'C:/Program Files/Blender Foundation/Blender 5.2/blender.exe' --background --factory-startup --disable-autoexec --python-exit-code 1 --python build/front-crown-cycle7/check_breadth.py
& 'C:/Program Files/Blender Foundation/Blender 5.2/blender.exe' --background --factory-startup --disable-autoexec --python-exit-code 1 --python build/front-crown-cycle7/locked_cameras.py
```

No native trial installation or game inspection occurred. Root's current frozen-source native work remains separate. Parent/root contracts are intentionally unchanged while this proposal is isolated. All sections remain open.
