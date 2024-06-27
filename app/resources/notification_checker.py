import json
import time
import logging
from os import environ
from datetime import datetime
from resources.message_parser import ARG_TZ
from dotenv import load_dotenv


logger = logging.getLogger("rabbitmq_consumer")


class NotificationRestriction:
    def is_satisfied(self, measurement, last_measurement, time_difference):
        raise NotImplementedError("Subclasses must implement this method")


class MinTimeBetweenNotificationsRestriction(NotificationRestriction):
    def __init__(self, restriction):
        self.restriction = restriction

    def is_satisfied(self, measurement, last_measurement, time_difference):
        logger.debug(f"Time difference: {time_difference}. "
                     f"Actual restriction: {self.restriction}")
        return time_difference >= self.restriction

    def __str__(self):
        return "min_time_between_notifications"


class PercentageDifferenceTriggerRestriction(NotificationRestriction):
    def __init__(self, restriction):
        self.restriction = restriction

    def is_satisfied(self, measurement, last_measurement, time_difference):
        logger.debug(f"Last measurement: {last_measurement} | "
                     f"Actual measurement: {measurement}.")

        if last_measurement == 0:
            return True
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
        logger.debug(f"Current hour: {datetime.now().hour}. "
                     f"Start hour: {self.start_hour}. "
                     f"End hour: {self.end_hour}.")
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
            logger.debug(f"No restrictions found for '{type_name}'... " +
                         "Ready to notify!")
            return True

        time_now = int(time.time())

        try:
            last_time_of_type = info_last_notification[
                                    f"{type_name}_sent_time"
                                ]
        except Exception:
            logger.debug(f"Never notified a measurement of '{type_name}'. " +
                         "Ready to notify!")
            return True

        if not last_time_of_type:
            logger.debug(f"Never notified a measurement of '{type_name}'. " +
                         "Ready to notify!")
            return True

        str_sent_time = datetime.fromtimestamp(last_time_of_type,
                                               tz=ARG_TZ).isoformat()
        str_time_now = datetime.fromtimestamp(time_now,
                                              tz=ARG_TZ).isoformat()
        logger.debug(f"The last '{type_name}' notification has been sent on " +
                     f"'{str_sent_time}'. " +
                     "Actual time is " +
                     f"'{str_time_now}'")

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
                         f" the attribute '{type_name}' was fulfilled. " +
                         "Checking next restriction...")
        else:
            logger.debug(f"The restriction '{format(restriction)}' for" +
                         f" the attribute '{type_name}' was not fulfilled. " +
                         "Not ready to notify!")
            return False

    logger.debug(f"All restrictions for the attribute '{type_name}' " +
                 "were fulfilled. Ready to notify!")
    return True


notification_restrictions = NotificationChecker()


def create_initial_notification_info(deaviated_param):
    sent_time = int(time.time())
    return {
        "temperature_sent_time": sent_time if deaviated_param[
            "temperature"
        ] is not None else None,
        "humidity_sent_time": sent_time if deaviated_param[
            "humidity"
        ] is not None else None,
        "light_sent_time": sent_time if deaviated_param[
            "light"
        ] is not None else None,
        "watering_sent_time": sent_time if deaviated_param[
            "watering"
        ] is not None else None
    }


def check_measurement_restriction(parameter_name,
                                  measurement_value,
                                  last_value,
                                  info_last_notification,
                                  deviated_param):
    return notification_restrictions.satisfies_restrictions(
        parameter_name,
        measurement_value,
        last_value,
        info_last_notification) and deviated_param[parameter_name] is not None


def update_last_notification_info(info_last_notification, results):
    sent_time = int(time.time())
    for parameter_name in results:
        if results[parameter_name]:
            info_last_notification[f"{parameter_name}_sent_time"] = sent_time
    return info_last_notification


def is_ready_to_notify(last_notifications, error, id_plant, measurement):
    last_notification, info_last_notification = last_notifications.\
        get(id_plant, (None, None))

    deviated_param = error.parameters.dict()

    if last_notification is None or info_last_notification is None:
        last_notifications[id_plant] = (measurement,
                                        create_initial_notification_info(
                                            deviated_param
                                        ))
        logger.info("No previous notification has been found. First "
                    f"notification. Ready to notify for plant '{id_plant}'")
        return True

    results = {
        "temperature":
            check_measurement_restriction("temperature",
                                          measurement.temperature,
                                          last_notification.temperature,
                                          info_last_notification,
                                          deviated_param),
        "light": check_measurement_restriction("light",
                                               measurement.light,
                                               last_notification.light,
                                               info_last_notification,
                                               deviated_param),
        "humidity": measurement.humidity is not None and
            last_notification.humidity is not None and
            check_measurement_restriction("humidity",
                                          measurement.humidity,
                                          last_notification.humidity,
                                          info_last_notification,
                                          deviated_param),
        "watering": check_measurement_restriction("watering",
                                                  measurement.watering,
                                                  last_notification.watering,
                                                  info_last_notification,
                                                  deviated_param)
    }

    updated_info = update_last_notification_info(info_last_notification,
                                                 results)
    last_notifications[id_plant] = (measurement, updated_info)

    if any(results.values()):
        logger.info("Any restriction is satisfied AND exists any deviated "
                    f"field. Ready to notify for plant '{id_plant}'")
        last_notifications[id_plant] = (measurement, info_last_notification)
        return True
    else:
        logger.info("Restrictions were not satisfied or there are " +
                    "no deviated field. " +
                    f"Not ready to notify for plant '{id_plant}'")
        return False
