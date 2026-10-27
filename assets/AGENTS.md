# Original art

## Purpose
Preserved procedural art/model sources and historical preview renders built from the user's video. Current reviewed cloud authoring is indexed in `../current-work/README.md`; old model filenames and previews here do not override that authority. Real-car reference findings remain relevant within their stated limits.
- `palette.svg` defines the original deterministic swatch atlas used by each mesh's face UVs.
- `front-artwork.svg` is the original editable physical-plan drawing for the complete hood/fender T and companion line. The generator consumes these paths directly; the previous graphic was discarded at the user's request.
- `model-manifest.json` records original per-part geometry and authored dimensions.
- `atlas-manifest.json` records semantic UV slots for native damage, rust, removable glass and independent headlights, tail lamps and brake lamps.
- `javelin-preview.png`, `javelin-side.png`, `javelin-front.png` and `javelin-rear.png` are reproducible studio views for silhouette, fender and trim review.
- `javelin-perspective.png` is a low front perspective inspection view for the video comparison, using an estimated camera rather than a measured lens solution.

## Ownership
Blender source, procedural palette definition and car previews.
- `engine-amc360-v28-cleanup/` holds the cleaned Astra V28 engine and its before/after evidence.
- `engine-amc360/` holds the separate original AMC 360-style exterior engine, its renders, verification and bay-fit diagnostic; it is not part of the car or mod package.
- `current-stl/` preserves the older complete STL-based assembly as a historical portable editable snapshot, separate from the earlier procedural production source. It is superseded by the cloud artifact indexed in `../current-work/`; preserve its exact binary/source identity and follow its child contract.

## Local Contracts
Create original geometry and textures. Keep reference screenshots in ignored local files. Preserve the red body, black T hood stripe, four rear lamps with reverse inserts on the inner pair only, chrome side exhausts, chrome trim and Cardin upholstery.
- Retain the current chrome window trim as the user's deliberate visual preference for now, even where the target video appears red. Keep trim treatment separate from the shape and fit of the painted structural A-pillars.
- Side exhausts on both sides follow the user's purple-car reference, with curved single inlets, perforated chrome guards, hollow rear outlets and a close rocker fit. No separate painted runner above the pipes. The spacing-reference video's two-into-one header arrangement is not the requested pipe design.
- Both door mirrors use round domed chrome pods with rearward-facing recessed reflective glass and short swept pedestals. Inspect their front shells and rear reflective faces separately on both sides; dimensions and fine curvature remain inferred from the video.
- Use supplemental car photographs to resolve mirror construction and mounting, while retaining the video car's round chrome identity. Distinguish painted sport pods and differently shaped chrome replacements rather than combining their outlines into the target.

