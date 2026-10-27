# Manual cabin hardware research

Research-only review, 2026-10-18. No model, canonical source, spec, package, profile or UI changes. Root owns implementation. Four fresh image comparisons are saved as `build/manual-cabin-research/comparison-1.png` through `comparison-4.png`; each was actually viewed after assembly, in addition to the full-size source images listed below.

## Candidate and evidence authority

The candidate is the saved 214322-triangle source in `build/parity-cycle6/checkpoint/assets/Javelin73PC.blend`, SHA-256 `c9c25499d084ded7bfe8910375247a9be5568f0c3235bce57166656dc01216c8`. Fresh read-only cutaway renders are under `build/manual-cabin-research/candidate214322/`, with camera settings and source hash in `report.json`. These are uncalibrated orthographic diagnostics. Roof/lower faces were hidden only in memory, and no blend was saved. Existing lights make the ceiling dark; brightness is not evidence of geometry depth.

| Source | Authority and limit |
| --- | --- |
| Target video, frames 47 and 53 | Target-specific white manual H-pattern ball, wheel and Cardin upholstery. Neither frame exposes pedals, visors or roof belt anchors. |
| [BaT 1973 AMX four-speed](https://bringatrailer.com/listing/1973-amc-javelin-amx-2/) | Same-year manual Cardin car with Hurst shifter. Restored car with replaced floor and clutch/brake components, not proof of every target detail or untouched factory finish. |
| [Druk 1973 Cardin car](https://www.drukautosales.com/vehicles/880/1973-amc-amk-javelin-pierre-cardin) | Useful assembled roof hardware and upholstery views. Automatic console and wide brake pedal differ from the target manual installation. |
| [Hosted 1973 AMC technical manual](https://www.amcjavelin.nl/dut/nl_javelinfo_bestanden.htm) | Contemporary factory technical content, hosted by an enthusiast. Chapters cover multiple AMC series; generic diagrams are not dimensional Javelin drawings. No 1971/72/74 photograph was substituted for the 1973 evidence. |

## Four fresh comparisons

### Pass 1: transmission and interior identity

Viewed target47/53, exact candidate cockpit/front-seats, BaT063/050 together (`comparison-1.png`). Target47's white ball supports a manual cabin; target53's cloth identifies the trim family but supplies no belt or pedal geometry. BaT063 independently shows the white manual ball, long metal lever and stepped rubber boot beside the front bucket. Candidate has the ball/rod but its plain dome-shaped base does not convey the photographed accordion boot. BaT050 exposes loose belt buckles near the seat bases and rear bench. Candidate's broad bare floor/seat junctions lack this visible hardware in the diagnostic views. Limits: target crop does not establish a Hurst-branded replacement lever or any exact boot dimensions; retain the target's own shifter identity.

### Pass 2: manual footwell versus automatic trap

Viewed target47/53, exact cockpit, BaT048/053 and Druk140 together (`comparison-2.png`), then full-size foot controls. BaT048 is the strongest manual layout: small separate far-left parking-brake pad, clutch on a long bent suspended arm, adjacent brake pad, and a tall narrow accelerator on the right. The clutch has a compact rounded rectangular rubber face with molded grooves. The neighboring brake face looks worn/bare brown in this restored car; do not copy corrosion as target factory material. The accelerator is a long upright ribbed face, visually distinct from both compact driving pads. BaT053 corroborates the grooved compact pedal and suspended arms, but the wheel obscures the complete brake/accelerator relationship. Druk140 visibly has a much wider automatic brake and no clutch, so it must not govern the target's pedal count or brake width. Current cockpit render has no visible pedal assembly; the frozen cockpit builder also contains no pedal construction. Limits: camera perspective, aftermarket gauge and damaged/replaced finishes prevent pad-size measurements or exact pivot coordinates.

### Pass 3: roof hardware and belt stowage

Viewed target47/53, exact headliner, BaT062, Druk115 and BaT048 together (`comparison-3.png`), then each roof photograph full-size. Druk115 shows a shallow cream dome lens inside a bright narrow rim, plus broad dark shoulder webbing folded along the roof rail, ending in a visible metallic fitting. This is a folded strip with thickness, doubled portions and loose curvature, not a taut modern diagonal belt or a solid handle. BaT062 has the dome lens removed, exposing the circular base and bulb, and a small loop/hook along the window rail. It must not be interpreted as a different completed lamp. BaT048 shows two padded dark sun visors at the windshield header, one angled down more than the other, and a rectangular rear-view mirror on a short upper mount. Candidate ceiling contains its stripe field and lamp but shows none of these visor/belt/clip silhouettes. Limits: the target frames do not reveal their arrangement; Druk's exact belt fold is a stowed pose, not fixed factory geometry. The BaT rail loop is visible, but its identity cannot be proved from that photograph alone.

### Pass 4: cross-check attachment and occlusion

Re-viewed target47/53, exact front-seats/headliner, BaT049 and Druk142 together (`comparison-4.png`), then revisited BaT048/062 and Druk115 at full size against the factory diagrams below. BaT049 locates a loose bright buckle on short webbing beside the front-seat/tunnel area, distinct from the shoulder webbing above. Druk142 is the passenger footwell: its broad carpeted toe-board and side kick panel are useful attachment context, but it supplies no driver pedal proof. Candidate's unobstructed geometric floor should not dictate photographed pedal exposure, which must also survive dash/column occlusion. The roof's uninterrupted stripe surface needs separate hardware attached below it, rather than painted symbols or strips replacing the ceiling. Limits: the cutaway hides some supporting shell and cannot prove installed-game visibility, actual anchor strength or occupant clearances.

## Factory cross-checks actually inspected

Downloaded ZIPs contain JPEG page scans, not PDFs. `factory-downloads.json` records the first four archives; the body chapter URL is listed here. Full pages actually viewed: clutch5-1/5-2; roof20-1/20-2; seats19-9/19-11; bodies13-1/13-2. Contact sheets also reviewed all downloaded seat, brake and roof pages, but thumbnail text is not treated as a read page. Brake chapter did not yield a useful manual pad drawing.

- [Clutch chapter](https://www.amcjavelin.nl/all/javelinfo/Man_07_AMC_Clutch.zip), pages5-1/5-2: suspended clutch pedal, upper pivot/bushings and rod to bellcrank. Supports a real arm reaching upward under the dash. Figure3 is a generic linkage illustration, not a cabin scale template.
- [Roof chapter](https://www.amcjavelin.nl/all/javelinfo/Man_23_AMC_Domelight_Headlining_Vinylcovered_roof_Exterior_Decals.zip), pages20-1/20-2: dome base mounts to roof support above front seat back; removable lens has a bright metallized edge. Headliner service explicitly removes sun visors, mirror, coat hooks, shoulder belts and dome. The70-series side edge uses a molded retainer/crash pad. Diagram cross-section supports a shaped rail return, not a bare sheet edge.
- [Seat chapter](https://www.amcjavelin.nl/all/javelinfo/Man_22_AMC_Seat_Asemblies_and_Adjusters.zip), pages19-9/19-11: shoulder harness and lap belt treated separately, with roof harness anchors and floor/seat belt equipment. Diagram26 explicitly depicts10/80-series automatic equipment, so do not trace its geometry into the Javelin.
- [Body chapter](https://www.amcjavelin.nl/all/javelinfo/Man_16_AMC_Bodies_Panels_Subassemblies.zip), pages13-1/13-2:70-series110-inch-wheelbase frame is shown separately from other AMC bodies. This is supporting series context; no cabin-hardware dimensions are extracted from the frame diagram.

## Usable construction and unresolved boundaries

| Feature | Supported original construction | Still uncertain |
| --- | --- | --- |
| Manual driving pedals | Separate compact clutch and brake pads on suspended arms, ribbed tall narrow accelerator to their right. Add separate small parking-brake control at far left. Use BaT048 spatial order, factory clutch pivot principle, and restrained black rubber/metal materials. | Exact pad widths/heights, pivot coordinates, travel, accelerator hinge, target pad-groove pattern. BaT brake wear is not a finish reference. |
| Upper shoulder harness | Dark flexible webbing returning from an upper rail attachment, folded/stowed near the rail with separate small retaining hardware and metal fitting. Keep this distinct from loose lap belts. | Target's deployed/stowed state, precise clip design and count, anchor cover form, webbing length, side-to-side symmetry. Do not assume modern three-point retractor routing. |
| Lap belt hardware | Short loose webbing and small bright buckle/tongue shapes beside front seats and rear cushion junction. | Target buckle logo, locking mechanism and hidden floor anchor. |
| Sun visors | Two thin padded rounded panels under the windshield header, with short pivot/support features; mirror separate at center. | Target position, outline taper, inner retaining-clip details, exact material shade and dimensions. BaT provides form, not a measured plan. |
| Dome lamp | Shallow convex cream lens, narrow bright rim and roof-facing base. Keep current assembled-lens concept. | Target lens texture, exact diameter and screw/clip layout. Do not reproduce BaT's missing-lens damage. |
| Roof perimeter | Shaped dark side-rail retainer/pad and distinct small roof hardware attached to it or the header, preserving Cardin cloth support. | Exact rail sections and local upholstery seams. Do not infer depth from shadow. |

Recommended first implementation slice is the manual pedal assembly and separate parking brake, followed by visor/mirror and roof belt hardware. Place items against the existing floor, dash and roof in three dimensions, then inspect driver-eye and open-door angles. Test normals, surface visibility and occupant/steering-column clearances after modeling; this research does not complete those gates or native inspection. Keep the supported shapes reversible while target-specific roof details remain unseen.

## Source image ledger

Target images actually viewed: `reference-47.png`, `reference-53.png`, from [the supplied video](https://www.youtube.com/watch?v=ZpfnHMBiRvA). The local frame names are existing project identifiers, not fabricated timestamps. Candidate images actually viewed: cockpit, headliner and front-seats listed above. Seller photographs actually viewed full-size and their exact source URLs:

- `build/six-pass2/bat-048.jpg`: [original image](https://bringatrailer.com/wp-content/uploads/2022/08/20220626_145233-81419-scaled.jpg).
- `build/six-pass2/bat-049.jpg`: [original image](https://bringatrailer.com/wp-content/uploads/2022/08/20220626_145256-81435-scaled.jpg).
- `build/six-pass2/bat-050.jpg`: [original image](https://bringatrailer.com/wp-content/uploads/2022/08/20220626_145301-81443-scaled.jpg).
- `build/six-pass2/bat-053.jpg`: [original image](https://bringatrailer.com/wp-content/uploads/2022/08/1973_amc_javelin-amx_20220926_130154-14067-scaled.jpg).
- `build/six-pass2/bat-062.jpg`: [original image](https://bringatrailer.com/wp-content/uploads/2022/08/20220626_145814-81505-scaled.jpg).
- `build/six-pass2/bat-063.jpg`: [original image](https://bringatrailer.com/wp-content/uploads/2022/08/1973_amc_javelin-amx_20220926_131723-13267-scaled.jpg).
- `build/six-pass2/druk-115.jpg`: [original image](https://cdn.dealeraccelerate.com/druk/1/890/152901/1920x1440/w/1973-amc-amk-javelin-pierre-cardin).
- `build/six-pass2/druk-140.jpg`: [original image](https://cdn.dealeraccelerate.com/druk/1/890/152932/1920x1440/w/1973-amc-amk-javelin-pierre-cardin).
- `build/six-pass2/druk-142.jpg`: [original image](https://cdn.dealeraccelerate.com/druk/1/890/152934/1920x1440/w/1973-amc-amk-javelin-pierre-cardin).

The BaT contact sheet is thumbnail discovery only. The full-size list above and factory pages identify the evidence actually inspected. URLs are also machine-readable in `build/manual-cabin-research/image-sources.json`. Downloads and visual comparison sheets remain local research artifacts outside the distributed mod.

DOX closeout: root AGENTS was re-read. The only durable change is this research record; project ownership, workflow and child boundaries are unchanged, so AGENTS documents are intentionally unchanged. No implementation or native-game gate is claimed.
