import json
import logging
from datetime import datetime, timedelta, timezone
from schemas.measurement import MeasurementReadingSchema

ARG_TZ = timezone(timedelta(hours=-3), name="America/Argentina/Buenos_Aires")
LUX_TO_FTC = 10.764
logger = logging.getLogger("rabbitmq_consumer")


def convert_lux_to_ftc(lux):
    return round(lux / LUX_TO_FTC, 2)


def get_formatted_time(time_stamp):
    if isinstance(time_stamp, int):
        formatted_time = datetime.fromtimestamp(time_stamp,
                                                tz=ARG_TZ).isoformat()
    else:
        formatted_time = time_stamp

    return formatted_time


def parse_light(item_json):
    if item_json["light"] is not None:
        item_json["light"] = convert_lux_to_ftc(item_json["light"])


def generate_item_json(decoded_json, formatted_time):
    return {
        "time_stamp": formatted_time,
        "id_device": decoded_json.get("id_device", None),
        "temperature": decoded_json.get("temperature", None),
        "light": decoded_json.get("light", None),
        "watering": decoded_json.get("watering", None),

        # nuestro sensor no mide humedad del ambiente!
        "humidity": decoded_json.get("humidity", None),
    }


def parse_message(last_measurements, msg):
    decoded = msg.payload.decode()
    logger.info(f"Received message: {decoded} on topic {msg.topic}")
    decoded_json = json.loads(decoded)

    if decoded_json.get("id_device", "").startswith("sensor_1"):
        if decoded_json.get("humidity"):
            decoded_json["watering"] = decoded_json["humidity"]
            del decoded_json["humidity"]
            logger.warn("HOTFIX: humidity field renamed to watering")

    if not decoded_json.get("time_stamp"):
        logger.error("Message discarded: no time_stamp field!")
        return None, None

    formatted_time = get_formatted_time(decoded_json.get("time_stamp"))

    item_json = generate_item_json(decoded_json, formatted_time)

    parse_light(item_json)

    save_measurement_if_not_exist(last_measurements, item_json)

    update_empty_field_in_last_measurement(last_measurements, item_json)

    update_fields_in_measurement(last_measurements, item_json)

    item = MeasurementReadingSchema(**item_json)

    if not item.is_partial():
        return item, item_json

    return None, None


def update_fields_in_measurement(last_measurements, item_json):
    for key, value in item_json.items():
        if value is None:
            item_json[key] = last_measurements[item_json["id_device"]][key]
        else:
            last_measurements[item_json["id_device"]][key] = value


def update_empty_field_in_last_measurement(last_measurements, item_json):
    for k, v in last_measurements[item_json["id_device"]].items():
        if not v and item_json[k]:
            last_measurements[item_json["id_device"]][k] = item_json[k]


def save_measurement_if_not_exist(last_measurements, item_json):
    if last_measurements.get(item_json["id_device"], None) is None:
        last_measurements[item_json["id_device"]] = item_json
