# Project status and takeover

Snapshot date: 2026-10-27. Read root `AGENTS.md` and the applicable child contracts before editing. The repository contains three independent development products, not three finished Workshop releases.

## Current vehicle

Open [`assets/current-stl/Javelin73PC-current.blend`](../assets/current-stl/Javelin73PC-current.blend) for the latest assembled car, with the accepted Meshy cockpit, V03 cabin closures, separate black skirts, exterior brightwork and closer side pipes. [`source.json`](../assets/current-stl/source.json) records its exact authoring-source hash. The older [`assets/Javelin73PC.blend`](../assets/Javelin73PC.blend) and root `Javelin73PC/` package are preserved procedural production work, not the latest STL prototype.

The saved active assembly was reopened on 2026-10-27: cockpit and functional panels are visible and Material Preview persists. Original/alternate sources remain hidden to prevent overlap. This was a display correction, with no geometry edit. Keep unsaved live Blender work before switching documents.

The complete user-owned STL controls body proportions. The restored-car video controls fitted equipment, artwork and interior. The user accepted the corrected Meshy front-seat appearance; continue fitting/reduction without rejecting its appearance merely for polygon count. Current priority is an economical presentable prototype. Headliner, Cardin door panels, rear enclosure coverage and whole-car reference parity remain open. Exact small lettering and fine artwork remain deferred under the root contract.

Read [`full-stl-trace.md`](full-stl-trace.md), [`exterior-brightwork-pipe-fit.md`](exterior-brightwork-pipe-fit.md), [`meshy-car-integration.md`](meshy-car-integration.md), [`cabin-closure-restoration.md`](cabin-closure-restoration.md) and [`meshy-native-test.md`](meshy-native-test.md). Older export holds and source paths describe historical iterations; root records their superseding user decisions.

The latest historical textured export is local under `build/stl-full-trace/slice-v03/integration/export-meshy-prototype/`. Its recorded importer, script, pose and atlas checks do not establish final driving, braking, interaction, seated-character visibility, appearance or save/reload acceptance. Those gates need reconciliation against the exact native-tested checkpoint. The display save has not been re-exported.

Use the dedicated textured atlas export path for the Meshy assembly. The old palette-only adapter can overwrite the accepted cabin UVs. `tools/build_mod.py` builds the earlier procedural source, not this STL assembly. A clone contains the editable current checkpoint; the complete experimental export pipeline and historical evidence still require the local development archive.

## Camera

Read [`camera/AGENTS.md`](../camera/AGENTS.md), [`camera/SPEC.md`](../camera/SPEC.md) and [`camera/verification.md`](../camera/verification.md). Candidate 0.1.1 provides native zoom and native PanCamera binding guidance with fixed isometric orientation. Native input/picking, lifecycle, compatibility and Workshop checks remain. Full gameplay 3D rotation is unproven. Floor reconstruction and framebuffer transformations are separate research probes, not product dependencies.

## Fast Load

Read [`fast-load/AGENTS.md`](../fast-load/AGENTS.md) and [`fast-load/verification.md`](../fast-load/verification.md). Current 0.0.8 is explicitly untested. Preserve the user's instruction to edit/package without running tests, syntax compilation or game launch unless superseded. It must stop at the main menu and never auto-load a save. Older 0.0.1 auto-continue evidence is superseded. Current artwork, 120-tip library and explicit startup-mod matching have documented unverified lifecycle/persistence/performance limits; no measured speedup is established.

## Local environment and publication

Native work uses the existing isolated Toolkit profile and Connection > Launch Project Zomboid (test profile), with debug mode. Read [`toolkit-setup.md`](toolkit-setup.md); verify desktop-side staging before use. Preserve normal saves, unrelated mods, game files and existing shortcuts. Toolkit is a game/debug/editor bridge, not a mod manager. Installed game/Toolkit, profile state, skills and bridge configuration are external prerequisites, not bundled dependencies.

GitHub contains original product sources, runtime assets, editable artwork, current model and portable records. Ignored `build/` retains local experiments, raw reductions, older checkpoints, reference captures and native receipts. Machine-specific Marlow handoff files and inventories remain local for pickup. This repository is not a full backup of that development archive. No Workshop publication is authorized by source synchronization.

## Synchronization checks, 2026-10-27

- Current STL snapshot: SHA256 matches the saved authoring checkpoint; background Blender inspection confirms packed textures, no linked libraries, visible cockpit/panels and saved Material Preview.
- Preserved procedural `Javelin73PC/` package: static validator reports zero errors; five files parse using installed game classes; native FBX probe resolves eleven meshes and three named clips; all 42 tools unit tests pass. These results belong to the procedural package and tools, not the newer STL native export.
- No game world was launched. Fast Load tests and syntax compilation were not run, preserving its explicit untested status and user instruction.
- Camera candidate: its controlled zoom-adapter fixture, sample behavior, UI syntax and standalone five-file packaging checks pass. Native gameplay remains separate.
