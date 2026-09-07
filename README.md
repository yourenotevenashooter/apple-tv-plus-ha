# Apple TV Plus for Home Assistant

*(formerly "Apple TV Enhanced" — same integration, new name; the internal domain stays `apple_tv_enhanced` so existing installs keep working.)*

Apple TV Plus adds a unified Apple TV media player with app launching, Home Screen shortcuts, custom sources/deep links, Fast Sleep, and HomeKit support, on top of Home Assistant's native Apple TV integration.

## Current Version

**0.0.6**

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

The Apple TV Plus media player can be exposed through Home Assistant's HomeKit Bridge. For TV-style behavior, expose the media player as an accessory according to Home Assistant's HomeKit documentation.

## Known Limitations

- Apple TV power behavior can vary between Home Assistant and Apple Home depending on the native Apple TV integration/device state — Apple Home tends to be more consistent for power.
- Apps must be installed on the Apple TV for their bundle identifier to launch.
- Bundle IDs are believed correct based on testing, but third-party apps can change theirs — treat any that don't launch as worth double-checking.
- Dynamic app discovery depends on your native Apple TV integration exposing a `source_list` state attribute — not guaranteed on every pairing/setup, and in practice it tends to reflect recently-used apps rather than every app installed. It's always layered on top of the built-in app list, never a replacement for it.
- There's an open pyatv issue (#2868) where tvOS can silently refuse to launch an app while pyatv reports success, with no fix yet. If a launch ever silently does nothing, this upstream bug is the likely cause, not this integration.

## Roadmap

### Future

- Volume controls
- Remote control actions / additional Apple TV commands
- Expanded, community-verified bundle-ID database
- Better Home Assistant dashboard power handling
- More HomeKit behavior testing

## License

MIT
