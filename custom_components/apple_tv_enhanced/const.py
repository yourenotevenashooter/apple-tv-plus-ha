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
