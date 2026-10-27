# Seat volume trial, cycle 4

All sections remain open. This proposal is isolated beneath `build/seat-volume-cycle4/`; it does not replace the shared generator, source blend or installed mod. Dimensions are inferred from photographs, with no likeness percentage assigned.

## Four fresh comparisons

These comparisons were made against the current cycle3 captures before changing the isolated copy.

1. `reference-53.png` versus `build/parity-cycle3/interior/front-seats.png`: the video cloth has rounded cream channels, shallow compressed transverse wrinkles and a soft lower U turn. The current face has some channel relief but reads as a flat rectangular panel with bevels. Retain the original palette, U direction and actual-triangle ribbon projection. The close crop does not establish the full highback outline.
2. Druk `140` versus cycle3 `cockpit.png` and `front-seats.png`: visible cushion edges are slender and turn down around a padded pan. The current tall front wall gives each cushion a box-like thickness. Preserve separate bucket centres and console space, retain the target's manual shifter, and reduce underside bulk without lowering the native support surface. The supplemental automatic console is not the target configuration.
3. Druk `141` versus cycle3 `front-seats.png`: broad soft side pads surround a shallow sitting surface, a transverse compression line crosses the front cushion, and a thin dark welt traces its rounded edge. Current padding has bowls and a thigh roll but its vertical slab and generic corners dominate. Revise actual shell volume, add a continuous thigh falloff and physically compressed stitch channels, and seat a restrained original welt on the same triangles. Perspective and loaded fabric prevent exact depth recovery.
4. Druk `140`, `141`, `142` and target `53` revisited against cycle3 `rear-seats.png`, `front-seats.png` and `cockpit.png`: the shared front highbacks remain too regular across face and side, while the rear is one continuous upholstered bench. Apply fuller lumbar/shoulder cross-sections and a softer front crown while retaining the rear arrangement. `142` shows floor and lower dashboard registration, not useful seat contour; none of these images establishes hidden rear-shell detail. The bench's exact drape remains inferred rather than justified by that floor photograph.

## Isolated proposal

The copied `tools/javelin_seats.py` lifts the cushion underside by up to58mm while retaining its upper support, replacing the former160mm slab with a thinner upholstered pan. A30mm front falloff wraps its thigh edge; narrow depressed channels compress the actual surface. A1.2mm dark welt follows the exposed cushion edge, stopping before the hidden lumbar overlap. The backrest has broader lumbar and shoulder fullness, a soft crown and a pinched hip transition. Extra cross-section samples retain the curved crown rather than a coarse corner bevel.

Both ribbon directions still clip into actual supporting triangles at1.5mm offsets. The existing `seat_centre_y -0.145m` hip-junction clipping is retained. Two front buckets and one continuous bench remain at the original centres with the same native attachment metadata. The patch does not change verifiers, axes, palette, scripts or package metadata.

## Evidence and limits

`build/seat-volume-cycle4/` contains isolated paint quarter/frontal/top views, clay quarter, an editable isolated seat blend, source hash and support records. The diagnostic uses the checkpoint's Part class and original atlas. Cameras match the earlier seat diagnostic, remain orthographic and uncalibrated, and do not constitute a photographic camera fit.

The first reviewed trial removed the dominant cushion slab but still showed coarse highback crown segments. The final trial adds cross-section samples and the thin welt. Paint and clay show a slimmer pan, visible front falloff and fuller highback faces. The upholstery remains too regular, the highback sidewalls remain simplified, and exact cloth compression, shells, adjusters, belts and buckles remain unresolved. The bench's inferred shape needs stronger dedicated reference evidence. Native appearance and motion are separate pending gates.

The final isolated geometry passes7,159 upward cushion samples and19,232 forward backrest samples at approximately1.5mm. The unchanged all-fabric cushion gate passes8,552 centre/near-corner rays at1.4997..1.5001mm against all actual seat padding, so the hip overlap fix is preserved.

The unchanged integrated gate rejects the stronger curved upper ribbon because its normal has Y0.869 on the two buckets and0.888 on the bench, below its Y>0.9 requirement. A brief10mm endpoint-shortening trial cleared the front requirement but not the bench. The original0.910m ribbon endpoint is restored in the delivered proposal, preserving the visible border. This rejection is not an unsupported or inward-facing surface: a separate proposed diagnostic casts onto the actual padding and measures minimum ribbon/padding normal agreement0.99999931, with Y>0.8. It retains the original centre/near-corner support thresholds and passes25,732 full-model backrest rays. This alternative tests conformity to the curved padding as well as positive cabin facing, but changing the shared verifier requires the root's explicit review. No verifier changes are in `proposal.patch`.

`pose-curved-trial.log` records that separate proposed gate, all four native seat placements, wheel/body clearance, original panel motion and all ten hinge fractions passing on the181,034-triangle isolated full build. It is not a pass of the unchanged Y>0.9 gate, and it is not native-game inspection. `pose.log` preserves the unchanged gate rejection. A first full build crashed with an installed add-on during factory-reset; relaunching with `--factory-startup` completed cleanly.

## DOX pass

Root owns this development report. Existing tools/assets ownership, seat count, axes, support and native-review contracts remain applicable. Their AGENTS.md files are intentionally unchanged because this isolated proposal introduces no durable ownership or workflow change. The root owns any subsequent shared implementation, specification update and native acceptance.

## Promoted after root review

The earlier isolated-only statements above describe proposal history. Root inspected the saved comparisons and promoted this proposal into the187,836-triangle combined cycle4 source, SHA-256 `363dfc71f833875a3c94f577bb094d19e52db2c9f2a1d82240629327871fccbf`. The169,766-triangle front-only source was frozen first. Fresh integrated evidence is under ignored `build/parity-cycle4/combined/`; all32 unit checks, static validation, native11mesh/3clip importing and the full saved-model pose/ten-fraction gate pass. The clean live Blender source is current. The installed/native-inspected candidate remains167,134 triangles; this combined geometry has not been installed or natively reviewed. All sections remain open, with no likeness percentage assigned.

The former backrest Y>0.9 gate assumed a nearly planar front and rejected the legitimate upper rollover. After explicit root review, the gate requires both cabin-forward Y>0.8 and actual supporting-padding normal dot>0.99. Ribbons were not shortened to pass; support rays and tolerances remain unchanged. `counterfactual.log` rejects the prior intersecting cup backing and a deliberately flipped actual backrest ribbon, while the corrected model passes. Combined source passes8,552 cushion and25,732 backrest support samples and3,770 cabin-forward border faces. The actual-padding normal test replaces the planar-axis assumption after root review; it is not endpoint shortening.
