# Purpose

- Preserve the latest assembled STL-based Javelin as an editable source snapshot available from a fresh clone.

# Ownership

- `Javelin73PC-current.blend` is a copy of the verified working assembly, including Meshy cabin, closures, skirts, trim and fitted pipes.
- `source.json` records the repository-relative authoring source, checksum and verification scope.

# Local Contracts

- Preserve the earlier `../Javelin73PC.blend` procedural source and ignored authoring history.
- Keep current assembled components visible in Material Preview; preserve originals and superseded variants hidden.
- Copy only the verified checkpoint. Update `source.json` with each snapshot refresh and distinguish display/asset checks from native gameplay results.

# Work Guidance

- Read `../../docs/project-status.md` and root instructions before authoring or exporting. The old procedural generator does not reproduce this assembly.

# Verification

- Compare the snapshot SHA256 with `source.json` and the verified authoring checkpoint.
- Open read-only in Blender and check assembly visibility and packed image availability. Native gameplay remains a separate gate.

# Child DOX Index

- None.
