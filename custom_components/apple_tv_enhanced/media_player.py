"""Media player platform for Apple TV Enhanced."""

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
from .const import DOMAIN


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Apple TV Enhanced media player."""
    async_add_entities([AppleTVEnhancedMediaPlayer(hass, entry)])


class AppleTVEnhancedMediaPlayer(MediaPlayerEntity):
    """Enhanced Apple TV media player."""

    def __init__(self, hass: HomeAssistant, entry: ConfigEntry) -> None:
        self.hass = hass
        self.entry = entry
        self._media_player_entity = entry.data["media_player_entity"]
        self._device_id = entry.data.get("device_id")

        self._attr_name = "Apple TV Enhanced"
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
        self._attr_source_list = list(self._get_sources().keys())

        self._attr_device_info = {
            "identifiers": {(DOMAIN, entry.entry_id)},
            "name": "Apple TV Enhanced",
            "manufacturer": "Nappyty11",
            "model": "Enhanced Apple TV Controller",
            "sw_version": "0.0.3",
        }

    def _get_sources(self):
        """Return built-in and custom sources."""
        sources = dict(APP_IDS)

        name = self.entry.data.get("custom_source_name", "").strip()
        target = self.entry.data.get("custom_source_target", "").strip()

        if name and target:
            sources[name] = target

        sources["Home Screen"] = "__HOME__"
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
        """Return source list."""
        return self._attr_source_list

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

        if target == "__HOME__":
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
