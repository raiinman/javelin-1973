# Dashboard volume trial

Isolated cycle5 trial, not promoted. Canonical source is the187,836-triangle Blender checkpoint SHA256 `363dfc71f833875a3c94f577bb094d19e52db2c9f2a1d82240629327871fccbf`. All dashboard/interior sections remain open; no fidelity score is assigned. Parent rejected the first candidate's cylindrical passenger pad. The second pass is now rendered and verified for parent review.

## Four fresh reference comparisons before implementation

1. **Target reference-47.png:** fresh visual inspection confirms the padded circular horn boss, broad slotted metal spoke and white manual-shift ball. The close crop gives no authority for full dash depth. Current original geometry already supplies these identity features; retain them unchanged. Do not use the supplemental automatic selector as target authority.
2. **Druk107/109 assembled dash:** fresh inspection of both full photographs shows a thick continuous rounded brow across the driver cluster, a substantial rolled lower ledge and a near-vertical central shoulder into the passenger pad. The existing generator uses two mostly constant-depth rounded blocks and a straight top slab. Correct the padding's large cross-sections while retaining fascia holes, original dial artwork and wheel registration. These oblique photographs are uncalibrated and do not establish millimetre dimensions.
3. **Druk117 gauge close-up:** the upper padded lip is a broad rounded bead, separated by a narrow dark reveal from the silver fascia. The three gauge apertures are rounded squares in one curved metal field, with a bowed lower control line. Preserve the original perforated fascia and dials while reshaping its surrounding pad. The right-hand clock in this supplemental car is not proof of the target's right dial; no instrument identity replacement is authorized by this view.
4. **Druk140 passenger cabin:** the passenger pad slopes down from the windshield, has a central shoulder, a vertical end vent and a projecting curved horizontal handle beneath a continuous bright boundary. The glovebox is a lower panel rather than a second padded rectangular top block. Current passenger geometry is a rounded cuboid with a tiny dark bar. Replace the major silhouette and add a real projecting handle with visible return supports. The image's automatic selector is excluded; hidden dash construction remains inferred.

Local supplemental evidence: `build/six-pass2/druk-107.jpg`, `druk-109.jpg`, `druk-117.jpg`, `druk-140.jpg`; target `reference-47.png`. These are four fresh comparison groups covering all five requested images, not four complete webpage analyses. Source code and fresh before/after captures will provide the model side of these comparisons. Camera estimates are diagnostic and are not optical matches to the photographs.

## Scope and validation

Only copied generator files and outputs under `build/dash-volume-cycle5/` are writable for the trial. Parent review controls any promotion. Preserve native driver attachments, moving door/release clearance, original artwork, white manual ball and metal three-spoke wheel. Source pose/clearance checks and cutaway renders are separate from native-game visibility and geometry parity.

## First candidate, parent rejected

- First trial source is preserved at `build/dash-volume-cycle5/rejected-pass1/javelin_cockpit.py`. Only the copied cockpit generator module changes geometry. `_pad_loft` supplies closed, rounded cross-section sweeps; the driver brow follows the existing transverse fascia bow and projects over its reveal. The passenger padding attempted a broad front, rounded top fall and deeper centre shoulder. A bowed handle stands off the pad with two return supports above a shallow lower glovebox. Its end vent moves cabinward to remain visible on the reshaped surface.
- Original `build_steering`, `build_cockpit`, `dashboard_face_y` and `_rounded_outline` functions are AST-identical to the baseline, recorded in `checkpoint.json`. Static dials/artwork, wheel, manual ball and native script attachments were preserved. No clock/automatic equipment was added.
- First saved trial is preserved at `build/dash-volume-cycle5/rejected-pass1/Javelin73PC.blend`, SHA256 `c30c499997cc85aa50fec26d3b9d81f42fe6ba8423e47447624e180de19fb37b`,195,436 triangles, alongside its cockpit module and rendered `after/` views. The added7,600 triangles are largely the padding sweeps and handle. No game-performance approval is implied.
- Fresh baseline and final views share the same fixed cameras: `before/` and `after/`, each containing `dashboard-front.png`, `dashboard-quarter.png`, `dashboard-passenger.png` and `whole-cabin.png`. `after-clay/` holds the same views with a neutral override. `review.py` removes the roof/headliner in memory; close dash cutaways additionally remove rear/floor geometry. The whole-cabin view retains both door cards and all seats. No review script saves its scene edits.
- First review rejected an overly rounded passenger section and a separate central upright that created a visible protruding nub. The final trial flattens the passenger front, removes that upright, and reseats the vent. Final passenger, quarter and whole-cabin images show the bowed handle's real gap and a more rounded driver brow than the initial cuboids.
- `pose.log` passes the full saved-model pose gate, including native seat/steering registration, all visible wheel clearances, sheet facing/component windings and ten hinge fractions with fixed cabin/door/glass clearance. The saved trial was reopened in fresh Blender processes for review and verification. This is source evidence, not native animation playback.
- `checkpoint.json` freezes copied Python modules, baseline source and final blend hashes, unchanged-function checks and reproducible commands. `build_no_render.py` is the copied build script with preview render calls suppressed; `build_mod.py` remains available as the original copied runner. Generated assets and FBX stay in this disposable trial.

