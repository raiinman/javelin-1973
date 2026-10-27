# Reference camera fit, open evidence

The fixed-geometry camera solve substantially improves full-frame registration, but does not calibrate the real lens or establish vehicle likeness. All sections remain open. The numerical residuals below are landmark errors, never a parity percentage.

## Inputs and reproducibility

- Target video captures: `reference-2.png` and `reference-30.png`, both 914 x 523 pixels, square pixels, no EXIF. Preserve the black frame bars and subtitles, with no alignment crop.
- Saved source: `assets/Javelin73PC.blend`, SHA256 `141cef8216124b362d24effa308aaa0986cf88f1eed9a8c052bb5d01cf1d5b3e`, Blender 5.2.1 LTS. No model or source-camera changes were saved by this review. The parent refinement subsequently changed the source file, so these renders are a hash-specific checkpoint, not proof of the later source appearance.
- Skill: installed `img2blender`, specifically `references/camera-and-landmarks.md` and `references/blender-execution.md`.
- Reproduction: `python build/parity-camera/fit.py`, `python build/parity-camera/fit_contacts.py`, then background Blender with `build/parity-camera/render.py` or `render_contacts.py`. Temporary scripts, fits, overlays and full-frame paint/clay renders stay in ignored `build/parity-camera/`.
- Fit uses SciPy least-squares, three initial seeds for the balanced and fascia-priority trials, fixed source point positions, a perspective camera, 36 mm sensor width and 7 fitted camera/framing variables. No geometry deformation is fitted.

## Landmarks and uncertainty

The four visible front lamp centres are readily identifiable within roughly 3 to 6 pixels. Their model positions are explicit generator coordinates, but their real lateral spacing, grille bow and depth remain shape-sensitive. Windshield corner junctions are identifiable within roughly 4 to 8 pixels, but model aperture width/rake is uncertain. Those eight landmarks constrain a useful comparison pose, not a metrically calibrated camera.

Neither frame exposes both wheel hubs clearly. Frame 2's near front tire hides its hub behind the body, and the near rear wheel is an extremely narrow dark sliver. Therefore no measured wheel-centre solve is claimed. A second frame-2 trial uses visible tire-ground contact proxies at (235,449) and (176,230), fixed existing 2.79 m axle spacing, and the source 0.33 m rolling radius. Contact position and tire steering introduce at least 8 to 15 pixels of uncertainty. Frame 30 has an open door and person masking the rear tire; those silhouettes are excluded.

## Candidate cameras

All coordinates are saved Blender source coordinates, including its -0.65 m chassis offset. Look targets use fixed X=0, Y=0.4. Apply roll in camera-local Z after `to_track_quat('-Z','Y')`. Sensor fit is HORIZONTAL, resolution 914 x 523, shift_y=0.

| Candidate | Camera XYZ | Look target Z | Roll radians | Lens mm | shift_x | Unweighted landmark RMS px |
|---|---|---:|---:|---:|---:|---:|
| Frame 2, balanced | 0.907182, 3.622512, 0.635985 | -0.572273 | -0.007153 | 22.6855 | 0.099862 | 8.06 |
| Frame 2, fascia priority | 0.857330, 3.371280, 0.572750 | -0.659618 | 0.010090 | 19.2342 | 0.104823 | 11.15 |
| Frame 30, balanced | 0.825377, 3.830721, 0.642986 | -0.347210 | 0.040431 | 22.5883 | 0.062469 | 8.24 |
| Frame 30, fascia priority | 0.805495, 3.649429, 0.601332 | -0.384501 | 0.055397 | 20.3492 | 0.066264 | 9.70 |
| Frame 2, tire-contact proxy | 1.164200, 4.558189, 0.843375 | -0.391951 | -0.042841 | 36.6526 | 0.104502 | 22.96 |

The principal-point shift is a framing/crop variable, not evidence of a physical shifted lens. Reported focal lengths are effective equivalent hypotheses. Unknown video crop, lens distortion, rolling attitude, steering and uncertain model point positions prevent recovering unique intrinsics.

Balanced frame-2 errors: near headlamp 2.5 px, near rally lamp 3.5, far rally lamp 6.7, far headlamp 6.3, near windshield base 6.0, far windshield base 12.7, near windshield top 8.7, far windshield top 11.9. Frame-30 errors respectively: 1.2, 1.1, 5.3, 5.2, 7.9, 10.2, 8.5, 15.7 px. Full coordinates are in `build/parity-camera/fit.json`.

## Four fresh complete image comparisons

1. **Projection inventory:** reviewed both full target frames and the existing `front-muscle-review/target-frame2-estimate-paint.png` and `target-frame30-estimate-paint.png`. The old 50 mm estimates use 914 x 518 rather than the actual 914 x 523 frame. Their roof centres sit too far right and low. Frame 30's open door/person is an explicit visibility difference. The old captures cannot independently justify proportion corrections.
2. **Landmark review:** rechecked both full reference frames against the balanced full-frame numerical overlays. The eight lamp/aperture points can register within approximately 8 px RMS with fixed geometry, but the four nearly collinear lamps alone cannot determine the full camera. Coherent windshield-corner residuals remain. No cropping, silhouette resizing or point-specific body motion was used.
3. **Material-independent review:** reviewed both full reference frames against `frame2-balanced-paint.png`, `frame30-balanced-paint.png`, and frame-2 clay. Much of the previous roof-framing discrepancy disappears under the fitted pose. The target's grille/rim and lower valance have curved volume, while the current render still reads as a broad recessed insert, flat chrome lower bar and planar low chin. Hood/fender transition and black-T curvature still differ. Opaque clay glass cannot assess cabin appearance. The model mirrors still have visibly large pale faces in these renders; later source revisions require recapture before judging their orientation.
4. **Anchor stress test:** re-reviewed both full frames, all balanced captures and the frame-2 tire-contact trial. The balanced camera predicts front/rear near-side ground proxies approximately (258,375) and (225,213), versus observed (235,449) and (176,230). Including contact proxies changes effective lens from 22.7 to 36.7 mm and leaves about 25 px front-contact error, 15 px rear-contact error and 17 to 45 px windshield errors. Its full render makes the source cabin broader than the target. Frame 30's hidden contacts cannot resolve the disagreement. This strong camera sensitivity prevents treating either fit as the final proportion authority.

## Next use and limits

Use the balanced pose for a reproducible front fascia/hood comparison and retain the contact-anchored pose as a sensitivity view. Lock both while judging a geometry change. Do not select whichever camera flatters an iteration. The main unanswered distinction is cabin/front-overhang proportion versus target wheel placement/steering and lens calibration. A clearer target side or wider front-quarter frame showing both near-side wheel hubs should arbitrate it before moving axles or narrowing the cabin. Supplemental cars may supply shape evidence but must not silently replace target-specific proportions or equipment.

These captures do not cover the entire exterior, cabin, underside, moving clearances or native game appearance. They cannot close a section or demonstrate the user's requested overall threshold. DOX pass: root owns `docs/`, no new boundary or operating contract was introduced, so owning AGENTS files are intentionally unchanged.
