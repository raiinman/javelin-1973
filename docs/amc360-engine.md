# AMC 360-style exterior engine

Original, game-oriented exterior model of an AMC 360-style V8 for the 1973 Javelin AMX Pierre Cardin project. Built 2026-10-27 with Blender 5.2.1 LTS (the official `bpy` 5.2.1 module) from the deterministic source `tools/amc360_engine.py`. Verification, renders and the car fit come from `tools/amc360_engine_review.py`.

This is a visible-exterior asset. It is not export-staged, has not been imported into Project Zomboid or Wreckfest, and is not part of the current body-only scope or the distributed mod.

## Evidence boundaries

| Class | What it supports | Source |
| --- | --- | --- |
| Target evidence | A round air cleaner with a visible 360 label (about 1:07); rolled domed cleaner and rounded covers recorded in earlier reviews | `research-1973.md`, `reference-study.md`, `likeness-four-pass.md`. The video was not re-watched in this session. |
| Comparable-car evidence | None inspected in this session | The supplied AMCCF illustration, AMCCF block drawing, RM Sotheby's lot page and its engine photo were all blocked by the session network policy (`amccf.com`, `rmsothebys.com`, `cdn.rmsothebys.com`). The clone has no photo archive (see `research-index.md`). |
| General family knowledge, unverified here | 90 degree V8, 4.75 in bore spacing, 9.21 in tall-deck crank-to-deck height, driver bank forward, front-mounted distributor and front oil filler on the timing cover | Author knowledge of the 1966-91 AMC V8 family. Recheck against the blocked references. |
| Fit and layout assumptions | Alternator on the passenger side, rear-sump stepped pan, oil filter on the lower passenger timing cover, engine colour, Motorcraft-4300-style carburettor body, snorkel direction, single V-belt layout | Chosen for a plausible, clash-free arrangement. These are the first items to correct against photographs. |

The 360 label is visual reference only. It does not prove displacement, internals or factory originality.

## Model

- 28 named mesh objects under `ENG_Root`, grouped as `ENG_Castings`, `ENG_Pressings`, `ENG_FuelIgnition` and `ENG_FrontDrive`. Pivots sit at mounting points: crank axis, pump and alternator pivot, cover rails, the cleaner stud and the distributor base.
- Engine frame: metres, +Y forward, +Z up, driver side -X. Origin on the crank axis at the block front face.
- Cast forms: block with bell flange, core plugs and mount bosses; chamfered heads with plug bosses; a sculpted intake with eight runner humps, plenum and thermostat neck; log exhaust manifolds with port pads, domed ends and a downturned outlet; a timing cover with distributor boss, filter adapter and filler tube; the water pump.
- Pressed forms: valve covers with flange, rolled crown, raised centre panel, flange bolts, breather and PCV grommet; the stepped rear-sump pan with drain plug; the round domed air cleaner with rolled lip, wing nut and forward snorkel.
- Front drive: damper, V-grooved pulleys, a V-belt computed from exact tangents around crank, alternator and pump, four-blade stamped fan, alternator with bracket, pivot and adjuster.
- Ignition: angled front distributor with vacuum canister and cap, eight swept leads running through two loom combs per side to seated plug boots.
- Label: a 40 mm original stroke-drawn "360" on the lid, readable from the front of the car. No font, logo or decal artwork was reused.
- Ten original Principled materials. There are no image textures; colours are placeholders pending reference review.

## Verification (`verification/engine_check.json`)

| Check | Result |
| --- | --- |
| Evaluated triangles | 29,192 (target about 30,000) |
| Degenerate faces, zero-length edges, loose vertices, non-manifold edges | 0 in all objects |
| Open boundaries | 0, except the intentionally flat 360 label |
| Winding and normals | No inconsistent edges; all closed shells have outward normals by signed volume |
| Unintended intersections between objects | 0 |
| Intended seated contacts | 13 listed pairs, such as leads into boots and cap towers, shank into boss, filter onto adapter and pulley onto hub |
| Determinism | Two independent builds produce identical geometry hashes for all 28 objects |

