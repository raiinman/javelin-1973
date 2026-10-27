# Front terminal assembly refinement

Canonical composition is now231893tri, SHA256`7985de86a18e3e0df4b6d1ba0299487d8b27ba394173213a4d9998147e676167`, loaded in the user's Blender. Root all36unit/static/parser/import/pose gates pass; composed20body captures and independent saved rear/nonBody audit are in `build/current-front-cycle11/`. The one-triangle front-decal weld sliver and bounded rear chrome rounding are documented there. No current native visual review is claimed. Broader fender width/crown/graphic span remains unresolved and is now the ONLY active refinement area. Seat and A-pillar work is stopped.

Isolated work in `build/front-nose-cycle10`, 18 October2026. All sections remain open. No canonical model, source, package, profile or UI mutation. The starting saved model is222146, SHA256`f13f3b43e1b4da9f5c8a88efec16cec8b5ff9e24deb920982ffb1aeddc318168`. All66 initial checkpoint files were verified while copying; the complete69input checkpoint supplies the three missing validation dependencies, recorded separately in `auxiliary-inputs.json`.

## Fresh comparisons before the first bounded slice

Four sheets named`*-before-evidence.png` contain every full target2/30 and Druk000/025 frame plus the actual canonical paint/clay pair. Original resolution references were also reopened. Cameras and photographs remain uncalibrated, with no pixel-derived dimensions.

1. Target-frame2 estimate: both target frames show an upper outer-lamp roll; Druk000 gives the long-wing context and025 resolves the rolled margin. Canonical clay retains a narrowing crown behind a straight-looking cap. Paint amplifies it but does not cause it.
2. Target-frame30 estimate: the same four references support continuous terminal shoulder volume from the other target framing. The model loses that shoulder before the lamp end. The open door/person and viewpoint prevent measured hood-length or height conclusions.
3. Full front-quarter: target2/30 retain target equipment authority; Druk000/025 support sheet-metal continuity only. Current long-wing volume is already substantial. A local trial must preserve the main crest, cowl, hood length, axles and envelope.
4. Fender close: all four full references were compared again.025 shows the graphic riding a rounded support. Clay exposes the model's thin terminal cap. Reflections do not recover an exact radius or normal field.

## Two rejected wing-only slices

Both preserve the Hood and central fixed strip, front module and all ten nonBody meshes. First trial adds a local zero-value/zero-slope bump over2.10..2.39, plus shared stations. It adds6.69..9.11mm at savedX.80/Y2.19..2.25 but only1.92mm at2.34 and effectively zero over2.365..2.385. This is more middle fullness, not a sufficient terminal roll. Its files and captures remain under`first-trial`.

Second trial moves the local support forward with a nonzero terminal descent. AtX.80 the measured gains are6.258mm atY2.34,3.789mm at2.365 and.938mm at2.385. It improves that distribution but fails actual outermost-surface visibility. AtX.78/Y2.385 the unchanged fascia black upper return isZ.777346, the red support.773400 and its decal.774200. The fascia buries support/decal by3.946/3.146mm. AtX.80 the same fascia is only.247mm below the red support. Red-only rays would hide this crossing. Both trials are223096 triangles, compared with222146 canonical. The initial saved guard rejects both and the baseline. The second trial is retained under`second-trial`.

This establishes a construction conflict between independent wing and fascia upper-return boundaries. It is not evidence of broken native normals. No hood or central-strip change was justified.

## Four fresh comparisons before the authorized assembly slice

After the two rejects, parent authorized the terminal fixed wing plus fascia upper return and adjacent fixed-side termination, with a shared curved boundary. Four new`*-expanded-before.png` sheets were freshly inspected before that patch. Each again contains all four full reference photos, canonical paint/clay and second-trial paint/clay.

1. Target2 estimate: target2/30 and Druk000/025 still show a rolled lamp end. V2 adds shoulder support but preserves a distinct leading cap. The buried graphic support is a geometric obstruction, not a reason to change the photo camera.
2. Target30 estimate: the same complete reference set confirms the residual terminal flattening from another locked view. V2 is not accepted merely because its middle shoulder reads fuller.
3. Full quarter: all four references keep the broad envelope constraint. V2 changes a very local run; no basis appears for a global height or hood-length change. The expanded correction must remain in the last fixed assembly.
4. Fender close: all four references distinguish the real rounded painted support from a graphic placed over a platform. V2's cap obstruction explains the surviving kink. Replace the conflicting upper-return construction with one shared edge rather than layering another cover over it.

