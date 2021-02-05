import math
from sys import argv


class EquationError(Exception):

    error = "Error"

    def __init__(self, err_msg):
        self.error = err_msg

    def __str__(self):
        return self.error

    def __repr__(self):
        return self.error


class Equation:

    def __init__(self, tokens):
        self.degree = 0
        self.discriminant = 0
        self.num_roots = 0
        self.is_complex = False
        self.answer = list()
        self.degrees = {0:0, 1:0, 2:0}
        self.extract_x(tokens)

    def extract_x(self, equation: list):
        for token in equation:
            token: str
            spl = token.split('^')
            degree = 1 if len(spl) == 1 else int(token.split('^')[1])
            q_str = token.split('*')[0]
            if '.' in q_str:
                q = float(q_str)
            else:
                q = int(q_str)
            if degree not in self.degrees.keys():
                self.degrees[degree] = q
            else:
                self.degrees[degree] += q
            self.degree = max_degree(self.degrees)

    def solve(self):
        if solution_is_all(self.degrees):
            raise EquationError("Solution is all numbers")
        elif self.degree > 2:
            raise EquationError("Degree higher than 2")
        elif self.degree == 2:
            q2 = self.degrees[2]
            q1 = self.degrees[1]
            q0 = self.degrees[0]
            self.discriminant = q1 * q1 - 4 * q2 * q0
            if self.discriminant < 0:
                self.is_complex = True
                self.num_roots = 2
                root1_i = math.sqrt(-self.discriminant) / (2 * q2)
                root2_i = -root1_i
                root_r = -q1 / (2 * q2)
                self.answer.append(complex(root_r, root2_i))
                self.answer.append(complex(root_r, root1_i))
            elif self.discriminant == 0:
                self.num_roots = 1
                root = -q1 / (2 * q2)
                self.answer.append(root)
            else:
                self.num_roots = 2
                root1 = (-q1 + math.sqrt(self.discriminant)) / (2 * q2)
                root2 = (-q1 - math.sqrt(self.discriminant)) / (2 * q2)
                self.answer.append(root1)
                self.answer.append(root2)
        elif self.degree == 1:
            q1 = self.degrees[1]
            q0 = self.degrees[0]
            self.num_roots = 1
            self.answer.append(-q0 / q1)
        else:
            raise EquationError("No solution")

    def __str__(self):
        s = ""
        ks = list(self.degrees.keys())
        ks.sort(reverse=True)
        first = True
        for dgr in ks:
            if self.degrees[dgr] != 0 and len(ks) != 1:
                if not first:
                    s = s + " + "
                else:
                    first = False
                s = s + str(self.degrees[dgr]) + " * x^" + str(dgr)
        if s == "":
            s = "0 * x^0"
        s = s + " = 0"
        return "Degree: " + str(self.degree) + "\n" + s


def solution_is_all(degrees: dict):
    ks = degrees.keys()
    return (2 in ks and degrees[2] == 0 or 2 not in ks) and (1 in ks and degrees[1] == 0 or 1 not in ks) and (0 in ks and degrees[0] == 0 or 0 not in ks)


def max_degree(degrees: dict):
    max_degr = 0
    for key in degrees.keys():
        if degrees[key] != 0 and key > max_degr:
            max_degr = key
    return max_degr


def expand_digit(equation, start):
    end = start + 1 if equation[start] == '-' else start
    length = len(equation)
    while end < length and (equation[end].isdigit() or equation[end] == '.'):
        end += 1
    return equation[start:end], (end - start - 1)


def isoper(char):
    return char == '+' or char == '-' or char == '*' or char == '^'


def isnum(str_num):
    if not (str_num[0].isdigit() or (len(str_num) > 1 and str_num[0] == '-' and str_num[1].isdigit())):
        return False
    i = 1 if str_num[0] == '-' else 0
    while i < len(str_num):
        if not str_num[i].isdigit() and str_num[i] != '.':
            return False
        i = i + 1
    return True


def invert_num(num_str):
    if '.' in num_str:
        dig = float(num_str) * -1
    else:
        dig = int(num_str) * -1
    return str(dig)


def update_tokens(tokens):
    updated_tokens = list()
    is_after_equal = False
    i = 0
    while i < len(tokens):
        if isnum(tokens[i]):
            if is_after_equal:
                tokens[i] = invert_num(tokens[i])
            if i + 1 < len(tokens) and tokens[i + 1] != '*' or i + 1 >= len(tokens):
                updated_tokens.append(tokens[i] + '*x^0')
                i = i + 1
            elif i + 2 < len(tokens) and tokens[i + 1] == '*' and tokens[i + 2] == 'x':
                if i + 4 < len(tokens) and tokens[i + 3] == '^' and isnum(tokens[i + 4]):
                    updated_tokens.append(tokens[i]+tokens[i+1]+tokens[i+2]+tokens[i+3]+tokens[i+4])
                    i = i + 5
                elif i + 3 < len(tokens) and tokens[i + 3] != '^':
                    updated_tokens.append(tokens[i] + tokens[i + 1] + 'x^1')
                    i = i + 3
                else:
                    raise EquationError("tokenizing error1 '" + tokens[i] + "' " + str(updated_tokens))
            else:
                raise EquationError("tokenizing error2 '" + tokens[i] + "' " + str(updated_tokens))
        elif tokens[i] == 'x':
            prefix = '-1*' if is_after_equal else '1*'
            if i + 2 < len(tokens) and tokens[i + 1] == '^' and isnum(tokens[i + 2]):
                updated_tokens.append(prefix + tokens[i] + tokens[i + 1] + tokens[i + 2])
                i = i + 3
            elif i + 1 >= len(tokens) or tokens[i + 1] != '^':
                updated_tokens.append(prefix + 'x^1')
                i = i + 1
            else:
                raise EquationError("tokenizing error3 '" + tokens[i] + "' " + str(updated_tokens))
        elif tokens[i] == '=':
            is_after_equal = True
            if i + 1 >= len(tokens):
                raise EquationError("no right side")
            i = i + 1
        elif tokens[i] == '+':
            if is_after_equal:
                tokens[i + 1] = '-' + tokens[i + 1]
            i = i + 1
        elif tokens[i] == '-':
            if not is_after_equal:
                tokens[i + 1] = '-' + tokens[i + 1]
            i = i + 1
        else:
            raise EquationError("tokenizing error4 '" + tokens[i] + "' " + str(updated_tokens))

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
            elif not equation[i].isspace():
                raise EquationError("unexpected symbol '%s'" % equation[i])
    print("TOKENS: ", tokens)
    tokens = update_tokens(tokens)
    print("UPDATED TOKENS: ", tokens)
    return tokens


def solve_equation():
    equation = argv[1]
    print(equation)
    if equation.count('=') != 1:
        raise EquationError("Equation false")
    equation = equation.strip().lower()
    tokens = tokenize(equation)
    eq = Equation(tokens)
    print(eq)
    eq.solve()
    print(eq.answer)


if __name__ == '__main__':
    solve_equation()
