import json
import time
import logging
from os import environ
from datetime import datetime
from schemas.measurement import MeasurementReadingSchema
from dotenv import load_dotenv


logger = logging.getLogger("rabbitmq_consumer")


class NotificationRestriction:
    def is_satisfied(self, measurement, last_measurement, time_difference):
        raise NotImplementedError("Subclasses must implement this method")


class MinTimeBetweenNotificationsRestriction(NotificationRestriction):
    def __init__(self, restriction):
        self.restriction = restriction

    def is_satisfied(self, measurement, last_measurement, time_difference):
        return time_difference >= self.restriction

    def __str__(self):
        return "min_time_between_notifications"


class PercentageDifferenceTriggerRestriction(NotificationRestriction):
    def __init__(self, restriction):
        self.restriction = restriction

    def is_satisfied(self, measurement, last_measurement, time_difference):
        significant_change = 100 * abs((
            measurement - last_measurement) / last_measurement)
        return significant_change >= self.restriction

    def __str__(self):
        return "percentage_difference_trigger"


class TimeRangeRestriction(NotificationRestriction):
    def __init__(self, start_hour, end_hour):
        self.start_hour = start_hour
        self.end_hour = end_hour

    def is_satisfied(self, measurement, last_measurement, time_difference):
        current_hour = datetime.now().hour
        return self.start_hour <= current_hour < self.end_hour

    def __str__(self):
        return "time_range"


class RestrictionFactory:
    def create_restrictions(self, restriction_data):
        restrictions = []

        if "percentage_difference_trigger" in restriction_data:
            restrictions.append(PercentageDifferenceTriggerRestriction(
                restriction_data["percentage_difference_trigger"])
            )

        if "min_time_between_notifications" in restriction_data:
            restrictions.append(MinTimeBetweenNotificationsRestriction(
                restriction_data["min_time_between_notifications"])
            )

        if "time_range" in restriction_data:
            restrictions.append(
                TimeRangeRestriction(*restriction_data["time_range"])
            )

        return restrictions


class NotificationChecker:
    def __init__(self):
        self.factory = RestrictionFactory()

        default_restrictions_config = {
            "temperature": {
                "percentage_difference_trigger": 5,
                "min_time_between_notifications": 60 * 5,
            },
            "light": {
                "percentage_difference_trigger": 5,
                "min_time_between_notifications": 60 * 15,
                # 10:00 - 17:59
                "time_range": [10, 18]
            },
            "humidity": {
                "percentage_difference_trigger": 5,
                "min_time_between_notifications": 60 * 5,
            },
            "watering": {
                "percentage_difference_trigger": 5,
                "min_time_between_notifications": 60 * 5,
            }
        }
        load_dotenv()
        restrictions_config = environ.get("NOTIFICATION_RESTRICTIONS")
        if restrictions_config:
            logger.debug("Using restrictions from environment")
            restrictions_config = json.loads(restrictions_config)
        else:
            restrictions_config = default_restrictions_config

        self.restrictions_config = restrictions_config
        self.type_restrictions = {
            key: self.factory.create_restrictions(value)
            for key, value in restrictions_config.items()
        }

    def satisfies_restrictions(self,
                               type_name,
                               measurement,
                               last_measurement,
                               info_last_notification):
        restrictions = self.type_restrictions.get(type_name)
        if not restrictions:
            return True

        time_now = int(time.time())

        try:
            last_time_of_type = info_last_notification[
                                    f"{type_name}_sent_time"
                                ]
        except Exception:
            logger.debug(f"Never notified a measurement of {type_name}. " +
                         "Ready to notify!")
            return True

        if not last_time_of_type:
            return True

        time_difference = time_now - last_time_of_type
        return check_all_restrictions(type_name,
                                      measurement,
                                      last_measurement,
                                      time_difference,
                                      restrictions)


def check_all_restrictions(type_name,
                           measurement,
                           last_measurement,
                           time_difference,
                           restrictions):
    for restriction in restrictions:
        if restriction.is_satisfied(measurement,
                                    last_measurement,
                                    time_difference):
            logger.debug(f"The restriction '{format(restriction)}' for" +
                         "the attribute '{type_name}' was fulfilled. " +
                         "Ready to notify!")
        else:
            logger.debug(f"The restriction '{format(restriction)}' for" +
                         "the attribute '{type_name}' was not fulfilled. " +
                         "Not ready to notify!")
            return False
    return True


notification_restrictions = NotificationChecker()


def is_ready_to_notify(last_notifications,
                       id_plant,
                       measurement:
                       MeasurementReadingSchema):
    last_notification, info_last_notification = last_notifications.\
        get(id_plant, (None, None))
    if last_notification is None or info_last_notification is None:
        logger.info("No previous notification has been found. " +
                    "Ready to notify!")
        return True

    if notification_restrictions.satisfies_restrictions(
        "temperature",
        measurement.temperature,
        last_notification.temperature,
        info_last_notification
    ):
        return True

    if notification_restrictions.satisfies_restrictions(
        "light",
        measurement.light,
        last_notification.light,
        info_last_notification
    ):
        return True

    if (measurement.humidity and
        last_notification.humidity and
        notification_restrictions.satisfies_restrictions(
            "humidity",
            measurement.humidity,
            last_notification.humidity,
            info_last_notification)):
        return True

    if notification_restrictions.satisfies_restrictions(
        "watering",
        measurement.watering,
        last_notification.watering,
        info_last_notification
    ):
        return True

    logger.info("No field with significant change has been found " +
                "or restrictions were not satisfied. Not ready to notify!")
    return False


def update_last_notifications(last_notifications,
                              device_plant,
                              measurement,
                              error):
    sent_time = int(time.time())
    error_dict = error.parameters.dict()

    if last_notifications.get(device_plant.id_plant) is not None:
        actual_time = last_notifications[device_plant.id_plant][1]
        itms = error_dict.items()
        for param, desviated in itms:
            if desviated is not None:
                actual_time[str(param) + "_sent_time"] = sent_time
        last_notifications[device_plant.id_plant] = (measurement,
                                                     actual_time)
    else:
        init_time_info = {
                            "temperature_sent_time": sent_time,
                            "humidity_sent_time": sent_time,
                            "light_sent_time": sent_time,
                            "watering_sent_time": sent_time
                         }
        last_notifications[device_plant.id_plant] = (measurement,
                                                     init_time_info)
