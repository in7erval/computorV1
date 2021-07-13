

def expand_digit(equation, start):
    end = start + 1 if equation[start] == '-' else start
    length = len(equation)
    while end < length and (equation[end].isdigit() or equation[end] == '.'):
        end += 1
    return equation[start:end], (end - start - 1)


def isoper(char):
    return char == '+' or char == '-' or char == '*' or char == '^' or char == '='


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


def nod(a, b):
    a = abs(a)
    b = abs(b)
    while a != 0 and b != 0:
        if a > b:
            a = a % b
        else:
            b = b % a
    return a + b
