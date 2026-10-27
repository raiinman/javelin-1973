# Survival tips: three research passes

Reviewed2026-10-18 for installed42.20.4. These are three sequential reviews before final tip selection, not three labels applied to one search. No game, tests or syntax compiler was run. Tips are original short summaries and strategy suggestions, not quotations or endorsements. Sources and personal names stay outside the distributed package.

## Pass1: experienced-player discovery and candidate review

Read the available text of these community sources, including conflicting comments rather than accepting titles as authority:

- [MR. FOODE's Build42.20 guide](https://steamcommunity.com/sharedfiles/filedetails/?id=3722551327): useful first-day priorities, combat retreat, vehicle checks and crafting workflow. Page presents removed/incompatible banners despite readable guide content; corroboration required. No reliance on its promotion, trait costs or fixed group-size rules.
- [Gabes' Basic Book of Survival](https://steamcommunity.com/sharedfiles/filedetails/?id=635586966): short fights, quiet movement, fallback shelters and strain management. Occupation/trait tables and numerical claims are excluded.
- [A returning1000-hour player's B42 report](https://www.reddit.com/r/projectzomboid/comments/1ilo00f/1000_hour_player_cant_make_it_more_than_a_week_in/): documents early-B42 confusion and balance churn. This is self-reported experience, not ranked expertise. Its book scarcity and XP claims were not adopted.
- [Build42 community questions](https://www.reddit.com/r/projectzomboid/comments/1q69hwu/any_tips_guys/): recipe/progression uncertainty; directs users toward current information rather than old assumptions.
- [Players struggling in B42](https://www.reddit.com/r/projectzomboid/comments/1ug3fl2/struggling_to_survive_in_b42/): candidate themes are stamina management, smaller encounters and clothing tradeoffs, not universal crowd-size limits.

Discovered MrAtomicDuck's [50+ tips](https://www.youtube.com/watch?v=Dxr7sHJR8N4) and [first-week series](https://www.youtube.com/watch?v=if_QfqNo8DE), plus community recommendations for Nurse/Retanaru. Only video descriptions/metadata were available, not transcripts or footage analysis. Therefore no individual gameplay tip is attributed to these creators and no claim of watching their videos is made. Generic search pages and unattributed derivative summaries were not treated as expert evidence.

Outcome: candidate families span combat, escape, condition, looting, shelter, water, food, wounds, vehicles, crafting, power/fire and long-term survival. Avoid padding the collection with copied jokes or minor rewrites of the same instruction.

## Pass2: mechanics and version cross-check

Read [PZwiki Water](https://pzwiki.net/wiki/Water), [Moodles](https://pzwiki.net/wiki/Moodles) and [Vehicles](https://pzwiki.net/wiki/Vehicles). Their version banners lag the installed game, so they corroborate broad systems only. Generator, Combat, Foraging, First Aid, Nutrition, Agriculture, Helicopter and Animal husbandry pages were unavailable through the web tool and are not claimed as read.

Cross-checked candidate mechanics against installed `media/lua/shared/Translate/EN/SurvivalGuide.json` and the native UI quick-tip entries: movement/noise, climbing load, fence lunges, aiming, encumbrance, water treatment, generator exhaust, food handling, wound care, sleep, escape ropes, crafting surfaces, animal water/feeding and weapon strain. These shipped descriptions are primary evidence for this build, but not runtime tests. Source strings were not copied into the new library.

Reviewed the developer's [Build42 release context](https://projectzomboid.com/blog/news/2024/12/build-42-unstable/) and [42 stable plans](https://projectzomboid.com/blog/news/2026/07/build-42-stable-plans/) for version churn, not detailed survival formulas.

Outcome: qualify walking advice for ordinary shamblers; distinguish sleepiness, exertion and strain; rely on in-game water status and recipe requirements. Do not promise rainwater plumbing purification, guaranteed infection outcomes, a mandatory generator magazine or a universal firearm strategy. Remaining planning tips are explicitly practical suggestions rather than new mechanical claims.

## Pass3: skeptical review and final selection rules

Revisited the candidate themes with fresh counterexamples and additional player reports:

- [B42 survival guide and replies](https://www.reddit.com/r/projectzomboid/comments/1vco148/guide_to_surviving_in_project_zomboid_v2/): useful logistics themes; rejected invincible-fence claims, weapon rankings, guaranteed spawns, extreme trait builds and herbal treatment recipes. Clothing protection has mobility/heat tradeoffs.
- [Agriculture by month](https://www.reddit.com/r/projectzomboid/comments/1q37415/build_42_agriculture_by_month/): explicitly42.12, therefore retain only checking the current crop's planting information, not its month table or growth timings.
- [Indoor generator discussion](https://www.reddit.com/r/projectzomboid/comments/1huaemz/generators_inside_more_specific/): reinforces the shipped indoor-exhaust warning; do not present a basement/range workaround.
- [B42 wound-care discussion](https://www.reddit.com/r/projectzomboid/comments/1qbmbf7/how_to_take_care_of_bullet_wounds_in_build_42/): prioritize immediate bleeding control and a safe treatment location; no real-world medical guidance, exact timers or guaranteed cure claims.
- Rechecked Water/Moodles version warnings and the Steam guide's unsupported group-size and trait assertions. Removed universal slogans such as always outwalking zombies or treating every infection label as the Knox virus.

Final selection:120 original English tips,12 groups of10. Most are short decisions a player can apply; no copied creator scripts, exact stat thresholds or outside links appear in game. Changing weather, zombies, settings or mods can invalidate a tactic, so the final group includes checking settings and current in-game information. This is curated advice, not proof of optimal play.

## Content provenance by ID range

| IDs | Theme | Evidence and interpretation |
| --- | --- | --- |
|001-010|Combat|Gabes/struggling-player discussion plus shipped combat guide; spacing and retreat suggestions|
|011-020|Escape|Shipped movement/fence guidance plus veteran discussions; route planning suggestions|
|021-030|Condition|PZwiki Moodles and shipped rest/strain guidance; avoid exact penalty numbers|
|031-040|Loot|MR. FOODE/Gabes and shipped inventory guidance; original prioritization suggestions|
|041-050|Shelter|Gabes and shipped windows/escape-rope guidance; redundancy rather than invulnerability|
|051-060|Water|PZwiki Water and shipped liquid/purification guidance; label-driven water safety|
|061-070|Food|Shipped food guide, Moodles and long-term community guide; no diet formulas|
|071-080|Wounds|Shipped first-aid guidance, wound discussion and native infection distinction; no cure promises|
|081-090|Vehicles|PZwiki Vehicles, MR. FOODE vehicle checklist and shipped vehicle UI; original travel planning|
|091-100|Crafting|Shipped crafting help and community recipe questions; current UI over old recipes|
|101-110|Power/fire|Shipped exhaust/cooking guidance and generator discussion; no ranges or fuel formulas|
|111-120|Long term|Shipped animal tips, crop-month discussion and community logistics; settings-qualified planning|

## Native loading integration evidence

REA identified the installed archive SHA256 `80e405a4bfc42f6072e75b3735f458a6514143da011d3226007ded305a442f44`. Read-only `GameLoadingState` bytecode in ignored `build/fast-load/loading-presentation-bytecode.txt` establishes:

- Constructor calls `loadQuickTipList`; it scans the already-loaded UI translation map for all keys starting `UI_quick_tip`, separating `UI_quick_tip_joke`.
- Native `doQuickTips` draws a centered bottom tip and advances at its own720 menu-time-unit threshold. It returns immediately for a new game; it also does not cover error/connection branches that return before it.
- `getNewQuickTip` samples with replacement and occasionally chooses a stock joke. Adding our keys extends that pool without removing stock tips or changing native loading/render state.
- Ordinary Workshop Lua cannot animate the earlier engine-initialization frame. Menu/boot tips are a separate12-second carousel; they cannot guarantee native loader ordering or repetition behavior.

Current implementation is a source-derived candidate. No native timing, high-DPI text-fit, localization, rotation or performance outcome is established. English tips use new namespaced UI keys; other-language UI will fall back to English only where native translation fallback includes them. No runtime web requests or player tracking are added.
