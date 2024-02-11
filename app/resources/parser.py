import pandas as pd
from datetime import datetime

file_path = 'resources/plants_dataset.csv'
df = pd.read_csv(file_path)
DELTA = 5


def is_in_range(value, min, max):
    return min <= value <= max


def check_t_rule(register, night_value, day_value):
    if is_daytime():
        return is_in_range(register, day_value-DELTA, day_value+DELTA)
    else:
        return is_in_range(register, night_value-DELTA, night_value+DELTA)


TEMP_RULES_MAP = {
    1: (check_t_rule, (10, 18)),
    2: (check_t_rule, (18, 24)),
    3: (check_t_rule, (21, 30)),
}

HUMIDITY_RULES_MAP = {
    1: (is_in_range, (50, 100)),
    2: (is_in_range, (25, 50)),
    3: (is_in_range, (5, 25)),
}

LIGHT_RULES_MAP = {
    1: (is_in_range, (350, 500)),
    2: (is_in_range, (200, 350)),
    3: (is_in_range, (75, 200)),
    4: (is_in_range, (25, 75)),
}

WATERING_RULES_MAP = {
    1: (is_in_range, (70, 100)),
    2: (is_in_range, (40, 70)),
    3: (is_in_range, (10, 40)),
}


def parse_values(string):
    values = string.split('-')
    return [int(value) for value in values]


def apply_rules(register, plant_name):
    plant_data = df[df['Botanical_Name'] == plant_name]
    h_value = plant_data['H'].values[0]
    l_value = plant_data['L'].values[0]
    t_value = plant_data['T'].values[0]
    w_value = plant_data['W'].values[0]

    parameters = []

    t_values = parse_values(t_value)
    h_values = parse_values(h_value)
    l_values = parse_values(l_value)
    w_values = parse_values(w_value)

    is_temperature_deviated = all(
        not apply_temperature_rule(t_value, register.temperature)
        for t_value in t_values
    )
    if is_temperature_deviated:
        parameters.append('temperature')

    is_watering_deviated = all(
        not apply_watering_rule(w_value, register.watering)
        for w_value in w_values
    )
    if is_watering_deviated:
        parameters.append('watering')

    is_light_deviated = all(
        not apply_light_rule(l_value, register.light)
        for l_value in l_values
    )
    if is_light_deviated:
        parameters.append('light')

    is_humidity_deviated = all(
        not apply_humidity_rule(h_value, register.humidity)
        for h_value in h_values
    )
    if is_humidity_deviated:
        parameters.append('humidity')

    return parameters


def apply_temperature_rule(rule, register):
    rule_function, rule_values = TEMP_RULES_MAP.get(rule, None)
    return rule_function(register, *rule_values)


def apply_watering_rule(rule, register):
    rule_function, rule_values = WATERING_RULES_MAP.get(rule, None)
    return rule_function(register, *rule_values)


def apply_light_rule(rule, register):
    rule_function, rule_values = LIGHT_RULES_MAP.get(rule, None)
    return rule_function(register, *rule_values)


def apply_humidity_rule(rule, register):
    rule_function, rule_values = HUMIDITY_RULES_MAP.get(rule, None)
    return rule_function(register, *rule_values)


def is_daytime():
    now = datetime.now()
    current_hour = now.hour
    daytime_start_hour = 6
    daytime_end_hour = 18
    return daytime_start_hour <= current_hour <= daytime_end_hour
