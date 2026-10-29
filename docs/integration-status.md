# Integration status and evidence boundaries

Snapshot: **2026-10-29**. The reusable editable vehicle asset is primary. Each integration lane must bind its own export, native observation and acceptance to an exact source checkpoint. See [current asset](../current-work/README.md) and [project specification](../SPEC.md).

## Wreckfest: current runtime work belongs to Claude

- The user's PC target is Wreckfest installed through the Xbox app / Microsoft Store. Do not replace the installed edition or touch its files as a side effect of documentation work.
- The route is **Blender / the existing writer → official `bgeometry` tooling**. There is no Max requirement.
- A user-provided screenshot confirms that **patched V40 using the temporary 158 donor-sphere workaround reaches the garage**. The screenshot is conversation evidence, not a newly published repository capture.
- This is a bounded native-load milestone, not driving, physics/collision, damage, controls, persistence or release acceptance. It does not validate the later V41 source, every package variant or every Wreckfest edition.
- Claude owns the current runtime fix. This housekeeping does not modify, export, stage, launch or test that work. No donor geometry, game content or new assets are uploaded here.

### Preserved failure history

The user/Claude handoff reports that V40's `body.vhcl` had **zero `collision_sphere` objects**, producing a zero-node soft body and a null read during Register physics. This is a **handoff-reported diagnosis**, not independent dump analysis by this housekeeping. The initial converter aggregate of 143 simulation nodes / 29 spheres did not certify body-specific soft-body readiness.

Later insertion of 158 donor spheres and official conversion led to the garage success shown in the owner's screenshot. At that evidence point, donor positions were not fitted; wheels/floating parts, donor thumbnail, proxies and panels remained unresolved. The latest user direction says Claude is fixing it; no new fix result is asserted here.

Keep this pre-fix failure and its original records separate from the patched load milestone. Do not erase a failed input/result or relabel it as successful because a workaround loads. No dumps, local paths, new screenshots or private runtime-artifact hashes are published.

Historical PZ failures also remain in their original records, including [native skin failure](native-skin-failure.md), [full-STL conversion](full-stl-trace.md) and [Meshy native tests](meshy-native-test.md). Those are not Wreckfest results.

### Remaining Wreckfest gates

Bind the exact source and exported package first. Then independently verify native appearance/materials, wheel and suspension/physics behavior, controls/driving/braking, collision/damage, required persistence and package performance. Any workaround needs its own scope/provenance review before release. A successful garage load alone closes none of those gates.

## Project Zomboid: preserved historical integration

The last user-confirmed historical target is **42.20.4**. Older 42.20.0 syntax/import observations remain tied to their recorded inputs. Preserve `Javelin73PC` identifiers, assets, scripts, source, tests and existing status; do not rewrite them to match the neutral project name.

- [Historical import contract](import-contract.md), [verification](verification.md), [full-STL work](full-stl-trace.md), [Meshy native tests](meshy-native-test.md).
- `tools/build_mod.py` reproduces the earlier procedural model, not V41.
- Earlier static/import/pose/native results do not establish a V41 export or current gameplay acceptance.
- Current PZ porting, installation and testing are not resumed by the broader asset framing.

## Other engines and delivery

Reuse remains a goal, not a compatibility matrix. Each new target requires explicit scope and its own units/axes, topology/budget, materials, rig/animation, collision and native acceptance evidence. No universal engine-ready or final-quality claim is made.

Keep the repository private. Source synchronization is not Workshop or public-release authorization. Machine-local inventories and private download links are not portable project documentation.
