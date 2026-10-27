# Current body-only work

Snapshot: **2026-10-27 18:48 UTC**. Current reviewed checkpoint: **BodyOnly V03**, SHA-256 `668ffbaed111e20833c963a519ce04373525dd7e873b5957ed8bea24aabbfa90`.

## Scope and exact change

The user clarified that Project Zomboid does not need the elaborate underneath additions. Current work is body geometry correction and proper slicing. Do not add more structure now.

V03 is a reversible visibility/export-exclusion successor, not a body-repair milestone. It hides/excludes all 69 newly authored underside meshes and four exhaust empties, restores the original `CabinMainFloor` and `TransmissionTunnel`, and preserves the original eight pipe/cover/ring pieces, rear structures, exterior, cockpit, rig and slicing. All optional work remains in history; no raw geometry or object was added/deleted by this change. The original 12-face history archive stays hidden.

![Actual body-only V03 rear-quarter authoring render](progress/body-only-v03-rear.png)

These exterior images are actual V03 authoring renders, not in-game screenshots or final likeness approval. No underbody render is used as current progress.

## Verification and next work

[Independent V03 receipt](receipts/body-only-v03-preservation.json): all **15 checks passed**. Exact mesh data, normals, UVs/attributes, material/image state, local transforms, hierarchy and actions are preserved. Still-active original motion is exact over seven actions × 51 half-frame samples; excluded objects were separately checked under equal original visibility context without saving that diagnostic state.

This proves preservation and the exact scope correction. It does not prove repaired body geometry, continuous clearance, visual likeness, native import or game behavior.

1. Review and correct the existing malformed body geometry, preserving the exterior and accepted cockpit. Body geometry repair is in progress, not adopted or pictured here.
2. Finish proper slicing with explicit ownership/seam/normal checks and moving-panel regression. Do not invent new aprons, towers, rails or mechanical systems.
3. Continue matched-view target-video/photo comparison. Existing real-car measurements and research remain relevant.
4. Reconcile any future exporter to the exact accepted body-only/repair checkpoint before claiming compatibility. Earlier V01 diagnostic exports do not validate V03. No current native-game gate has passed.
5. Investigate custom-mod/import support for the exact Wreckfest PC edition installed through the Xbox app/Microsoft Store. That support and the delivery route remain unverified; the later goal is not publication authority.

## Model and artifact index

| Artifact | Role |
| --- | --- |
| BodyOnly V03, exact SHA above | Current reviewed authoring/scope checkpoint; body repair pending |
| Prior V01/V02 floor/exhaust/rail milestones | Preserved history, not current structure authority |
| `assets/current-stl/Javelin73PC-current.blend` | Historical Git-stored STL assembly; filename does not make it current |
| `assets/Javelin73PC.blend`, `Javelin73PC/` | Earlier procedural model/package, preserved unchanged |

[Exact artifact manifest](artifact-manifest.json). V03 is preserved in the owner's private ChatGPT Library as `DSI_Javelin_Current_Cloud_Model.blend`, identity `libfile_dc7967b8d0088191ad558887bc71a3dd`, **version 2**, 27,862,912 bytes. The successful delivery receipt was inspected and its exact delivered bytes independently matched to the V03 SHA above. Its `.blend` is **not included in a GitHub clone**. Earlier Library versions remain history. Separate private image IDs in the manifest identify the exterior renders, not model binaries. No model/script/package binaries or source changes are part of this documentation-only proposal.
