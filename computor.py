import math
from sys import argv
import re


class Complex:

    def __init__(self, r, i):
        self.r = r
        self.i = i

    def __str__(self):
        s = str(self.r)
        if self.i < 0:
            s += " - " + str(-self.i) + " * i"
        else:
            s += " + " + str(self.i) + " * i"
        return s


class Equation:

    def __init__(self, tokens):
        self.x2 = 0
        self.x1 = 0
        self.x0 = 0
        self.degree = 0
        self.discriminant = 0
        self.num_roots = 0
        self.is_complex = False
        self.answer = list()
        self.extract_x(tokens)

    def extract_x(self, equation: list):
        for token in equation:
            token: str
            degree = int(token.split('^')[1])
            q_str = token.split('*')[0]
            if '.' in q_str:
                q = float(q_str)
            else:
                q = int(q_str)
            if degree == 2:
                self.x2 += q
            elif degree == 1:
                self.x1 += q
            elif degree == 0:
                self.x0 += q
            self.degree = max(self.degree, degree)

    def solve(self):
        if self.degree == 2:
            self.discriminant = self.x1 * self.x1 - 4 * self.x2 * self.x0
            if self.discriminant < 0:
                self.is_complex = True
                self.num_roots = 2
                root1_i = math.sqrt(-self.discriminant) / (2 * self.x2)
                root2_i = -root1_i
                root_r = -self.x1 / (2 * self.x2)
                self.answer.append(Complex(root_r, root2_i))
                self.answer.append(Complex(root_r, root1_i))
            elif self.discriminant == 0:
                self.num_roots = 1
                root = -self.x1 / (2 * self.x2)
                self.answer.append(root)
            else:
                self.num_roots = 2
                root1 = (-self.x1 + math.sqrt(self.discriminant)) / (2 * self.x2)
                root2 = (-self.x1 - math.sqrt(self.discriminant)) / (2 * self.x2)
                self.answer.append(root1)
                self.answer.append(root2)
        elif self.degree == 1:
            self.num_roots = 1
            self.answer.append(-self.x0 / self.x1)
        else:
            pass  # error No solution or Degree higher

    def __str__(self):
        s = ""
        if self.x2 != 0:
            s = str(self.x2) + " * x^2"
            if self.x1 > 0:
                s = s + " + " + str(self.x1) + " * x^1"
            elif self.x1 < 0:
                s = s + " - " + str(-self.x1) + " * x^1"
        else:
            s = str(self.x1) + " * x^1"
        if self.x0 > 0:
            s = s + " + " + str(self.x0) + " * x^0"
        elif self.x0 < 0:
            s = s + " - " + str(-self.x0) + " * x^0"
        s = s + " = 0"
        return s


def expand_digit(equation, start):
    end = start
    length = len(equation)
    while end < length and (equation[end].isdigit() or equation[end] == '.'):
        end += 1
    return equation[start:end], end-start


def isoper(char):
    return char == '+' or char == '-' or char == '*' or char == '^'


def isnum(str_num):
    if not str_num[0].isdigit():
        return False
    for x in str_num:
        if not x.isdigit() and x != '.':
            return False
    return True



def update_tokens(tokens):
    updated_tokens = list()
    is_after_equal = False
    for i in range(len(tokens)):
        if tokens[i] == '*':
            mult = tokens[i - 1] + '*' + tokens[i + 1]
            updated_tokens.append(mult)
        elif tokens[i] == '=':
            is_after_equal = True
            if isnum(tokens[i + 1]):
                if '.' in tokens[i + 1]:
                    dig = float(tokens[i + 1]) * -1
                else:
                    dig = int(tokens[i + 1]) * -1
                tokens[i + 1] = str(dig)
        elif tokens[i] == '+' and is_after_equal:
            tokens[i+1] = '-' + tokens[i + 1]
        elif tokens[i] == '-' and not is_after_equal:
            tokens[i + 1] = '-' + tokens[i + 1]
        elif tokens[i] == '^':
            last = updated_tokens.pop()
            last = last + '^' + tokens[i+1]
            updated_tokens.append(last)
    return updated_tokens



def tokenize(equation):
    tokens = list()
    end = 0
    for i in range(len(equation)):
        if end > 0:
            end -= 1
        else:
            if isnum(equation[i]):
                digit, end = expand_digit(equation, i)
                tokens.append(digit)
            elif isoper(equation[i]):
                tokens.append(equation[i:i+1])
            elif equation[i] == 'x':
                tokens.append('x')
            elif equation[i] == '=':
                tokens.append('=')
            else:
                pass  # error
    print("TOKENS: ", tokens)
    tokens = update_tokens(tokens)
    print("UPDATED TOKENS: ", tokens)
    return tokens
    # tokens_plus = re.split('\+|-|=', equation)
    # tokens_plus_stripped = list()
    # for token in tokens_plus:
    #     tokens_plus_stripped.append(token.strip())
    #
    # tokens_plus = tokens_plus_stripped
    # print(tokens_plus)


def solve_equation():
    equation = argv[1]
    print(equation)
    if '=' not in equation:
        raise ValueError
    equation.strip().lower()
    tokens = tokenize(equation)
    eq = Equation(tokens)
    print(eq)
    eq.solve()
    for root in eq.answer:
        print(root)


if __name__ == '__main__':
    solve_equation()
