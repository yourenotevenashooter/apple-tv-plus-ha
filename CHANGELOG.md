# Changelog

All notable changes to Apple TV Plus (internal domain `apple_tv_enhanced`) are documented here.

## 1.0.0 — First stable release

- **Accurate playback state**: the entity now mirrors the native Apple TV entity's real state (playing, paused, buffering, etc.) instead of only ever reporting on/off, so dashboard cards, voice assistants, and automations checking "is this playing" get a real answer.
- **Bundle-ID correction and additions**: fixed Apple Podcasts' bundle ID casing to match Apple's official documentation (`com.apple.podcasts`), and added three more officially-documented Apple apps: Apple Arcade, Apple Fitness+, and FaceTime.
- Built-in source list now notes which entries are from Apple's official bundle-ID documentation versus community/testing-verified third-party apps.
- No breaking changes — safe to update from 0.0.8.

## 0.0.8 — Apple Home remote-control popup

- Apple Home's HomeKit remote-control popup (arrows, select, back, exit, skip/rewind/fast-forward) now actually drives the Apple TV. Home Assistant's HomeKit Bridge only auto-wires play/pause for TV accessories; every other button previously just fired an inert `homekit_tv_remote_key_pressed` event. This integration now listens for that event and forwards it to the Apple TV as real remote commands.
- Documented the HomeKit Bridge **accessory mode** requirement for getting the full Television accessory (Power/Inputs/Remote) in Apple Home at all, and the pitfall of exposing the same entity through more than one HomeKit Bridge instance.
- Noted that the remote is reached through the Apple Remote app / Control Center, not necessarily an inline icon on the accessory's own tile — this is expected behavior for bridged (non-native) Television accessories, confirmed working end-to-end.

## 0.0.7 — Volume controls

- Added volume up/down, set, and mute, forwarded to the native Apple TV entity — works if your specific Apple TV setup can report/control volume (AirPlay volume or HDMI-CEC to the TV/soundbar).
- Added the "liquid glass" `icon.png`/`logo.png` so HACS shows proper branding for this custom repository.

## 0.0.6 — Dynamic app discovery

- Added live app discovery from the native Apple TV integration's own `source_list` state attribute, layered on top of (not replacing) the built-in app list — an earlier version of this feature briefly replaced the built-in list outright, which silently hid apps that otherwise worked fine, and was corrected same-release once caught in testing.
- No new pyatv connection is opened for this — it reads state Home Assistant already has, avoiding any conflict with the native integration's existing connection to the same Apple TV.

## 0.0.5 — Favorites

- Added a favorite flag per custom source: favorited sources sort to the top of the list with a ★ prefix, visible in Apple Home's TV input picker too.

## 0.0.4 — Multiple custom sources, better setup UX

- Replaced the single custom source (name/target pair) with a full add/edit/remove list, managed from **Configure** without reinstalling.
- Narrowed the setup form's entity/device pickers to only show Apple TV entities and devices, and added inline help text — first-run setup was confusing multiple Apple TVs and other media players together.
- Migrated existing single-custom-source config entries automatically.

## 0.0.3 and earlier — Foundation

- Original "Apple TV Enhanced" baseline: unified media player facade over Home Assistant's native Apple TV integration, app launching via bundle ID or deep link, Home Screen shortcut, Fast Sleep, single custom source, HomeKit exposure.
- Renamed to "Apple TV Plus" (the internal domain stays `apple_tv_enhanced` so existing installs and entity IDs keep working).
- Fixed the HACS repository structure (`custom_components/` and `hacs.json` at repo root) so HACS could detect and install it as a custom repository at all.
