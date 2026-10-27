# DOX framework

- DOX is highly performant AGENTS.md hierarchy installed here
- Agent must follow DOX instructions across any edits

## Core Contract

- AGENTS.md files are binding work contracts for their subtrees
- Work products, source materials, instructions, records, assets, and durable docs must stay understandable from the nearest applicable AGENTS.md plus every parent AGENTS.md above it

## Read Before Editing

1. Read the root AGENTS.md
2. Identify every file or folder you expect to touch
3. Walk from the repository root to each target path
4. Read every AGENTS.md found along each route
5. If a parent AGENTS.md lists a child AGENTS.md whose scope contains the path, read that child and continue from there
6. Use the nearest AGENTS.md as the local contract and parent docs for repo-wide rules
7. If docs conflict, the closer doc controls local work details, but no child doc may weaken DOX

Do not rely on memory. Re-read the applicable DOX chain in the current session before editing.

## Update After Editing

Every meaningful change requires a DOX pass before the task is done.

Update the closest owning AGENTS.md when a change affects:

- purpose, scope, ownership, or responsibilities
- durable structure, contracts, workflows, or operating rules
- required inputs, outputs, permissions, constraints, side effects, or artifacts
- user preferences about behavior, communication, process, organization, or quality
- AGENTS.md creation, deletion, move, rename, or index contents

Update parent docs when parent-level structure, ownership, workflow, or child index changes. Update child docs when parent changes alter local rules. Remove stale or contradictory text immediately. Small edits that do not change behavior or contracts may leave docs unchanged, but the DOX pass still must happen.

## Hierarchy

- Root AGENTS.md is the DOX rail: project-wide instructions, global preferences, durable workflow rules, and the top-level Child DOX Index
- Child AGENTS.md files own domain-specific instructions and their own Child DOX Index
- Each parent explains what its direct children cover and what stays owned by the parent
- The closer a doc is to the work, the more specific and practical it must be

## Child Doc Shape

- Create a child AGENTS.md when a folder becomes a durable boundary with its own purpose, rules, responsibilities, workflow, materials, or quality standards
- Work Guidance must reflect the current standards of the project or user instructions; if there are no specific standards or instructions yet, leave it empty
- Verification must reflect an existing check; if no verification framework exists yet, leave it empty and update it when one exists

Default section order:
- Purpose
- Ownership
- Local Contracts
- Work Guidance
- Verification
- Child DOX Index

## Style

- Keep docs concise, current, and operational
- Document stable contracts, not diary entries
- Put broad rules in parent docs and concrete details in child docs
- Prefer direct bullets with explicit names
- Do not duplicate rules across many files unless each scope needs a local version
- Delete stale notes instead of explaining history
- Trim obvious statements, repeated rules, misplaced detail, and warnings for risks that no longer exist

## Closeout

1. Re-check changed paths against the DOX chain
2. Update nearest owning docs and any affected parents or children
3. Refresh every affected Child DOX Index
4. Remove stale or contradictory text
5. Run existing verification when relevant
6. Report any docs intentionally left unchanged and why

## User Preferences

