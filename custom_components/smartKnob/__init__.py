from homeassistant.core import HomeAssistant

async def async_setup_entry(hass: HomeAssistant, entry):
    hass.data["smartknob"] = {
        "light_entity": entry.data["light_entity"],
        "media_player_entity": entry.data["media_player_entity"],
    }
    return True
