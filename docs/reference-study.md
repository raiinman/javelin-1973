# Reference and reconstruction contract

## Primary reference

[Bob La Cross, 1973 AMC AMX Javelin Pierre Cardin](https://www.youtube.com/watch?v=ZpfnHMBiRvA).

The original description identifies a 2009 restoration; publication is 2012-09-16. [Four research passes](research-1973.md) compare this individual car with contemporary AMC literature. Preserve its visible restored configuration while using factory sources to correct dimensions and defining trim.

Observed features used for this original reconstruction:

- Low, wide red body, long hood, curved front fender crowns and swelling rear quarters.
- A rounded fastback roof with broad rear sail panels, small rear quarter windows and a short rear deck.
- Black T-shaped hood graphic with a raised stamped centre section.
- Mesh grille, round outer headlights and two round inner rally lamps with red lenses.
- Chrome front and rear bumpers with black vertical overriders.
- Four individually framed rear lamps; the inner pair has pale reverse-light inserts while the outer pair remains red (approximately 0:22).
- Exposed chrome side exhausts with slotted heat shields (approximately 0:16).
- Side exhaust outlets terminate behind their heat shields. The reconstruction should not add unsupported rear exhaust stubs.
- Dark cabin and magenta, burgundy and cream Pierre Cardin upholstery ribbons (approximately 0:53).
- White ball manual shifter (approximately 0:47) and 360 V8 air-cleaner label (approximately 1:07).

Additional side-view geometry reference: [Mecum's 1973 AMX listing](https://www.mecum.com/lots/502692/). This is another car, used only to understand the body contour. Its paint graphics and equipment do not override the video car.

## Ownership

The geometry is authored in `tools/build_mod.py`. The deterministic atlas comes from the project's original `assets/palette.svg` colours. No old-mod mesh, UV layout, texture, rig or animation is included. The previously generated donor-atlas edit was rejected and is not part of this repository or package.

The source video and external photographs are viewing references. Their pixels are not packaged or published as mod assets. Local reference screenshots stay ignored.

## Fidelity gate

Review `assets/javelin-preview.png`, `assets/javelin-side.png`, `assets/javelin-front.png` and `assets/javelin-rear.png` after every geometry rebuild. The original reconstruction must show curved body sections and fender crowns, a rounded roof, broad painted rear sail panels, integrated hood stamping, individually framed rear lamps, side exhausts and the observed cabin details. The current candidate revises the beltline, quarter-light size and flared arch volumes. Its complete silhouette and surface transitions still require reference approval. The hood graphic continues across both fixed fenders, as documented in [the decal review](decal-reference.md). Studio views establish source-model proportions only; inspect the imported car at gameplay distance and with opening panels before treating it as finished.

## Reverse-engineering evidence

- REA opened the installed `projectzomboid.jar`, SHA-256 `e4661ca9cb168abc995d3cf59994fa17f66ba8a4e2c2899cbfa48f7eacea54b8`.
- Retained REA archive inspection: `ev_1376cef60c07636f48c5d320ceea2311b59195ba558d263e5709bfa584b2bc99`. It inventories the shipped archive; it does not establish importer behavior.
- Focused REA inventory view: `ev_5a74972772b39ea7de4aa7f9abb7b45cba4de3491b16d7a904e25b4848d4e3d8`, including `ModelLoader.class` and `VehicleScript.class` identities.
- REA's Java decompiler is unavailable because its JEB MCP endpoint is not connected. Native Windows PTY process capture is also unsupported by this installed REA adapter. No configuration or software installation was performed.
- `tools/InspectFbx.java` invokes the game's own Assimp importer and mesh resolver. It exposed split-material mesh lookup failures, an incorrect up-axis and an incorrect animation clip name in the first export. These are direct native importer observations, independent of the REA archive inventory.
- The export contract is one material slot per object, atlas UV colours, named actions and the temporary native-coordinate bake documented in `docs/import-contract.md`. Exported mesh nodes have identity transforms and model scale remains `0.01`. In-game testing was required to detect displaced skeletal panels, shader UV-layout mismatch and inward-facing open surfaces that static import and two-sided studio views missed.
