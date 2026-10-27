# Toolkit connection

The installed Project Zomboid Toolkit v0.4.0 is a direct game/debug/editor
bridge. Mod development stays in this repository. The game and Steam Workshop
handle mod management; the app has no mod-creation or folder wizard.

- Open Start menu > Dead Signal Interactive > Project Zomboid Toolkit.
- Connection > Connect to game reuses the existing saved settings.
- Launch Project Zomboid (test profile) starts the installed game with `-debug`,
  the existing isolated cache and `-modfolders mods`.
- Enable PZ Toolkit Bridge and the existing mod through the game's Mods screen,
  enter a disposable single-player world and unpause. Then Check connection.
- Game tools requests the built-in debug, vehicle, attachment, animation and
  world-map editors, controls god mode and shows logs. Advanced Lua sends code
  directly without creating a scenario or report file per command.
- God mode is enabled once when the character loads or respawns. Actual bridge
  status is authoritative; manual disablement remains respected.
- Preserve the original Start-menu DEBUG shortcut and normal saves. Do not
  recreate the experimental Javelin shortcut.

The saved connection uses `%LOCALAPPDATA%/PZToolkit/config.json`, the game at
`C:/Games/ProjectZomboid` and the owned isolated cache at
`%LOCALAPPDATA%/PZToolkit/game-profile`. Existing workspace/staging copies are
retained for compatibility, but the toolbelt does not require a new workspace.
Original project files and the existing mod deployment are unchanged.

Actual PC verification through Remote Desktop Commander confirmed v0.4.0 file
hashes, Start-menu target, unchanged configuration/token, 11 default CLI tools
and a real installed MCP initialize/list/call exchange. The global Codex server
`project-zomboid` uses the installed `pz.exe serve`; reload the MCP connection
if this chat has not picked it up. No world was loaded, so live bridge commands,
startup god mode and visible editor opening remain pending. Final rendered GUI
inspection is pending after desktop control was stopped.

For PC operations, verify files through Remote Desktop Commander on APeX-2.
The execution workspace and Windows desktop can expose different AppData
contents at identical paths. Local writes alone do not prove PC installation.
