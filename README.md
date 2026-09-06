# Apple TV Enhanced for Home Assistant

Apple TV Enhanced adds a unified Apple TV media player with app launching, Home Screen shortcuts, custom sources/deep links, Fast Sleep, and HomeKit support.

## Current Version

**0.0.3**

## Requirements

1. Add and configure the official Home Assistant **Apple TV** integration first.
2. Apple TV Enhanced uses that native integration as its underlying Apple TV connection.

## Installation with HACS

Add this repository as a custom HACS repository:

`https://github.com/Nappyty11/apple-tv-enhanced-ha`

Select **Integration**.

Then install **Apple TV Enhanced**.

## Setup

Go to:

**Settings → Devices & Services → Add Integration → Apple TV Enhanced**

Enter the entity ID of your existing Apple TV media player and the remote device ID when requested.

## Features

- Apple TV app launcher
- Home Screen shortcut
- Fast Sleep
- Custom source name and target
- Deep-link groundwork
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

## Custom Sources

The current version supports one custom source through:

- **Custom Source Name**
- **Custom Source Target**

Targets can be an Apple TV app bundle identifier or a URL/deep link.

Examples:

`com.netflix.Netflix`

`youtube://www.youtube.com/watch?v=VIDEO_ID`

## Home Screen

Selecting **Home Screen** sends the Apple TV Home command instead of launching an app.

## HomeKit

The Apple TV Enhanced media player can be exposed through Home Assistant's HomeKit Bridge. For TV-style behavior, expose the media player as an accessory according to Home Assistant's HomeKit documentation.

## Known Limitations

- Apple TV power behavior can vary between Home Assistant and Apple Home depending on the native Apple TV integration/device state.
- Apps must be installed on the Apple TV for their bundle identifier to launch.
- The current custom-source editor supports one custom source; multiple-source management is planned for the next release.

## Roadmap

### 0.0.4

- Multiple custom sources
- Add/edit/delete source management
- Cleaner options flow
- Expanded deep-link support
- Favorite shows and movies
- Better source management without reinstalling

## License

MIT
