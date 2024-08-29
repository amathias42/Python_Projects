"""Testing how passing an object as a variable handler performs"""

import unittest as ut


class VarHandler:
    def __init__(self):
        self.a = 0
        self.b = 1.5
        self.c = "see"

        self.d = {"hi": "Hello world!", "bye": "Adios", "no": "Nope"}


class Grandpa:
    def __init__(self):
        self.vH = VarHandler()
        self.uncle = Uncle(self.vH)
        self.dad = Dad(self.vH)


class GrandpaTwin(Grandpa):
    def __init__(self):
        super().__init__()


class GrandpaEvilTwin(Grandpa):
    def __init__(self):
        self.vH = VarHandler()
        self.uncle = Uncle(self.vH)
        self.dad = Dad(self.vH)


class Dad:
    def __init__(self, varHandler):
        self.vH = varHandler
        self.you = You(self.vH)


class Uncle:
    def __init__(self, varHandler):
        self.vH = varHandler


class You:
    def __init__(self, varHandler):
        self.vH = varHandler


class objectPassingTester(ut.TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.gpa = Grandpa()
        self.gpaT = GrandpaTwin()
        self.gpaET = GrandpaEvilTwin()

    def testVarHandlerExists(self):
        self.assertIsNotNone(self.gpa.vH, "Grandpa vh is None")
        self.assertIsNotNone(self.gpa.dad.vH, "Dad vh is None")
        self.assertIsNotNone(self.gpa.uncle.vH, "Uncle vh is None")
        self.assertIsNotNone(self.gpa.dad.you.vH, "You vh is None")

        self.assertIsNotNone(self.gpaT.vH, "Grandpa Twin vh is None")
        self.assertIsNotNone(self.gpaT.dad.vH, "Twin Dad vh is None")
        self.assertIsNotNone(self.gpaT.uncle.vH, "Twin Uncle vh is None")
        self.assertIsNotNone(self.gpaT.dad.you.vH, "Twin You vh is None")

        self.assertIsNotNone(self.gpaET.vH, "GrandpaEvil Twin  vh is None")
        self.assertIsNotNone(self.gpaET.dad.vH, "Evil Twin Dad vh is None")
        self.assertIsNotNone(self.gpaET.uncle.vH, "Evil Twin Uncle vh is None")
        self.assertIsNotNone(self.gpaET.dad.you.vH, "Evil Twin You vh is None")

    def testGrandpaOnlyAffectsChildren(self):

        self.assertEqual(self.gpa.vH.c, "see")
        self.assertEqual(self.gpa.uncle.vH.c, "see")
        self.assertEqual(self.gpa.dad.vH.c, "see")
        self.assertEqual(self.gpa.dad.you.vH.c, "see")

        self.assertEqual(self.gpaT.vH.c, "see")
        self.assertEqual(self.gpaT.uncle.vH.c, "see")
        self.assertEqual(self.gpaT.dad.vH.c, "see")
        self.assertEqual(self.gpaT.dad.you.vH.c, "see")

        self.assertEqual(self.gpaET.vH.c, "see")
        self.assertEqual(self.gpaET.uncle.vH.c, "see")
        self.assertEqual(self.gpaET.dad.vH.c, "see")
        self.assertEqual(self.gpaET.dad.you.vH.c, "see")

        self.gpa.vH.c = "sea"

        self.assertEqual(self.gpa.vH.c, "sea")
        self.assertEqual(self.gpa.uncle.vH.c, "sea")
        self.assertEqual(self.gpa.dad.vH.c, "sea")
        self.assertEqual(self.gpa.dad.you.vH.c, "sea")

        self.assertEqual(self.gpaT.vH.c, "see")
        self.assertEqual(self.gpaT.uncle.vH.c, "see")
        self.assertEqual(self.gpaT.dad.vH.c, "see")
        self.assertEqual(self.gpaT.dad.you.vH.c, "see")

        self.assertEqual(self.gpaET.vH.c, "see")
        self.assertEqual(self.gpaET.uncle.vH.c, "see")
        self.assertEqual(self.gpaET.dad.vH.c, "see")
        self.assertEqual(self.gpaET.dad.you.vH.c, "see")

    def testGrandpaOnlyAffectsChildrenDict(self):

        self.assertEqual(self.gpa.vH.d["no"], "Nope")
        self.assertEqual(self.gpa.uncle.vH.d["no"], "Nope")
        self.assertEqual(self.gpa.dad.vH.d["no"], "Nope")
        self.assertEqual(self.gpa.dad.you.vH.d["no"], "Nope")

        self.assertEqual(self.gpaT.vH.d["no"], "Nope")
        self.assertEqual(self.gpaT.uncle.vH.d["no"], "Nope")
        self.assertEqual(self.gpaT.dad.vH.d["no"], "Nope")
        self.assertEqual(self.gpaT.dad.you.vH.d["no"], "Nope")

        self.assertEqual(self.gpaET.vH.d["no"], "Nope")
        self.assertEqual(self.gpaET.uncle.vH.d["no"], "Nope")
        self.assertEqual(self.gpaET.dad.vH.d["no"], "Nope")
        self.assertEqual(self.gpaET.dad.you.vH.d["no"], "Nope")

        self.gpa.vH.d["no"] = "Yep"

        self.assertEqual(self.gpa.vH.d["no"], "Yep")
        self.assertEqual(self.gpa.uncle.vH.d["no"], "Yep")
        self.assertEqual(self.gpa.dad.vH.d["no"], "Yep")
        self.assertEqual(self.gpa.dad.you.vH.d["no"], "Yep")

        self.assertEqual(self.gpaT.vH.d["no"], "Nope")
        self.assertEqual(self.gpaT.uncle.vH.d["no"], "Nope")
        self.assertEqual(self.gpaT.dad.vH.d["no"], "Nope")
        self.assertEqual(self.gpaT.dad.you.vH.d["no"], "Nope")

        self.assertEqual(self.gpaET.vH.d["no"], "Nope")
        self.assertEqual(self.gpaET.uncle.vH.d["no"], "Nope")
        self.assertEqual(self.gpaET.dad.vH.d["no"], "Nope")
        self.assertEqual(self.gpaET.dad.you.vH.d["no"], "Nope")

    def testGrandpaTwinOnlyAffectsChildren(self):

        self.assertEqual(self.gpa.vH.c, "see")
        self.assertEqual(self.gpa.uncle.vH.c, "see")
        self.assertEqual(self.gpa.dad.vH.c, "see")
        self.assertEqual(self.gpa.dad.you.vH.c, "see")

        self.assertEqual(self.gpaT.vH.c, "see")
        self.assertEqual(self.gpaT.uncle.vH.c, "see")
        self.assertEqual(self.gpaT.dad.vH.c, "see")
        self.assertEqual(self.gpaT.dad.you.vH.c, "see")

        self.assertEqual(self.gpaET.vH.c, "see")
        self.assertEqual(self.gpaET.uncle.vH.c, "see")
        self.assertEqual(self.gpaET.dad.vH.c, "see")
        self.assertEqual(self.gpaET.dad.you.vH.c, "see")

        self.gpaT.vH.c = "sea"

        self.assertEqual(self.gpa.vH.c, "see")
        self.assertEqual(self.gpa.uncle.vH.c, "see")
        self.assertEqual(self.gpa.dad.vH.c, "see")
        self.assertEqual(self.gpa.dad.you.vH.c, "see")

        self.assertEqual(self.gpaT.vH.c, "sea")
        self.assertEqual(self.gpaT.uncle.vH.c, "sea")
        self.assertEqual(self.gpaT.dad.vH.c, "sea")
        self.assertEqual(self.gpaT.dad.you.vH.c, "sea")

        self.assertEqual(self.gpaET.vH.c, "see")
        self.assertEqual(self.gpaET.uncle.vH.c, "see")
        self.assertEqual(self.gpaET.dad.vH.c, "see")
        self.assertEqual(self.gpaET.dad.you.vH.c, "see")

    def testGrandpaTwinOnlyAffectsChildrenDict(self):

        self.assertEqual(self.gpa.vH.d["no"], "Nope")
        self.assertEqual(self.gpa.uncle.vH.d["no"], "Nope")
        self.assertEqual(self.gpa.dad.vH.d["no"], "Nope")
        self.assertEqual(self.gpa.dad.you.vH.d["no"], "Nope")

        self.assertEqual(self.gpaT.vH.d["no"], "Nope")
        self.assertEqual(self.gpaT.uncle.vH.d["no"], "Nope")
        self.assertEqual(self.gpaT.dad.vH.d["no"], "Nope")
        self.assertEqual(self.gpaT.dad.you.vH.d["no"], "Nope")

        self.assertEqual(self.gpaET.vH.d["no"], "Nope")
        self.assertEqual(self.gpaET.uncle.vH.d["no"], "Nope")
        self.assertEqual(self.gpaET.dad.vH.d["no"], "Nope")
        self.assertEqual(self.gpaET.dad.you.vH.d["no"], "Nope")

        self.gpaT.vH.d["no"] = "Yep"

        self.assertEqual(self.gpa.vH.d["no"], "Nope")
        self.assertEqual(self.gpa.uncle.vH.d["no"], "Nope")
        self.assertEqual(self.gpa.dad.vH.d["no"], "Nope")
        self.assertEqual(self.gpa.dad.you.vH.d["no"], "Nope")

        self.assertEqual(self.gpaT.vH.d["no"], "Yep")
        self.assertEqual(self.gpaT.uncle.vH.d["no"], "Yep")
        self.assertEqual(self.gpaT.dad.vH.d["no"], "Yep")
        self.assertEqual(self.gpaT.dad.you.vH.d["no"], "Yep")

        self.assertEqual(self.gpaET.vH.d["no"], "Nope")
        self.assertEqual(self.gpaET.uncle.vH.d["no"], "Nope")
        self.assertEqual(self.gpaET.dad.vH.d["no"], "Nope")
        self.assertEqual(self.gpaET.dad.you.vH.d["no"], "Nope")

    def testGrandpaETOnlyAffectsChildren(self):

        self.assertEqual(self.gpa.vH.c, "see")
        self.assertEqual(self.gpa.uncle.vH.c, "see")
        self.assertEqual(self.gpa.dad.vH.c, "see")
        self.assertEqual(self.gpa.dad.you.vH.c, "see")

        self.assertEqual(self.gpaT.vH.c, "see")
        self.assertEqual(self.gpaT.uncle.vH.c, "see")
        self.assertEqual(self.gpaT.dad.vH.c, "see")
        self.assertEqual(self.gpaT.dad.you.vH.c, "see")

        self.assertEqual(self.gpaET.vH.c, "see")
        self.assertEqual(self.gpaET.uncle.vH.c, "see")
        self.assertEqual(self.gpaET.dad.vH.c, "see")
        self.assertEqual(self.gpaET.dad.you.vH.c, "see")

        self.gpaET.vH.c = "sea"

        self.assertEqual(self.gpa.vH.c, "see")
        self.assertEqual(self.gpa.uncle.vH.c, "see")
        self.assertEqual(self.gpa.dad.vH.c, "see")
        self.assertEqual(self.gpa.dad.you.vH.c, "see")

        self.assertEqual(self.gpaT.vH.c, "see")
        self.assertEqual(self.gpaT.uncle.vH.c, "see")
        self.assertEqual(self.gpaT.dad.vH.c, "see")
        self.assertEqual(self.gpaT.dad.you.vH.c, "see")

        self.assertEqual(self.gpaET.vH.c, "sea")
        self.assertEqual(self.gpaET.uncle.vH.c, "sea")
        self.assertEqual(self.gpaET.dad.vH.c, "sea")
        self.assertEqual(self.gpaET.dad.you.vH.c, "sea")

    def testGrandpaETOnlyAffectsChildrenDict(self):

        self.assertEqual(self.gpa.vH.d["no"], "Nope")
        self.assertEqual(self.gpa.uncle.vH.d["no"], "Nope")
        self.assertEqual(self.gpa.dad.vH.d["no"], "Nope")
        self.assertEqual(self.gpa.dad.you.vH.d["no"], "Nope")

        self.assertEqual(self.gpaT.vH.d["no"], "Nope")
        self.assertEqual(self.gpaT.uncle.vH.d["no"], "Nope")
        self.assertEqual(self.gpaT.dad.vH.d["no"], "Nope")
        self.assertEqual(self.gpaT.dad.you.vH.d["no"], "Nope")

        self.assertEqual(self.gpaET.vH.d["no"], "Nope")
        self.assertEqual(self.gpaET.uncle.vH.d["no"], "Nope")
        self.assertEqual(self.gpaET.dad.vH.d["no"], "Nope")
        self.assertEqual(self.gpaET.dad.you.vH.d["no"], "Nope")

        self.gpaET.vH.d["no"] = "Yep"

        self.assertEqual(self.gpa.vH.d["no"], "Nope")
        self.assertEqual(self.gpa.uncle.vH.d["no"], "Nope")
        self.assertEqual(self.gpa.dad.vH.d["no"], "Nope")
        self.assertEqual(self.gpa.dad.you.vH.d["no"], "Nope")

        self.assertEqual(self.gpaT.vH.d["no"], "Nope")
        self.assertEqual(self.gpaT.uncle.vH.d["no"], "Nope")
        self.assertEqual(self.gpaT.dad.vH.d["no"], "Nope")
        self.assertEqual(self.gpaT.dad.you.vH.d["no"], "Nope")

        self.assertEqual(self.gpaET.vH.d["no"], "Yep")
        self.assertEqual(self.gpaET.uncle.vH.d["no"], "Yep")
        self.assertEqual(self.gpaET.dad.vH.d["no"], "Yep")
        self.assertEqual(self.gpaET.dad.you.vH.d["no"], "Yep")

    def testDifferentVHs(self):
        self.assertIs(self.gpa.vH, self.gpa.dad.you.vH)
        self.assertIs(self.gpa.vH.a, self.gpa.dad.you.vH.a)
        self.assertIs(self.gpa.vH.d, self.gpa.dad.you.vH.d)

        self.assertIs(self.gpaT.vH, self.gpaT.dad.you.vH)
        self.assertIs(self.gpaT.vH.a, self.gpaT.dad.you.vH.a)
        self.assertIs(self.gpaT.vH.d, self.gpaT.dad.you.vH.d)

        self.assertIs(self.gpaET.vH, self.gpaET.dad.you.vH)
        self.assertIs(self.gpaET.vH.a, self.gpaET.dad.you.vH.a)
        self.assertIs(self.gpaET.vH.d, self.gpaET.dad.you.vH.d)

        self.assertIsNot(self.gpa.vH, self.gpaT.vH)
        self.assertIsNot(self.gpa.vH, self.gpaET.vH)
        self.assertIsNot(self.gpaET.vH, self.gpaT.vH)
        self.assertIsNot(self.gpa.dad.vH, self.gpaT.vH)
        self.assertIsNot(self.gpa.dad.you.vH, self.gpaT.vH)
        self.assertIsNot(self.gpa.dad.vH, self.gpaET.vH)
        self.assertIsNot(self.gpa.dad.you.vH, self.gpaET.vH)

        self.assertIs(self.gpa.uncle.vH.d, self.gpa.dad.you.vH.d)


ut.main()