## Assembly trial and source verification

The assembly slice keeps the original lamp apertures, original fascia columns and outline, recess walls, lenses/bezels, bumper/valance and moving Hood. The original front outline/columns/bounds/depth are factored into shared read-only functions. Wing terminal rows now turn into that exact fascia upper edge. Existing fascia front faces receive only extra vertices along their upper perimeter so that the saved boundary can weld; their aperture vertices and closed walls are retained. The conflicting upper return is removed where the wing now owns the outer sheet. Adjacent outer corner return and fixed upper side termination are explicitly included in the expanded scope.

The inferred roll starts atY2.34 with the existing wing position/tangent and uses a depth curve ending with a vertical terminal tangent into the front field. No global roof/fender displacement or camera compensation. Fender graphics use the same actual support triangles at.8mm vertical clearance. Their terminal parametric boundary is shortened to retain a physical painted forward margin after the changed depth parameterization. The centre fixed-strip artwork stays unchanged.

The final isolated saved blend is230318 triangles, SHA256`677b8780cae707bc85fd4155dc102c03ecca72da152592b9f5e877c236e66b83`. This is an incremental local improvement suitable for independent composition review, not a completed nose or overall likeness claim. Native review remains parent's separate gate. Source captures and parser/import checks are not native driving or visual approval.

### Final visual review

The four`*-final-comparison.png` sheets retain the complete target2/30 and Druk000/025 frames, canonical paint/clay and final paint/clay. The final close clay has a continuous downturn into the lamp end instead of the V2 crossing cap. Both front quarters support that local improvement. The balanced frame2/frame30 and contact-anchored frame2 locked cameras retain it without camera compensation. The full side/top sheets show the existing long hood, ride position, width and roof intact. All renders retain whole model frames; the `fender-close` inspection camera is explicitly a detail view accompanied by full reference and whole-car views.

The model still has broad front identity differences. The grille/nose assembly and bumper proportions remain more planar and different in mass distribution than the supplied car. The T graphic and hood-to-fixed-strip transition remain conspicuous. The hood and centre strip were intentionally preserved. Those broader issues are open, not a reason to call the local roll complete. Druk's differing equipment is not adopted. Coordinates, the radius distribution and the.70m fixed-side blend boundary are inferred, not measured factory construction. Clay is reviewed directly; passing a25degree rejection ceiling does not establish a photo-derived tangent.

There are22 before and22 after body captures, plus three locked paint/clay pairs before and after,56 total. `before/body/report.json`, `after/report.json` and both `camera-fit/source.json` files identify exact saved inputs and unchanged cameras. Ten comparison sheets combine these with uncropped references. `comparison-inputs.json` hashes the images used.

### Saved guards and preservation

