# Preserved disk-save reconciliation

The preserved disk save contains no detected authored vehicle or staging changes relative to the frozen front checkpoint. Its differences are viewport/selection state and two unassigned utility node groups. Keep the preserved save; no model merge is indicated by this comparison.

## Inputs

- Frozen `build/parity-cycle11/front-checkpoint/assets/Javelin73PC.blend`: SHA256 `7985de86a18e3e0df4b6d1ba0299487d8b27ba394173213a4d9998147e676167`.
- Preserved `build/live-preservation-cycle13/disk-save-3ddceda7.blend`: SHA256 `3ddceda75652261abd66a472ceb8c8b5e0d9b1f21adc6ee70a57fe19e46ae182`.
- Blender 5.2.1 background reads, factory startup, automatic scripts disabled. Neither blend nor the live GUI was mutated. Both hashes remained unchanged after inspection.

## Exact comparisons

All 15 mesh objects match, comprising 11 vehicle parts and four wheel previews. Exact typed-array hashes and discrete values match for positions, connectivity, loops, UV layers, active UV index, weights, vertex groups, corner normals, sharp edges, seams, polygon smoothing/material indices, material slots and non-selection mesh attributes. Object transforms, parenting, modifiers, constraints, animation assignments and custom properties also match. No mesh has shape keys.

The bounded state comparison found zero differences in the seven rest bones, seven pose bones, rig constraints, three actions and their keyframes, materials and node/socket settings, images and packed bytes, external libraries, object set, staging objects, scene/render/world settings and color management. This compares explicitly collected finite properties rather than recursively traversing RNA ownership graphs.

## Differences

- 56 editor-state leaves: 15 selection flags, one properties-editor search-results list and 40 viewport projection, rotation, matrices and camera-zoom leaves. The save changes the inspected viewport from perspective to orthographic. Scene frame and authored camera/staging data match.
- Added `i.visualizer` and `i.mixer` Geometry Node trees. Both have fake users. `i.visualizer` contains two references to `i.mixer`; no object has a Geometry Nodes modifier, and no material/world/compositor tree or other group references `i.visualizer`. They do not affect the car. Preserve them in the backup rather than silently deleting them.

## Evidence and limits

Machine-readable evidence is in ignored `build/live-preservation-cycle13/`: `meshes-exact.json`, `state-comparison.json`, both full state snapshots and `dependency-users.json`. The reviewed scripts and successful process logs are retained there. An initial dependency probe encountered the removed `Scene.node_tree` property; the corrected finite probe uses the installed scene compositor group and completed successfully.

This verdict covers the two hashed saved files. It does not claim to inspect later edits or an unsaved live session. It establishes preservation safety, not reference likeness, export correctness or native-game appearance. Front-fender refinement remains open.

DOX pass: root and assets contracts were reviewed. Their preservation rule and ownership already cover this read-only record, so no contract or child-index changes were needed. No production source, blend, package or GUI was changed.
