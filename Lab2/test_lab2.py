import unittest

from Lab2 import guess_number


class TestMath(unittest.TestCase):
    def test_positive_seq(self):
        self.assertEqual(guess_number(7, [1, 2, 8, 4, 7], method="seq"), [7, 4])

    def test_positive_bin(self):
        self.assertEqual(guess_number(11, [5, 8, 4, 11], method="bin"), [11, 3])

    def test_positive_bin_list(self):
        self.assertEqual(guess_number(8, [1, 20], method="bin_with_making_list"), [8, 4])

    def test_negative_target_seq(self):
        self.assertEqual(guess_number(-11, [-11, -5, -8, -4], method="seq"), [-11, 1])

    def test_negative_target_bin(self):
        self.assertEqual(guess_number(-11, [-11, -5, -8, -4], method="bin"), [-11, 2])

    def test_negative_target_bin_list(self):
        self.assertEqual(guess_number(-13, [-1, -18], method="bin_with_making_list"), [-13, 3])

    def test_target_none_seq(self):
        self.assertEqual(guess_number(10, [1, 2, 5, 8, 4], method="seq"), [None, 5])

    def test_target_none_bin(self):
        self.assertEqual(guess_number(20, [1, 2, 5, 8, 4], method="bin"), [None, 3])

    def test_target_none_bin_list(self):
        self.assertEqual(guess_number(50, [1, 9], method="bin_with_making_list"), [None, 4])

    def test_empty_list_seq(self):
        self.assertEqual(guess_number(11, [], method="seq"), [None, 0])

    def test_empty_list_bin(self):
        self.assertEqual(guess_number(11, [], method="bin"), [None, 0])

    def test_empty_list_bin_list(self):
        self.assertEqual(guess_number(11, [], method="bin_with_making_list"), None)

    def test_half_empty_list_bin_list(self):
        self.assertEqual(guess_number(11, [9], method="bin_with_making_list"), None)

    def test_targ_integrity(self):
        with self.assertRaises(TypeError):
            guess_number(3.14, [4, 7, 2], method="seq")

    def test_integrity(self):
        with self.assertRaises(TypeError):
            guess_number(3, [4.7, 7, 8.2], method="seq")

    def test_targ_str(self):
        with self.assertRaises(TypeError):
            guess_number("14", [4, 7, 2, 14], method="seq")

    def test_str_in_list(self):
        with self.assertRaises(TypeError):
            guess_number(19, ["4", 7, 8], method="seq")


if __name__ == "__main__":
    unittest.main()