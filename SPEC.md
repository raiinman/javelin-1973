# DSI Javelin 1973

## Objective

Develop a reusable, editable 1973 AMC Javelin AMX Pierre Cardin vehicle asset from the user-owned STL and restored red reference car. The canonical vehicle source is independent of any one game. Reusability is the project direction, not a claim that the model is finished, optimized or ready for every engine.

Current source authority and exact identity live in [current-work](current-work/README.md) and its [artifact manifest](current-work/artifact-manifest.json). V41 supersedes earlier model checkpoints, not their research, preservation duties or evidence history.

## Source and visual requirements

- Preserve the user-owned STL's overall body authority and original project work. Preserve accepted Meshy cockpit appearance while fitting and reducing it as needed.
- Depict the reference car's red body, black hood/fender T, close-fitting chrome side pipes, recognizable trim, four rear lamps and Cardin cabin. The visible 360 air-cleaner label does not authenticate engine internals or factory options.
- Keep geometry, panel ownership, rig/motion, material and texture organization editable. Preserve original and superseded work as inactive history instead of overwriting it.
- Continue section-based reference comparison and whole-vehicle visual review. Source checks and adopted iterations are not final likeness approval or a numerical fidelity measurement.
- Correct body and slicing as needed without inventing unnecessary new underneath structure. Hidden optional modules are not automatically part of an export.

## Structure and ownership

| Location | Role |
| --- | --- |
| `current-work/` | Current external canonical artifact identity, bounded receipts and documentation images |
| `docs/` | Portable status, research, integration gates and checkpoint-specific history |
| `assets/` | Preserved original artwork and historical model sources |
| `.img2blender/` | Reconstruction intent and historical section-review evidence |
| `Javelin73PC/`, `tools/` | Historical PZ package and its procedural build/verification tools |
| `camera/`, `fast-load/` | Independent PZ products with separate contracts and unchanged status |

The current cloud source is not included in a clone. Do not rename old Git-stored binaries or procedural generators to imply they reproduce it.

## Independent acceptance gates

1. **Editable asset:** verify exact source identity, visible assembly, packed/external dependencies, units/axes, ownership, normals, seams, motion and material references against the reviewed checkpoint.
2. **Visual refinement:** inspect actual pixels against the correct target references in matched and complementary views. Preserve disagreements and inferred dimensions.
3. **Target export/import:** validate the exact exported source, writer/tool versions, transforms, materials and target requirements. A successful export is not successful native behavior.
4. **Native runtime:** assess appearance, controls, driving, braking, physics/collision, damage and persistence as applicable to that target. Do not transfer acceptance between checkpoints or games.
5. **Release:** separately review packaging, performance, provenance/license notices and publication authorization. Source synchronization alone is not release authority.

## Integration lanes

- **Wreckfest:** active runtime-fix ownership belongs to Claude. Use Blender / the existing writer into official `bgeometry` tooling, not a mandatory Max conversion. The user's patched-V40 garage screenshot is a bounded milestone only. See [integration status](docs/integration-status.md).
- **Project Zomboid:** preserve the historical `Javelin73PC` integration and its unique identifiers. The last user-confirmed historical target is 42.20.4; older 42.20.0 syntax records retain their original scope. No V41 port or current native acceptance is claimed.
- **Other targets:** research and adapt only within separate authorization. No universal engine support promise.

## Boundaries

Keep this repository private and preserve history, source/binaries, licenses, installations, mods and saves. Do not copy unrelated donor-mod assets. No PC control, model/exporter implementation, game execution, asset upload or new image publication is part of this documentation refresh. The repository was renamed on 2026-10-29 to [raiinman/javelin-1973](https://github.com/raiinman/javelin-1973), preserving its identity, private visibility, default `main` branch and history.

Earlier PZ-specific specifications and test results remain available in Git history and the linked development records. Their local install/test instructions do not authorize a new run for this broader asset project.
