from EquationError import EquationError
from utils import isnum, isoper, invert_num, expand_digit


def update_tokens(tokens):
    updated_tokens = list()
    is_after_equal = False
    i = 0
    flag = False  # чередование оператора и переменной
    while i < len(tokens):
        if isnum(tokens[i]):
            if flag and float(tokens[i]) > 0:
                raise EquationError("flag")
            flag = True
            if is_after_equal:
                tokens[i] = invert_num(tokens[i])
            if i + 1 < len(tokens) and (
                    tokens[i + 1] in '-+=' or (isnum(tokens[i + 1]) and float(tokens[i + 1]) < 0)) or i + 1 >= len(
                    tokens):
                updated_tokens.append(tokens[i] + '*x^0')
                i = i + 1
            elif i + 2 < len(tokens) and tokens[i + 1] == '*' and tokens[i + 2] == 'x':
                if i + 4 < len(tokens) and tokens[i + 3] == '^' and isnum(tokens[i + 4]):
                    updated_tokens.append(tokens[i] + tokens[i + 1] + tokens[i + 2] + tokens[i + 3] + tokens[i + 4])
                    i = i + 5
                elif i + 3 < len(tokens) and tokens[i + 3] != '^' or i + 3 >= len(tokens):
                    updated_tokens.append(tokens[i] + tokens[i + 1] + 'x^1')
                    i = i + 3
                else:
                    raise EquationError("tokenizing error1 '" + tokens[i] + "' " + str(updated_tokens))
            else:
                raise EquationError("tokenizing error2 '" + tokens[i] + "' " + str(updated_tokens))
        elif tokens[i] == 'x':
            if flag:
                raise EquationError("flag")
            flag = True
            prefix = '-1*' if is_after_equal else '1*'
            if i + 2 < len(tokens) and tokens[i + 1] == '^' and isnum(tokens[i + 2]):
                updated_tokens.append(prefix + tokens[i] + tokens[i + 1] + tokens[i + 2])
                i = i + 3
            elif i + 1 >= len(tokens) or tokens[i + 1] != '^' and isoper(tokens[i + 1]):
                updated_tokens.append(prefix + 'x^1')
                i = i + 1
            elif isnum(tokens[i + 1]) and float(tokens[i + 1]) < 0:
                updated_tokens.append(prefix + 'x^1')
                tokens.insert(i + 1, '+')
                i = i + 1
            else:
                raise EquationError("tokenizing error3 '" + tokens[i] + "' " + str(updated_tokens))
        elif tokens[i] == '=':
            flag = False
            is_after_equal = True
            if i + 1 >= len(tokens):
                raise EquationError("no right side")
            i = i + 1
        elif tokens[i] == '-':
            flag = False
            if isnum(tokens[i + 1]):
                tokens[i + 1] = invert_num(tokens[i + 1])
            elif tokens[i + 1] == 'x':
                tokens.insert(i + 1, '-1')
                tokens.insert(i + 2, '*')
            i = i + 1
        elif isoper(tokens[i]):
            flag = False
            if isoper(tokens[i + 1]):
                raise EquationError("tokenizing error4 '" + tokens[i] + "' " + str(updated_tokens))
            i = i + 1
        else:
            raise EquationError("tokenizing error5 '" + tokens[i] + "' " + str(updated_tokens))

    return updated_tokens


def tokenize(equation):
    tokens = list()
    i = 0
    while i < len(equation):
        if isnum(equation[i]) or (equation[i] == '-' and isnum(equation[i + 1])):
            digit, end = expand_digit(equation, i)
            i = i + end
            tokens.append(digit)
        elif isoper(equation[i]):
            tokens.append(equation[i:i + 1])
        elif equation[i] == 'x':
            tokens.append('x')
        elif equation[i] == '=':
            tokens.append('=')
        elif not equation[i].isspace():
            raise EquationError("unexpected symbol '%s'" % equation[i])
        i = i + 1
    # print("TOKENS: ", tokens)
    tokens = update_tokens(tokens)
    # print("UPDATED TOKENS: ", tokens)
    return tokens
