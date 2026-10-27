Development probe, not a finished gameplay camera.
Enable in a disposable debug single-player world. Right-click the world and choose Camera research: nearby map probe.
Left-drag to rotate and tilt. Right-drag to pan. Wheel to zoom. Refresh samples the nearby loaded floor and collision edges again.
The colored geometry is a bounded snapshot of map collision flags. It does not show complete buildings, furniture, characters, vehicles or textures, and does not change gameplay.
No external renderer, Java addon or installer is used by this probe.
The separate Camera research: audit actual world access action reports live camera API access, nearby object model coverage and the actual world render callback to the game console. It does not modify camera state or enable debug reflection.
Camera research: textured ground uses actual nearby floor sprite textures with an original projection. Left-drag changes yaw and tilt; right-drag pans; the wheel zooms. Presets expose 90-degree turns and 5/85-degree tilt. A click reports ground coordinates only, without issuing gameplay actions.
This floor-only bounded snapshot does not render buildings or characters. The cyan marker tracks the actual player position. Floor sprite shifts assume zero; unusual shifted or layered textures need further handling.