## First candidate limits

The centre-side cheek still uses the existing fascia housing; the real continuous padded return and exact junction remain approximate. The passenger end is a closed sweep cap, not a recovered factory moulding. Its top slope, vent size/position and handle thickness are inferred from uncalibrated supplemental photographs. Silver fascia relief and dial numerals remain simplified. Studio highlights emphasize new curvature but do not prove native paint/fabric lighting or accurate likeness.

The large driver brow now reads as a rounded projecting pad, and the passenger handle has real depth, but the trial is not a claim of target parity. Parent must compare the final cutaways to Druk107/109/117/140, inspect whether the broad pad has become too inflated, and integrate only the copied cockpit module if accepted. Canonical geometry changed independently during this isolated task; do not replace the newer whole model or promote the whole trial package over that work.

Native interior visibility, multi-angle game appearance and all reference-parity section gates remain open. No profile hook, UI operation, canonical source change or native installation was performed by this trial.

## Second pass ready for parent review

The copied `tools/javelin_cockpit.py` and `assets/Javelin73PC.blend` now contain the final second pass,200,164 triangles. It steps the broad passenger face toward the windshield, makes the tall central cheek part of one continuous closed sweep, and seats an original horizontal vent against the cheek's actual front function. Its cross-section uses a wide planar front and a sloped upper surface rather than the first pass's circular-looking extrusion. The manual/wheel/dial functions remain AST-identical to the baseline.

Final second-pass blend SHA256 is `3f2abb9b3db83980beb753c146f8ce9c817bc71fd2a9e0f4bdd1a60d1c3a2d12`; cockpit module SHA256 is `9e709dfb8a1d67aa56a553cdcd24c9a53f05a091b154dc2f4c48aced7d025a8e`.

Fresh `after/` front/quarter/passenger/whole-cabin views, `after-clay/`, `pose.log` and `checkpoint.json` now describe this second pass. The full saved-model gate again passes, including all four native seat/steering registration checks and ten moving-panel fractions against fixed cabin/adjacent glass. Fresh Blender processes reopened the saved candidate for these checks.

The initial second-pass centre vent used nonplanar spanning polygons that cut through each other's offsets. Visual review rejected that artifact. Its final chrome/dark bezel uses surface-following quad strips and its black field uses32 narrow strips following the cheek, avoiding a planar plaque across the curved support. This is shallow original geometry, not a copied photograph or a claimed functional HVAC opening.

Fresh comparison of final `after/dashboard-passenger.png` with the full actual `references/druk-140.jpg` confirms the correct *type* of central vent cheek, the step into a shallow broad passenger face, vertical outer vent and bowed physical handle. The whole cabin shows the step's depth independently of the close crop. Shape/size still remain inferred: the driver's right brow return is a separate existing housing junction, the cap at the outer end remains simplified, the real padding's subtle cloth grain and lower central stack are incomplete. These are improvements to the rejected volumes, not an asserted match or likeness score.

The five actual reference images are copied unchanged under `build/dash-volume-cycle5/references/` for side-by-side review; their original source boundaries remain those recorded above. Do not promote the whole trial package: parent cargo and runtime-activation fixes advanced independently after the frozen187,836 baseline. Parent should compose only the reviewed cockpit module into its latest source and rerun integrated gates/native review.

DOX pass: root owns `docs/` and this disposable build record. No durable project ownership or operating rule changed; root/tools/assets AGENTS.md intentionally remain unchanged. No trial module is added to the distributed package.

## Root second-pass promotion

Root compared final second-pass passenger and whole-cabin views against actualDruk140. The central vent cheek and broad passenger face improve the rejected cylindrical first pass. An independent reviewer agrees while retaining the abrupt upper-pad junction, rectangular driver fascia and simplified lower stack as defects. Only the cockpit module is promoted over the frozen202,046backlight source, retaining cargo closure and the original runtime init callback. Canonical combined clearances and native appearance remain separate checks. No section closure or likeness percentage is assigned.
