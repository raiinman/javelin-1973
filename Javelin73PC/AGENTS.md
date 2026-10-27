# Mod package

## Purpose
Original 1973 Javelin AMX Pierre Cardin for Build 42.

## Ownership
`common/media/` assets and `42/` scripts and metadata.

## Local Contracts
Credit Dead Signal Interactive in `42/mod.info`. Package only runtime assets/configuration; exclude development docs, promotional links and optional provenance metadata. Preserve model identifiers, animation data and functional texture references.
Use unique Javelin73PC identifiers. Use native game mechanics templates. Spawn registration must preserve unrelated entries.
- All original meshes use the `vehicle` shader. The generated native vehicle vertex layout does not match `vehiclewheel` UV attributes.
- Door, hood and trunk tracks retain full ancestor transforms. Window-only bone masks layer their independent lowering clip onto the native parent door's animation player.

## Work Guidance
Derive compatibility syntax from the installed 42.20.0 vanilla scripts.

## Verification
Check all mod-owned references, meshes, texture dimensions and Lua hooks with `tools/validate_mod.py`.

## Child DOX Index
- `42/AGENTS.md`: Build 42 gameplay configuration, localization and spawn/loot integration.
