"""Media player platform for Apple TV Plus."""

import asyncio

from homeassistant.components.media_player import MediaPlayerEntity
from homeassistant.components.media_player.const import (
    MediaPlayerEntityFeature,
    MediaPlayerState,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .apps import APP_IDS
from .const import (
    CONF_CUSTOM_SOURCES,
    CONF_DEVICE_ID,
    CONF_MEDIA_PLAYER_ENTITY,
    DOMAIN,
    HOME_SCREEN_LABEL,
    HOME_SCREEN_TARGET,
    LEGACY_CUSTOM_SOURCE_NAME,
    LEGACY_CUSTOM_SOURCE_TARGET,
    NATIVE_SOURCE_PREFIX,
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the Apple TV Plus media player."""
    async_add_entities([AppleTVPlusMediaPlayer(hass, entry)])


class AppleTVPlusMediaPlayer(MediaPlayerEntity):
    """Apple TV Plus media player — a facade over the native Apple TV integration."""

    def __init__(self, hass: HomeAssistant, entry: ConfigEntry) -> None:
        self.hass = hass
        self.entry = entry
        self._media_player_entity = entry.data[CONF_MEDIA_PLAYER_ENTITY]
        self._device_id = entry.data.get(CONF_DEVICE_ID)

        self._attr_name = "Apple TV Plus"
        self._attr_unique_id = f"{entry.entry_id}_media_player"
        self._attr_device_class = "tv"
        self._attr_supported_features = (
            MediaPlayerEntityFeature.TURN_ON
            | MediaPlayerEntityFeature.TURN_OFF
            | MediaPlayerEntityFeature.SELECT_SOURCE
            | MediaPlayerEntityFeature.PLAY
            | MediaPlayerEntityFeature.PAUSE
        )
        self._attr_source = None

        self._attr_device_info = {
            "identifiers": {(DOMAIN, entry.entry_id)},
            "name": "Apple TV Plus",
            "manufacturer": "Apple TV Plus",
            "model": "Enhanced Apple TV Controller",
            "sw_version": "0.0.6",
        }

    def _get_custom_sources(self) -> list[dict]:
        """Return configured custom sources, migrating a v0.0.3 single source."""
        sources = self.entry.options.get(CONF_CUSTOM_SOURCES)
        if sources is not None:
            return sources

        legacy_name = (
            self.entry.options.get(LEGACY_CUSTOM_SOURCE_NAME)
            or self.entry.data.get(LEGACY_CUSTOM_SOURCE_NAME, "")
        ).strip()
        legacy_target = (
            self.entry.options.get(LEGACY_CUSTOM_SOURCE_TARGET)
            or self.entry.data.get(LEGACY_CUSTOM_SOURCE_TARGET, "")
        ).strip()

        if legacy_name and legacy_target:
            return [{"name": legacy_name, "target": legacy_target}]
        return []

    def _get_installed_apps(self) -> dict[str, str]:
        """Return apps the native Apple TV integration reports as actually installed.

        Reads the native entity's own `source_list` state attribute — the same
        data its own app-launching already relies on — instead of opening a
        second pyatv connection to ask the Apple TV directly. A second direct
        connection risks conflicting with the native integration's existing
        one to the same device, so this stays a read of state HA already has.

        Returns {} if that attribute isn't present (older HA/pyatv, or this
        Apple TV's pairing doesn't support app listing) so callers can fall
        back to the static APP_IDS list.
        """
        state = self.hass.states.get(self._media_player_entity)
        if state is None:
            return {}

        native_sources = state.attributes.get("source_list") or []
        return {
            name: f"{NATIVE_SOURCE_PREFIX}{name}"
            for name in native_sources
            if isinstance(name, str) and name.strip()
        }

    def _get_sources(self):
        """Return sources in display order: favorites, apps, other custom sources, Home Screen.

        Favorites are shown with a star prefix and sorted to the top so they're
        immediately visible in the source list — including in Apple Home's TV
        input picker, which reads this same list. The star is display-only;
        the source's stored name stays plain so editing it isn't affected.

        For apps: if the native Apple TV integration currently reports a live
        installed-apps list, that's used (so only apps actually on the Apple
        TV show up); otherwise this falls back to the static APP_IDS list.
        """
        favorites: dict[str, str] = {}
        others: dict[str, str] = {}

        for custom in self._get_custom_sources():
            name = custom.get("name", "").strip()
            target = custom.get("target", "").strip()
            if not name or not target:
                continue
            if custom.get("favorite"):
                favorites[f"★ {name}"] = target
            else:
                others[name] = target

        sources: dict[str, str] = {}
        sources.update(favorites)
        sources.update(self._get_installed_apps() or APP_IDS)
        sources.update(others)
        sources[HOME_SCREEN_LABEL] = HOME_SCREEN_TARGET
        return sources

    @property
    def state(self):
        """Return Apple TV state."""
        state = self.hass.states.get(self._media_player_entity)
        if state is None or state.state in ["off", "unavailable", "unknown"]:
            return MediaPlayerState.OFF
        return MediaPlayerState.IDLE

    @property
    def source(self):
        """Return selected source."""
        return self._attr_source

    @property
    def source_list(self):
        """Return the current source list (recomputed so option edits show up)."""
        return list(self._get_sources().keys())

    async def async_turn_on(self) -> None:
        """Turn Apple TV on."""
        await self.hass.services.async_call(
            "media_player",
            "turn_on",
            {"entity_id": self._media_player_entity},
            blocking=True,
        )
        self.async_write_ha_state()

    async def async_turn_off(self) -> None:
        """Turn Apple TV off using fast sleep."""
        await self.hass.services.async_call(
            "remote",
            "send_command",
            {
                "device_id": self._device_id,
                "command": "suspend",
            },
            blocking=True,
        )
        await asyncio.sleep(5)
        self.async_write_ha_state()

    async def async_select_source(self, source: str) -> None:
        """Launch selected app or deep link."""
        sources = self._get_sources()

        if source not in sources:
            return

        target = sources[source]
        self._attr_source = source

        if target == HOME_SCREEN_TARGET:
            await self.hass.services.async_call(
                "remote",
                "send_command",
                {
                    "device_id": self._device_id,
                    "command": "home",
                },
                blocking=True,
            )
            self.async_write_ha_state()
            return

        if target.startswith(NATIVE_SOURCE_PREFIX):
            # A live, actually-installed app from the native integration's own
            # list — let IT launch it via its existing connection, rather than
            # us guessing a bundle ID or opening a second pyatv connection.
            native_source_name = target[len(NATIVE_SOURCE_PREFIX):]
            await self.hass.services.async_call(
                "media_player",
                "select_source",
                {
                    "entity_id": self._media_player_entity,
                    "source": native_source_name,
                },
                blocking=True,
            )
            self.async_write_ha_state()
            return

        media_type = "app"

        if "://" in target:
            media_type = "url"

        await self.hass.services.async_call(
            "media_player",
            "play_media",
            {
                "entity_id": self._media_player_entity,
                "media_content_id": target,
                "media_content_type": media_type,
            },
            blocking=True,
        )

        self.async_write_ha_state()

    async def async_media_play(self) -> None:
        """Play media."""
        await self.hass.services.async_call(
            "media_player",
            "media_play",
            {"entity_id": self._media_player_entity},
            blocking=True,
        )

    async def async_media_pause(self) -> None:
        """Pause media."""
        await self.hass.services.async_call(
            "media_player",
            "media_pause",
            {"entity_id": self._media_player_entity},
            blocking=True,
        )
