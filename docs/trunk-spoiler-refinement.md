# Trunk and rear spoiler refinement

All sections remain open. This is a saved Blender refinement, not native-game appearance approval or a likeness percentage.

The installed Blender skill and the current raiinman/skill-library Blender instructions were checked for this work. The original generator remains authoritative and rebuilds the editable source and native FBX together. The live Blender watcher loads clean saved builds without replacing an unsaved document.

## Reference comparisons

The earlier complete four-review source study remains [six-source-four-analyses.md](six-source-four-analyses.md). The following focused comparisons concern this section; they do not replace those whole-page reviews.

1. Target video rear close-up, local `reference-22.png`: retain red rear paint, moving rear lettering, broad raised return and a latch seated low inside its recess. The cropped top prevents a complete crest measurement.
2. Druk low rear-quarter photograph, local `build/six-pass2/druk-034.jpg`: the ramp has substantial end cheeks, rounded transitions and a narrow seam above the lamp panel. A thin folded shell left a triangular end opening in the first render and was rejected.
3. BaT straight rear photograph, local `build/six-pass2/bat-010.jpg`: the spoiler is broad, with rounded upper ends and a gently bowed face. Comparison rejected the shorter 180mm return and restored the 205mm centre height. This modified car corroborates shape, not the target's finish or badges.
4. Druk latch close-up, local `build/six-pass2/druk-040.jpg`, checked against target22: the recess is a vertically oval pressed cup with a blended rim and lower lock. Both the initial soft Gaussian dent and the subsequent cylindrical-looking pocket were rejected. The current cup uses a tangent boundary and continuously curved bowl.

Photo inventories and exact gallery URLs remain in ignored `build/six-pass2/*-evidence.json`. Cameras are diagnostic estimates, not calibrated photo projections. Dimensions and hidden undersides are inferred.

## Implemented surfaces

- Replaced the flat lid quad with a closed crowned grid, retaining its original four seam anchors. Maximum added camber is12mm.
- Replaced the single straight spoiler ramp with a sampled curved rise, 10mm rolled crest and denser rounded outer stations.
- Bowed the rear face forward at its ends and gave it an original134x160mm,48mm-deep oval cup. The lock sits below its centre.
- Closed both end cheeks. A first solid-wedge underside intersected the fixed fascia; a stepped underside removes that collision while preserving the visible end closure.
- Kept the lid, spoiler, lock and rear badges on the same moving part. Lettering follows the actual bowed rear face.
- Replaced diagonal outer shoulders with elliptical corner drops and tightened the ramp/return width against the fixed quarter. This reduces the outer seam without closing its moving-panel clearance.

## Verification and limits

Current captures: ignored `build/trunk-spoiler-fix/`, including rear quarters from both sides, straight rear, deck top, side fit and open trunk. `report.json` records the source hash and diagnostic cameras. `before.zip` preserves the starting source and affected generators.

The144,919-triangle source passes32 unit tests, static validation, native importing of11 meshes/3 clips, outward lid-face and closed-component checks, both rear seam anchors, wheel/steering checks and all ten hinge fractions. Six source captures were inspected, with an independent reviewer identifying the end-fit and corner refinements. Native culling, game animation playback and complete rear/body likeness remain separate pending gates. Backlight-apron facets and surrounding rear-quarter shape are still visible and remain open; the lid crown does not conceal them.

The final independent review of rear-quarter, deck-top and straight views confirmed that the elliptical corners now read rounded and the widened shoulders reduce the deep slit to a narrow moving-panel seam. The render report, saved blend and frozen35-file checkpoint share the same source hash.

DOX pass: updated tools and artwork ownership for the revised surfaces, plus reconstruction intent. Root and package instructions remain unchanged because project-wide policy and runtime interfaces did not change.
