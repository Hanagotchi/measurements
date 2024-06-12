from datetime import datetime, timedelta, timezone
import json
from schemas.measurement import MeasurementReadingSchema
import logging


ARG_DELTA_TZ = timedelta(hours=-3)
LUX_TO_FTC = 10.764
logger = logging.getLogger("rabbitmq_consumer")


def convert_lux_to_ftc(lux):
    return round(lux / LUX_TO_FTC, 2)


def get_formatted_time(time_stamp):
    if isinstance(time_stamp, int):
        utc_time = datetime.fromtimestamp(time_stamp, tz=timezone.utc)
        local_time = utc_time + ARG_DELTA_TZ
        formatted_time = local_time.strftime("%Y-%m-%d %H:%M:%S")
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
