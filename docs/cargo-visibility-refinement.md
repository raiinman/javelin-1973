# Cargo visibility refinement, cycle 5

All sections remain open. This isolated trial changes only inferred cargo lining, not exterior proportions, paint, wheels, rigging or other sections. No likeness percentage is claimed.

## Four fresh comparisons

1. Target video comparison: re-examined `reference-30.png`, `reference-67.png` and `reference-78.png` against the latest combined clay and prior open-trunk source render. The supplied target frames show exterior/engine construction, including continuous painted compartment-side surfaces, but no usable open cargo view. They support retaining the red exterior and hidden-tire compartment principle; they do not establish the target's cargo lining, spare, ribs or wheelhouse dimensions.
2. Supplied Druk cargo photograph comparison: re-examined `build/web-pass-three/druk152912.jpg` at full resolution against the open-trunk source. The photograph shows a continuous dark enclosed luggage cavity, broad raised side wheelhouse regions, a floor mat, exposed upper structural recesses and hinges, and a spare on the right. No road tire is visible through the cavity. The current narrow box liners omit the outer shoulder closure. This is a different restored car, so only the enclosure principle is transferred. The spare and mat are not copied into the target.
3. Supplied Druk exterior and cabin comparison: re-examined `druk-contact.png` and `druk-more.png`, including rear quarters, profile, rear bench and open cargo thumbnail, against `build/parity-cycle4/combined/body/rear-quarter-clay.png`. Rear tire volumes lie beneath the rounded rear quarters beside the rear bench/cargo region. The source exterior crown should stay unchanged; widening tires or exterior skins would not repair the missing interior return. Photos do not calibrate the hidden inner panel thickness or exact wheelhouse radius.
4. Supplemental/source countercomparison: re-examined `build/six-pass1/batfull-sheet-060.jpg` and the fresh BaT listing text, then the same current clay and prior source open-trunk image. BaT engine photos show formed enclosure panels but this reviewed sheet supplies no open cargo geometry; listing replacement quarter/floor work further limits factory authority. In the source open-trunk image the far wheel arch outlines a hole beyond the x=0.60 liner. The proposed original dark curved upper returns therefore repair a known source visibility defect, while hidden form remains inferred. Fresh live Druk/forum/YouTube text retrieval failed; local previously downloaded photographs were available and visually examined. This is four targeted comparisons, not a claim of four whole-site reviews.

Sources: [target](https://www.youtube.com/watch?v=ZpfnHMBiRvA), [Druk gallery](https://www.drukautosales.com/vehicles/880/1973-amc-amk-javelin-pierre-cardin), [BaT listing](https://bringatrailer.com/listing/1973-amc-javelin-amx-2/).

## Isolated proposal

`build/cargo-visibility-cycle5/tools/javelin_cargo.py` supplies mirrored original dark crowned upper rear-wheelhouse returns. Their inboard lip overlaps the existing narrow cargo wall; the outboard edge follows the actual procedural side-skin envelope with 4 mm inset. Two connected closed 8 mm shells retains upward and downward visible faces. Crown height and thickness are inferred for clearance, not recovered factory dimensions. The proposal is called only by the copied `build_mod.py`. Trial build outputs remain under that folder. Production source, assets and package are untouched.

## Verification

- Trial source SHA-256: `b1d31f181b5c8458dd1b11acf10dd0f5da40efdb62aef1b10612fcac05175f0c`. The two connected shells add 1,056 triangles (188,892 total). Exact coordinate/topology digests for all ten non-Interior meshes match the canonical 187,836 checkpoint.
- `visibility.json`: 163,128 actual saved-mesh rays from 28 points inside the trunk opening to native-position upper/rear wheel triangle centres. Baseline exposes 48,931 rays; trial exposes 0. Both baseline and final trial have 0 backward-facing first hits. A superseded per-cell sheet trial blocked the rays but produced backward first hits; the final connected shells fix that culling defect.
- `cargo_visibility_guard.py` is a proposed callable-only guard, `check_cargo_visibility(vehicle_script)`, with no blend paths, writes or scene mutations. It parses both native rear wheel offsets and samples the fixed Body/Interior only, deliberately excluding the lid so a closed lid cannot hide a missing liner. `guard-counterfactual.json` proves it rejects canonical 187,836 (48,957 unblocked rays, zero backward first hits) and passes the exact trial save. Its baseline count is 26 larger than the open-lid test because it excludes the lid. Camera coverage remains finite and native rendering remains separate.
- `shell-check.json`: 528 new faces/1,056 triangles, zero new-shell/fixed-Body surface intersections, nearest rear-wheel vertex gap 66.38 mm. This vertex gap is supplemental; complete existing triangle-intersection wheel checks also pass.
- `pose.log`: complete saved-model gate passes, including four-wheel rest and front +/-0.30 rad steering, all original cabin/seat/lamp/cup checks, and ten intermediate panel fractions. No wheel positions or tolerances were relaxed.
- Inspected `open-left.png`, `open-right.png` and `cargo-top.png`: dark cargo is enclosed, no road tire is visible, original central cargo volume remains. The fresh `before-*` renders preserve identical camera settings for root comparison.
- Native inspection remains a separate root-agent gate. One isolated rebuild crashed with an access violation before saving; a fresh retry completed successfully, and all final checks read the subsequently saved exact hash above. No stale result from the failed attempt is used.

## DOX pass

Root owns this research record. Owning AGENTS.md files intentionally unchanged: no production contract or durable ownership change is introduced by the isolated unpromoted trial.

## Root promotion

Root reviewed both open-cargo close-ups and promoted the module/call to canonical source. The resulting saved source is188,828triangles (net992 added after generation/welding), SHA-256 `e0a754a30ba42a3ad7e8ef4db72769fa9e09a6cc16cf7cb92a1c82fc44d56235`. Canonical unit/static/native import/full pose gates pass, including163,128 fixed-lining rays with the moving lid excluded. The source trial used1,056 raw shell triangles; raw and net counts are distinct. Fresh canonical captures are under ignored `build/parity-cycle5/cargo/`. Native confirmation remains pending. Tools/assets AGENTS now own the closure and regression contract; package interfaces remain unchanged.

## Native result, unresolved

Toolkit-launched188,828source was observed in a no-save world with hood, trunk and both doors open. A rear tire remains visible through cargo, while the cabin is black. This contradicts the source-only visibility result and is not a pass. Source Interior geometry is present and imports, but its actual native part/model activation is under investigation. Do not add more hidden panels merely to compensate for a potentially absent submodel. Temporary diagnostic hooks were removed after normal exit; cleanup manifest is under `build/parity-cycle5/`.

## Fresh-spawn activation confirmed

Fresh Toolkit no-save spawn confirms the original init callback activates itemless J73Interior, with13 active model entries and a non-null J73_Interior model instance at10/20seconds. The open door visibly reveals Cardin cushion ribbons and dashboard trim; the cargo opening no longer exposes the rear tire from the inspected high rear-quarter angle. This resolves that fresh-spawn activation/visibility defect, not whole-cabin likeness or every viewing angle. Real saved-vehicle reload and multiplayer remain untested. The game exited normally, both hash-matching temporary audit hooks were removed, and the separate inspection latest-save pointer was restored. The permanent original shared callback remains in the mod. Evidence: ignored `build/parity-cycle5/interior-native-audit/audit-markers.txt` and completed `build/parity-cycle5/interior-temporary-hooks.json`.
