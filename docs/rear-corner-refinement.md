# Rear corner closure investigation, cycle 7

All sections remain open. This isolated task diagnoses the symmetric dark arrow shapes beside/below the outer tail lamps. Native 214,322 remains under root control; no UI, profile, installation or canonical source was changed here.

## Four fresh reference comparisons before construction

1. Re-examined target `reference-22.png` against the exact source rear orthographic. The photographed red tail field remains continuous below and outside the outer lamps until the chrome bumper. It does not contain the source's deep black wedge. The tight target crop limits the far outer corner, so it does not independently recover the hidden return depth.
2. Re-examined `build/six-pass2/druk-002.jpg` against the source right corner. The supplemental rear-quarter image shows a narrow panel seam and continuous painted material over the bumper return. Reflections and the differently finished roof are not target colour authority. A broad open arrow is not supported.
3. Re-examined opposite-quarter `druk-004.jpg` against the source left corner. Its painted lamp-to-quarter transition remains enclosed above the bumper, confirming that the first side is not merely hiding an intended opening. Preserve the target lamp apertures and moving trunk rather than covering the whole fascia.
4. Re-examined low close `druk-032.jpg` and rear close 040, then target 22 again against the source orthographic and existing rear-quarter paint capture. These show real dark seams/recesses and lamp wells, but continuous lower corner sheet metal. No photograph calibrates the unseen flange dimensions. The intended correction is continuity of the existing lower body panel at its shared fascia edge, not a generic added block or a paint/normal workaround.

## Saved-mesh diagnosis

Frozen exact 214,322 source, SHA-256 `c9c25499d084ded7bfe8910375247a9be5568f0c3235bce57166656dc01216c8`. `before-rear-ortho.png` reproduces the symmetric arrows with backface culling enabled. `rear-rays.json` records actual hits with semantic UV zone/colour, normals, face indices and vertices.

At source X=.84 and Z=.56/.58/.60, rays from rear Y=-3 toward +Y pass through the tail and first hit original black front engine housing Body faces 43905/43904 near Y=+1.055..1.082. At X=.82, Z=.58 a ray also reaches that front housing. Neighbouring fascia hits are red, guardrr and rearward facing. Thus this is an actual missing rear surface, not proof of incorrect paint normals or a native shader bug.

The existing lower rear `rounded_plate` has a top contour rounding down toward its outer tips. The independent tail fascia lower contour rounds up at those tips. Their incompatible outlines leave a wedge. The central outlines overlap slightly, also producing a separate dark horizontal seam in this source view. Passing closed-component winding checks does not detect a gap between two separately closed components.

## Localized proposal

The isolated copied `javelin_rear.py` supplies one shared `rear_fascia_depth` and `rear_fascia_half_height` boundary to the lamp fascia and rebuilt lower rear panel. The old standalone `rounded_plate` call is removed from copied `build_mod.py`. The replacement lower panel retains the prior lower rounded profile and 150 mm forward return, while its upper edge meets the actual fascia at every transverse station. Its half-width is reconciled from 845 mm to the fascia's 850 mm. These are existing model-construction coordinates, not recovered factory measurements.

The lower panel's front follows the existing bowed fascia depth rather than intersecting it as an independent flat block. The fascia's redundant bottom caps at the shared edge are omitted; the lower return starts from its 18 mm inner skin, avoiding an internal coplanar cap overlap at that interface. No overlay cover is added. No paint swatch, mask, normal target, lamp, bumper or moving trunk is changed. A render-stop after saving appears only in copied `build_mod.py` for isolated execution and must not be promoted.

## Verification

- Final trial 215,002 triangles (+680 versus 214,322), SHA-256 `6f0fa35569cf9be70a54d1610eaf248fcd07be829da111e42c64ec34b1d6f85d`.
- Proposed callable-only guard `rear_corner_guard.py`, `check_rear_corner_closure(atlas)`, casts 4,182 actual rear rays over both defect regions. Exact baseline fails 1,256 rays, including remote black engine-housing hits. Trial has 0 failures: every ray hits a red rear-facing tail surface before Y=-2.25, with rearward normal Y<-.95. No lid/body pose or file is changed by the guard.
- `scope-report.json` confirms all ten other mesh coordinate/topology digests unchanged. The coordinate/material face sets of 1,507 nonpaint rear lamp/bezel/bumper/plate faces are identical. Actual saved rear-lens rays retain their original 15..45 mm recess gate.
- Full `pose.log` passes original source geometry, normals/closed-component winding, lamp/cup/backlight/cargo/interior checks, native wheel/rest/steering and ten intermediate moving-panel fractions. The moving trunk clears the rebuilt fixed panel. No check or tolerance was relaxed.
- Final 32 unit tests pass, static validation reports 0 errors, and the installed game's native importer resolves 11 meshes and 3 clips. This importer check does not render a native vehicle.
- `before/` and `after/` contain identical-camera rear orthographic, both low corner closeups and full rear quarter, in paint and opaque clay with backface culling. Visual inspection confirms both wedge holes and the central lower-panel overlap line are removed. The quarter/fascia seam and broader rear likeness remain open; this is localized closure work.
- Source geometry alone establishes the hole cause, so no native shader hypothesis or paint/normal workaround was needed. Native confirmation of the exact trial is a separate root gate. No UI/profile/game file was edited by this subtask.

## DOX pass

Root owns this research record. Owning AGENTS documents intentionally unchanged for an unpromoted isolated construction trial.
