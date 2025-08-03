import logging

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

    async def mqtt_message_received(msg):
        identifier = msg.topic.split("/")[1]  # smartknob/<identifier>/...
        topic_type = msg.topic.split("/")[2]

        for knob in hass.data[DOMAIN].values():
            if knob["identifier"] == identifier:
                if topic_type == "light":
                    await hass.services.async_call("light", "turn_on", {
                        "entity_id": knob["light_entity"],
                        "brightness": int(msg.payload)
                    })
                elif topic_type == "volume":
                    await hass.services.async_call("media_player", "volume_set", {
                        "entity_id": knob["media_player_entity"],
                        "volume_level": int(msg.payload) / 100.0
                    })

    await hass.components.mqtt.async_subscribe("smartknob/+/light", mqtt_message_received)
    await hass.components.mqtt.async_subscribe("smartknob/+/volume", mqtt_message_received)

    return True
