# Textured Meshy native prototype

The user authorized export, isolated installation and game testing on2026-10-19, superseding the prior Meshy export hold. Source: `integration/prototype-meshy-exterior-trim/DSI_Javelin_Meshy_Exterior_Trim_Pipes.blend`, SHA256 `bf17f37889cba01d75c922dea60763d73bb88b3cd91db4a7c1020d8f59446e85`. It includes the accepted V02 cockpit, V03 front enclosure, separate black skirts, narrow brightwork and85mm inward pipe translation.

## Export contract

`build/stl-full-trace/slice-v03/integration/export-meshy-prototype/` owns this isolated export. `assemble.py` merges active extras into16 semantic export copies according to fixed/moving ownership. Source geometry remains untouched. `textured_slice_adapter.py` is a separately adapted copy, with `texture_atlas.py`/`pack_atlas.py` packing the four cabin textures and semantic vehicle swatches. Do not use the palette-only source adapter on textured cabin UVs.

All eight runtime textures are4096x4096. Four accepted image tiles are resized to1784px with4px edge gutters inside1792px regions. This preserves appearance with a modest texture-resolution reduction for the prototype; it does not preserve Blender clear-coat or PBR shading. Cabin texture regions use neutral native masks. Original semantic panel/glass/light masks remain separate. Body mask zones are recovered by matching polygon coordinates against I5, avoiding shifted indices after skirt-face removal.

## Verification

Native importer16 meshes/3 clips; five game script parses; static0 errors;16 bounds/108 imported-pose comparisons; native four-seat passenger flags pass. All17 payload hashes match. The four cabin atlas tile pixel interiors match independently resized source images. Exported Blender UV verification covers221,997 loops/73,999 textured faces, maximum error2.98e-8. This is not a native UV0 visual check. Exact commands, dependencies and hashes are frozen under `verify/`.

## Deployment

`deploy.py` backs up the owned isolated profile's existing `mods/Javelin73PC`, stages the checked17-file package and verifies exact payload hashes. Backup is recorded in `deployment.json`. Normal-profile mods, game files, unrelated mods and saves are untouched. Launch through Toolkit `game_launch` with the existing isolated profile and `-debug`. Native appearance and user operation remain separate from importer checks.

DOX: root records the newly authorized export/test workflow. Product/tool child contracts and Child DOX Indices are unchanged because the authored source and isolated deployment do not alter production ownership or original product files.
