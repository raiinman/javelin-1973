# Meshy interior integration

The current combined car is the V03-based exterior trim/closer-pipe checkpoint documented in `exterior-brightwork-pipe-fit.md`. It retains the accepted cockpit and added cabin closures. The user subsequently authorized the textured export and isolated test; see `meshy-native-test.md`. The V03 and V02 records below describe its preserved inputs.

## Active fit correction, export held

The user stopped export after finding the floating instrument panel and unsupported steering column. The current correction is `build/stl-full-trace/slice-v03/integration/prototype-meshy-v02/DSI_Javelin_Meshy_Interior_V02.blend`, SHA256 `d9d921f34fad40f453dfe997130d4f93b2efe2ce6bf89fe5995b51b279245020`. V01 below is preserved history. No export, installation or game launch was performed for this correction; export remains held pending the user's direction.

- The fascia is narrower, bent in depth to follow the opening and recessed into it. Its top/bottom black mounting bezel joins the existing dash lip at98 measured support samples with1mm offset. All96 bezel faces point toward the driver. The fit is authored against the existing dashboard mesh, not factory dimensions.
- The wheel position is retained. Its new shrouded column continues to a joint near(-0.43,0.69,0.0025m), then a lower shaft reaches the measured floor surface. A boot and flange mount it at approximately(-0.43,0.715,-0.2395m).
- `correct_fit.py` reproduces the correction; `fit-report.json` binds hashes, preserved mesh signatures and support measurements. The old column is archived and hidden. Dashboard, wheel, seats, body and all unrelated mesh geometry/transforms are unchanged from V01.
- `verification.json` records35 strict static crossing checks for the corrected fascia and six column/mount components against body, doors, windshield and retained Interior, with no crossings. Deliberate fascia-to-dash mounting contact is separate. Finite-vertex and bezel-winding checks pass. These are source checks, not native-game or occupant-motion verification.
- The dirty live V01 was saved as `prototype-meshy-v02/live-before-fit-20261019T163239700628Z.blend`; the bounded reconciliation reports no authored mesh/transform/material-slot differences. The corrected version is shown in the same Blender window. `cockpit-above.png`, `driver-eye.png` and `column-side.png` show the correction with exterior parts hidden for inspection.
- DOX: root records the export hold and fit requirements. Child contracts and indices are unchanged because no product files, tool ownership or domain boundaries changed.

## Original V01 integration

The four existing Meshy assets are fitted into the complete I5 car in `build/stl-full-trace/slice-v03/integration/prototype-meshy-v01/DSI_Javelin_Meshy_Interior.blend`. The front-seat asset is instanced twice. The dashboard shell, instrument fascia and steering wheel replace the former front cockpit geometry. The original rear bench, floor, console, shifter and compatible I5 equipment remain. Every non-Interior mesh retains its input geometry and object transform, including the body, decals, skirts, pipes and moving panels.

## Source and recovery

- Input I5 SHA256: `5b6eae4aa6f6cd488e9f4be6686acf45649f5461a2b4e28cc75333152f702ff8`.
- Integrated output SHA256: `f6cb6439527cf00511a213c7395664eaaa644b059285458cc0fe906a98b369ff`.
- Raw Meshy sources remain in `build/meshy-seat-trial/` and `build/meshy-cockpit-trial/`. Integration consumes existing downloads; no additional generation credits were spent.
- Dirty live H2 was preserved as `prototype-meshy-v01/live-before-meshy-20261019T103410197630Z.blend`. `live-reconciliation.json` reports no differences in the bounded mesh geometry, transforms and material-slot comparison against H2. Viewport state is excluded.
- `integration-report.json` binds input/output hashes, retained exterior signatures, placements and counts. `integration/live-state.json` records the displayed model and recovery. Prior sources and installed packages remain preserved.

## Reduction and fitting

| Asset | Raw triangles | Fitted triangles |
| --- | ---: | ---: |
| Front seat, each of two instances | 705,980 | 18,000 |
| Dashboard | 602,050 | 15,999 |
| Instrument fascia | 494,118 | 14,000 |
| Steering wheel | 335,960 | 8,000 |

The fitted Meshy meshes total 73,999 triangles across both seats and the three cockpit components, plus a small steering column. Raw disconnected vertices must be welded before collapse reduction. The initial unwelded reduction produced fragmented surfaces and texture mapping and remains an inactive checkpoint. `prepare_assets.py` welds matching vertices, reduces geometry, creates replacement UVs and projects original base color onto four packed 2048px textures. The accepted seat design is retained. Detailed PBR maps remain in the raw sources; this reduction uses rebaked base color and preview material settings.

Fitting uses uniform component scale. Seats face forward, retain the calibrated left/right occupant registration and place cushion support at Z -0.035m. The wheel retains the original driver centre (-0.43, 0.36, 0.25m) and driver-facing axis. The fascia is fitted within the dashboard opening. These are authored fit dimensions, not measured factory specifications.

## Verification and limits

- Reopened saved output and confirmed finite Meshy vertices, UVs and packed images.
- Thirty static strict triangle-crossing checks compare five Meshy components against body, both doors, windshield and both side windows. No transverse crossings were found. Coplanar contact, animated panel sweeps and occupant pose clearance are outside this check.
- Visually inspected front-seat, side-cabin and driver-eye renders after the weld/rebake correction. `cabin-front.png`, `cabin-side.png`, `driver-eye.png` and `car-quarter.png` are local evidence. Cabin-only views hide exterior parts for inspection.
- Native game export, appearance, interaction, moving-panel sweep and save/reload remain pending. The current palette-only runtime adapter must not overwrite these textured UVs. A supported atlas/export path is required before staging this revision in the game.
- DOX pass: root owns this ignored build experiment and its documentation. Other child AGENTS and child indices remain unchanged because product files, tools ownership and domain boundaries did not change.

## Current front enclosure checkpoint

V03 in `integration/prototype-meshy-v03-closures/DSI_Javelin_Meshy_Cabin_Closures_V03.blend` carries the accepted v02 cockpit fit, separate downward black skirts and five front enclosure pieces. The source is checked and visible in Blender; no native export occurred. See `cabin-closure-restoration.md` for recovery, exact checks and missing headliner/Cardin door panels. V01 above remains the original integration/reduction record, not the latest working source.
