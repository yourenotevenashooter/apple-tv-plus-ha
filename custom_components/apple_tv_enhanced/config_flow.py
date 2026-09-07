"""Config and options flow for Apple TV Plus."""

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback
from homeassistant.helpers import selector

from .const import (
    CONF_CUSTOM_SOURCES,
    CONF_DEVICE_ID,
    CONF_MEDIA_PLAYER_ENTITY,
    DOMAIN,
    LEGACY_CUSTOM_SOURCE_NAME,
    LEGACY_CUSTOM_SOURCE_TARGET,
)

RESERVED_SOURCE_NAMES = {"home screen"}


class AppleTVPlusConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle the initial setup of Apple TV Plus.

    Only asks for the two things required to get a working entity.
    Custom sources are managed afterward through the options flow
    (Settings -> Devices & Services -> Apple TV Plus -> Configure),
    not crammed into this first-run form.
    """

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle the initial setup step."""
        errors = {}

        if user_input is not None:
            await self.async_set_unique_id(user_input[CONF_MEDIA_PLAYER_ENTITY])
            self._abort_if_unique_id_configured()

            return self.async_create_entry(
                title="Apple TV Plus",
                data=user_input,
                options={CONF_CUSTOM_SOURCES: []},
            )

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_MEDIA_PLAYER_ENTITY): selector.EntitySelector(
                        selector.EntitySelectorConfig(
                            domain="media_player", integration="apple_tv"
                        )
                    ),
                    vol.Optional(CONF_DEVICE_ID): selector.DeviceSelector(
                        selector.DeviceSelectorConfig(integration="apple_tv")
                    ),
                }
            ),
            errors=errors,
        )

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        """Return the options flow used to manage custom sources."""
        return AppleTVPlusOptionsFlow()


class AppleTVPlusOptionsFlow(config_entries.OptionsFlow):
    """Add, edit, and delete custom sources without reinstalling.

    HA attaches `self.config_entry` automatically once this flow starts,
    so this class deliberately has no __init__ that sets it manually
    (that pattern is deprecated on current Home Assistant core).
    """

    _sources: list[dict] | None = None
    _edit_index: int | None = None

    def _load_sources(self) -> list[dict]:
        """Load the working copy of sources, migrating v0.0.3's single source once."""
        if self._sources is not None:
            return self._sources

        sources = self.config_entry.options.get(CONF_CUSTOM_SOURCES)
        if sources is None:
            legacy_name = (
                self.config_entry.options.get(LEGACY_CUSTOM_SOURCE_NAME)
                or self.config_entry.data.get(LEGACY_CUSTOM_SOURCE_NAME, "")
            ).strip()
            legacy_target = (
                self.config_entry.options.get(LEGACY_CUSTOM_SOURCE_TARGET)
                or self.config_entry.data.get(LEGACY_CUSTOM_SOURCE_TARGET, "")
            ).strip()
            sources = (
                [{"name": legacy_name, "target": legacy_target}]
                if legacy_name and legacy_target
                else []
            )

        self._sources = [dict(s) for s in sources]
        return self._sources

    async def async_step_init(self, user_input=None):
        """Show the add/edit/remove/done menu."""
        sources = self._load_sources()

        menu_options = ["add_source"]
        if sources:
            menu_options += ["edit_source", "remove_source"]
        menu_options.append("done")

        return self.async_show_menu(step_id="init", menu_options=menu_options)

    async def async_step_add_source(self, user_input=None):
        """Add one custom source (app bundle ID or deep link)."""
        errors = {}

        if user_input is not None:
            name = user_input["name"].strip()
            target = user_input["target"].strip()
            existing = {s["name"].lower() for s in self._sources}

            if not name or not target:
                errors["base"] = "missing_fields"
            elif name.lower() in RESERVED_SOURCE_NAMES:
                errors["name"] = "reserved_name"
            elif name.lower() in existing:
                errors["name"] = "duplicate_name"
            else:
                self._sources.append({"name": name, "target": target})
                return await self.async_step_init()

        return self.async_show_form(
            step_id="add_source",
            data_schema=vol.Schema(
                {
                    vol.Required("name"): str,
                    vol.Required("target"): str,
                }
            ),
            errors=errors,
        )

    async def async_step_edit_source(self, user_input=None):
        """Pick which existing source to edit."""
        names = [s["name"] for s in self._sources]

        if user_input is not None:
            self._edit_index = names.index(user_input["source"])
            return await self.async_step_edit_source_details()

        return self.async_show_form(
            step_id="edit_source",
            data_schema=vol.Schema({vol.Required("source"): vol.In(names)}),
        )

    async def async_step_edit_source_details(self, user_input=None):
        """Edit the chosen source's name/target."""
        errors = {}
        current = self._sources[self._edit_index]

        if user_input is not None:
            name = user_input["name"].strip()
            target = user_input["target"].strip()
            existing = {
                s["name"].lower()
                for i, s in enumerate(self._sources)
                if i != self._edit_index
            }

            if not name or not target:
                errors["base"] = "missing_fields"
            elif name.lower() in RESERVED_SOURCE_NAMES:
                errors["name"] = "reserved_name"
            elif name.lower() in existing:
                errors["name"] = "duplicate_name"
            else:
                self._sources[self._edit_index] = {"name": name, "target": target}
                return await self.async_step_init()

        return self.async_show_form(
            step_id="edit_source_details",
            data_schema=vol.Schema(
                {
                    vol.Required("name", default=current["name"]): str,
                    vol.Required("target", default=current["target"]): str,
                }
            ),
            errors=errors,
        )

    async def async_step_remove_source(self, user_input=None):
        """Pick and remove an existing source."""
        names = [s["name"] for s in self._sources]

        if user_input is not None:
            self._sources = [
                s for s in self._sources if s["name"] != user_input["source"]
            ]
            return await self.async_step_init()

        return self.async_show_form(
            step_id="remove_source",
            data_schema=vol.Schema({vol.Required("source"): vol.In(names)}),
        )

    async def async_step_done(self, user_input=None):
        """Save the current source list and close the options flow."""
        return self.async_create_entry(
            title="", data={CONF_CUSTOM_SOURCES: self._sources}
        )
