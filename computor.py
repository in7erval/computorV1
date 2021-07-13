from sys import argv

from Equation import Equation
from tokenize import tokenize
from EquationError import EquationError

USAGE = "Usage: python3 computor.py [--bonus | -b] EQUATION"

def solve_equation(equation_input, bonus=False):
    if equation_input.count('=') != 1:
        print("There is no single '=' sign")
        return
    equation_input = equation_input.replace(" ", "").lower()
    try:
        tokens = tokenize(equation_input)
        if len(tokens) == 0:
            raise EquationError("error")
        eq = Equation(tokens)
        print(eq)
        eq.solve()
        for x in eq.answer:
            print(x)
        if bonus:
            print('Solution with irrational fractions:')
            for x in eq.fractions_answer:
                print(x)
    except EquationError as e:
        print(e.error)


if __name__ == '__main__':
    if len(argv) == 3 and argv[1] in ('--bonus', '-b'):
        solve_equation(argv[2], True)
    elif len(argv) == 2 and argv[1] in ('--bonus', '-b'):
        solve_equation(input(), True)
    elif len(argv) == 2:
        solve_equation(argv[1])
    elif len(argv) == 1:
        solve_equation(input())
    else:
        print("Error command arguments!")
        print(USAGE)
