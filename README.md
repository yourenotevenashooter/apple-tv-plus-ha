# Apple TV Plus for Home Assistant

*(formerly "Apple TV Enhanced" — same integration, new name; the internal domain stays `apple_tv_enhanced` so existing installs keep working.)*

Apple TV Plus adds a unified Apple TV media player with app launching, Home Screen shortcuts, custom sources/deep links, Fast Sleep, and HomeKit support, on top of Home Assistant's native Apple TV integration.

## Current Version

**0.0.8**

## Requirements

1. Add and configure the official Home Assistant **Apple TV** integration first.
2. Apple TV Plus uses that native integration as its underlying Apple TV connection.

## Installation with HACS

Add this repository as a custom HACS repository:

`https://github.com/yourenotevenashooter/apple-tv-plus-ha`

Select **Integration**.

Then install **Apple TV Plus**.

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
- Deep links (app bundle IDs or URLs)
- HomeKit exposure
- HACS installation

## Built-in Sources

- Apple TV
- Apple Music
- Apple Podcasts
- Apple Photos
- Apple Settings
- Apple App Store
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
- **Power** and **Inputs** work automatically — no extra setup, they come straight from this integration's existing turn on/off and source list.
- **Play/pause** in the remote popup works automatically too — Home Assistant wires that straight to this integration's play/pause support.
- **Arrows, select, back, exit, and skip/rewind/fast-forward** in the remote popup are forwarded by this integration (as of v0.0.8) to the Apple TV as real remote button presses, via the same remote device used for Fast Sleep and Home Screen — so the **Apple TV remote device** picked during setup must be set for these to work, the same requirement as Fast Sleep and Home Screen already have.

## Known Limitations

- Apple TV power behavior can vary between Home Assistant and Apple Home depending on the native Apple TV integration/device state — Apple Home tends to be more consistent for power.
- Apps must be installed on the Apple TV for their bundle identifier to launch.
- Bundle IDs are believed correct based on testing, but third-party apps can change theirs — treat any that don't launch as worth double-checking.
- Dynamic app discovery depends on your native Apple TV integration exposing a `source_list` state attribute — not guaranteed on every pairing/setup, and in practice it tends to reflect recently-used apps rather than every app installed. It's always layered on top of the built-in app list, never a replacement for it.
- There's an open pyatv issue (#2868) where tvOS can silently refuse to launch an app while pyatv reports success, with no fix yet. If a launch ever silently does nothing, this upstream bug is the likely cause, not this integration.
- Volume controls only work if the native Apple TV integration itself can report/control volume for your setup (this varies by Apple TV model and how it's connected to your TV/soundbar). If volume isn't available there, it won't be available here either.
- The Apple Home remote-control popup (arrows/select/back/exit/skip) only appears if this media player is bridged through a HomeKit Bridge instance set to **accessory mode**, per Home Assistant's own requirement for `device_class: tv` — see the HomeKit section above. In a shared/normal-mode bridge it still shows up, just without the full Television/remote experience.
- HomeKit's "information" remote-popup button has no Apple TV equivalent and is intentionally left unmapped (does nothing).
- "Back" is sent as a single Menu press and "Exit" as a long Menu press (jump to the true Home Screen) — the closest real Apple TV button behavior for each, but not identical to how those buttons behave on every other kind of TV in Apple Home.

## Roadmap

### Future

- Expanded, community-verified bundle-ID database
- Better Home Assistant dashboard power handling
- More HomeKit behavior testing

## License

MIT
