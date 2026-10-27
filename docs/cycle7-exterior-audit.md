# Cycle 7 skeptical exterior audit

Reviewed combined 218,034-triangle model, SHA-256 `ee99eb2206df0c62ff121990f522f544c422105f10f3ff7848ae2bfceee76e75`. The body report and locked-camera source report identify this same saved blend. This is research-only review. No model, profile, camera, package or native UI was changed. All sections remain open; no numerical likeness is assigned.

Blender and img2blender skills informed the review: full-frame references first, opaque clay and off-axis volume checks, then paint. Root/assets DOX and current reconstruction specification/history were reread. Existing balanced and contact-anchored cameras were inspected without selecting a more flattering camera. They are estimated alternatives, not calibrated recovery of the video lens.

## Four fresh comparison groups

The four sheets under `build/cycle7-exterior-audit/` retain complete input frames. Images are uniformly fitted into independently scaled tiles, without alignment, crop, warping or color changes. The original supplemental close photographs remain close photographs; their missing surroundings are not reconstructed. `inputs.json` records paths, dimensions and hashes. Actual observations below come from freshly opening the original files as well as the sheets.

### 1. Target front identity and camera sensitivity

Evidence: full `reference-2.png`, `reference-30.png`; all six `build/parity-cycle7/camera-fit/` paint/clay captures; `body/target-frame2-estimate-paint.png`, `target-frame30-estimate-paint.png` and clay; opposite off-axis front clay. Sheet: [01-target-front.png](../build/cycle7-exterior-audit/01-target-front.png).

The real target retains strong rounded shoulders on both sides of the hood. The broader current crests are useful, but their forward ends still appear to fold down and inward sharply onto the straight leading face. The painted black graphic exaggerates that step; clay retains the geometric transition, so changing the graphic alone would not resolve it. The target's upper lamp-end surround and hood leading edge read as one curved nose assembly. Current source views read as separate domed wings behind a straight-front platform. Both balanced and contact-anchored views retain this concern despite their different visible hood/windshield proportions.

The target's grille, outer lamp ends, bumper and lower valance form a fuller curved end. Current view shows a thin horizontal bumper line and angular side termination. This remains an assembly-level concern rather than a proposed global width change. The contact-anchored image does change apparent hood length substantially, so these images do not justify shortening the whole hood, lowering the whole windshield, or moving the axle. Target30 has an open door/person and cannot validate a closed left-door silhouette. Different lighting, transparent glass and chrome also prevent treating brighter image patches as recovered height.

### 2. Front fender volume independently of the target camera

Evidence: complete `build/six-pass2/druk-000.jpg`, `druk-025.jpg`; current `body/fender-close-clay.png`, both front-quarter clay views, side clay and top clay. Sheet: [02-front-volume.png](../build/cycle7-exterior-audit/02-front-volume.png).

Druk000 supports a broad rounded wheel shoulder that flows into the nose. Druk025 shows that the outboard front turn continues around the lamp corner, while the hood graphic follows the underlying crown rather than defining it. Current clay has improved transverse breadth, but its final forward transition still makes a relatively narrow sloping end beside a broad central hood. The off-axis views show an abrupt change of character from shoulder bulge to straight fascia. Side clay confirms that the front crown has a long smooth run, so simply adding more peak height would target the wrong defect.

Top clay is useful for checking the unchanged overall envelope, but does not by itself prove the three-dimensional lamp-end wrap. Druk025 is a close oblique photograph with strong reflected sky; it cannot supply a metric nose radius. Druk000 has different roof covering, wheels and equipment. Those features are not adopted from this car.

### 3. Greenhouse, quarter-window shape and rear shoulder

Evidence: complete Druk005 side photograph and Druk004 rear-quarter photograph; current side paint/clay, sail-close paint/clay and full rear-quarter clay. Sheet: [03-greenhouse-haunch.png](../build/cycle7-exterior-audit/03-greenhouse-haunch.png).

The strongest discrete identity defect is the quarter-window aft outline. Druk005 and Druk004 show a roof-side upper run followed by a recognizable descending aft edge, turning through a lower rounded corner into the beltline. The model makes a smooth oval cap, with curvature spread across almost the whole aft boundary. Its side silhouette reads as a small teardrop opening. The same shape persists in sail-close clay, so glass reflection or lack of vinyl is not the explanation. The current code's `quarter_controls` distributes the upper and lower boundary turns progressively to a common tip, consistent with the observed oval result.

The shared sail is much more continuous than earlier iterations, but the lower sail/rear shoulder ends in a small angular shelf near the deck join. The model's side and sail-close views show a local change of slope above and behind the rear wheel. Druk005 shows a broad convex haunch continuing rearward; Druk004 shows its roll into the tail without that small stepped plateau. A straight, persistent horizontal side band also makes the current flank read more uniform than the photographed shoulder-to-waist variation. This does not justify scaling the whole rear quarter outward: the overall width limit and moving seams remain binding.

