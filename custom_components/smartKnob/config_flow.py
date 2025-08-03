import voluptuous as vol
from homeassistant import config_entries
from homeassistant.helpers import entity_registry

class SmartKnobConfigFlow(config_entries.ConfigFlow, domain="smartknob"):
    async def async_step_user(self, user_input=None):
        if user_input is not None:
            return self.async_create_entry(title="SmartKnob", data=user_input)

        entities = self._get_light_and_media_entities()
        schema = vol.Schema({
            vol.Required("light_entity"): vol.In(entities["light"]),
            vol.Required("media_player_entity"): vol.In(entities["media_player"]),
        })

        return self.async_show_form(step_id="user", data_schema=schema)

    def _get_light_and_media_entities(self):
        registry = entity_registry.async_get(self.hass)
        light_entities = [e.entity_id for e in registry.entities.values() if e.domain == "light"]
        media_entities = [e.entity_id for e in registry.entities.values() if e.domain == "media_player"]
        return {
            "light": light_entities,
            "media_player": media_entities
        }
