import unittest

from app.resources.rule_parser import LIGHT_RULES_MAP, apply_light_rule, apply_temperature_rule, check_l_rule, check_t_rule, eval_deviation, is_daytime, is_deviated, DELTA

class ServiceTests(unittest.TestCase):
    
    def test01_lower_value_returns_lower(self):
        self.assertEqual(is_deviated(2, 3, 4), "lower")
        
    def test02_middle_value_returns_none(self):
        self.assertEqual(is_deviated(4, 3, 5), None)
        
    def test03_higher_value_returns_higher(self):
        self.assertEqual(is_deviated(5, 3, 4), "higher")
        
    def test04_good_temperature_return_none(self):
        if is_daytime():
            self.assertEqual(check_t_rule(18, 10, 18), None)
        else:
            self.assertEqual(check_t_rule(10, 10, 18), None)
        
    def test05_higher_temperature_return_higher(self):
        if is_daytime():
            self.assertEqual(check_t_rule(18+1+DELTA, 10, 18), "higher")
        else:
            self.assertEqual(check_t_rule(10+1+DELTA, 10, 18), "higher")

    def test06_lower_temperature_return_lower(self):
        if is_daytime():
            self.assertEqual(check_t_rule(18-1-DELTA, 10, 18), "lower")
        else:
            self.assertEqual(check_t_rule(10-1-DELTA, 10, 18), "lower")
    
    def test07_good_light_return_none(self):
        self.assertEqual(check_l_rule(300, 200, 500), None)
        
    def test08_higher_light_return_higher(self):
        self.assertEqual(check_l_rule(600, 200, 500), "higher")

    def test09_lower_light_at_day_return_lower_but_at_night_return_none(self):
        self.assertEqual(check_l_rule(10, 200, 500), "lower" if is_daytime() else None)
        
    def test10_apply_temperature_rule(self):
        if not is_daytime():
            self.assertEqual(apply_temperature_rule(1, 10), None)
            self.assertEqual(apply_temperature_rule(2, 18), None)
            self.assertEqual(apply_temperature_rule(3, 21), None)
            
            self.assertEqual(apply_temperature_rule(1, 10-1-DELTA), "lower")
            self.assertEqual(apply_temperature_rule(2, 18-1-DELTA), "lower")
            self.assertEqual(apply_temperature_rule(3, 21-1-DELTA), "lower")
            
            self.assertEqual(apply_temperature_rule(1, 10+1+DELTA), "higher")
            self.assertEqual(apply_temperature_rule(2, 18+1+DELTA), "higher")
            self.assertEqual(apply_temperature_rule(3, 21+1+DELTA), "higher")
        else:
            self.assertEqual(apply_temperature_rule(1, 18), None)
            self.assertEqual(apply_temperature_rule(2, 24), None)
            self.assertEqual(apply_temperature_rule(3, 30), None)
            
            self.assertEqual(apply_temperature_rule(1, 18-1-DELTA), "lower")
            self.assertEqual(apply_temperature_rule(2, 24-1-DELTA), "lower")
            self.assertEqual(apply_temperature_rule(3, 30-1-DELTA), "lower")
            
            self.assertEqual(apply_temperature_rule(1, 18+1+DELTA), "higher")
            self.assertEqual(apply_temperature_rule(2, 24+1+DELTA), "higher")
            self.assertEqual(apply_temperature_rule(3, 30+1+DELTA), "higher")
        
    def test11_apply_light_rule(self):
        self.assertEqual(apply_light_rule(4, 52), None)
        self.assertEqual(apply_light_rule(3, 120), None)
        self.assertEqual(apply_light_rule(2, 410), None)
        self.assertEqual(apply_light_rule(1, 3300), None)
        
        self.assertEqual(apply_light_rule(4, 10), "lower" if is_daytime() else None)
        self.assertEqual(apply_light_rule(3, 50), "lower" if is_daytime() else None)
        self.assertEqual(apply_light_rule(2, 100), "lower" if is_daytime() else None)
        self.assertEqual(apply_light_rule(1, 250), "lower" if is_daytime() else None)
        
        self.assertEqual(apply_light_rule(4, 100), "higher")
        self.assertEqual(apply_light_rule(3, 300), "higher")
        self.assertEqual(apply_light_rule(2, 2000), "higher")
        self.assertEqual(apply_light_rule(1, 11000), "higher")
    
    def test_eval_multiple_light_rules(self):
        
        self.assertEqual(eval_deviation([2, 3, 4], lambda x: apply_light_rule(x, 10)), "lower" if is_daytime() else None)
        self.assertEqual(eval_deviation([2, 3, 4], lambda x: apply_light_rule(x, LIGHT_RULES_MAP[4][1][0]-1)), "lower" if is_daytime() else None)
        self.assertEqual(eval_deviation([2, 3, 4], lambda x: apply_light_rule(x, LIGHT_RULES_MAP[4][1][0])), None)
        self.assertEqual(eval_deviation([2, 3, 4], lambda x: apply_light_rule(x, LIGHT_RULES_MAP[4][1][0]+1)), None)
        self.assertEqual(eval_deviation([2, 3, 4], lambda x: apply_light_rule(x, 50)), None)
        self.assertEqual(eval_deviation([2, 3, 4], lambda x: apply_light_rule(x, LIGHT_RULES_MAP[4][1][1]-1)), None)
        self.assertEqual(eval_deviation([2, 3, 4], lambda x: apply_light_rule(x, LIGHT_RULES_MAP[4][1][1])), None)
        self.assertEqual(eval_deviation([2, 3, 4], lambda x: apply_light_rule(x, LIGHT_RULES_MAP[4][1][1]+1)), None)
        
        self.assertEqual(eval_deviation([2, 3, 4], lambda x: apply_light_rule(x, LIGHT_RULES_MAP[3][1][0]-1)), None)
        self.assertEqual(eval_deviation([2, 3, 4], lambda x: apply_light_rule(x, LIGHT_RULES_MAP[3][1][0])), None)
        self.assertEqual(eval_deviation([2, 3, 4], lambda x: apply_light_rule(x, LIGHT_RULES_MAP[3][1][0]+1)), None)
        self.assertEqual(eval_deviation([2, 3, 4], lambda x: apply_light_rule(x, 125)), None)
        self.assertEqual(eval_deviation([2, 3, 4], lambda x: apply_light_rule(x, LIGHT_RULES_MAP[3][1][1]-1)), None)
        self.assertEqual(eval_deviation([2, 3, 4], lambda x: apply_light_rule(x, LIGHT_RULES_MAP[3][1][1])), None)
        self.assertEqual(eval_deviation([2, 3, 4], lambda x: apply_light_rule(x, LIGHT_RULES_MAP[3][1][1]+1)), None)
        
        self.assertEqual(eval_deviation([2, 3, 4], lambda x: apply_light_rule(x, LIGHT_RULES_MAP[2][1][0]-1)), None)
        self.assertEqual(eval_deviation([2, 3, 4], lambda x: apply_light_rule(x, LIGHT_RULES_MAP[2][1][0])), None)
        self.assertEqual(eval_deviation([2, 3, 4], lambda x: apply_light_rule(x, LIGHT_RULES_MAP[2][1][0]+1)), None)
        self.assertEqual(eval_deviation([2, 3, 4], lambda x: apply_light_rule(x, 300)), None)
        self.assertEqual(eval_deviation([2, 3, 4], lambda x: apply_light_rule(x, LIGHT_RULES_MAP[2][1][1]-1)), None)
        self.assertEqual(eval_deviation([2, 3, 4], lambda x: apply_light_rule(x, LIGHT_RULES_MAP[2][1][1])), None)
        self.assertEqual(eval_deviation([2, 3, 4], lambda x: apply_light_rule(x, LIGHT_RULES_MAP[2][1][1]+1)), "higher")
        self.assertEqual(eval_deviation([2, 3, 4], lambda x: apply_light_rule(x, 700)), "higher")
        
        