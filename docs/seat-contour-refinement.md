# Seat contour refinement

All seating remains open. This is a geometric iteration with inferred dimensions, not a likeness percentage or native acceptance.

## Four fresh comparisons before editing

1. Target `reference-53.png` against `build/parity-cycle2/interior/front-seats.png`: the target's cream channels have rounded padded relief and a deep, soft lower turn. The baseline borders are flat colour on a generic slab. Preserve the target palette and U direction; add volume to their underlying padding rather than hovering decorative tubes above it. The close video frame cannot establish the complete seat silhouette.
2. Druk `141` against the same baseline: the cushion has a shallow occupant bowl, a raised thigh edge and broad side pads. The baseline is a uniformly thick rounded block. Retain longitudinal stripes while shaping the support surface and tapering its plan outline. Photograph perspective and upholstery compression prevent exact dimension recovery.
3. Druk `144` against baseline front and rear seats: the front highback has a rounded crown and broad soft shoulders, while the bench is continuous with two padded occupant regions. The baseline highbacks have straight rectangular tops and the bench is uniformly flat. Preserve two buckets plus one continuous bench and its rear native support locations. The partially hidden rear/front shells remain inferred.
4. Druk `140` and `142` against baseline cushion placement and profiles: the two front cushions remain separate around the console and their fronts roll down rather than ending in a flat shelf. `142` shows floor and trim registration but no useful seat contour, so it limits the inference rather than providing additional shape evidence. Retain the existing front seat centres and native attachment arrangement; do not copy the supplemental automatic console.

## Source correction

`tools/javelin_seats.py` retains the existing native support centres, original palette, two front buckets and continuous rear bench. Its padding deformation now adds a rounded highback crown, shoulder and lumbar fullness, tapered cushion plan outlines, shallow occupant bowls and a thigh roll. Paired cream-channel relief is part of the padded volume, with explicit grid sampling for the channels.

Both backrest ribbons and cushion graphics now clip into the actual supporting triangles and interpolate their planes at 1.5mm clearance. Backrest polygons retain explicit cabin-forward +Y orientation. Backrest triangle projection replaces the previous analytic round-box surface assumption, which would become invalid after shape changes.

## Verification and skeptical review

Blender 5.2.1 renders in ignored `build/seat-contours-cycle3/` use the actual extracted project Part class and original palette. They do not rebuild or save the shared source. `isolated-seats.blend` is a diagnostic snapshot only. `seats-review.json` records source hash and fixed uncalibrated cameras. `support.json` records 5,484 cushion and 10,576 backrest centre/near-corner probes, all approximately 1.5mm from their corresponding padding triangles. Python compilation passes. These isolated support probes select cushion tops and forward backrest surfaces separately, avoiding the intentional cushion/backrest overlap at the hip junction; they do not establish assembled clearance.

Inspected quarter, frontal and overhead colour views and a quarter clay view. The crowned top and thigh roll make visible volume progress, but the pads remain too clean and regular. Shoulder corner radii, lower hip fullness, rear bench contour/drape, cloth compression, seam relief and fabric response need further reference-led work. Seat shells, adjusters, hardware, belts and buckles remain missing or simplified. The isolated captures cannot establish dashboard, console, door or native-game fit. The root owns the integrated build, four native support checks, forward ribbon normals, complete moving-door sweep and native review.

An initial copied diagnostic retained its prior output path and overwrote the disposable `build/parity-audit-interior/new-seats-quarter.png`, `new-bench.png`, `new-seat-top.png` and `seats-review.json`. Subsequent captures use the assigned cycle3 directory. The cycle2 integrated baseline and shared source blend were preserved.

## Hip-junction correction after integrated rejection

The radical sail candidate's saved full Interior failed the unchanged all-fabric cushion gate at three samples. Two front samples at source Y -0.242414 and one rear at -0.963259 hit the lumbar front instead of the cushion, at only 0.157mm and 0.218mm. Forward normals near +Y 0.994 confirmed an actual ribbon/lumbar intersection. The earlier separately selected support audit missed this visibility defect and was insufficient.

`cushion_patch` now clips its exposed polygons ahead of `seat_centre_y - 0.145m`, then clips them into the actual cushion support triangles. This removes the rear ribbon portions beneath the overlapping lumbar solid while preserving visible longitudinal bands and the rear loop's exposed front/sides. The pad volume and native registration stay unchanged. No verifier is weakened. `all-fabric-support.json` repeats the existing gate's final welded-mesh rays against every seat-colour triangle; it passes after this correction. The full integrated saved-model gate remains the root's required confirmation.

## DOX pass

Root owns this report. The existing tools/assets seat contracts still apply; no ownership, child index, arrangement, axes or native registration contract changes. Those AGENTS.md files are intentionally unchanged. The actual-triangle support rule is now implemented on the backrest as well as the cushion. All sections remain open.
