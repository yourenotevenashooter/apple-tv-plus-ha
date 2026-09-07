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
