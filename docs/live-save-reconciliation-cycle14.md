# Saved Blender file reconciliation

The current disk save was copied before inspection to `build/live-preservation-cycle14/disk-save-a8de6dbb.blend`. Its SHA-256 is `a8de6dbbabefc4e327fc2a333529dda142b644697e34997ec51d5dfe0bc4936a`, matching `assets/Javelin73PC.blend` at preservation time. This inspection did not save, reload or otherwise change the user's running Blender session.

The comparison baseline is the frozen `build/parity-cycle11/front-checkpoint/assets/Javelin73PC.blend`, SHA-256 `7985de86a18e3e0df4b6d1ba0299487d8b27ba394173213a4d9998147e676167`. Later fender trials were not used as this baseline.

## Findings

- All 15 mesh objects, including the 11 vehicle meshes, match exactly in the inspected arrays and properties: vertex positions, topology, UVs, weights, corner normals, sharp edges, seams, smoothing, material indices/slots, non-editor attributes, shape-key state, transforms, parent relationships, modifiers, constraints and animation assignments. The mesh comparison found no changed fields.
- The rig, seven rest bones, seven pose bones, three actions and their keyframes match exactly in the bounded comparison. Materials and their node trees, packed images, external libraries, staging objects and scene/render/world settings also match.
- There are 56 editor-state differences and two additional geometry node groups, `i.visualizer` and `i.mixer`. Neither group is assigned to an object modifier or a material/world/scene tree. `i.visualizer` references `i.mixer` twice; both have fake users. They remain preserved in the backup.
- No saved vehicle-model edits require merging into the procedural baseline. This finding covers the preserved disk save only. It does not establish that the running Blender session has no newer unsaved changes, and does not authorize discarding those changes.

## Evidence

The ignored `build/live-preservation-cycle14/` folder contains the preserved save, finite comparison scripts, `meshes-exact.json`, `state-comparison.json`, both state snapshots, `dependency-users.json` and the three background Blender logs. Each background process exited successfully. The comparison scripts only opened files and wrote these reports; they contain no Blender save operation.

## DOX review

Root and `assets/AGENTS.md` were read before preservation. No ownership, structure, operating contract or child index changed. Those instruction files remain unchanged. This record documents the existing user-save preservation requirement, without closing any vehicle section or claiming visual parity.