When the user requests a durable behavior change, record it here or in the relevant child AGENTS.md
- Current body-only authority (2026-10-27 18:48 UTC): reviewed BodyOnly V03 SHA-256 `668ffbaed111e20833c963a519ce04373525dd7e873b5957ed8bea24aabbfa90` supersedes older model checkpoints. Start at `current-work/README.md`. User narrowed the task to body geometry correction and proper slicing: do not add more underneath structure now. Newly authored underside modules are retained only as hidden, export-excluded optional history; original floor/tunnel and original side pipes remain. Preserve real-car research and citations. The later target is Wreckfest for PC installed through the Xbox app/Microsoft Store; this exact edition's custom-mod/import support is unverified, not an established supported export route. Current model is not game-ready. Keep this repository private; a cloud/Library-only artifact is not in a clone.
- GitHub source synchronization (2026-10-27): include product sources, editable artwork, contracts and portable development documentation. `current-work/` indexes the current reviewed cloud authoring artifact and selected evidence records; `assets/current-stl/` retains the older Git-stored model as historical work. Keep ignored experiment history, game/profile files, reference captures and machine-local handoff inventories local. `docs/project-status.md` is the portable takeover entry point. Refresh the current artifact manifest from exact reviewed source hashes; do not relabel the historical binary as current or claim Library-only binaries are in a clone. The user authorized recreating `raiinman/project-zomboid-javelin-1973` as private; preserve that visibility. `main` is the default branch.
- Marlow/DOT handoff (2026-10-27): user requested the entire project handed off and left locally for pickup. Read local `docs/MARLOW-HANDOFF.md` for the complete machine inventory, or `docs/project-status.md` in GitHub for portable current-state guidance. Historical ignored experiments remain local. Delivery remains local, without external messaging or Workshop publication.
- Blender reopen visibility (2026-10-27): save working car checkpoints with the current assembled panels, Meshy cabin, cabin closures and brightwork visible, using Material Preview. Keep preserved originals and superseded variants hidden to avoid overlapping geometry. Verify saved visibility by reopening after display corrections.
- Exterior finish and pipe fit (2026-10-19): add narrow window/aperture, belt and wheel-opening brightwork for readable native body lines; preserve the STL panel form. Bring both complete side-pipe assemblies closer to the separate black skirts through rigid inward translation, preserving length, slots and outlets. The combined authoring checkpoint is `build/stl-full-trace/slice-v03/integration/prototype-meshy-exterior-trim/DSI_Javelin_Meshy_Exterior_Trim_Pipes.blend`, built on V03 cabin closures. See `docs/exterior-brightwork-pipe-fit.md` for exact source, checks and owner/palette handoff. The user authorized export and isolated game staging on2026-10-19; see `docs/meshy-native-test.md` for the packaged checkpoint and native appearance status.
- Meshy interior direction (2026-10-19): the user accepts the corrected Meshy front seat as visually accurate. Carry it forward for mesh reduction and fitting; high polygon count is an implementation task, not a reason to reject the accepted appearance. Continue reference-based Meshy authoring for the steering wheel, dashboard and instrument fascia, keeping compute economical. User acceptance supersedes the earlier agent recommendation to retain the seat only as an unaccepted shape candidate.
- Meshy integration source: `build/stl-full-trace/slice-v03/integration/prototype-meshy-v03-closures/DSI_Javelin_Meshy_Cabin_Closures_V03.blend` carries the accepted Meshy v02 cockpit, separate downward black skirts and fitted front cabin closures. Preserve prior versions, raw GLBs, reductions and original sources. See `docs/meshy-car-integration.md` and `docs/cabin-closure-restoration.md`. The user authorized the combined textured export and isolated native test; remaining operation/appearance gates are tracked in `docs/meshy-native-test.md`. Headliner, original Cardin door panels and rear enclosure coverage remain open.
- Meshy export hold was superseded by the user's explicit2026-10-19 request to put the current car in game for testing. Preserve the accepted V02 fascia/column correction, V03 enclosure and combined exterior trim/closer pipes. Use the textured atlas export, never the old palette-only overwrite, and stage only in the owned isolated Toolkit profile.
- Current prototype priority (2026-10-19): make the STL-based car visually presentable with a readable basic interior, wheels, lights, grille and trim for a Steam Workshop prototype. Keep work economical with the user's limited remaining Codex usage. Fine artwork remains deferred; incomplete braking/persistence checks remain disclosed but do not block authoring this appearance pass. Prepare a reviewable package before any Workshop publication.
- Current expansion: the side skirts must be separate editable black pieces extending downward from the stock sill toward the pipes. Remove the rejected outward running-board shelf; preserve original body form, doors and pipe geometry. Audit and refine interior topology/design, enable and verify seated-character visibility, and bring forward recognizable front chrome and the original hood/fender T artwork. Restart the decal from clean hood and fender surfaces. The user confirmed this reset applies only to the decal, not the car model. Use the original drawing as closer shape evidence than the rejected rounded T experiments, but rebuild directly against the actual upper surfaces and reference landmarks. Preserve complete outer corners, the reference taper and fine contour; avoid distortion from global fitting formulas. Preserve prior experiments as inactive history. This specifically authorizes these features before the remaining native slice gates; exact small lettering stays deferred.
- Interior completeness correction (2026-10-19): audit the original authored pre-STL cabin for missing enclosure pieces, especially the firewall. Refit compatible original cowl, floor and liners around the accepted Meshy cockpit; explicitly reconstruct genuinely missing firewall/toe-board closures. Preserve Meshy appearance, seats, column, registration and exterior work. Do not hide missing structure behind the dashboard or substitute third-party mod assets.
- Carry useful original project work forward into the STL conversion. Refit our previously authored cabin, equipment and artwork where compatible instead of rebuilding generic substitutes. Preserve the STL body authority and distinguish our own prior assets from the unrelated third-party old mod.
- Prototype appearance corrections: use the video's bright glossy candy-red appearance, with a corresponding game palette. Fit separate black downward skirt panels beneath the stock sill on both sides, with minimal outward offset and no running-board shelf. Shorten pipes by removing a section from their straight centres and joining the halves; preserve slot sizes, rear outlets and door geometry. Level each assembly through rigid rotation, without deforming or globally scaling it. Trim or replace only the front inlet terminal tip as needed to meet the new rocker. Outlets must end forward of the rear wheel openings. Preserve the STL body; distinguish Blender clear-coat shading from the game's appearance. The deformed G pipe experiment is rejected and must not become the active model.
- Camera development prioritizes the most usable camera the supported game APIs allow in a standalone Steam Workshop package, without Viewpoint or an external installer. Build and verify native isometric controls now; retain Sims-style full 3D rotation/tilt as separate unproven research. Read `camera/AGENTS.md` for camera work; the vehicle fender scope applies to vehicle refinement.
- Maintain two independent product mods: the camera mod and a fast-loading mod. The fast-loading mod targets intro/menu delays and time to a loaded game, with measured improvements and preserved required initialization. Camera research probes are development artifacts, not additional product dependencies.
- Fast Load must stop at the main menu and never automatically load the last save. Current optimization edits are to be packaged without running tests or launching the game; label the revision untested.
- Active vehicle scope is the entire user-owned STL, traced as the full-car shape master in `build/stl-full-trace/`. Preserve its hood, fenders, nose, cabin, doors, rear quarters, trunk and spoiler proportions; use the video for target-specific equipment and artwork. Preserve the prior production and hybrid checkpoints. Keep the latest checked working model visible in the user's single Blender window, reconciling unsaved edits before switching. Read `docs/full-stl-trace.md` for the active source and conversion contract.
- Deliver the complete STL-faithful usable vehicle slice before fine details: functional panels, running gear, glazing, basic cabin, export/package and isolated native driving/interactions/save-reload verification. Keep decorative artwork, exact lettering and upholstery patterns deferred until the slice gates in `docs/full-stl-trace.md` pass.
- Reuse one working Blender inspection window when safe. Close redundant inspection/reference windows after preserving their unsaved state, and coordinate with other active chats before closing a window they may be using.
- Keep a live Blender window visible during car modeling so the user can watch work. Display the current isolated prototype when that is the active task, preserve unsaved documents before switching, and show subsequent checked changes in the same working window.
- Prioritize substantial, reference-driven car-form changes over repeated small detail passes when the user rejects visible progress. Use clear same-view before/after evidence, preserve checkpoints, and keep delegated work focused to avoid unnecessary credit use.
- Reconstruction skill improvements should combine demonstrated project lessons with established geometric/optical reasoning, distinguish evidence from workflow heuristics, and receive independent scenario review. The installed img2blender video/convergence and surface-reasoning guides contain the reusable methods; keep project records outside the skill.

