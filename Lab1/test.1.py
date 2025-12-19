from Lab1 import sumdva
import unittest
class TestSumdva(unittest.TestCase):

    def test_sumdva_positive1(self):  #положительные только одна пара подходит
        self.assertEqual(sumdva([1,2,3,4,7], 3), [0,1])

    def test_sumdva_positive2(self):
        self.assertEqual(sumdva([3,4,5,2], 7), [0, 1]) #несколько пар чисел дают target(должна быть первая пара)

    def test_sumdva_negative(self): # все числа отрицательные
        self.assertEqual(sumdva([-1,-2,-4,-5],-6),[0,3])

    def test_sumdva_differentsigns(self): # числа разного знака
        self.assertEqual(sumdva([-1,2,-5,8],-3),[1,2])

    def test_sumdva_noanswer(self): # нет ответа
        self.assertEqual(sumdva([1,1,1,1,1],9),None)

    def test_sumdva_emptylist(self): # пустой список
        self.assertEqual(sumdva([],9),None)

    def test_sumdva_line(self):# в списке есть элемент представленный в виде строки
        self.assertEqual(sumdva([1,2,'4',5], 9), None)

    def test_sumdva_mixednumbers(self):# смешанные числа
        self.assertEqual(sumdva([1,2,2.4,5], 7), None)


if __name__ == "__main__":
    unittest.main()
