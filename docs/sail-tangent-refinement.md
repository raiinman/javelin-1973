# Sail tangent refinement

All sections remain open. This record proposes a source correction; no numerical likeness score or native-game approval follows.

## Four fresh comparisons before correction

1. Compared `assets/javelin-rear.png` with `reference-2.png` and `reference-30.png`. The target frames establish roof and side continuity but obscure most of the aft quarter light. They cannot locate the aft tip or calibrate the sail curvature. The source render shows a concentrated highlight immediately behind that tip.
2. Compared `build/parity-cycle1/rear/rear-quarter.png` with `reference-side.png`. The supplemental side photograph has a broad uninterrupted painted sail and swept quarter-light opening. The source has a triangular reflection fan, despite a continuous perimeter. The cameras differ; the photograph does not justify moving the existing roof or glass anchors.
3. Compared the same source rear-quarter with `build/six-pass2/druk-032.jpg`. The supplemental car's shoulder rolls broadly into the quarter flank. Its vinyl roof boundary is trim, not evidence of a painted crease. The source highlight pinches into its lower sail join.
4. Compared `assets/javelin-rear.png` and the closer rear-quarter with `build/six-pass2/druk-034.jpg`, cross-checking `reference-22.png`. The rear close photographs do not expose the quarter-window tip. They do show a continuous painted quarter with a tighter rear return. They support retaining an uninterrupted shoulder, but cannot establish the hidden sail derivative or a measured radius.

## Cause and proposal scope

The surround and sail use coincident positions at the tip but different longitudinal derivatives. The surround adds the frozen tip-section residual to moving edge/glass chords; the sail adds it to a moving sinusoidal section. Equal endpoints therefore do not establish a shared tangent plane. At the lower haunch, the sine section tends to zero lateral derivative while the side skin has a nonzero lateral derivative with height. These are actual geometric differences, independent of smoothing flags.

The isolated proposal and derivative probes live in ignored `build/sail-tangent-cycle3/`. Shared `tools/build_mod.py` and `assets/Javelin73PC.blend` remain owned by the integrating agent.

The proposed tip cross-section is piecewise cubic Hermite. Its middle tangent equals the actual affine quarter-glass X/Z slope. A local longitudinal correction makes its fixed-height fore/aft slope equal the glass slope at the collapsed aperture tip. Both surround bands then evaluate this same scaffold and seat their exact glass edge with a cubic weight. Setting only the longitudinal derivative failed because the former transverse middle tangent did not equal the glass slope.

The lower sail gets a geometric endpoint-tangent correction against the actual side skin from Y=-.85 through -1.35, fading smoothly to zero at -1.52. Every glass/perimeter anchor stays fixed. The aft section at and behind -1.52 stays exactly unchanged under the existing regression contract, so the remaining aft side/sail tangent difference is explicitly unresolved.

## Isolated verification

- `prepare.py` extracts actual generator functions using AST and checks 16 mirrored upper/lower seam probes in fixed-height coordinates. Maximum surround/sail slope difference drops from .757976 to .0000562 m/m at a 1 micrometre finite-difference step. These are derivative differences, not likeness measurements.
- Both mirrored seam and glass anchors are preserved within 1e-12 metres, and the tested aft sections at -1.52, -1.72 and -1.87 are unchanged within 1e-12 metres.
- `haunch-derivatives.json` records actual side and sail X/Z slopes. At the tip on the negative-X side, the former sail slope .736966 changes to .061888 against side slope .061894. The mirrored side agrees by sign.
- Isolated geometry, source blend and paint captures are redirected to `build/sail-tangent-cycle3/`. The initial derivative-only render improved the tip but exposed a stronger lower-haunch reflection, so it was superseded by the endpoint-tangent correction. That first render is not acceptance evidence.
- Integration needs an updated AST loader in `tools/test_sail_surface.py` for the factored `sail_base`, `tip_section` and measured derivative setup. Existing affine mock-edge tests alone do not exercise the actual side-skin tangent. Keep the saved-mesh quarter-tip four-face, culling and panel-clearance checks.

Native-game inspection remains pending. The source proposal is not a completed sail or whole-car likeness gate.

## Broader volume trial

The integrating agent rejected the derivative-only candidate after reviewing its reflection. The old unchanged-aft regression describes an authored shape, not factory evidence. A second, isolated trial replaces that construction with `rear_quarter_surface`: one cubic cross-section from roof/backlight border to the side skin, including the sail, surround and aft glass. Its lower tangent follows actual side-skin slope. No fixed tip-section residual or aft residual fade remains.

`build/sail-tangent-cycle3/radical-proposal.patch` supplies this trial. The lower patch boundary now spans a broad section of flank, with up to130mm drop and exact original endpoints at the rear door and deck. The quarter-light tip moves100mm aft to Y=-.95; intermediate perimeter controls extend proportionally. This is an explicitly reversible, uncalibrated side-photograph hypothesis, not a recovered factory measurement. The front quarter divider and belt anchors, roof/backlight, door, wheelbase, vehicle length and deck endpoints stay fixed. Aft glass seats on the shared surface; its lateral position therefore changes.

The new paint capture `radical-sail.png` visibly removes the concentrated tip fan and the strong lower triangular stripe from `before-sail.png` and `after-sail.png`. `radical-side.png` shows the longer quarter opening and preserved main-window/roof silhouette. A small bright ledge under the forward fixed quarter light, broad aft shoulder reflection, glass curvature and exact window outline still require review. The earlier source-only candidate is superseded, not accepted.

Reopening the isolated saved blend in a fresh Blender process passed the existing exterior subset:24 mirrored shoulder culling rays, all eleven positive object bases and closed-component winding checks, quarter tips sharing at least four sail faces, all seven lower-backlight/apron columns, closed-window frame/divider proximity, three rig clips and all ten moving-panel clearance fractions. Full `check_model_pose.py` stopped in the separate interior cushion-support check before the later exterior checks; that failure is recorded in `pose-radical.log`. `exterior_pose.py` explicitly omits that combined placement/cabin call and passes the remaining exterior and motion checks, recorded in `exterior-pose-radical.log`. This does not claim full pose or native-game approval.

## DOX pass

This is a root-owned development record. It changes no workflow, package output, source ownership or existing aft-surface contract. Applicable root, tools, assets and reconstruction AGENTS files were read and intentionally left unchanged. Any integrated change to the unchanged-aft-surface or sail regression contracts requires the root agent's corresponding tools contract update.
