import unittest as ut

class baseTester(ut.TestCase):
    def testAssertsCorrect(self):
        self.assertEqual(2, 2)
        self.assertNotEqual(2, 3)

    def testAssertsIncorrect(self):
        self.assertNotEqual(2, 2)

    def testAssertsIncorrect2(self):
        self.assertEqual(2, 3)



if __name__ == "__main__":
    ut.main()
