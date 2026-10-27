# Supplied-car graphics and emblems

Original vector artwork in `assets/front-artwork.svg`, consumed by
`tools/javelin_front_artwork.py`, reconstructs the complete front T and fine
contour. `tools/javelin_decals.py` dispatches this and the other visible trim
from the [supplied Bob La Cross video](https://www.youtube.com/watch?v=ZpfnHMBiRvA).
The ignored local reference frames are viewing evidence, never packaged pixels.

| Detail | Visible evidence | Reconstruction boundary |
| --- | --- | --- |
| Full-width black front T | 0:02 and 0:30 | Broad front crossbar continues from the opening hood across both fixed fender noses above the outer headlights, with a narrow longitudinal stem, curved merging corners and a thin secondary contour behind the crossbar. Dimensions are judged from perspective views, not claimed as measured factory artwork. |
| Pierre Cardin fender emblem | 0:16 | Open metallic stacked P/C monogram ahead of the door. Red paint shows through its loops; there is no solid black square behind it. Original stroke paths approximate the cast emblem. |
| Rear AMC and AMX | 0:22 and 0:26 | Small AMC at the left rear lid return, larger metallic slab-serif AMX at the right. The geometry belongs to the moving trunk, with seating coordinates supplied by the body generator. |
| Tire lettering | 0:16 | BFGoodrich is legible. The partial lower/remaining tire text is consistent with Radial T/A, but less completely visible in the saved frame. Uppercase original vector lettering is a legibility approximation, not exact proprietary logotype parity or proof of tire dimensions. |
| Air-cleaner label | 1:07 | Large 360 with red and blue rules on a metallic label. Does not establish engine internals. Tiny secondary copy is omitted because it is not reliably legible at the model scale. |

The original video at0:05 clearly shows a raised chrome cursive Javelin script
on the front black hood band. Fresh0:02 context places it inboard of the
driver-side hood/fender seam. This supersedes the earlier missing-evidence
decision; an original stroke reconstruction is included with the full
graphic redraw in `front-decal-rebuild-cycle14.md`. Badge dimensions remain
inferred. No exterior360 side badge is added without evidence on this car.
The separate comparison auction car's graphics do not override the supplied
video's red paint and black hood treatment. The front
AMX insert and AMO club medallions are owned by `tools/javelin_front.py`.

## Supplied in-game AMC comparison

The user's blue/white/red AMC screenshot is additional visual evidence, not an asset donor. Its white graphic reads as a shallow front crossbar with a narrow longitudinal stem, relatively short outer returns and tighter inside transitions. The current I5/Meshy black graphic reads heavier in the saved quarter/top renders, particularly its long outer tapers and rounded inside corners. Perspective, lighting, body shape and white-versus-black contrast prevent a calibrated dimension comparison. This comparison does not establish factory artwork dimensions or authorize copying the other mod. The original video remains the target. No further decal geometry is changed in the separate downward-skirt correction.

## Current STL decal reset

The saved I5 review candidate uses `build/stl-full-trace/slice-v03/integration/prototype-i-front/pixel-trace/`: cyan trace overlays document the original video and Druk photographs. A fixed-STL camera fit exposes remaining correspondence uncertainty, rather than warping the drawing. The final symmetric plan keeps the observed straighter bar and restrained stem; upper corner/cowl registration is explicit inference. Runtime inputs are `apply_front.py`, `front-artwork.svg` and `prototype_i_front_helpers.py`, frozen together. The production `assets/front-artwork.svg` remains unchanged. See `full-stl-trace.md` for source/package hashes and review limits.

The user explicitly confirmed a fresh decal rebuild, preserving the car model. Start with clean Hood and fender surfaces and draw from video/reference landmarks directly in the actual supported top field. I4 is also rejected for its helmet-like arched bar and deep points, despite technical coverage checks. Trace the actual photo/video contour and inspect a source overlay before another 3D fit. The original drawing was closer than the rejected rounded replacement; use it as comparison evidence, not as a shape to distort through another global mapping. Check the complete main band, outer tapered ends and fine border, including the highlighted outer corners. Preserve the I3, redraw and original-fit trials as inactive diagnostics.

## Historical clean restart

The user rejected further adjustment of the previous contour. Remove the old
hood/fender artwork before drawing its replacement. The saved bare checkpoint
is `build/front-decal-cycle14/new-drawing/bare/assets/Javelin73PC.blend`.
Its three actual captures show the exposed red hood and both fenders. The
preservation check retains all nine other mesh geometries and UVs exactly;
nonblack Hood face coordinates are exact and Body face coordinate drift is
at most0.000000238419m from vertex welding. This is a source/render checkpoint,
not a native-game visual approval.

The promoted replacement is a new physical-plan SVG consumed by a
separate module, without the rejected hood/fender contour builders. The checked
graphic baseline is243156triangles, SHAa617d127; current fender form is tracked in `front-fender-form-cycle15.md`. Both wing returns and the separate raised
Javelin script are present. The82-input frozen checkpoint passes42 tests,
static validation, five native parsers,11mesh/3clip import, full pose and saved
graphic support/visibility checks. Native-game visual inspection is pending. See
`front-decal-rebuild-cycle14.md` for the four full reference comparisons and
current implementation evidence. Preserve the bare checkpoint for comparison.

## Historical integration and verification

- Paint the base hood red and explicitly split each original hood grid cell into
  triangles `(0,1,2)` and `(0,2,3)`. `build_hood_graphic` clips its vector polygons
  to those exact triangles and seats them 0.8 mm above the actual planes.
- Remove the old black hood-cell condition and old black-square PC crests before
  calling `build_decals` once, after base parts are generated and before objects
  are created. Do not retain duplicate emblems or overlapping generic hood bars.
- `build_decals` accepts the existing palette-aware body, hood, trunk and wheel
  Parts plus `hood_point`, the hood X/Y grids, `side_x` and `tail_face`. Rear lid
  badge surface height/depth can be passed explicitly when the rear changes.
- Supply `fender_point(side,y,t)`, `fender_y` and optional `fender_t` to continue
  the graphic on both fixed fenders. The outer-to-inner parameter runs 0 to 1;
  base crown quads must use `[point(a,t1),point(b,t1),point(b,t2),point(a,t2)]`
  with explicit triangle splits `(0,1,2)` and `(0,2,3)`. Each vector polygon is
  clipped in parameter space and seated 0.8 mm vertically above its actual
  triangle. The shared vertical offset preserves coincident boundary vertices
  between neighbouring graphic triangles.
- Hood and fender broad-band edges share longitudinal station 2.185 m at the
  seam; their fine contours share 2.160 m. The black fender graphic ends at
  2.385 m to preserve the same red forward rim as the fixed nose return.
- Vector faces carry explicit exterior normals. Graphics remain assigned to the
  same moving panel or wheel and shared material atlas as their supporting part.
- Inspect hood top/front quarters, both PC crests, rear lid closed/open and both
  wheel outside faces after generation. Native rendering remains a separate gate.
- The authored vector geometry is a concrete improvement against these frames;
  it is not a certification of 1:1 visual parity.

## Historical three additional front-graphic passes

1. **Reference recheck:** the original hood-only revision missed the black
   crossbar continuing onto both fixed front fender noses. The seam lies inside
   the graphic; it must not become the paint boundary. Frames 0:02 and 0:30 show
   the outer corner curving aft, rather than a simple transverse rectangular
   patch. The close-up at 0:08 establishes club-badge details, not hood geometry.
2. **Geometry correction:** the hood outer black boundary now meets its seam at
   2.185 m, avoiding the old triangular red wedge. Its thin contour reaches the
   seam at 2.160 m and continues over both fenders. The incorrect hood-only
   outer longitudinal outline was removed. Both fixed fender graphics use exact
   base-triangle projection, mirrored placement and the red forward-rim limit.
3. **Verification:** a recorder using the current generator's actual front
   fender sampling functions checks 86 added fender faces (384 triangles).
   Every graphic face is 0.800 mm vertically above one supporting source
   triangle, remains inside it, and has the exact mirrored counterpart with matching exterior
   normal. Both broad and fine seam stations agree, and the red forward rim is
   retained. Integrated backface-culling renders show the graphic continuing
   over both hood/fender seams, with matching left/right placement and readable
   PC/rear lettering. Close-ups exposed small PC stroke-joint gaps and an
   engine-block-obscured 360 label. The cast-metal paths now have filled rounded
   joins, and the label follows the raised air-cleaner centre at 0.798 m.
   Refreshed renders confirm continuous PC metal and a fully visible 360 label.
   Further front close-ups exposed fine red seams between graphic triangles:
   independently offsetting triangles along different normals separated their
   shared edges. The final projection uses a shared vertical 0.8 mm offset,
   preserving identical edge vertices while retaining exact base-plane fitting.
   Final refreshed top, left and right culling views confirm those fine red
   triangle cracks are gone, the hood crossbar continues onto both fixed
   fenders, and the front red rim remains visible. Both PC close-ups retain
   continuous metal joins, and the raised air-cleaner label is fully visible.
   The final broader `hood_base` sampler also passes the finite, mirrored,
   upward-facing and shared-edge recorder checks. All three additional decal
   passes are complete at source/render level. Supporting nose/fender shape is
   tracked separately by the generator owner. These source checks do not certify native in-game
   appearance or exact factory artwork dimensions.
