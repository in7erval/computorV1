import math
from sys import argv


def nod(a, b):
    a = abs(a)
    b = abs(b)
    while a != 0 and b != 0:
        if a > b:
            a = a % b
        else:
            b = b % a
    return a + b


class EquationError(Exception):

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
        self.fractions_answer = list()
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
                sqrt_discr = math.sqrt(-self.discriminant)
                if sqrt_discr == int(sqrt_discr):
                    sqrt_discr = int(sqrt_discr)
                root1_i = sqrt_discr / (2 * q2)
                if sqrt_discr % (2 * q2) == 0:
                    root1_i = int(root1_i)
                    root1_i_str = str(root1_i) + ' * i'
                else:
                    if type(sqrt_discr) is int:
                        nd = nod(sqrt_discr, 2 * q2)
                        root1_i_str = '%s/%s * i' % (int(sqrt_discr/nd), int((2 * q2)/nd))
                    else:
                        root1_i_str = 'sqrt(%s)/%s * i' % (-self.discriminant, 2 * q2)
                root2_i = -root1_i
                if sqrt_discr % (2 * q2) == 0:
                    root2_i = int(root2_i)
                    root2_i_str = str(root2_i) + ' * i'
                else:
                    if type(sqrt_discr) is int:
                        nd = nod(sqrt_discr, 2 * q2)
                        root2_i_str = '-%s/%s * i' % (int(sqrt_discr/nd), int((2 * q2)/nd))
                    else:
                        root2_i_str = '-sqrt(%s)/%s * i' % (-self.discriminant, 2 * q2)
                root_r = -q1 / (2 * q2)
                if -q1 % (2 * q2) == 0:
                    root_r = int(root_r)
                    root_r_str = str(root_r)
                else:
                    if type(q1) is int and type(q2) is int:
                        nd = nod(-q1, 2*q2)
                        root_r_str = '%s/%s' % (int(-q1/nd), int((2 * q2)/nd))
                    else:
                        root_r_str = '%s/%s' % (-q1, 2 * q2)
                self.answer.append(complex(root_r, root2_i))
                self.answer.append(complex(root_r, root1_i))
                self.fractions_answer.append(root_r_str + ' + ' + root1_i_str)
                self.fractions_answer.append(root_r_str + ' + ' + root2_i_str)
            elif self.discriminant == 0:
                self.num_roots = 1
                root = -q1 / (2 * q2)
                if -q1 % (2 * q2) == 0:
                    root = int(root)
                    root_str = str(root)
                else:
                    root_str = str(-q1) + '/' + str(2*q2)
                self.answer.append(root)
                self.fractions_answer.append(root_str)
            else:
                self.num_roots = 2
                sqrt_discr = math.sqrt(self.discriminant)
                if sqrt_discr == int(sqrt_discr):
                    sqrt_discr = int(sqrt_discr)
                root1 = (-q1 + sqrt_discr) / (2 * q2)
                root2 = (-q1 - sqrt_discr) / (2 * q2)
                if (-q1 + sqrt_discr) % (2 * q2) == 0:
                    root1 = int(root1)
                    root1_str = str(root1)
                else:
                    if type(sqrt_discr) is int:
                        if type(q1) is int and type(q2) is int:
                            nd = nod(-q1 + sqrt_discr, 2 * q2)
                            root1_str = '%s/%s' % (int((-q1 + sqrt_discr)/nd), int((2 * q2)/nd))
                        else:
                            root1_str = '%s/%s' % ((-q1 + sqrt_discr), (2 * q2))
                    else:
                        root1_str = '(%s + sqrt(%s))/%s' % (-q1, self.discriminant, (2 * q2))
                if (-q1 - sqrt_discr) % (2 * q2) == 0:
                    root2 = int(root2)
                    root2_str = str(root2)
                else:
                    if type(sqrt_discr) is int:
                        if type(q1) is int and type(q2) is int:
                            nd = nod(-q1 - sqrt_discr, 2 * q2)
                            root2_str = '%s/%s' % (int((-q1 - sqrt_discr) / nd), int((2 * q2) / nd))
                        else:
                            root2_str = '%s/%s' % (-q1 - sqrt_discr, (2 * q2))
                    else:
                        root2_str = '(%s - sqrt(%s))/%s' % (-q1, self.discriminant, (2 * q2))
                self.answer.append(root1)
                self.answer.append(root2)
                self.fractions_answer.append(root1_str)
                self.fractions_answer.append(root2_str)
        elif self.degree == 1:
            q1 = self.degrees[1]
            q0 = self.degrees[0]
            self.num_roots = 1
            root = -q0 / q1
            if -q0 % q1 == 0:
                root = int(root)
                root_str = str(root)
            else:
                root_str = '%s/%s' % (-q0, q1)
            self.answer.append(root)
            self.fractions_answer.append(root_str)
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
                    s = s + " + " if self.degrees[dgr] > 0 else s + " - "
                    dgr_str = str(abs(self.degrees[dgr]))
                else:
                    dgr_str = str(self.degrees[dgr])
                    first = False
                s = s + dgr_str + " * x^" + str(dgr)
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
                elif i + 3 < len(tokens) and tokens[i + 3] != '^' or i + 3 >= len(tokens):
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
        elif tokens[i] == '-':
            if isnum(tokens[i + 1]):
                tokens[i + 1] = invert_num(tokens[i + 1])
            elif tokens[i + 1] == 'x':
                tokens.insert(i+1, '-1')
                tokens.insert(i+2, '*')
            i = i + 1
        elif isoper(tokens[i]):
            i = i + 1
        elif isoper(tokens[i]) and isoper(tokens[i + 1]):
            raise EquationError("tokenizing error4 '" + tokens[i] + "' " + str(updated_tokens))
        else:
            raise EquationError("tokenizing error5 '" + tokens[i] + "' " + str(updated_tokens))

    return updated_tokens


def tokenize(equation):
    tokens = list()
    i = 0
    while i < len(equation):
        if isnum(equation[i]) or (equation[i] == '-' and isnum(equation[i+1])):
            digit, end = expand_digit(equation, i)
            i = i + end
            tokens.append(digit)
        elif isoper(equation[i]):
            tokens.append(equation[i:i+1])
        elif equation[i] == 'x':
            tokens.append('x')
        elif equation[i] == '=':
            tokens.append('=')
        elif not equation[i].isspace():
            raise EquationError("unexpected symbol '%s'" % equation[i])
        i = i + 1
    print("TOKENS: ", tokens)
    tokens = update_tokens(tokens)
    print("UPDATED TOKENS: ", tokens)
    return tokens


def solve_equation():
    equation = input() if len(argv) == 1 else argv[1]
    if equation.count('=') != 1:
        raise EquationError("Equation false")
    equation = equation.replace(" ", "").lower()
    print(equation)
    # try:
    tokens = tokenize(equation)
    if len(tokens) == 0:
        raise EquationError("error")
    eq = Equation(tokens)
    print(eq)
    eq.solve()
    print('-----------')
    for x in eq.answer:
        print('x = ' + str(x))
    print('-----------')
    for x in eq.fractions_answer:
        print('x = ' + x)


if __name__ == '__main__':
    solve_equation()
