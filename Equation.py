from EquationError import EquationError
from utils import nod


class Equation:

    def __init__(self, tokens):
        self.degree = 0
        self.discriminant = 0
        self.num_roots = 0
        self.is_complex = False
        self.answer = list()
        self.fractions_answer = list()
        self.degrees = {0: 0, 1: 0, 2: 0}
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
            self.degree = self.max_degree()

    def solve(self):
        if self.solution_is_all():
            raise EquationError("Solution is all numbers")
        elif self.degree > 2:
            raise EquationError("Degree higher than 2")
        elif min(self.degrees.keys()) < 0:
            raise EquationError("Degree less than 0")
        elif self.degree == 2:
            q2 = self.degrees[2]
            q1 = self.degrees[1]
            q0 = self.degrees[0]
            self.discriminant = q1 * q1 - 4 * q2 * q0
            if self.discriminant < 0:
                print("Discriminant is negative, the two complex solutions are:")
                self.is_complex = True
                self.num_roots = 2
                sqrt_discr = (-self.discriminant) ** 0.5
                if sqrt_discr == int(sqrt_discr):
                    sqrt_discr = int(sqrt_discr)
                root1_i = sqrt_discr / (2 * q2)
                if sqrt_discr % (2 * q2) == 0:
                    root1_i = int(root1_i)
                    root1_i_str = str(root1_i) + ' * i'
                else:
                    if type(sqrt_discr) is int:
                        nd = nod(sqrt_discr, 2 * q2)
                        root1_i_str = '%s/%s * i' % (int(sqrt_discr / nd), int((2 * q2) / nd))
                    else:
                        root1_i_str = 'sqrt(%s)/%s * i' % (-self.discriminant, 2 * q2)
                root2_i = -root1_i
                if sqrt_discr % (2 * q2) == 0:
                    root2_i = int(root2_i)
                    root2_i_str = str(root2_i) + ' * i'
                else:
                    if type(sqrt_discr) is int:
                        nd = nod(sqrt_discr, 2 * q2)
                        root2_i_str = '-%s/%s * i' % (int(sqrt_discr / nd), int((2 * q2) / nd))
                    else:
                        root2_i_str = '-sqrt(%s)/%s * i' % (-self.discriminant, 2 * q2)
                root_r = -q1 / (2 * q2)
                if -q1 % (2 * q2) == 0:
                    root_r = int(root_r)
                    root_r_str = str(root_r)
                else:
                    if type(q1) is int and type(q2) is int:
                        nd = nod(-q1, 2 * q2)
                        root_r_str = '%s/%s' % (int(-q1 / nd), int((2 * q2) / nd))
                    else:
                        root_r_str = '%s/%s' % (-q1, 2 * q2)
                self.answer.append(complex(root_r, root2_i))
                self.answer.append(complex(root_r, root1_i))
                self.fractions_answer.append(root_r_str + ' + ' + root1_i_str)
                self.fractions_answer.append(root_r_str + ' + ' + root2_i_str)
            elif self.discriminant == 0:
                print("Discriminant is equal to zero, the solution is:")
                self.num_roots = 1
                root = -q1 / (2 * q2)
                if -q1 % (2 * q2) == 0:
                    root = int(root)
                    root_str = str(root)
                else:
                    root_str = str(-q1) + '/' + str(2 * q2)
                self.answer.append(root)
                self.fractions_answer.append(root_str)
            else:
                print("Discriminant is strictly positive, the two solutions are:")
                self.num_roots = 2
                sqrt_discr = self.discriminant ** 0.5
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
                            root1_str = '%s/%s' % (int((-q1 + sqrt_discr) / nd), int((2 * q2) / nd))
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
            print("The solution is:")
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
        return "Reduced form: %s\nPolynomial degree: %d" % (s, self.degree)

    def solution_is_all(self):
        ks = self.degrees.keys()
        return (2 in ks and self.degrees[2] == 0 or 2 not in ks) and \
               (1 in ks and self.degrees[1] == 0 or 1 not in ks) and \
               (0 in ks and self.degrees[0] == 0 or 0 not in ks)

    def max_degree(self):
        max_degr = 0
        for key in self.degrees.keys():
            if self.degrees[key] != 0 and key > max_degr:
                max_degr = key
        return max_degr