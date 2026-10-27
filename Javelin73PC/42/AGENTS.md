# Build 42 gameplay package

## Purpose
`42/` owns the original `Base.Javelin73PC` vehicle definition, version metadata, localization, loot and world spawn registration.

## Ownership
Models, animations and textures resolve from `../common/media/`. This folder owns gameplay configuration only.

## Local Contracts
- Require Project Zomboid 42.20.0 or newer in `mod.info`.
- Reference native mechanics templates selectively. Keep original `J73_` models on every visible component and tire.
- Preserve two physical doors and four seats. Rear passengers use the corresponding front door.
- Keep native interaction targets outside the 0.15 m padded vehicle navigation polygon. Native side-area targets move inward by 30% of area width; longitudinal service targets move inward by 30% of area height. Side area centres and passenger outside offsets use 1.45 m; front/rear service area centres use 3.0 m. Preserve at least 25 mm clearance beyond navigation padding.
- Keep vehicle model offset and centre-of-mass offset at zero. Wheel offsets and source geometry already share the authored origin. Adding 0.65 m to both shifts native wheel connections upward and lets suspension compression place the rigid-body origin below ground, producing a native seat path target on floor -1. Zero offsets preserve the body/wheel fit and keep native walk-up targets on floor 0.
- Represent the reference car's white-ball manual shifter with four forward gear ratios. Ratios are authored gameplay tuning, not verified factory specifications; the game retains its native shifting controls. Use native sports-car sounds and mechanics for the side-exhaust presentation.
- Register only `Base.Javelin73PC` in existing vehicle zones; never replace zone tables or other vehicles.
- Append a unique `Javelin73PC` loot entry using native sports loot pools.
- Localize with `IGUI_VehicleNameJavelin73PC` in `IGUI_EN.txt`.
- `Javelin73PC_Visual.lua` defines only the original `J73Vehicles.InitInterior(vehicle, part)` shared init callback. The permanent itemless `J73Interior` part must explicitly enable its `Default` model on native initialization, including loaded vehicles. A model declaration alone does not activate it. Preserve the two-argument signature and idempotent native visibility call; do not override vanilla globals or add startup events.
- Keep callbacks on current native mechanics implementations. Do not replace global vehicle functions or mechanics overlays.
- Exterior models use the native vehicle shader and original semantic J73 texture masks for lamps, glass, panels, damage and rust. Palette alpha255 preserves red paint instead of random hue changes.
- `J73_Panels` runs from closed to open. Open uses normal playback; Close reverses it.
- Windows use independent `J73_WindowLeft` and `J73_WindowRight` clips through `ClosedToOpen`, with `animate=false` and `reverse=false`. Native window `openDelta` selects the clip position, from closed at zero to lowered at one. Preserve the inherited door parent and native window sound animations.

## Work Guidance
Use the installed Build 42 generated vehicle templates as the compatibility authority. Changes to seat positions, wheel centres and palette paths must match the original model source.

## Verification
- Run `tools/validate_mod.py` from the repository root when available.
- Resolve native template names against the installed game and verify balanced script blocks.
- In-game verification must cover spawn, all four seat entries, driving, removable parts, panel animation, light beams, fuel, loot and save/reload.

## Child DOX Index
None.
