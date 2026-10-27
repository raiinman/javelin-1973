# Cabin closure restoration

The active prototype carries the accepted Meshy cockpit, separate downward black skirts and the original project cabin equipment. Missing enclosure pieces must be restored from our pre-STL work where compatible, with actual source geometry distinguished from newly inferred closures. The unrelated third-party Javelin mod is not an asset source.

## Source and preservation

- Input: `build/stl-full-trace/slice-v03/integration/prototype-meshy-v02-skirts/DSI_Javelin_Meshy_Interior_Skirts.blend`.
- Restoration work: `build/stl-full-trace/slice-v03/integration/prototype-meshy-v03-closures/`.
- `original-components.json` and `original-inspection.log` inventory the actual authored pre-STL source. `inputs/` freezes the consumed blends and source modules.
- The original floor slab and cowl return are recovered and fitted. No explicit continuous original firewall was found; the old solid dashboard concealed missing enclosure. The toe-board/firewall and adjoining side returns are new inferred geometry.
- Preserve every existing exterior, skirt, pipe, moving panel and accepted Meshy mesh, its transform/material assignments/UVs, packed textures and occupant registration. Added enclosure pieces remain separate editable objects.

## Verification boundary

Use same-view footwell and behind-dashboard renders, a saved-file reopen, existing-mesh and packed-image comparisons, new-solid normals/manifold checks, static clipping checks and longitudinal visibility probes. Bounded checks do not establish animated clearance, seated-character visibility or native appearance. Keep the accepted cockpit appearance and export hold in place; do not overwrite textured UVs with the palette-only adapter.

Root owns this ignored experiment and its records. Existing product/tool child contracts and Child DOX Indices remain unchanged because no installed package or domain boundary changes.

## Checked V03 result

Saved source: `DSI_Javelin_Meshy_Cabin_Closures_V03.blend`, SHA256 `8fdc2c7a1f445f0719cca3d26bea241d311c463c300c2ed6592954356cdfeb4b`. Reopen checks preserve all 48 preexisting meshes (including attributes, UVs, custom/evaluated corner normals, material slots and transforms) and all four packed images. Five added solids have positive outward volume and no zero-area faces. The 155 static/door-pose checks report no unplanned strict crossings. The floor deliberately overlaps the retained floor by 11mm; 13 seam samples show maximum height step 1.49e-8m. A 460-ray forward footwell grid has zero open rays after the correction, versus 194 before. These are bounded source checks.

The material driver-footwell and before/after behind-dashboard views were independently inspected. V03 is loaded in the existing Blender window after preserving the user's skirt session; `integration/closure-live-reconciliation.json` records no bounded source differences before loading. The firewall is selected and the current interior is visible. No installed mod or native export changed.

## Remaining original interior pieces

The original downward headliner has 234 recoverable faces but is absent from the active cabin. Original Cardin door cards, pulls and cranks are archived; active door faces lack their upholstery. Those require a separate fit to the STL roof and moving doors, rather than blind reuse of the old dimensions. Rear parcel-shelf and rear wheel-tub/cargo-cover completeness remain unverified. `restoration-inventory.json` records these omissions. This checkpoint fixes the front enclosure and does not close the interior parity work.
