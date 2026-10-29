# Project status and takeover

Snapshot: **2026-10-29**. **DSI Javelin 1973** is a reusable editable vehicle asset, with separate target integrations. This repository remains private. Read root and applicable child `AGENTS.md` before editing.

## Canonical editable asset

**V41** is current cloud authoring authority, SHA-256 `aad667f38b8c7a449b0ea148cefa2a71b0c6eecfd568ad2e5c5b6808e8d06289`. The exact reviewed outer-tire candidate was adopted without an additional geometry edit; the prior canonical source remains preserved. [Current work](../current-work/README.md), [artifact manifest](../current-work/artifact-manifest.json).

The asset remains under visual refinement. Adoption/source checks do not certify final likeness, continuous clearance, whole-car quality or engine readiness. Preserve the user-owned STL authority, accepted cockpit, original artwork and optional hidden/export-excluded underside history. Do not add unnecessary underneath structure.

The V41 binary remains external to this Git tree. A clone does not contain it or the complete cloud development archive. The existing `assets/current-stl/` snapshot, unchanged `source.json`, `assets/Javelin73PC.blend` and `Javelin73PC/` remain historical work. `tools/build_mod.py` builds the older procedural model, not V41. Do not overwrite current source/UVs using old filename labels or palette-only export.

The README hero and existing progress images depict **historical V03**, not V41. No new captures/assets are published by this refresh.

## Independent integration lanes

- **Wreckfest:** Claude owns the current runtime fix. User screenshot evidence shows patched V40 with the temporary 158 donor-sphere workaround reaches the garage. Driving and physics remain unaccepted; this does not validate V41. Blender / the existing writer → official `bgeometry` tooling is the route, with no Max requirement.
- **Project Zomboid:** preserved historical package and research, last user-confirmed target 42.20.4. Older input-specific receipts are not current-model approval; this housekeeping resumes no PZ work.
- **Other targets:** potential reuse, requiring separate target-specific export/import, appearance, physics/performance and runtime gates.

[Integration status and preserved failure boundaries](integration-status.md). [Asset specification](../SPEC.md).

## Research and history

[Actual-car research remains relevant](research-index.md). Preserve measurements, photo/video citations, source disagreements and provenance. Superseded model critiques apply to their recorded checkpoints. Keep original crash/failure records separate from later workaround success; do not rewrite history as a pass.

## Camera

Candidate **0.1.1** provides native zoom and native PanCamera binding guidance with fixed isometric orientation. Read [contract](../camera/AGENTS.md), [specification](../camera/SPEC.md) and [verification](../camera/verification.md). Existing fixture and limited native observations remain as recorded. Input/picking, lifecycle, compatibility and Workshop checks remain. Full gameplay 3D rotation is unproven; floor/image-transform probes are separate research. This refresh did not alter or resume Camera work.

## Fast Load

Revision **0.0.8 is explicitly untested**. Read [README](../fast-load/README.md), [contract](../fast-load/AGENTS.md) and [verification](../fast-load/verification.md). Preserve the instruction to package without tests, syntax compilation or game launch unless superseded. It stops at the main menu and never auto-loads a save. No measured speedup is established. This refresh did not alter or resume Fast Load work.

## Environment and publication boundaries

The native environment is not reproduced by a clone. Existing game/Toolkit/profile prerequisites remain external; see [historical Toolkit setup](toolkit-setup.md). Preserve normal saves, unrelated mods, game files and shortcuts. No PC, game, exporter or implementation actions are part of this docs refresh.

The repository rename completed on 2026-10-29: [raiinman/javelin-1973](https://github.com/raiinman/javelin-1973) is the canonical URL. The same repository identity, private visibility, default `main` branch and history are preserved. The old repository name resolves to the renamed repository through the authenticated GitHub connector. External clones/remotes/integrations remain an unverified migration follow-up, not a reason to resume PC work. Keep visibility private and never reuse the old `project-zomboid-javelin-1973` name.
