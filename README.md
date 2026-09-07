# Apple TV Plus for Home Assistant

*(formerly "Apple TV Enhanced" — same integration, new name; the internal domain stays `apple_tv_enhanced` so existing installs keep working.)*

Apple TV Plus adds a unified Apple TV media player with app launching, Home Screen shortcuts, custom sources/deep links, Fast Sleep, and HomeKit support, on top of Home Assistant's native Apple TV integration.

## Current Version

**1.0.0**

## Requirements

1. Add and configure the official Home Assistant **Apple TV** integration first.
2. Apple TV Plus uses that native integration as its underlying Apple TV connection.

## Installation with HACS

Add this repository as a custom HACS repository:

`https://github.com/yourenotevenashooter/apple-tv-plus-ha`

Select **Integration**.

Then install **Apple TV Plus**.

### Getting listed in HACS's default repositories

Right now, installing requires adding this as a custom repository (above). Getting listed in HACS's own default list — so it shows up in HACS search with no custom-repository step — is a real submission process to a separate repository, `hacs/default`, and the last few steps require your own GitHub account (can't be done from here). Steps, in order:

1. **On GitHub**, add a repository description, add some topics (e.g. `home-assistant`, `hacs`, `apple-tv`), and confirm issues are enabled — all in the repo's own Settings.
2. **Push this update** (adds `.github/workflows/hacs.yml` and `hassfest.yml`) and confirm both Actions pass with no errors under the repo's **Actions** tab. These are what HACS's own submission process checks for.
3. **Publish an actual GitHub Release** (Releases → Draft a new release, not just a git tag) once the Actions are green — tag it `v1.0.0` to match `manifest.json`.
4. **Fork [hacs/default](https://github.com/hacs/default)**, branch off `master`, and add this repository's URL alphabetically to the `integration` file in that fork.
5. **Open a PR** from that fork using their PR template. Do this from your personal GitHub account, not an organization — HACS requires the PR stay editable by you.

A bot in that PR re-runs the same validation and will flag anything missing.


## Setup

Go to:

**Settings → Devices & Services → Add Integration → Apple TV Plus**

Pick your existing Apple TV media player entity, and optionally its remote device (needed for Fast Sleep and Home Screen). Custom sources are no longer part of first-time setup — add them afterward from **Configure**.

## Features

- Apple TV app launcher
- Home Screen shortcut
- Fast Sleep
- Multiple custom sources — add, edit, and delete from Configure, no reinstall needed
- Favorites — star a source to sort it to the top of the list, including in Apple Home's TV input picker
- Dynamic app discovery — when the native Apple TV integration reports additional apps it currently knows about beyond the built-in list below, those are added automatically
- Volume up/down, set, and mute — when your Apple TV setup reports volume support (e.g. via AirPlay volume or HDMI-CEC to the TV/soundbar)
- Apple Home remote-control popup — arrows, select, back, exit, and skip/rewind/fast-forward from the Home app's Device Controls remote actually drive the Apple TV (see HomeKit section below for the one-time setup this needs)
- Accurate playback state — reports actual playing/paused/buffering status, not just on/off, so dashboards and automations checking "is this playing" get a real answer
- Deep links (app bundle IDs or URLs)
- HomeKit exposure
- HACS installation

## Built-in Sources

Apple's own apps below are sourced from Apple's official tvOS bundle-ID documentation. Everything else is community/testing-verified rather than officially documented — see Known Limitations.

- Apple TV
- Apple Music
- Apple Podcasts
- Apple Photos
- Apple Settings
- Apple App Store
- Apple Arcade
- Apple Fitness+
- FaceTime
- Netflix
- YouTube
- Hulu
- Disney+
- Max
- Amazon Prime Video
- Peacock
- Twitch
- Crunchyroll
- Calendar by Dashbd

## Managing Custom Sources

Go to **Settings → Devices & Services → Apple TV Plus → Configure** to add, edit, or remove sources. Each source has:

- **Name** — what shows up in the source list
- **Target** — an app bundle identifier or a URL/deep link
- **Favorite** — sorts this source to the top of the list with a ★, in front of the built-in apps

Examples:

`com.netflix.Netflix`

`youtube://www.youtube.com/watch?v=VIDEO_ID`

Changes apply immediately — no need to remove and re-add the integration.

## Home Screen

Selecting **Home Screen** sends the Apple TV Home command instead of launching an app. It's a fixed built-in source and can't be renamed or removed.

## HomeKit

The Apple TV Plus media player exposes `device_class: tv`, which is what makes Home Assistant's HomeKit Bridge represent it as a Television accessory in Apple Home — Power, an Inputs list (this integration's own source list), and a remote-control popup with play/pause, a D-pad, select, back, exit, and skip controls.

**Getting the full Television accessory (not just a plain switch) requires one setup step in Home Assistant, not in this integration:** per Home Assistant's own HomeKit docs, a `media_player` with `device_class: tv` must be bridged in **accessory mode** — its own dedicated HomeKit Bridge instance, not lumped into a shared bridge with your other entities. To set this up:

