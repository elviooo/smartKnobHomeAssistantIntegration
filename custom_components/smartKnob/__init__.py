import logging
from homeassistant.helpers import mqtt

_LOGGER = logging.getLogger(__name__)
DOMAIN = "smartknob"

async def async_setup_entry(hass, entry):
    if DOMAIN not in hass.data:
        hass.data[DOMAIN] = {}

    data = {
        "identifier": entry.data["identifier"],
        "light_entity": entry.data["light_entity"],
        "media_player_entity": entry.data["media_player_entity"],
    }

    hass.data[DOMAIN][entry.entry_id] = data
    _LOGGER.info(f"[SmartKnob] Setup für {data['identifier']} erfolgreich.")

    async def mqtt_message_received(msg):
        identifier = msg.topic.split("/")[1]  # smartknob/<identifier>/...
        topic_type = msg.topic.split("/")[2]
        payload = msg.payload.decode()

        _LOGGER.debug(f"MQTT empfangen: {msg.topic} → {payload}")

        for knob in hass.data[DOMAIN].values():
            if knob["identifier"] == identifier:
                if topic_type == "light":
                    await hass.services.async_call("light", "turn_on", {
                        "entity_id": knob["light_entity"],
                        "brightness": int(payload)
                    })
                elif topic_type == "volume":
                    await hass.services.async_call("media_player", "volume_set", {
                        "entity_id": knob["media_player_entity"],
                        "volume_level": int(payload) / 100.0
                    })

    await mqtt.async_subscribe(hass, "smartknob/+/light", mqtt_message_received)
    await mqtt.async_subscribe(hass, "smartknob/+/volume", mqtt_message_received)

    return True
