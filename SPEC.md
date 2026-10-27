# 1973 AMC Javelin AMX Pierre Cardin

## Objective and authorization
Build the driveable car in Bob La Cross's reference video for the installed Project Zomboid 42.20.0. The user's request authorizes implementation and local installation. Keep existing mods and saves intact.

## Assumptions
- Target Build 42.20.0 first, using the installed game's scripts as the authoritative compatibility reference.
- Depict the red, four-seat, left-hand-drive restored AMX with Cardin upholstery, manual shifter and 360-labelled air cleaner visible in the video. That label does not authenticate engine internals or original factory options.
- Create original geometry, textures, rigging and scripts from the video. The unrelated broken mod is technical reference only; none of its assets are part of this project.
- A separate mod ID avoids replacing existing Javelin prototypes.

## Structure and style
- `Javelin73PC/common/media/`: normalized models and textures.
- `Javelin73PC/42/`: mod metadata, vehicle scripts, server spawn and loot registration, translations.
- `tools/`: reproducible Blender build, package validation, local installation.
- `docs/`: source provenance and verification results.
- `assets/`: editable Blender source and preview renders.
- Lua follows the game's table conventions, e.g. `vehicles["Base.Javelin73PC"] = { index = -1, spawnChance = 1 }`.

## Commands
- Build: `& 'C:/Program Files/Blender Foundation/Blender 5.2/blender.exe' --background --python tools/build_mod.py`
- Validate: `python tools/validate_mod.py --game 'C:/Games/ProjectZomboid'`
- Install: `python tools/install_mod.py`

## Plan and checks
1. Inspect the source video and local game templates. Establish units, axes, closed pose and asset provenance.
   The four-pass factory/video research in `docs/research-1973.md` supplies the dimension and trim baseline; retain the video car's visible restored configuration.
2. Create original meshes, red 1973 AMX appearance and striped upholstery. Render a preview and check mesh extents and part alignment.
3. Use native B42 mechanics templates, two doors, four passenger positions, sports parts, gasoline, trunk, headlights, loot, and rare parking/good/sport spawns. No legacy recipes or global mechanics-overlay replacement.
4. Validate model/texture/template/Lua references and geometry; install a new local mod folder. Test loading and spawning in an isolated game cache if the runtime is available.

## Success criteria
- Discoverable as a separate Build 42 mod with vehicle `Base.Javelin73PC`.
- Red Javelin AMX silhouette with Cardin interior, four individual rear lamps and the video's trim details.
- Four wheel models, two functional doors, usable hood/trunk, seats and ordinary maintenance using current vanilla templates.
- World spawn and loot registration does not alter other vehicles.
- No missing mod-owned references, undefined legacy callbacks or unbalanced scripts.
- Verification report distinguishes static, Blender, game-load and actual driving checks.

## Boundaries
- Always: preserve other projects and saves, use unique asset names, validate before installation.
- Ask first: public Workshop publishing or unresolved decisions outside the requested car mod.
- Never: change game installation files, overwrite previous Javelin prototypes, silently claim runtime tests passed.
