# Front fascia aperture trial

2026-10-18. The four fresh comparisons in `docs/cycle3-visual-audit.md` precede this isolated implementation. They identify the flat assembled-lamp appearance and front volume relationships as open defects. This trial addresses only outer headlamp apertures and recess registration. It does not close the fascia or claim reference parity.

## Preserved baseline and scope

- Frozen input: `build/parity-cycle3/checkpoint`, with source blend SHA-256 `2cf24956ef2b112398a3788cf35802033686964bcdcf610b4735cd5e40616e2a`.
- Trial tree: `build/front-fascia-cycle4`. The real `tools/javelin_front.py`, original blend, current package and deployed package were not changed.
- Reviewable patch: `build/front-fascia-cycle4/proposal.patch`, targeting only `tools/javelin_front.py`.
- Trial saved blend: `build/front-fascia-cycle4/assets/Javelin73PC.blend`. Its generated manifest reports169766triangles.
- The frozen generator and modules were copied into the trial tree. `build_trial.py` executes the unchanged generator text with only automatic render calls suppressed; generator-relative outputs resolve inside the trial tree. The proposed front module is the sole geometry difference. `runtime_gameplay.lua` was additionally copied into the trial tools for existing unit-test fixtures; it does not participate in geometry generation.

## Geometry change

The former full front shadow polygon and rear cap spanned both outer headlamps. New sampled front/back fields exclude circular apertures centered at X +/-.708, Z .641 with122mm radius. Connected black returns join their front and rear perimeters. Shared stations preserve the existing outer outline and bow. Both broad skins now have explicit outward normal targets.

The old capped black cylinders are removed. The black/chrome rolled profiles and lens planes derive from the same local field depth. This places the lens within a real opening, behind the adjacent field, instead of mounting the complete assembly forward of the field. Flutes follow the relocated lens crown.

Central grille art/UVs, rally lamps, medallions, AMX trim, outer silhouette, fender crown, moving hood seam, valance and `build_mod.py` bumper remain unchanged. This is deliberately the first geometric slice, so their outstanding visual findings still apply.

## Captures and visual review

All paths below are under `build/front-fascia-cycle4`:

| View | Before | After |
| --- | --- | --- |
| Estimated target front, paint | `before/target-front-paint.png` | `after/target-front-paint.png` |
| Estimated target front, clay | `before/target-front-clay.png` | `after/target-front-clay.png` |
| Front detail, paint | `before/front-close-paint.png` | `after/front-close-paint.png` |
| Front detail, clay | `before/front-close-clay.png` | `after/front-close-clay.png` |

The target-front pair uses identical914x523output,50mmcamera,36mmsensor, position and target. The close pair uses identical1100x800orthographic settings. `review_trial.py` retains those settings and `comparison.json` records saved-source hashes and sampled lens evidence. These cameras remain estimates, not calibrated reference matches.

Vision review confirms a visible pocket and rolled edge around the outer lenses in the after captures. Clay exposes that physical recess independently of the gray lens shader. The grille/bumper still reads relatively rectangular and the fender-to-nose transition remains abrupt against the video. Those defects are outside this patch. The trial's darker lamp appearance is not independently evidence of native headlight quality.

## Verification

- Isolated build completed. `build.log` records the169766triangle output.
- Existing isolated unit suite:32tests pass, `unit.log`. Initial fixture failures from the absent Lua file were resolved by supplying the existing fixture file, then the suite passed.
- Full saved-model pose gate passed, `pose.log`: normal orientation, semantic lamp zones, factory dimensions, attachment registration, steering clearances, upholstery support and ten actual hinge fractions. These checks are source geometry evidence.
- Native importer passed, `import.log`:11resolved meshes and three expected clips. This is importer evidence, not native visual inspection.
- `review.log` records existing saved-model surface audits passing for both baseline and trial. The checker reports252closed components for the baseline and247for the trial; it checks closed-component winding but does not establish that all surfaces are manifold.
- Proposed durable saved-mesh regression: `front_lamp_regression.py`, suitable for integration into `check_vehicle_placement.py`. It rejects the frozen baseline because shadow caps span the openings. The trial passes eight rays across both semantic headlamp lenses, outward normals, absence of spanning front/back shadow fields, and9.829..17.029mmrecess relative to the actual adjacent field. Threshold is8..25mm, scoped to this trial's intended recess, not represented as a measured factory dimension. `aperture-regression.log` preserves both outcomes.

Reproduction from the project root:

```powershell
& 'C:/Program Files/Blender Foundation/Blender 5.2/blender.exe' --background --factory-startup --disable-autoexec --python-exit-code 1 --python build/front-fascia-cycle4/build_trial.py
python -m unittest discover -s build/front-fascia-cycle4/tools -p 'test_*.py'
python tools/check_model_pose.py --blend build/front-fascia-cycle4/assets/Javelin73PC.blend
python tools/check_fbx_import.py --game C:/Games/ProjectZomboid --package build/front-fascia-cycle4/Javelin73PC --manifest build/front-fascia-cycle4/assets/model-manifest.json
& 'C:/Program Files/Blender Foundation/Blender 5.2/blender.exe' --background --factory-startup --disable-autoexec --python-exit-code 1 --python build/front-fascia-cycle4/front_lamp_regression.py
```

## Remaining gate and DOX

Root review precedes promotion. Native game appearance, light activation, surface visibility from both sides and front, and moving hood inspection remain required after promotion/export. This isolated trial was not installed or launched.

Root and `tools/AGENTS.md` were re-read. The geometry patch has not changed the active tools contract. Root instructions remain unchanged because this document records development evidence under existing ownership. If promoted, update `tools/AGENTS.md` to name the actual front apertures and their saved-mesh regression alongside the existing rear-lamp contract.

## Authoritative first-slice integration

Root inspected the matched before/after paint views and integrated the aperture patch into the real generator. The169,766-triangle saved build passes32 unit tests, static validation, native11mesh/3clip importing and the complete pose gate, including the new eight-ray actual-fascia recess regression. The previously installed/native-inspected167,134-triangle checkpoint remains separate; this later front geometry is not yet installed or natively reviewed. Asset/tool contracts now name the actual apertures and support checks. All front-end and other sections remain open.
