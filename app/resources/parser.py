import pandas as pd
from datetime import datetime

file_path = 'resources/plants_dataset.csv'
df = pd.read_csv(file_path)
DELTA = 5


def is_in_range(value, min, max):
    return value >= min and value <= max


def check_t_rule(register, day_value, night_value):
    if not is_daytime():
        return not is_in_range(register, day_value-DELTA, day_value+DELTA)
    else:
        return not is_in_range(register, night_value-DELTA, night_value+DELTA)


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
    1: (is_in_range, (200, 350)),
    2: (is_in_range, (200, 350)),
    3: (is_in_range, (75, 200)),
    4: (is_in_range, (25, 75)),
}


def parse_values(string):
    values = string.split('-')
    return [int(value) for value in values]


# asumimos register: nombre_planta, humedad, luz, temperatura
def apply_rules(register, plant_name):
    plant_data = df[df['Botanical_Name'] == plant_name]
    h_value = plant_data['H'].values[0]
    l_value = plant_data['L'].values[0]
    t_value = plant_data['T'].values[0]
    print("h_value", h_value)
    print("l_value", l_value)
    print("t_value", t_value)

    parameters = []

    t_values = parse_values(t_value)
    h_values = parse_values(h_value)
    l_values = parse_values(l_value)

    print("h_values", h_values)
    print("l_values", l_values)
    print("t_values", t_values)

    for t_value in t_values:
        if apply_temperature_rule(t_value, register.temperature):
            parameters.append('temperature')
            break

    for l_value in l_values:
        if apply_light_rule(l_value, register.light):
            parameters.append('light')
            break

    for h_value in h_values:
        if apply_humidity_rule(h_value, register.humidity):
            parameters.append('humidity')
            break

    return parameters


def apply_temperature_rule(rule, register):
    rule_function, rule_values = TEMP_RULES_MAP.get(rule, None)
    if rule_function:
        return rule_function(register, *rule_values)


def apply_light_rule(rule, register):
    rule_function, rule_values = LIGHT_RULES_MAP.get(rule, None)
    if rule_function:
        return not rule_function(register, *rule_values)


def apply_humidity_rule(rule, register):
    rule_function, rule_values = HUMIDITY_RULES_MAP.get(rule, None)
    if rule_function:
        return not rule_function(register, *rule_values)


def is_daytime():
    now = datetime.now()
    current_hour = now.hour
    daytime_start_hour = 6
    daytime_end_hour = 18
    return daytime_start_hour <= current_hour <= daytime_end_hour
