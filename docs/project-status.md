# Project status and takeover

Snapshot: 2026-10-27 18:48 UTC. This repository remains private. Read root and applicable child `AGENTS.md` before editing.

## Current vehicle: body correction and slicing

The reviewed **BodyOnly V03** checkpoint, SHA-256 `668ffbaed111e20833c963a519ce04373525dd7e873b5957ed8bea24aabbfa90`, is current authoring authority. [Current work](../current-work/README.md), [artifact manifest](../current-work/artifact-manifest.json), [15-check scope/preservation receipt](../current-work/receipts/body-only-v03-preservation.json).

User direction: the elaborate new underneath structure is unnecessary for this Project Zomboid task. Correct the existing body geometry and slice it properly; do not add more now. V03 preserves all optional work but hides/excludes 69 new underside meshes and four empties, restores the original main floor/tunnel and retains the original side pipes and rear structures. This scope correction added/deleted no raw geometry. Actual body repair is pending review, not certified by the preservation checks.

Current user-confirmed PZ target is 42.20.4; Blender authoring is 5.2.1. No V03 export/native-game acceptance is claimed. Earlier V01 runtime experiments and old package receipts are historical input-specific evidence, not validation of the current model. The later goal is Wreckfest for PC installed through the Xbox app/Microsoft Store. Custom-mod/import support for this exact edition and the delivery route remain unverified.

## Research, history and clone limits

[Actual-car research remains relevant](research-index.md). Preserve measurements, photo/video citations, disagreements and provenance. Superseded model critiques apply to their recorded checkpoints.

The V03 binary remains external to this Git tree. A clone does not contain it or the full cloud development archive. The existing `assets/current-stl/` snapshot, its unchanged `source.json`, `assets/Javelin73PC.blend` and `Javelin73PC/` remain historical work. `tools/build_mod.py` builds the older procedural model, not V03. Do not use old filename labels or palette-only export to overwrite the newer source/cockpit.

## Camera

Candidate **0.1.1** provides native zoom and native PanCamera binding guidance with fixed isometric orientation. Read [contract](../camera/AGENTS.md), [specification](../camera/SPEC.md) and [verification](../camera/verification.md). Existing fixture and limited native observations remain as recorded. Input/picking, lifecycle, compatibility and Workshop checks remain. Full gameplay 3D rotation is unproven; floor/image-transform probes are separate research. This refresh did not alter or resume Camera work.

## Fast Load

Revision **0.0.8 is explicitly untested**. Read [README](../fast-load/README.md), [contract](../fast-load/AGENTS.md) and [verification](../fast-load/verification.md). Preserve the instruction to package without tests, syntax compilation or game launch unless superseded. It stops at the main menu and never auto-loads a save. No measured speedup is established. This refresh did not alter or resume Fast Load work.

## Environment and publication boundaries

The current native environment is not reproduced by a clone. Existing game/Toolkit/profile prerequisites remain external; see [Toolkit setup](toolkit-setup.md). Preserve normal saves, unrelated mods, game files and shortcuts. Source synchronization is not Workshop-publication authority. Keep repository visibility private.