1. **Settings → Devices & Services → Add Integration → HomeKit Bridge**
2. Add a new instance (don't reuse your main one if you have other entities in it)
3. Set **Mode** to **Accessory**
4. Under **Entities**, include only the Apple TV Plus media player entity
5. Finish setup and pair this new bridge with the Home app if it isn't auto-discovered

Once that's done:
- **Power** and **Inputs** work automatically — no extra setup, they come straight from this integration's existing turn on/off and source list. Input names sometimes show as generic "Input Source #" placeholders right after (re-)pairing — that's Apple Home's own local cache, not this integration; a full Home Assistant restart plus a clean re-pair of the accessory clears it.
- **Play/pause** works automatically too — Home Assistant wires that straight to this integration's play/pause support.
- **Arrows, select, back, exit, and skip/rewind/fast-forward** are forwarded by this integration (as of v0.0.8) to the Apple TV as real remote button presses, via the same remote device used for Fast Sleep and Home Screen — so the **Apple TV remote device** picked during setup must be set for these to work, the same requirement as Fast Sleep and Home Screen already have.
- Access the remote control through the **Apple Remote app or Control Center's remote widget** — pick this accessory from the device list there. A bridged (non-native) Television accessory like this one isn't guaranteed to also show a remote-control icon directly on its own Device Controls tile in the Home app; the Remote app/Control Center path is the platform's standard way to reach it either way, and everything above works through it.
- If you run more than one HomeKit Bridge instance, make sure this entity is included in only the one dedicated accessory-mode bridge — including it in a second (especially a shared/normal-mode) bridge causes Apple Home to see it as more than one accessory, which can produce exactly this kind of stale-name and inconsistent-icon behavior.

## Known Limitations

- Apple TV power behavior can vary between Home Assistant and Apple Home depending on the native Apple TV integration/device state — Apple Home tends to be more consistent for power.
- Apps must be installed on the Apple TV for their bundle identifier to launch.
- Apple's own apps use bundle IDs from Apple's official documentation and can be trusted as-is. Third-party apps (Netflix, Disney+, etc.) don't have publicly documented tvOS bundle IDs, so those are only as good as real-device testing, and a developer changing theirs will break launching until this list is updated — treat any that don't launch as worth double-checking.
- Dynamic app discovery depends on your native Apple TV integration exposing a `source_list` state attribute — not guaranteed on every pairing/setup, and in practice it tends to reflect recently-used apps rather than every app installed. It's always layered on top of the built-in app list, never a replacement for it.
- There's an open pyatv issue (#2868) where tvOS can silently refuse to launch an app while pyatv reports success, with no fix yet. If a launch ever silently does nothing, this upstream bug is the likely cause, not this integration.
- Volume controls only work if the native Apple TV integration itself can report/control volume for your setup (this varies by Apple TV model and how it's connected to your TV/soundbar). If volume isn't available there, it won't be available here either.
- Getting Power/Inputs/Remote at all (not just a plain switch) requires this media player to be bridged through a HomeKit Bridge instance set to **accessory mode**, per Home Assistant's own requirement for `device_class: tv` — see the HomeKit section above. In a shared/normal-mode bridge it still shows up, just without the full Television experience.
- Remote control is reached through the Apple Remote app / Control Center, not necessarily an icon on the accessory's own Device Controls tile — see the HomeKit section above.
- HomeKit's "information" remote button has no Apple TV equivalent and is intentionally left unmapped (does nothing).
- "Back" is sent as a single Menu press and "Exit" as a long Menu press (jump to the true Home Screen) — the closest real Apple TV button behavior for each, but not identical to how those buttons behave on every other kind of TV in Apple Home.
- **AirPlay directly to this accessory doesn't update its state.** If your Apple TV also shows up as its own AirPlay target in Control Center/the Remote app (common when it's bridged to HomeKit), sending audio there plays correctly, but this integration's state stays Off/Idle instead of Playing. This integration only ever mirrors the native Apple TV entity's own reported state — if that AirPlay session isn't something the native integration's own connection detects, there's nothing accurate for this integration to mirror. Playback state works correctly for anything played through the native connection itself (an app on the Apple TV, or `media_player.play_media`). Not yet confirmed whether this is fixable here at all, or is a Home Assistant/pyatv-level gap — candidate for further investigation in 1.1+.
- **Brand icon may show as unavailable in HACS's own downloads panel.** As of Home Assistant 2026.3+, integration brand icons are served through a new inline mechanism (`custom_components/<domain>/brand/`, used here). HACS's own frontend hasn't been updated to read that new path yet ([hacs/integration#5223](https://github.com/hacs/integration/issues/5223)), so the icon may show "icon not available" specifically inside HACS's UI even though it displays correctly elsewhere in Home Assistant. This is a HACS bug being tracked upstream, not something fixable from this repository — `home-assistant/brands` itself no longer accepts new icon submissions for custom (non-core) integrations, so the inline approach is the current correct one regardless.

## Roadmap

**1.0.0 is the first stable release** — every feature originally planned for it (app launching, Home Screen, Fast Sleep, custom sources, favorites, dynamic app discovery, volume, the Apple Home remote popup, and accurate playback state) is implemented and tested.

### Future (1.1+)

- More third-party bundle IDs, as they get community/real-device verification (see Known Limitations)
- Home Assistant's built-in diagnostics download for the config entry, to make troubleshooting reports easier
- Convenience for setting up a second Apple TV Plus entity (copying custom sources from an existing one)
- An example Home Assistant automation blueprint for handling `homekit_tv_remote_key_pressed`, for anyone who wants that behavior without this integration

## License

MIT