## Work Guidance
- Historical procedural refinement scope was front fenders only: broad width, crown distribution/height and hood-to-fender graphic span. The checked terminal-roll checkpoint is an intermediate improvement, not a finished fender. Keep the user's open Blender on the latest checked source while preserving their saves.
- The front ceiling carries two static stowed padded visors with seated mounts and a short-stalk interior mirror facing into the cabin. Preserve Cardin roof ribbons and the dome. Exact target dimensions/pose and mirror optical alignment remain open; review driver-eye, ceiling and open-door captures before native inspection.
- The manual cabin has distinct compact clutch/brake pads, tall narrow accelerator and small separate far-left parking-brake control, with physical suspended arms and upper supports. Do not substitute the supplemental automatic car's wide brake. Exact dimensions, pivots and tread pattern remain inferred; inspect seated/open-door views before native review.
- Rear fascia/lower sheet corners share a continuous curved boundary, closing actual holes beside the outer lamps. Both moving door cards carry original Cardin spiral/caption appliques seated on their inlays, readable from the cabin on each side. These changes do not establish overall likeness or close a section.
Target the supplied car's 1:1 visual identity before reducing detail for game scale. Generic muscle-car proportions or passing geometry checks do not establish likeness.
- Review flared wheel-arch volumes, waist-to-fender width change and rounded transverse crown sections in front/rear quarters. Uniform-width vertical fender panels are insufficient.
- Current fender/roof refinement evidence and unresolved likeness limits are tracked in `../docs/fender-roof-refinement.md` and `../.img2blender/reviews.jsonl`. All sections remain open. Review each iteration before advancing; recheck the rear haunch with the sail because they share one continuous surface.
- Follow the four fresh comparisons and ordered section gates in `../docs/likeness-four-pass.md`. Front crowns, smooth fastback stations, body-side fullness, thin recessed tail trim and sculpted seat padding require separate source renders before moving on.
- The hood T and its fine contour continue onto both fixed fenders. Edit the new `front-artwork.svg`, then regenerate through `javelin_front_artwork.py`; do not revive rejected old contour functions. See `../docs/decal-reference.md` and `../docs/front-decal-rebuild-cycle14.md` for evidence and current checks.
- Review the complete hood T, curved stem joins, crossbar and both fender returns as one graphic. The supplied video's appearance controls the redraw; supplemental photographs clarify construction. Keep the newly observed front Javelin script separate from unverified side badges, and preserve the user's latest saved model before replacing source.
- Keep the fixed apron and moving trunk as thin closed sheet metal. The rear return, AMC/AMX lettering and deck spoiler belong to the opening trunk; inspect their entire sweep. Blender's double-sided preview must not conceal inward top faces.
- The latch cup has a pressed backing following its depressed surface, not a flat underside fold crossing the bowl. Inspect both rear visibility and inner backing thickness. The current modestly lowered crest and proportionally smaller oval cup remain inferred and open to reference correction.
- Preserve the shallow lid crown, raised rounded-end spoiler, rolled crest and vertically oval pressed latch cup from the user's supplemental rear galleries. The ramp ends must be closed, with clearance over the fixed fascia. Rear badges follow the bowed moving face. See `../docs/trunk-spoiler-refinement.md` for captures and remaining limits. The rear bumper wraps forward at its ends and has a lower central plate notch. The video car's red tail panel remains authoritative over the supplemental black-panel car.
- Closed door skins keep 6mm perimeter clearance to the body opening. Main glass, A/B-pillar trim and quarter glass use shared roof/beltline anchors; preserve their continuous chrome line when changing the cabin silhouette.
- Back door clearances with recessed fixed jambs. Join the quarter-window tip to the same subdivided sail boundary, and close the fixed tail between the trunk and fascia before seating the spoiler lip.
- The backlight has rounded upper/lower corners and mildly bowed side edges, with shared painted support and chrome following the same perimeter. Hidden support and radii remain inferred; inspect both rear quarters and do not treat a rounded outline as whole-roof likeness approval.
- Quarter-glass aft outline retains an upper run, a more direct descending edge and a localized lower round corner. Generate glass, chrome and painted support from the same controls; retain shared divider/tip anchors when refining inferred intermediate heights. Avoid returning to an oval cap or an unsupported triangular insert.
- Sail, surround and aft quarter glass follow one continuous roof-to-flank surface, with side-skin tangency and a broader rounded aperture. Preserve actual top/bottom/frame joins when refining inferred stations. The backlight-to-deck apron follows every lower glass point, including its centre crown, as one closed crowned grid without a duplicate flat sheet.
- Keep one painted owner at the aft sail/wing transition and shared apron/sail/deck/tail borders. The rear construction repair preserves the moving trunk and roof silhouette; the broader longitudinal shelf and diagonal apron reflection remain separate likeness findings.
- Keep the dashboard behind and below the windshield foot; exterior cowl and wiper trim remain separate from interior geometry.
- Keep the hood as a closed contoured sheet with matching underside and perimeter faces. Fixed nose trim must meet its closed front edge.
- Outer headlamps seat in real fascia apertures with connected pocket walls and rolled bezels. Inspect recess depth against the actual surround; a lamp placed over a solid fascia face does not establish this construction.
- Engine and cargo cavities use original dark side liners and bulkheads to hide wheels and road while preserving visible engine detail and empty cargo space. Closed crowned upper rear-wheelhouse returns bridge the outboard shoulder gap without changing the exterior. Their dimensions are inferred; inspect both sides of the open cargo cavity with backface culling.
- Door windows lower 0.45 metres to clear the beltline completely, including when their parent doors are open.
- Mechanical hinges sit at the moving panel's physical front edge; inspect intermediate motion against fixed bodywork and the spoiler, not just endpoints.
- Floors and compartment liners must clear the entire wheel assembly at rest and the front steering sweep. Studio wheel placement matches native offsets at lateral 0.77 metres.
- Shared rear stations target a 4.88442-metre Body length and 2.794-metre factory wheelbase, within the existing 10mm regression tolerance. Cabin and sail proportions require reference comparison independently of overall dimensions.
- Two front Cardin buckets use continuous nested U backrest ribbons and lengthwise cushion bands. The rear has one full-width bench with continuous back/cushion loops, preserving both native occupants. Keep the video cream, magenta and burgundy palette; upholstery faces point into the cabin and headliner faces downward.
- Seat cushions use thinner upholstered pans, front falloff, compression channels and seated welts; preserve native support heights. Raised backrest shoulders may roll ribbon normals away from a nearly planarY axis, so test facing against the actual padding while retaining cabinward orientation and physical support.
- Open interior sheets carry explicit facing directions through generation, applied after general normal recalculation: seatback ribbons face source +Y and headliner base/ribbons face source -Z.
- Headliner ribbons are clipped to the same planar grid cells as their base, with a 1mm cabin-side gap; an analytic roof offset alone can hide rounded corners behind the coarser base.
- Preserve the original procedural PC fender crests and restrained silver/dark AMX instrument surround with three driver dials, the metal three-spoke wheel and white manual-shift ball.
- Dashboard major padding includes a rounded driver brow and tall central vent cheek stepping into a recessed broad passenger face with sloped top and bowed physical handle. The driver/passenger upper junction, lower stack, small hardware and surface grain remain approximate and open.
- The driver fascia has real rounded-square gauge openings, a separate padded hood and control ledge; the passenger side has glovebox and end vent. Wheel spokes are flat and slotted, with a padded horn boss. Door cards have pleated pulls, separate cranks and releases; inspect them against the fixed dash during opening. Exact dial identity, upholstery drape and missing small hardware remain open in `../docs/parity-target.md`.

## Verification
Inspect the generated source model and render at gameplay distance.
- Historical procedural build uses `tools/build_mod.py`, not the current cloud model; it recreates `Javelin73PC.blend`, the preview, model/animation FBX, palette PNG and model definitions.

## Child DOX Index
- `current-stl/AGENTS.md`: preserved historical STL source snapshot, checksum and visibility checks; current cloud authority remains indexed outside assets.
- `engine-amc360/AGENTS.md`: original procedural AMC 360-style exterior engine, verification records and the V10 empty-bay fit diagnostic.
- `engine-amc360-v28-cleanup/AGENTS.md`: cleanup of the user-supplied Astra V28 engine (shading, fan blades, exhaust manifolds) with before/after evidence; transforms and parts unchanged.
