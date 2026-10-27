# Changelog

## Unreleased - 2026-10-27 source snapshot

### Added
- Included the current complete STL-based Javelin with accepted Meshy cockpit, restored front enclosure, separate black skirts, narrow brightwork and fitted side pipes as an editable source snapshot with packed textures and checksum.
- Added portable takeover guidance distinguishing the current assembly, preserved procedural mod, independent camera candidate and untested Fast Load revision.

- Added an original procedural AMC 360-style exterior engine (separate file, 29,192 triangles) with verification, actual-mesh renders and a bay-fit diagnostic against the historical car snapshot. Reference photographs were not available in the build session; see `docs/amc360-engine.md` for unverified layout choices.

### Fixed
- Saved and reopened the current car with the assembled cabin and functional panels visible in Material Preview.

This source snapshot is not a Workshop release or a claim of completed native gameplay verification.

## 0.1.1 - 2026-10-17

### Changed
- Rebuilt the raised deck spoiler, curved notched rear bumper and rearward-rolling lower nose after four additional passes on the user-supplied galleries.
- Replaced rear plate placeholders with original Michigan artwork; preserved registration-reading ambiguity in development records.
- Rounded the air cleaner, valve covers and inner front wheel housings; added visible brake-booster and curved-hose forms.
- Added original cockpit dial markings, projected white-shifter-ball markings and moving interior door-release hardware.
- Rounded and tapered the restored car's grille surround after a new front-frame comparison.
- Refined rolled front crowns, smooth fastback and sail sections, curved door outlines and a pressed side character line after four fresh likeness comparisons.
- Rebuilt tapered/reclined Cardin seat padding and projected cushion ribbons onto actual support triangles.
- Replaced coarse grille wires with original fine repeating artwork; added an estimated low perspective source view and source-only material finishes.
- Added factory body-width, recessed rear-lens ray and curved cushion-support checks.
- Rebuilt candidate cabin proportions and flared fender sections; whole-car likeness remains under review.
- Added a shaped grille, recessed lamps and moving trunk return/spoiler.
- Added rounded tires and dished five-spoke wheels, preserving wheel radius and steering clearance.
- Reconstructed the hood/fender T graphic and original vector emblems/lettering, with three additional source decal passes.
- Credited Dead Signal Interactive and removed optional FBX exporter provenance and local texture paths from the distributed assets.

### Fixed
- Removed the painted runner above both side pipes; rebuilt close-set mirrored pipes with curved inlets, perforated chrome guards and hollow rear outlets from the user's purple-car reference.
- Corrected the rear sail blend so its upper and lower seams follow the local body sections instead of a frozen quarter-tip boundary.
- Closed the opening below the crowned rear glass with an apron following all seven sampled lower-edge columns.
- Corrected cabin-facing upholstery normals and matched the headliner ribbon tessellation to its base so its rounded corners remain visible.
- Shortened the excess rear overhang to match the factory body length while preserving axle and cabin positions.
- Aligned the door skins, frameless door glass and rear quarter-window trim using shared frame anchors and narrow perimeter gaps.
- Closed the fixed rear-deck surfaces that disappeared under the game's backface culling.
- Added recessed door jambs and closed the quarter-window/sail-panel and trunk-to-tail gaps.
- Seated the rear spoiler lip and tucked the dashboard behind the windshield.
- Moved seat and service interaction points outside the native navigation obstacle so walking to them can succeed.
- Corrected the physics coordinate origin so seat pathfinding targets the ground floor under suspension load.
- Closed the hood/grille return and hood underside; lined the engine and cargo compartments.
- Extended window travel to 0.45 m so the glass retracts below the beltline.

### Added
- Original continuous Cardin U seat ribbons, coordinated headliner, PC fender crests and restrained AMX dash detailing.
- Source checks for door/window fit and outward-facing rear-deck surfaces.
- Full mesh winding and orientation checks using the native import flags.
- Opt-in isolated tests for native timed entry, component maintenance, lights and saved vehicle state.

## 0.1.0 - 2026-10-17

### Added
- Original red 1973 AMC Javelin AMX Pierre Cardin model, textures, rigging and Build 42 integration.
- Four seats, two doors, native sports-car mechanics, loot and rare world-spawn registration.
- Reproducible Blender source, native import checks and isolated powered-movement/braking tests.