- `check_front_nose_terminal(atlas)` is a callable read-only guard. It opens/writes no files and needs no historical baseline. Its58 probe rays trace the entire actual Body and retain the outermost hit, including any elevated black return. Two out-of-domain probes atX.82/Y2.388 are skipped because they lie beyond the immutable bowed fascia depth. This is a geometric domain limit, not a semantic exclusion. No upper-hit Z filtering remains. Mirrored support positions must agree within2micrometres.
- The actual final first-hit support has zero cap occlusions. All12749 graphic samples (face centres and inset corners) find actual red support at0.798956..0.800923mm, and no other Body surface above the graphic. These samples cover the complete forward fender graphic, not just its terminal outline.
- Each side has14 two-owner support edges at the shared hood-end row and59 welded red/fascia front edges. Maximum saved face turn is3.359degrees at the support row and6.643degrees at the front seam. The guard rejects a front fold above25degrees; the measured result is substantially smaller and was separately reviewed in clay. Initial underresolved cap rows failed this guard. Final stations are rounded to avoid duplicate endpoint floats, and the cap includes the original fascia column samples through the roll.
- Baseline, V1 and V2 all fail the same guard. Independent in-memory missing, flipped and elevated black cap counterfactuals are rejected. `terminal-guard.json` and `counterfactuals.json` retain failures and sample details. No counterfactual is saved into the model.
- All ten nonBody meshes are exactly identical to the frozen roof baseline across positions, topology, loop vertices, all UVs, weights, groups, materials, CORNER_NORMALS and sharp flags. This includes the moving Hood and new roof Interior. See`invariants.json`.
- The92 central-strip saved faces are exact, including UV and corner normals. Whole Body axis bounds are identical. Factory length4.88342m, width1.91859m and axle separation2.79000m pass. Bumper, valance and lamp geometry source functions retain their original construction.
- All276 actual aperture-wall faces remain present with unchanged original source vertices/centre/radius/recess/wall construction. Saved weld ordering introduces at most0.0000596mm point drift and1.43e-6 maximum corner-normal component delta. These are not bit-exact arrays; `protected.json` states that limit explicitly. Both actual headlamp aperture rays pass, with lens recession9.830..17.029mm. The protected aft Body comparison also exposes nonlocal weld rounding: maximum old-to-new point distance0.0001333mm and common-corner normal component delta.0019105, largely chrome at welded junctions. It does not indicate an authored rear deformation, and is not hidden behind the exact nonBody claim.
- Additional shared stations retessellate the fixed front side and lower arch lip as well as the upper wing. Their analytic profiles are unchanged below the localized upper-side terminal remap. The saved family count reports those additions rather than pretending all extra triangles belong to the roll.

### Exact saved triangle accounting

`triangle-breakdown.json` classifies every saved face by object, semantic, authored facing tag and region, with no double counting. Net counts are:

| Saved family | Triangle change |
|---|---:|
| Fixed wing and red upper corner return |+4288|
| Fender graphic actual triangle supports |+2786|
| Fixed front side station grid |+792|
| Front lower arch-lip station grid |+256|
| Removed black upper return |−216|
| Fascia upper perimeter subdivisions |+38|
| Remaining Body retessellation/connectors |+228|
| All ten nonBody objects |0|
| Total |+8172|

Final total222146+8172=230318. The residual228 bucket is explicitly retained as a saved semantic/spatial classification remainder, not attributed to a fabricated component. Shared samples increase the triangle count because both wing and clipped original artwork follow the real support grid.

### Completed checks and composition boundary

`gates.json` records36 unit tests, static0 errors, five packaged Lua/script files parsed by installed game classes, native11mesh/3clip import and the full saved pose suite passing. The pose suite calls the new terminal guard alongside existing roof/rear-corner/crest/pedal/cargo/backlight guards and tests all ten intermediate hinge fractions and rest/steering wheel clearances. The AST-only front section fixture imports the new helper, retains the earlier side/hood seam/tangent assertions throughY2.34, and additionally tests the actual terminal side seam, exact fascia endpoint and vertical terminal tangent. It does not assert the obsolete fixed side endpoint beyondY2.34.

No native game launch, install or live Blender action was performed here. Parent owns native composition review. The independent rear trial and current canonical source were untouched.

`proposal.patch` contains only local front changes in`build_mod.py`, factored front boundary construction, fender graphic support parameters and the new original`javelin_nose.py`. `verification.patch` contains the new callable guard, its pose invocation and the AST fixture change. Apply those hunks to the current canonical source; do not replace the entire generator or check_model_pose, because current canonical includes independently promoted rear work. Against parent's223722 rear composition, the expected triangle count is231894 if these independent deltas compose unchanged. Rebuild, compare ten nonBody arrays/normals against that exact baseline, rerun all current guards including the newer rear-haunch guard, and perform native both-quarter/front/top review before promotion.

The final isolated checkpoint freezes the exact source, all tools.py/.lua/.java dependencies, spec and generated package inputs. `frozen-inputs.json` and `auxiliary-inputs.json` preserve original69-input provenance; none of the stale earlier source modules was substituted.

## DOX

Root/tools/assets contracts and Blender/img2blender skills were reread. No accepted production contract or ownership changes yet, so AGENTS files remain unchanged. Promotion would require parent updating the relevant tools/assets contracts to describe shared terminal ownership and its saved guard. Only this document and ignored scoped artifacts are written.
