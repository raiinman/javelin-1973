# AMC 360-style exterior engine

Original, game-oriented exterior model of an AMC 360-style V8 for the 1973 Javelin AMX Pierre Cardin project. Built with Blender 5.2.1 LTS (the official `bpy` 5.2.1 module) from the deterministic source `tools/amc360_engine.py`. Verification, renders and the car fit come from `tools/amc360_engine_review.py`.

This is a visible-exterior asset. It is not export-staged, has not been imported into Project Zomboid or Wreckfest, and is not part of the distributed mod.

## Research and evidence boundaries

**No reference image has been viewed while building this model.** The supplied AMCCF illustration, AMCCF block drawing, RM Sotheby's 1974 lot and its engine photo, and every other image host tried (Wikipedia/Wikimedia, YouTube thumbnails, image search) are blocked by the session network policy. The repository has no photo archive (`research-index.md`). The layout below therefore rests on text sources and general knowledge. Comparing it against photographs remains the first open task.

| Class | Item | Basis |
| --- | --- | --- |
| Target evidence | Round air cleaner with a visible 360 label (about 1:07); rolled domed cleaner and rounded covers | `research-1973.md`, `reference-study.md`, `likeness-four-pass.md`. The video was not re-watched. |
| Text sources (web search, 2026-10-27) | Passenger cars use a centre or slightly forward sump; rear sumps are truck/Jeep pans | Forum and parts discussions: [Milodon AMC road-race pan (JEGS)](https://www.jegs.com/i/milodon-697-31681-road-race-oil-pan-amc), [FABO 360 sump thread](https://www.forabodiesonly.com/mopar/threads/360-oil-sump.352276), [AMC Lives passenger-car pan](https://www.amclives.com/collections/all/products/1968-1979-amc-v8-mildon-performance-stock-appearing-engine-oil-pan). Not factory documentation; one listing conflicts. |
| Text sources | Alternator on the passenger side is the 1972+ factory location; factory Motorola alternators | Parts-seller listings, e.g. [AMC Lives Motorola alternator](https://www.amclives.com/collections/all/products/1967-1979-amc-v8-chrome-150-amp-motorola-case-1-wire-alternator-1-or-6-groove-pulley-1). Not factory documentation. |
| Text sources | Timing cover carries the distributor, fuel pump and oil pump; the oil filter mounts on the oil-pump cover | [Holley: modifying AMC oiling](https://www.holley.com/blog/post/modifying_amc_oiling_for_performance/), [JEDI timing-cover article](https://www.jedi.com/amc-v8-timing-cover-inspection-and-dress-up/) |
| Text sources | Metallic blue engine enamel sold for 1967-73 AMC including Javelin AMX; a 1973 AMX listing describes blue metallic valve covers; chrome lid and covers appear on a car with Edelbrock aftermarket parts | [AMC Lives engine paint](https://amclives.com/products/engine-pain-amc-metallic-blue-12-oz-aerosol-can-1967-1973-amc) (vendor claim), dealer listings. Factory shade unconfirmed. |
| General family knowledge, unverified | 90 degree V8, 4.75 in bore spacing, 9.21 in tall-deck crank-to-deck height, driver bank forward, front oil filler on the timing cover | Recheck against drawings. |
| Fit and layout assumptions | Distributor lean, filter angle, carburettor body, snorkel direction, single V-belt layout, valve-cover pressing shape, fan blade count | Chosen for a plausible, clash-free arrangement. |

The 360 label is visual reference only. It does not prove displacement, internals or factory originality.

## Model

- 31 named mesh objects under `ENG_Root`, grouped as `ENG_Castings`, `ENG_Pressings`, `ENG_FuelIgnition` and `ENG_FrontDrive`. Pivots sit at mounting points.
- Engine frame: metres, +Y forward, +Z up, driver side -X. Origin on the crank axis at the block front face.
- Castings: block with bell flange, core plugs and mount bosses; rolled-end heads with plug bosses; an intake with smooth cast runner humps, plenum, faded end walls and thermostat neck; log manifolds that swell toward a swept, flaring outlet elbow with a thick flange, with flared primaries and a top rib; timing cover with cast bolt lugs, a centre web, distributor boss, filter adapter, filler tube and fuel pump; water pump.
- Pressings: tall valve covers with flange, full rolled crown, raised centre panel, flange bolts, breather and PCV valve; a passenger-car pan with forward-centre sump; a round domed air cleaner with rolled lip, wing nut and forward snorkel.
- Front drive: damper, V-grooved pulleys, a V-belt from exact tangents, four-blade stamped fan, passenger-side alternator with finned cooling fan, case ribs, through-bolts, bracket, pivot and adjuster.
- Fuel and ignition: Motorcraft-4300-style carburettor with fuel inlet, PCV hose to the carb base, angled front distributor with vacuum canister and cap, eight leads through loom combs to seated boots, dipstick. The pump-to-carb fuel line is omitted because the passenger front is too crowded to route it cleanly.
- Label: a 40 mm original stroke-drawn "360" on the lid, readable from the front of the car. No font, logo or decal artwork was reused.
- Finish: `--finish stock` (default) gives metallic blue painted covers, a black can and lid, and a silver label. `--finish dressup` gives polished covers and lid with a dark label (`renders/amc360_variant_dressup_front_quarter.png`, preview quality). Both are original materials without image textures.

## Research parity checklist

This counts research items the model meets. It is a checklist, not a likeness percentage: no reference image has been compared, so visual likeness is unmeasured.

| # | Research item | Source class | Model |
| --- | --- | --- | --- |
| 1 | Round air cleaner with a 360 label | Target | Met |
| 2 | Rolled, domed cleaner | Target (earlier review) | Met |
| 3 | Rounded valve covers | Target (earlier review) | Met |
| 4 | 90 degree V, 4.75 in bore pitch, 9.21 in deck, driver bank forward | General knowledge | Met |
| 5 | Distributor at the front, on the timing cover | Text source | Met |
| 6 | Fuel pump on the timing cover | Text source | Met |
| 7 | Oil filter on the oil-pump cover at the timing cover | Text source | Met (angle assumed) |
| 8 | Front oil filler on the timing cover | General knowledge | Met |
| 9 | Alternator on the passenger side (1972+) | Text source | Met |
| 10 | Factory Motorola alternator | Text source | Partial: generic round case, not a Motorola-specific shape |
| 11 | Passenger-car forward-centre sump | Text source | Met |
| 12 | Metallic blue engine enamel | Vendor claim | Met (shade unconfirmed) |
| 13 | Painted stock valve covers; chrome is dress-up | Listings | Met (`stock` default, `dressup` option) |
| 14 | Log-type exhaust manifolds | General knowledge | Unverified |

Result: 12 of 14 met, 1 partial, 1 unverified. The remaining gap to real likeness is the image comparison in Open work 1.

## Verification (`verification/engine_check.json`)

| Check | Result |
| --- | --- |
| Evaluated triangles | 29,818 (target about 30,000) |
| Degenerate faces, zero-length edges, loose vertices, non-manifold edges | 0 in all objects |
| Open boundaries | 0, except the intentionally flat 360 label |
| Winding and normals | No inconsistent edges; all closed shells have outward normals by signed volume |
| Unintended intersections between objects | 0 |
| Intended seated contacts | Listed pairs only, such as leads into boots and cap towers, hoses onto nipples, shank into boss, filter onto adapter and pump flange to cover |
| Determinism | Independent builds produce identical per-object geometry hashes |

Single objects can contain overlapping closed sub-shells where cast or bolted pieces join; no booleans were applied.

## Bay fit (`verification/bayfit_v10_emptybay.json`)

- Car: the user-supplied V10 empty-bay fitting reference, `Javelin_CurrentV10_EmptyBay_FittingReference.blend`, SHA-256 `d8b32bd9...1523d`. This is a reference subset of accepted V10, `8c3c4764...ba9f`. The reference is not stored in the repository, and its hash was unchanged after the fit.
- Root **(0, 1.49, -0.235)**. These are project-fit values, not factory measurements.
- Contacts: **none** with any car mesh. Closest approach is 15.6 mm, to `Body`.
- Hood: both rig actions, `DSI_Hood_Open` and `DSI_Reference_Combined_1_26`, swept at 51 half-frame samples each (102 total), from 0 to 29.6 degrees. Minimum clearance is 59.5 mm, at the air cleaner with the hood closed. No overlaps occurred at any sample; clearance grows as the hood opens.
- A root search on V10 showed firewall and floor-extension contacts at y 1.30 to 1.40 and minor `Body` contact at y 1.45. Contact-free roots start at y 1.49; y 1.53 is also contact-free.
- Not checked: front-wheel steering or suspension travel (the reference has no such animation), radiator and shroud (not in the car), transmission and tunnel fit (no transmission modelled), and engine mounts (none modelled; the reference warns against inferring them).
- `AMC360_BayFit_V10_DIAGNOSTIC.blend` is a separately named copy of the reference with the engine appended. It is not a car checkpoint.
- An earlier fit against the historical `assets/current-stl/` snapshot found contacts only with placeholder liners and STL patch artifacts. Those objects are absent from V10, so that result is superseded.

## Renders (`assets/engine-amc360/renders/`)

Cycles CPU renders of the actual mesh, not illustrations: front quarter, rear quarter, side, front, top, label close-up and the component isolation (exploded) view. Fit evidence: the open bay at frame 26 of `DSI_Hood_Open`, top view, closed-hood exterior and section slices (red is car, blue is engine).

## Licenses and dependencies

All geometry, materials and the label strokes are original and procedural. Nothing was downloaded, traced or reused, and no reference image is bundled. Tools used, which are not redistributed with the asset: Blender/`bpy` 5.2.1 (GPL-3.0-or-later; Blender states that its output files are not covered by the GPL), Cycles and OpenImageDenoise (Apache-2.0), and Pillow (MIT-CMU) for the section diagram only. This is a record, not a legal guarantee; review before commercial distribution.

## Open work

1. Allow image access (`amccf.com`, `rmsothebys.com`, `cdn.rmsothebys.com`, or other photo sources), then compare against the illustration, block drawing, the 1974 comparable car and target frames. Correct pressing shapes, distributor and filter position, colours, fan and manifolds.
2. Recheck the fit against steering and suspension once available, and against any radiator, shroud, mounts or transmission added later.
3. Export and import tests for any game pipeline. Compatibility is not claimed.
