import unittest
from Lab_3 import gen_bin_tree


class TestMath(unittest.TestCase):
    def test_another(self):
        self.assertEqual(gen_bin_tree(3, 16, lambda x: x//2, lambda y: y**2),
                         {'16': [{'8': [{'4': []}, {'64': []}]}, {'256': [{'128': []}, {'65536': []}]}]})

    def test_float_main_root(self):
        self.assertEqual(gen_bin_tree(3, 16, lambda x: x//2.3, lambda y: y**2.5),
                         {'16': [{'6.0': [{'2.0': []}, {'88.18163074019441': []}]},
                                 {'1024.0': [{'445.0': []}, {'33554432.0': []}]}]})

    def test_float_both_roots(self):
        self.assertEqual(gen_bin_tree(3, 16.5, lambda x: x//2, lambda y: y**2),{'16.5': [{'8.0': [{'4.0': []}, {'64.0': []}]}, {'272.25': [{'136.0': []}, {'74120.0625': []}]}]})

    def test_height_zero(self):
        self.assertEqual(gen_bin_tree(0, 16, lambda x: x//2, lambda y: y**2),
                         {'16': []})

    def test_negativ(self):
        self.assertEqual(gen_bin_tree(3, 16, lambda x: x - 1, lambda y: y ** 2),
                         {'16': [{'15': [{'14': []}, {'225': []}]}, {'256': [{'255': []}, {'65536': []}]}]})

    def test_float_height(self):
        with self.assertRaises(TypeError):
            gen_bin_tree(3.7, 16, lambda x: x //2, lambda y: y**2)
    def test_str_height(self):
        with self.assertRaises(TypeError):
            gen_bin_tree("3", 16, lambda x: x//2, lambda y: y**2)


if __name__ == "__main__":
    unittest.main()