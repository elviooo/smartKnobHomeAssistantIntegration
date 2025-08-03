import voluptuous as vol
from homeassistant import config_entries
from homeassistant.helpers import entity_registry

DOMAIN = "smartknob"

class SmartKnobConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        registry = entity_registry.async_get(self.hass)

        if user_input is not None:
            identifier = user_input["identifier"]
            # Prüfen ob schon verwendet (optional)
            for entry in self._async_current_entries():
                if entry.data.get("identifier") == identifier:
                    return self.async_abort(reason="identifier_exists")

            return self.async_create_entry(title=user_input["name"], data=user_input)

        light_entities = [e.entity_id for e in registry.entities.values() if e.domain == "light"]
        media_entities = [e.entity_id for e in registry.entities.values() if e.domain == "media_player"]

        schema = vol.Schema({
            vol.Required("name"): str,
            vol.Required("identifier"): str,
            vol.Required("light_entity"): vol.In(light_entities),
            vol.Required("media_player_entity"): vol.In(media_entities),
        })

        return self.async_show_form(step_id="user", data_schema=schema)
