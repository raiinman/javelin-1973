# Side-pipe correction

The user identified both side assemblies and rejected the detached red runner above them. Assembly-style authority is the [purple1973 AMX, CC-1616004](https://classiccars.com/listings/view/1616004/1973-amc-amx-for-sale-in-hopedale-massachusetts-01747). The supplied [video around7:50](https://www.youtube.com/watch?v=qOiQftO8yWo&t=470s) supplies rocker-to-pipe spacing context only; its two-into-one header arrangement is expressly excluded.

Inspected the timestamped video in browser playback and purple-car photographs32921092 and32921093. The visible pipe has a curved inlet behind the front wheel, a long chrome slotted shield close beneath the rocker, and a rear outlet ahead of the rear wheel. Perspective photographs do not establish exact fabrication dimensions.

`tools/javelin_sidepipes.py` generates both assemblies from one mirrored definition. The obsolete red rail was removed from `build_mod.py`. Compared with the prior source, the main centre moves from0.895m to0.835m laterally and from0.170m to0.217m vertically:60mm inward and47mm upward. The guard radius is55mm, and it has29 actual elongated openings. Original swept tube walls form a hollow34mm-radius outlet with a curved outward rear turn. These dimensions are authored fit choices, not recovered factory specifications.

The rebuild preserves the other car sections and gameplay scripts. Source, original modules and baseline views are preserved in ignored `build/sidepipe-before.zip`. Both updated close-ups and saved-mesh mirror evidence are under ignored `build/sidepipe-review/`. Blender source, model exports and reproducible generator remain consistent. Native game appearance remains a separate check.

DOX: tools and artwork contracts now own the side-pipe style and spacing constraints. Gameplay child instructions remain unchanged because no runtime behavior changed.

Verification:96,547-triangle source;31 unit tests; static validator0errors; native importer11nodes and3clips; full saved-model pose, steering and ten-fraction panel clearances pass. Both culling-enabled close-ups were inspected, and the saved-mesh mirror probe matches2,581 selected vertices per side. The clean live-view Blender session reports this source current.

## Active STL prototype correction

The G inlet-deformation experiment is rejected. The preserved H2 prototype starts from F2 and shortens the pipes by cutting192mm from their straight centres, welding matching bands and translating the rear halves. It preserves original rear outlet shapes and trims only a small front terminal section, without whole-pipe scaling or a new inlet curve. The long axes are already level; the recorded rigid rotation is0degrees. H2 used separate black fixed rocker extensions; the subsequent painted I5 outward shelf is now rejected. Original body and door geometry remain exact. New extension winding is corrected in H2. See `full-stl-trace.md` for the source, hashes and export evidence. The existing low inlet dip and exact native appearance remain open. Original production generators and their historical verification above are unchanged.

DOX pass: root records the clarified centre-cut/rotation/terminal-only policy. No child index or production child contract changes are required because this remains an isolated STL prototype and does not change the original tools or installed product.

## Separate downward black skirts

The latest user correction supersedes the painted sill-continuation experiment: two separate editable black panels must drop downward under the stock sill rather than project outward as running boards. The isolated `integration/prototype-meshy-v02-skirts/` candidate removes only the 724 positively marked I5 skirt faces. It retains surviving body coordinates, UVs and material assignments, both doors, all 7,814 pipe faces and the textured Meshy cabin. The new panels have a maximum authored drop of 69mm and outward offset of 12mm, tapering at their ends. Those dimensions are fit choices, not measured fabrication specifications.

Both side closeups are reviewed. Static closed-manifold/positive-volume checks and pipe/closed-door overlap checks pass; sampled pipe clearance and UV/image preservation are recorded in `verification.json`. Animated clearances and native game appearance remain unverified. This is a separate review checkpoint, not a native package update. The other chat continues cockpit corrections in `prototype-meshy-v02/`; keep this skirt patch isolated and merge against a preserved latest cabin before replacing its live window. Reusable `apply_skirts.py` carries only the skirt correction.

DOX pass: root preference now explicitly specifies separate downward black pieces. Production tools, installed package and their child contracts remain unchanged. No new domain boundary or Child DOX Index change is required.

The frozen cockpit input SHA256 is `d9d921f34fad40f453dfe997130d4f93b2efe2ce6bf89fe5995b51b279245020`; final skirt checkpoint SHA256 is `a9dd44edbf1d28640f91c224739b85ced423c2e2680b973cf40dca06a1b897f9`. Fresh-process reopen checks pass for retained mesh signatures, packed texture bytes, surviving body-face count, finite skirt vertices and closed outward skirt volume. Both closed-door overlap checks are zero. These checks do not certify animated or native-game clearance.

Live display: the released Meshy v02 session was saved to `prototype-meshy-v02-skirts/live-before-skirts-20261019T164312707742Z.blend` and its bounded geometry/material/action comparison matched the frozen source. The checked skirt checkpoint was displayed in the existing Blender window and is retained by V03 cabin closures. `integration/live-state.json` records this display; later interior closure work must carry it forward.
