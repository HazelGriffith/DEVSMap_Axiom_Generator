import unittest
from axiom import Axiom, Binary_Formula, Unary_Formula, Constant

class TestAxiom(unittest.TestCase):

    def test__str__1(self):
        lhs = Constant("count")
        rhs = Constant("1")
        fo = Binary_Formula("",lhs, rhs, "==")
        ax = Axiom('tff','axiom_0','axiom', fo)
        self.assertEqual("tff(axiom_0,axiom,count = 1).", f"{ax}")

    def test__str__2(self):
        fo1 = Unary_Formula("",Constant("Boolean"), "!")
        ax = Axiom("tff", "axiom_123", "axiom", fo1)
        self.assertEqual("tff(axiom_123,axiom,~(Boolean)).", f"{ax}")

    def test__str__3(self):
        f1221 = Binary_Formula("", Constant("sigma"), Constant("4"), "*")
        f122 = Binary_Formula("", Constant("next_increment"), f1221, "==")
        f1211 = Binary_Formula("", Constant("count"), Constant("increment"), "+")
        f121 = Binary_Formula("", Constant("next_count"), f1211, "==")
        f12 = Binary_Formula("", f121, f122, "&&")
        f11 = Binary_Formula("", Constant("countUp"), Constant("true"), "==")
        f1 = Binary_Formula("",f11,f12,"=>")
        ax = Axiom('tff', 'delta_int_0', 'axiom', f1)
        self.assertEqual("tff(delta_int_0,axiom,countUp = $true => next_count = $sum(count,increment) & next_increment = $product(sigma,4)).", f"{ax}")

class TestConstant(unittest.TestCase):

    def testTranslate0(self):
        op = Constant("0")
        self.assertEqual("0", f"{op}")

    def testTranslateTrue(self):
        op = Constant("True")
        self.assertEqual("$true", f"{op}")

    def testTranslatetrue(self):
        op = Constant("true")
        self.assertEqual("$true", f"{op}")

    def testTranslateTRUE(self):
        op = Constant("TRUE")
        self.assertEqual("$true", f"{op}")

    def testTranslateFalse(self):
        op = Constant("False")
        self.assertEqual("$false", f"{op}")

    def testTranslatefalse(self):
        op = Constant("false")
        self.assertEqual("$false", f"{op}")

    def testTranslateFALSE(self):
        op = Constant("FALSE")
        self.assertEqual("$false", f"{op}")

    def testTranslateBag(self):
        op = Constant("direction_in.bag(-1)")
        self.assertEqual("val_rcvd(direction_in)", f"{op}")

    def testTranslateBagSize(self):
        op = Constant("increment_in.bagSize()")
        self.assertEqual("num_rcvd(increment_in)", f"{op}")

if __name__ == '__main__':
    unittest.main()