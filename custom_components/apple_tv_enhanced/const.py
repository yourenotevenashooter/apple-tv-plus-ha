"""Constants for Apple TV Plus (internal domain stays apple_tv_enhanced)."""

DOMAIN = "apple_tv_enhanced"

CONF_MEDIA_PLAYER_ENTITY = "media_player_entity"
CONF_DEVICE_ID = "device_id"

# v0.0.4+ storage: list of {"name": str, "target": str}
CONF_CUSTOM_SOURCES = "custom_sources"

# v0.0.3 legacy single-source keys. Read-only, for migrating old config
# entries into CONF_CUSTOM_SOURCES automatically. Do not write these anymore.
LEGACY_CUSTOM_SOURCE_NAME = "custom_source_name"
LEGACY_CUSTOM_SOURCE_TARGET = "custom_source_target"

HOME_SCREEN_LABEL = "Home Screen"
HOME_SCREEN_TARGET = "__HOME__"

# v0.0.6+: prefix marking a source that came from the native Apple TV
# integration's own live app list (its `source_list` state attribute),
# rather than our static APP_IDS fallback or a user-defined custom source.
# Selecting one of these calls media_player.select_source on the NATIVE
# entity instead of play_media, since the native integration already knows
# how to launch it — this avoids opening a second pyatv connection just to
# discover or launch installed apps.
NATIVE_SOURCE_PREFIX = "__NATIVE_SOURCE__:"

# v0.0.8+: Home Assistant's own HomeKit Bridge integration, when a media_player
# is bridged into Apple Home as a Television accessory (device_class "tv", in
# HomeKit "accessory mode"), gives Apple Home a remote-control popup with a
# D-pad, select, and back/exit buttons. Play/pause is wired up automatically
# by Home Assistant's homekit component itself since it maps straight to our
# existing PLAY/PAUSE support — but every other button (arrows, select,
# back, exit, and the transport keys) just fires this HA event with no
# effect on the actual Apple TV until something listens for it. That's what
# this maps: this event's key_name values, forwarded to the native Apple
# TV's remote entity as real pyatv remote commands, so the Home app's
# remote popup actually drives the Apple TV.
EVENT_HOMEKIT_TV_REMOTE_KEY_PRESSED = "homekit_tv_remote_key_pressed"

# HomeKit key_name -> pyatv RemoteControl command (what remote.send_command
# accepts for the native apple_tv integration's remote entity). "back" maps
# to a single "menu" press (that's what the physical Apple TV remote's menu
# button does), "exit" maps to "top_menu" (a long menu press — jumps further,
# to the true top-level Home Screen) so the two keys stay meaningfully
# different instead of both doing the same thing. HomeKit's "information"
# key has no real Apple TV equivalent and is intentionally left unmapped.
HOMEKIT_REMOTE_KEY_TO_COMMAND = {
    "arrow_up": "up",
    "arrow_down": "down",
    "arrow_left": "left",
    "arrow_right": "right",
    "select": "select",
    "back": "menu",
    "exit": "top_menu",
    "rewind": "skip_backward",
    "fast_forward": "skip_forward",
    "next_track": "next",
    "previous_track": "previous",
}
