from typing import Literal, Optional
import pandas as pd
from datetime import datetime


from schemas.measurement import DeviatedParametersSchema, Measurement

file_path = 'resources/plants_dataset.csv'
df = pd.read_csv(file_path)
DELTA = 5


def is_in_range(value, min, max):
    return min <= value <= max


def is_deviated(value, min, max) -> Optional[Literal["lower", "higher"]]:
    if value < min:
        return "lower"

    if value > max:
        return "higher"

    return None


def check_t_rule(
        register,
        night_value,
        day_value) -> Optional[Literal["lower", "higher"]]:
    if is_daytime():
        return is_deviated(register, day_value - DELTA, day_value + DELTA)
    else:
        return is_deviated(register, night_value - DELTA, night_value + DELTA)


def check_l_rule(register, min, max) -> Optional[Literal["lower", "higher"]]:
    if not is_daytime():
        return is_deviated(register, 0, max)

    return is_deviated(register, min, max)


TEMP_RULES_MAP = {
    1: (check_t_rule, (10, 18)),
    2: (check_t_rule, (18, 24)),
    3: (check_t_rule, (21, 30)),
}

HUMIDITY_RULES_MAP = {
    1: (is_deviated, (50, 100)),
    2: (is_deviated, (25, 50)),
    3: (is_deviated, (5, 25)),
}

# FOOT CANDLE (ftc)
LIGHT_RULES_MAP = {
    1: (check_l_rule, (500, 10000)),
    2: (check_l_rule, (200, 500)),
    3: (check_l_rule, (75, 200)),
    4: (check_l_rule, (25, 75)),
}

WATERING_RULES_MAP = {
    1: (is_deviated, (70, 100)),
    2: (is_deviated, (40, 70)),
    3: (is_deviated, (10, 40)),
}


def parse_values(string):
    values = string.split('-')
    return [int(value) for value in values]


def eval_deviation(
        values: list[int],
        apply_rule_fn) -> Optional[Literal["lower", "higher"]]:

    results = list(map(lambda v: apply_rule_fn(v), values))
    return None if any(map(lambda v: v is None, results)) else results[0]


def apply_rules(
        register: Measurement,
        plant_name: str) -> DeviatedParametersSchema:
    plant_data = df[df['Botanical_Name'] == plant_name]
    h_value = plant_data['H'].values[0]
    l_value = plant_data['L'].values[0]
    t_value = plant_data['T'].values[0]
    w_value = plant_data['W'].values[0]

    t_values = parse_values(t_value)
    h_values = parse_values(h_value)
    l_values = parse_values(l_value)
    w_values = parse_values(w_value)

    return DeviatedParametersSchema(
        temperature=eval_deviation(
            t_values,
            lambda x: apply_temperature_rule(x, register.temperature)),
        humidity=eval_deviation(
            h_values,
            lambda x: apply_humidity_rule(x, register.humidity))
        if register.humidity else None,
        light=eval_deviation(
            l_values,
            lambda x: apply_light_rule(x, register.light)),
        watering=eval_deviation(
            w_values,
            lambda x: apply_watering_rule(x, register.watering)),
    )


def apply_temperature_rule(
        rule,
        register) -> Optional[Literal["lower", "higher"]]:
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
    return 6 <= now.hour <= 18
