# Rainy Knox County startup artwork

The user requested Project Zomboid themed animation, with no Dead Signal branding in the artwork. The original background was generated with the built-in image generation tool and saved in `DeadSignalFastLoad/42/media/textures/FastLoad_KnoxCounty.png`. Its dark left side reserves room for the game's existing logo and menu. It is original concept art, not official game art.

`startup-preview.html` offers an approximate browser preview of the weather overlays and original survival-tip library via startup-preview-tips.js. Its title text and manual navigation buttons are preview composition only; the game retains its actual native logo and controls. The preview was created but not opened or executed during development.

## Runtime contract

- Native UI draws the background with an aspect-preserving cover fit. The native logo, controls, terms and menu entry remain under game control.
- Slow ground fog, subdued moving light reflections and48 rain strokes animate over one cached texture. No video decoding, audio, added timer, fake progress or game-state transition belongs to the scene.
- Reduced motion freezes time and removes rain. The scene toggle restores the native backdrop. Scene rendering is confined to boot UI when permitted and the visible front menu, excluding submenus and gameplay.
- Workshop Lua cannot animate the pre-Lua warning/initialization frame. The former whitespace warning overrides are removed so that this earlier frame shows native warning text again. No claim of full startup coverage or faster engine loading is made.
- Draw errors disable the scene for the session after one log entry. Native artwork/menu remains behind it.

## Prompt, built-in image generation

Use case: stylized-concept. Asset type: original widescreen background painting for a Project Zomboid themed startup/main menu mod. Create a beautiful atmospheric hand-painted survival horror game background, abandoned rural Kentucky town in 1993 after a zombie outbreak, nightfall after rain, boarded brick storefronts and a decaying gas station on the RIGHT two thirds, an abandoned period sedan, tangled utility poles, wet cracked road receding toward a dim amber streetlamp, low ground fog, small distant silhouettes of infected people, desolate, quietly terrifying. Restrained painterly realism with subtle illustrated texture, rich charcoal and desaturated blue-green shadows, sparse amber windows, excellent environmental storytelling and architectural detail. Composition: very wide 16:9 landscape. LEFT 40 percent extremely dark with almost no detail, smooth shadow, reserved for a game logo and vertical menu, most detailed composition right of center; lower street visible for rain reflections. No UI, no buttons, NO TEXT, NO LOGOS, no watermarks, no developer branding. No graphic gore. No bright lightning or flashing effects. Paint fog and wet atmosphere but do not add foreground rain streaks, these are animated separately. The artwork itself is original, not a copy of official title art. Crisp high-quality finished game art.

## Evidence and limits

Shipped `OptionScreens/MainScreen.lua` renders its logo in `prerender`, with child controls afterward. The scene wraps that method and draws before calling the original. Shipped terms UI uses native UIManager and requests render events; the boot panel is put behind it and consumes no mouse events. REA reconfirmed installed archive identity `80e405a4bfc42f6072e75b3735f458a6514143da011d3226007ded305a442f44`. Read-only GameLoadingState bytecode shows its normal loading path draws native status directly rather than regular UIManager rendering; no custom world-loading overlay is claimed.

Context7 API lookup corroborated ISPanel/drawing methods. Installed source establishes the actual integration order. No tests, syntax compilation, game launch, native animation observation, accessibility check or performance measurements were performed. Boot visibility, crop/layout at different aspect ratios, reset lifecycle and mod conflicts remain unverified.
