import io
import unittest.mock

from computor import solve_equation


class MyTestCase(unittest.TestCase):

    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def assert_stdout(self, eq, expected_output, mock_stdout):
        solve_equation(eq)
        self.assertEqual(mock_stdout.getvalue(), expected_output)

    def test_something(self):
        self.assert_stdout("x^2 + x + 1 = 0", """Reduced form: 1 * x^2 + 1 * x^1 + 1 * x^0 = 0
Polynomial degree: 2
Discriminant is negative, the two complex solutions are:
(-0.5-0.8660254037844386j)
(-0.5+0.8660254037844386j)
Solution with irrational fractions:
-1/2 + sqrt(3)/2 * i
-1/2 + -sqrt(3)/2 * i
""")

    def test_right1(self):
        self.assert_stdout("3 * x^2 + 2 * x^1 + 1 * x^0 = 0 * x ^ 0", """Reduced form: 3 * x^2 + 2 * x^1 + 1 * x^0 = 0
Polynomial degree: 2
Discriminant is negative, the two complex solutions are:
(-0.3333333333333333-0.47140452079103173j)
(-0.3333333333333333+0.47140452079103173j)
Solution with irrational fractions:
-1/3 + sqrt(8)/6 * i
-1/3 + -sqrt(8)/6 * i
""")

    def test_right2(self):
        self.assert_stdout("x^2 + 2 * x + 1 = 0", """Reduced form: 1 * x^2 + 2 * x^1 + 1 * x^0 = 0
Polynomial degree: 2
Discriminant is equal to zero, the solution is:
-1
Solution with irrational fractions:
-1
""")

    def test_right3(self):
        self.assert_stdout("100*x + x^2 + 10*x^2 - -3*x + 4 = 50*x + 100 + 1 + 1 + 1 + 1 + 1 + 1 + 78*x + 78*x^2", """Reduced form: -67 * x^2 - 25 * x^1 - 102 * x^0 = 0
Polynomial degree: 2
Discriminant is negative, the two complex solutions are:
(-0.1865671641791045+1.2196641967983073j)
(-0.1865671641791045-1.2196641967983073j)
Solution with irrational fractions:
25/-134 + sqrt(26711)/-134 * i
25/-134 + -sqrt(26711)/-134 * i
""")

    def test_right4(self):
        self.assert_stdout("1 + 2*x + 3*x^2 + 4 + 5*x + 6*x^2 = -7*x^2 + -8*x + 9", """Reduced form: 16 * x^2 + 15 * x^1 - 4 * x^0 = 0
Polynomial degree: 2
Discriminant is strictly positive, the two solutions are:
0.2166160062331659
-1.154116006233166
Solution with irrational fractions:
(-15 + sqrt(481))/32
(-15 - sqrt(481))/32
""")

    def test_right5(self):
        self.assert_stdout("x^1+x+-3 =3+ 1*x-7", """Reduced form: 1 * x^1 + 1 * x^0 = 0
Polynomial degree: 1
The solution is:
-1
Solution with irrational fractions:
-1
""")

    def test_all_solution1(self):
        self.assert_stdout("123=123", """Reduced form: 0 * x^0 = 0
Polynomial degree: 0
Solution is all numbers
""")

    def test_all_solution2(self):
        self.assert_stdout("x^2 = x^2", """Reduced form: 0 * x^0 = 0
Polynomial degree: 0
Solution is all numbers
""")

    def test_all_solution3(self):
        self.assert_stdout("x^3 - x^3 = 0", """Reduced form: 0 * x^0 = 0
Polynomial degree: 0
Solution is all numbers
""")

    def test_all_solution4(self):
        self.assert_stdout("1 + 2 + 3 - x^2 - x = 1 + 5 + x^2 - x^2 + x - 7*x + 5*x", """Reduced form: -1 * x^2 = 0
Polynomial degree: 2
Discriminant is equal to zero, the solution is:
0
Solution with irrational fractions:
0
""")

    def test_no_solution1(self):
        self.assert_stdout("0 = 1", """Reduced form: -1 * x^0 = 0
Polynomial degree: 0
No solution
""")

    def test_no_solution2(self):
        self.assert_stdout("x^2 + 3*x + x^1 + 5 = x^2 + 4*x", """Reduced form: 5 * x^0 = 0
Polynomial degree: 0
No solution
""")

    def test_higher_degree(self):
        self.assert_stdout("x^100 + x^3 = 1", """Reduced form: 1 * x^100 + 1 * x^3 - 1 * x^0 = 0
Polynomial degree: 100
Degree higher than 2
""")

    def test_error1(self):
        self.assert_stdout("3 * x^2 + 2 * x^1 + 1 * x^0 =", "no right side\n")

    def test_error2(self):
        self.assert_stdout("3x = x = x", "There is no single '=' sign\n")

    def test_error3(self):
        self.assert_stdout("3x^2 + 2 * x^1 + 1 * x^0 = 0 * x ^ 0", "tokenizing error2 '3' []\n")

    def test_error4(self):
        self.assert_stdout("3*x^2x + 2^ * x^1 + 1 * x^0 = 0 * x ^ 0", "flag\n")

    def test_error5(self):
        self.assert_stdout("3*x^2 + 2^1 * x^1 + 1 * x^0 = 0 * x ^ 0", "tokenizing error2 '2' ['3*x^2']\n")


if __name__ == '__main__':
    unittest.main()
