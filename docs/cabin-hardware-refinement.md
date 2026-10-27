# Cabin hardware refinement, cycle 6

All sections remain open. Scope is one related section first: the missing small Cardin door-insert crest. This isolated trial does not add pedals, visors, belts or unseen hardware. Supplemental detail is not claimed to have been observed on the target car.

## Four fresh comparisons before implementation

1. Re-examined target `reference-47.png` and `reference-53.png` against the latest dashboard/interior source captures. Frame 47 confirms the original metal-spoke wheel and white manual-shift ball; 53 resolves the cream/magenta/burgundy upholstery. Neither frame shows the door-insert crest. Preserve target manual equipment and palette. Do not transfer the supplemental automatic console or its pedal arrangement.
2. Re-examined `build/six-pass2/druk-105.jpg` and its close crest photograph106 against the current source door card. The long dark insert carries a small raised bright spiral/P-C monogram just aft of the ribbon group, with a separate short caption footer. The source has the inset/ribbons but no crest. Photo106 resolves an open lower curved area and a curled upper interior, not the exterior open stacked-letter emblem. Reflections do not determine the exact metal pigment or enamel colour.
3. Re-examined opposite card138 and full card105 against the source. Each door carries the same readable badge beside the ribbon group; the artwork should face the cabin and remain readable on both doors, not mirror the wordmark. Its small size relative to the long strip supports a roughly 50 mm high inferred version within the existing inset. Existing manual crank, release and padded pull stay in place.
4. Re-examined roof115 and cabin/floor140/142, then both door cards and target 47/53 again against latest headliner/cockpit/card captures. Roof115 resolves headlining, dome lamp and an upper belt strap/retainer; it does not show a useful front sunvisor.140 shows the supplemental automatic brake/accelerator area, and 142 the passenger carpet/underside. These support a future evidence-led hardware pass but cannot establish the target's manual clutch, pedals, visor outline or hidden belt installation. The crest is the clearest missing small identity feature with a reversible local implementation.

## Isolated proposal

`build/cabin-hardware-cycle6/tools/javelin_doorcrest.py` provides hand-authored vector silhouette/curl paths, rounded cast turns and a compact original lowercase stroke caption. It adds a roughly 31 mm wide by 48 mm high appliqué to each long inset, immediately aft of the vertical ribbons. Main metal, bright rim and dark caption remain within the existing original palette. No inferred enamel pigment was added: the red/orange in the close photograph could include reflection. No photograph pixels, third-party mesh or system font are used.

The only proposed existing-module change is the final import/call in the isolated `javelin_doorcard.py`; add the new `javelin_doorcrest.py` alongside it. The copied `build_mod.py` differs only by a render-stop after saving for trial execution and is not a promotion patch. All existing manual controls, upholstery, dashboard, floor, roof and exterior geometry are preserved. Exact badge size, typography and metallic response remain inferred and approximate. The visible crest is based on supplemental cards, not a claimed observation in target 47/53.

Root owns promotion. Canonical source/tools/assets/profile were not written by this subtask.

## Verification

- Exact frozen baseline: 214,322 triangles, SHA-256 `c9c25499d084ded7bfe8910375247a9be5568f0c3235bce57166656dc01216c8`. This is the integrated cycle6 crown/dashboard/backlight/cargo candidate, not the earlier 214,374 dashboard-only save. Counts were recomputed directly from the frozen blend.
- Final isolated trial: 217,354 triangles (+3,032), SHA-256 `9c5f1ae2e6b0e99fd59e70cdeda7b17cd5546d178480d7f84e607e2233304b91`.
- `badge-check.json`: all nine non-door mesh coordinate/topology digests match the exact baseline. Every pre-existing door face, its coordinates and winding is retained; each door adds 376 artwork faces.
- Actual saved-mesh rays sample 6,064 points per badge across every new artwork triangle. Both sides face the cabin and hit the original semantic seat-colour inlay 1.600..2.200 mm behind the art. No sample is buried or detached beyond the unchanged 0.25..2.5 mm support criterion. Hand-authored silhouette has no segment crossings.
- `before/` and `after/` contain identical-camera full cards and enlarged badges for both sides. Backface culling is enabled. Visual inspection confirms a readable nonmirrored spiral/caption on each side, clear of ribbons and controls. Initial faceted curves/dark metal were rounded and the existing metal palette used before final capture. The source-only lighting is not native material approval, and the tiny caption will not stay readable at every game distance.
- Final full `pose.log` passes all existing geometry checks, wheel/rest/steering and ten intermediate hinge fractions, including the already-promoted dashboard. No gate or tolerance was changed. 32 unit tests pass, static validation reports 0 errors, and the installed game's native importer resolves 11 meshes/3 clips.
- Native open-door viewing of this exact appliqué remains pending. This is a small identity increment, not closure of door-card proportions, padding, releases or whole-cabin likeness. Pedals, visors and unseen hardware were not added.

## DOX pass

Root owns this research record. Owning AGENTS documents intentionally unchanged for an unpromoted isolated trial that introduces no durable ownership or behavioral contract.