Single objects can contain overlapping closed sub-shells where cast or bolted pieces join, such as manifold stubs into the log. This is normal for game meshes; no booleans were applied.

## Bay fit (`verification/bayfit_historical_car.json`)

- Car used: `assets/current-stl/Javelin73PC-current.blend`, SHA-256 `3b7d3551...0d64`. This is the only car in a clone and is the historical snapshot, not the current Library-only BodyOnly V03. The hash was unchanged afterwards, and no car object's visibility changed.
- Root moved from the suggested (0, 1.35, -0.235) to **(0, 1.49, -0.235)**. At 1.35, the bell flange crossed `Cabin_ToeBoardFirewall` and `Cabin_FloorExtension`, and the air cleaner touched a black cowl wall at y about 1.01 to 1.02. Moving to y 1.44 or later removed the firewall and floor-extension contacts; y 1.49 also clears the cowl wall. These are fit values, not factory measurements.
- Closed hood: minimum clearance 59.5 mm, at the air cleaner, at every half-frame sample from frame 1 to 26.
- Hood motion: this file has **no actions, armature, shape keys or constraints**, so all 51 half-frame samples show the closed hood. The animated V03 rig was not available. As a labelled diagnostic, a rear-edge hinge at (0, 0.898, 0.381) was assumed and swept to 55 degrees: clearance only increases as the hood opens. This is not evidence of the real rig.
- Remaining contacts are all with placeholder, closure or source-artifact faces of the historical car:
  - `Body` faces 16846 to 16876, identical to `STL_SourceBoundary_WheelWell_Patches` 286 to 316: STL hole-fill triangles about 0.7 m across, crossing the empty bay diagonally. They are visible as the grey wedge in the bay renders.
  - `Body` 17765 to 17788: a double-sided flat liner floor at z -0.25. The pan, lower block, damper, belt, filter and manifold outlets pass through it.
  - `Body` 449 to 451, 1089, 16214 and 16216: a flat underbody closure from z -0.32 to -0.41. The rear sump extends about 0.1 m below it.
  - Hidden, superseded `Original_J73Mesh_*` history objects.
- Side liners at x about ±0.347: no contacts after the plug boots, loom and alternator were tucked in. The engine was not narrowed beyond realistic proportions to fit placeholder liners.
- Per the current scope, the car was not modified and no underside structure was added. A real bay needs the car's liner and closure geometry reconciled first.

## Renders (`assets/engine-amc360/renders/`)

Cycles CPU renders of the actual mesh, not illustrations: front quarter, rear quarter, side, front, top, label close-up and the component isolation (exploded) view. Fit evidence: open bay views with the hood hidden (the file cannot open it), the closed-hood exterior, and a sheet of section slices (red is car, blue is engine).

## Licenses and dependencies

All geometry, materials and the label strokes are original and procedural. Nothing was downloaded, traced or reused, and no reference photo is bundled. Tools used, which are not redistributed with the asset: Blender/`bpy` 5.2.1 (GPL-3.0-or-later; Blender states that its output files are not covered by the GPL), Cycles and OpenImageDenoise (Apache-2.0), and Pillow (MIT-CMU) for the section diagram only. This is a record, not a legal guarantee; review before commercial distribution.

## Open work

1. Allow the blocked hosts and compare against the period illustration, block drawing and the 1974 comparable car. Correct the alternator side, sump position, filter location, distributor position, colours and cover details.
2. Rerun the fit against the current V03 car and its real hood rig once that file is available, at frames 1 to 26 in half-frame steps.
3. Hand the remaining body contacts (patch triangles, liner floor, underbody closure) to the body-repair work. Do not resolve them by deforming the engine.
4. Export/import tests for any game pipeline. Compatibility is not claimed.