Druk005 is near side-on, not calibrated orthographic. It supports the shape of boundaries and distribution of curvature more strongly than exact cabin length/height. The supplemental vinyl roof makes its sail boundary conspicuous; the target remains painted red. Missing vinyl must not be diagnosed as missing geometry. No global roof raise, lowering or shortening is established by this group.

### 4. Rear end and tail-to-quarter continuity

Evidence: complete Druk002 rear quarter, Druk032 low quarter, Druk040 rear close photograph and target `reference-22.png`; current full rear-quarter paint/clay and sail-close clay. Sheet: [04-rear-volume.png](../build/cycle7-exterior-audit/04-rear-volume.png).

The closed rear corner wedges no longer dominate the source view. That repair does not make the tail composition correct. The reference has a substantial rolled quarter end, a bowed tail field and a broad bumper return. Current full rear clay still reads as a flat rectangular tail with small horizontal apertures over a comparatively large uninterrupted lower painted region. Druk040 and target22 show taller-looking rounded lamp openings and more prominent bumper section. This is a proportion/construction concern for the rear assembly, not an instruction to enlarge lenses alone. Model and photographic obliquities differ, so exact aperture aspect and bumper height require a dedicated end-on/quarter comparison before modification.

Druk032 is especially useful for the convex flank flowing around the tail corner. Current sail-close shows the localized shelf noted in group3, followed by an angular termination at the trunk/fixed-quarter seam. Druk002/004 support a smoother broad wrap. Preserve the fixed lower-panel closure and lamp pockets while addressing any future outer-quarter contour. The recent corner repair should not be reverted to conceal a new seam mismatch.

Target22 is itself a tight video frame; it cannot establish full tail width or overall rear-overhang length. Druk040 is also close and partly cuts off the outermost lamps. Neither licenses whole-tail scaling. Native lighting and material behavior remain a separate inspection route.

## Top three shape defects

1. **Quarter-window aft perimeter and its surrounding sail read as an oval cap.** Strong cross-view evidence in group3; the shape is visible in side and off-axis clay. Correcting the aperture boundary is a high-confidence next identity step with a localized scope.
2. **Front fender crowns end abruptly at the nose/lamp-end transition.** Groups1/2 support the concern across fixed camera alternatives. The last breadth change improved the shoulder; additional crest height is not justified. The next front-specific trial should redistribute curvature through the final forward run and its corner wrap while retaining the lamp/hood anchors.
3. **Rear shoulder/deck transition retains a localized shelf and angular tail termination.** Groups3/4 support this in paint and clay. Investigate the shared longitudinal stations and lower sail-to-side derivative near the deck join rather than globally widening or lifting the rear quarter. Rear aperture/bumper composition is a related unresolved check, but its dimensional correction is less well established by these oblique frames.

These are remaining blockers to the target's body identity. Count, dimensions, seam and motion checks do not close them.

## Recommended next precise section

Prepare an isolated **quarter-window perimeter and local sail-border** trial first. Begin with four fresh comparisons dedicated to this boundary, including the target's useful side frames and supplemental Druk000/004/005. Retain the main window/divider anchors, existing quarter-tip support attachment and shared `rear_quarter_surface`; revise the upper/lower `quarter_controls` distribution to create a more legible descending aft run with the turn concentrated near the lower corner. The current tip location itself remains an inferred coordinate, not a measured factory point. Test the existing anchors before changing tip position or cabin proportions.

Generate quarter glass, its chrome and adjoining fixed sail from the same revised perimeter so no old oval trim remains. Preserve the current cubic side seating, backlight support, roof height/longitudinal profile, axle offsets, door seams and 20 backlight intervals. A correction that breaks the shared sail or creates a sharp pasted-on triangle is not acceptable. If perimeter redistribution cannot reproduce the references without moving anchors, record that conflict rather than moving the whole roof to improve one view.

Review the same full side, both quarter, top and sail-close paint/clay views plus locked target cameras. Verify saved glass/body joins and actual supported aft-tip vertices, outward normals, all window/door hinge fractions, backlight/cargo/rear-corner/crest guards, wheel clearances and native importer output. Then inspect native views with both doors shut and open. This audit does not perform those future gates or authorize a canonical geometry edit.

## DOX and limits

Only this research record and ignored audit sheets/metadata were written. Root/tools/assets instruction contracts and the reconstruction specification are intentionally unchanged: this audit adds no durable ownership, behavior or accepted geometry. No factory dimensions were inferred from photograph pixels; no camera was refit; no native inspection was performed. Original target and supplemental evidence remain distinct. The report is an ordered correction proposal, not exterior completion.
