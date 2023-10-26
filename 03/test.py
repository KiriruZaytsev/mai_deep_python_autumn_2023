from CustomList import CustomList
import unittest

class TestCustomList(unittest.TestCase):
    custom_list1 = CustomList([1, 2, 5])
    default_list1 = [1, 2]
    custom_list2 = CustomList([0, 3, 5])
    default_list2 = [1, 2, 3, 4]
    custom_list3 = CustomList([1, 2, 3])

    def test_eq(self):
        self.assertTrue(self.custom_list1 == self.custom_list2)
    
    def test_ge(self):
        self.assertTrue(self.custom_list1 >= self.custom_list2)
        self.assertTrue(self.custom_list2 >= self.custom_list1)
        self.assertTrue(self.custom_list1 >= self.custom_list3)
        self.assertFalse(self.custom_list3 >= self.custom_list2)
    
    def test_le(self):
        self.assertTrue(self.custom_list1 <= self.custom_list2)
        self.assertTrue(self.custom_list2 <= self.custom_list1)
        self.assertTrue(self.custom_list3 <= self.custom_list1)
        self.assertFalse(self.custom_list2 <= self.custom_list3)

    def test_gt(self):
        self.assertFalse(self.custom_list1 > self.custom_list2)
        self.assertTrue(self.custom_list1 > self.custom_list3)
        
    def test_lt(self):
        self.assertFalse(self.custom_list1 < self.custom_list2)
        self.assertTrue(self.custom_list3 < self.custom_list1)

    def test_str(self):
        res = self.custom_list1.__str__()
        predicted_res = "[1, 2, 5], Sum = 8"
        self.assertEqual(predicted_res, res)

    def test_add(self):
        res = CustomList([1, 5, 8])
        self.assertEqual(res, self.custom_list1 + self.custom_list2)

    def test_add(self):
        res1 = CustomList([2, 4, 5])
        self.assertEqual(res1, self.custom_list1 + self.default_list1)
        res2 = CustomList([1, 5, 8])
        self.assertEqual(res2, self.custom_list2 + self.custom_list3)
        res3 = CustomList([1, 5, 8, 4])
        self.assertEqual(res3, self.default_list2 + self.custom_list2)

    def test_sub(self):
        res1 = CustomList([0, 0, 2])
        self.assertEqual(res1, self.custom_list2 - self.custom_list3)
        res2 = CustomList([0, 0, 0, 4])
        self.assertEqual(res2, self.default_list2 - self.custom_list3)