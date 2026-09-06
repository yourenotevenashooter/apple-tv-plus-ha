"""Config flow for Apple TV Enhanced."""

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback

from .const import DOMAIN


class AppleTVEnhancedConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Apple TV Enhanced."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle the initial setup step."""
        errors = {}

        if user_input is not None:
            await self.async_set_unique_id(
                f"{user_input['media_player_entity']}"
            )
            self._abort_if_unique_id_configured()

            return self.async_create_entry(
                title="Apple TV Enhanced",
                data=user_input,
            )

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required("media_player_entity"): str,
                    vol.Optional("device_id", default=""): str,
                    vol.Optional("custom_source_name", default=""): str,
                    vol.Optional("custom_source_target", default=""): str,
                }
            ),
            errors=errors,
        )

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        """Return the options flow."""
        return AppleTVEnhancedOptionsFlow()


class AppleTVEnhancedOptionsFlow(config_entries.OptionsFlow):
    """Handle Apple TV Enhanced options."""

    async def async_step_init(self, user_input=None):
        """Manage the integration options."""
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema(
                {
                    vol.Optional("custom_source_name", default=""): str,
                    vol.Optional("custom_source_target", default=""): str,
                }
            ),
        )
