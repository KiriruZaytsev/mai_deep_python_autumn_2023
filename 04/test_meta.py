from meta import CustomMeta, CustomClass
from unittest import TestCase

class TestMeta(TestCase):

    inst = CustomClass()

    def test_inst(self):
        self.assertTrue(self.inst.custom_x == 50)
        self.assertTrue(self.inst.custom_val == 99)
        self.assertTrue(self.inst.custom_line() == 100)
        self.assertTrue(str(self.inst) == "Custom_by_metaclass")
        self.assertTrue(hasattr(self.inst, "__init__"))

    def test_errors(self):
        self.assertFalse(hasattr(self.inst, "x"))
        self.assertFalse(hasattr(self.inst, "val"))
        self.assertFalse(hasattr(self.inst, "line"))

    def test_dynamic(self):
        self.inst.dynamic = "zzz"
        self.assertTrue(hasattr(self.inst, "custom_dynamic"))
        self.assertTrue(self.inst.custom_dynamic == "zzz")