## Child DOX Index

- `camera/AGENTS.md`: separate camera mod specification, renderer integration, source and verification.
- `fast-load/AGENTS.md`: independent fast-loading mod, startup investigation, packaging and native timing evidence.
- `tools/AGENTS.md`: original model generation, build, validation and installation tools.
- `Javelin73PC/AGENTS.md`: packaged Build 42 vehicle assets and gameplay scripts.
- `assets/AGENTS.md`: original editable artwork and model sources.
- `.img2blender/AGENTS.md`: reconstruction specification, evidence boundaries and section-review records.
- `build/stl-full-trace/slice-v03/native-test/AGENTS.md`: scoped development-only native audit hooks, research and offline verification; root retains profile staging and native execution authority.
- `current-work/AGENTS.md`: current body-only model authority, verification evidence, artifact access and scope limits.
- Root owns project specifications, README, versioning and documentation in `docs/`.

## Project contract

- This is a Dead Signal Interactive creation. Distributed mod files must have no personal author credits, external redirects, local filesystem paths or optional exporter provenance. Preserve functional game metadata and any required third-party license notices. Keep research citations and development records outside the distributed package.
- Build an original 1973 AMC Javelin AMX Pierre Cardin mod from https://www.youtube.com/watch?v=ZpfnHMBiRvA for Project Zomboid 42.20.4 (current user-confirmed target).
- New authored geometry, textures and scripts are original project work; the user-owned STL base is the explicit reuse exception below. The old Javelin mod under the user's Zomboid directory belongs to another project and is technical reference only. Do not copy its assets or publish derived copies.
- The user owns the supplied STL and now authorizes using its entire shape as the vehicle base. Stage the full-car trace in ignored `build/stl-full-trace/`, with source provenance and shape-preservation evidence. The earlier `build/stl-front-prototype/` hybrid experiments are preserved historical checkpoints. Keep installed mods and the prior production source intact while converting the new base into functional vehicle parts.
- Front-assembly reference corrections: replace the fabricated thick silver bumper with the observed thin continuous silver trim returning onto the fenders; the two black guards overlap that trim. Recess both red auxiliary lamps, deepen the headlamp bowls, correct grille shape and all three grille badge positions/artwork from visible reference evidence, soften excessive hood ridges, and construct/fix wheel-well geometry rather than treating dark inner paint as a fit correction.
- Preserve existing game installations, mods and saves. Normal-profile installation is limited to the separate `Javelin73PC` mod. Camera development probes may be staged only in the owned isolated Toolkit profile.
- Launch native tests through Toolkit Connection > Launch Project Zomboid (test profile), using the installed game with `-debug` and the isolated Toolkit profile. The experimental Javelin test shortcut has been removed at the user's request; do not recreate it. Preserve the original Start-menu DEBUG shortcut and normal saves.
- Use Context7 for current library, framework, API and CLI documentation, beginning with resolve-library-id.
- Apply relevant skills from installed catalogs and raiinman/skill-library; avoid unrelated workflows.
- Reference research requires four passes: factory identity/options; dimensions/exterior/powertrain; Cardin interior; the supplied restored car. Prefer contemporary AMC literature, preserve source disagreements, and distinguish factory specifications from video observations and gameplay tuning.
- When the user requests four analyses of supplied webpages, perform four complete reviews covering every supplied page's text and relevant photographs. Four topic categories or four Blender changes do not count. Record each review's evidence, findings and limits before implementation. The corrected initial gallery review is `docs/webpage-four-analyses.md`; the subsequent six-source review including Hagerty is `docs/six-source-four-analyses.md`.
- Subagents are always authorized for this project without asking again. Give them distinct file scopes and verify their outputs.
- Resume background work through its existing session handle. Before stopping a job, verify its live PID, executable and exact command line belong to that worker's task; never stop a guessed or neighboring process.
- Use the REA skill/plugin for game and existing-mod investigation when shipped behavior is uncertain. Record tool limits and separate native importer observations from hypotheses.
- Native debug probes must verify exposed methods and use checked reflection for fields. `pcall` still enters Break On Error for unsupported userdata access; report unavailable data without speculative calls and preserve debugger settings.
- Visual likeness is a required gate: compare body proportions, fender crowns, roof/sail-panel silhouette and reference trim before treating a model as finished. Passing script checks alone is insufficient.
- All car sections remain open during the current refinement. Saved checkpoints and passing checks record iterations, not closed sections or a claimed likeness percentage. The user rejects the current model as substantially short of the original video's likeness.
- Pursue at least90% reference parity across every exterior and interior section. Whenever a review appears to reach90%, restart a skeptical whole-vehicle audit using45% as the review baseline, preserving the model and prior evidence. This resets scrutiny, not geometry. Do not manufacture numerical fidelity measurements; support assessments with reference comparisons, individual critical-feature gates and native-game inspection. Continue corrective iterations beyond default skill iteration limits under this explicit instruction.
- Refinement proceeds section by section after four fresh research comparisons. Review the original video frames and photographs against the latest saved Blender model, finish and verify the selected section before advancing, and continue until the real car's visual identity is met. Use script-driven Blender refinement without mouse or keyboard when requested; do not equate a passing source check with 1:1 parity.
- Use the installed local Blender for interactive refinement and multi-angle inspection when the user makes the PC available. Keep saved source and procedural generation consistent; source checks and viewport inspection do not replace native game review.
- Geometry review requires four explicit passes: body seams; moving-panel fit; face normals and axis consistency; native in-game alignment from both sides and front/rear/top views. Fix findings and rerun affected checks before closeout.
- The current geometry closeout also requires five additional passes requested by the user: intermediate moving-part clearances; underside/wheel wells and mirrored trim; seat/wheel/hinge registration; surface visibility; reference proportions and trim. Source reviews must not be presented as completed native inspection.
- Keep progress updates brief. User messages steer ongoing work; continue independent work.
- Do not use em dashes. After an asynchronous question form, wait at least 30 seconds before ending the turn unless answered sooner.
- GitHub repository is user-owned. Keep generated reference screenshots, local paths, game files and unrelated project material out of published commits.
- DOX was installed from raiinman/dox at b88194c34ace1a2a3dc01831d36b8a65986a41f5. Its MIT license is preserved at `docs/licenses/DOX-MIT.txt`.

- Toolkit is a direct game/debug/editor bridge for Codex, not a mod manager. Use the game and Steam Workshop for mod management; do not add mod-creation, folder-setup or scenario-file workflows to the app. Existing mod development stays in this repository.
- Toolkit connection, isolated profile and first-launch workflow are documented in `docs/toolkit-setup.md`. Verify PC-side files through Remote Desktop Commander before relying on them in the Windows GUI.

## README presentation

Keep `README.md` centered and lead with an actual render of the indexed reviewed cloud authoring milestone, captioned with its checkpoint and evidence limits. Preserve the original decorative artwork in `readme-banner.png` and its brief in `readme-banner-prompt.txt` as clearly labeled historical links lower down. Use compact logo badges using Shields.io `label-message-color` URLs, and a linked section index with verified project-file shortcuts. Center documentation tables and code containers while preserving code spacing. Public repository metrics may use live Shields.io or Badgen badges. Preserve project status, attribution, evidence boundaries, and operational authority; artwork and badges are presentation only.
