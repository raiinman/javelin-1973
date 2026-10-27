# Camera implementation order

1. Verify supported APIs and native rendering order before advertising controls.
2. Deliver native zoom presets, a compact movable toolbar and native PanCamera binding guidance.
3. Test actual gameplay, input, picking and lifecycle through Toolkit's isolated profile.
4. Correct runtime findings and package only working controls.
5. Complete remaining native gates and Workshop uploader validation before publication.

The 0.1.0 raw-offset adapter failed native pan: render-time recenter overwrites it. Its controller tests are research only. Full 3D remains separate research. Preserve normal profiles and other agents' work.
