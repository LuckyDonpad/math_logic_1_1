def is_operation(token):
    return token in "~>|?-"


def get_priority(token):
    if not is_operation(token):
        raise SyntaxError("Undefined operation")
    return "~>|?-".find(token) + 1


def get_postfix(infix) -> list:
    infix = list(infix)
    output = []
    stack = []
    # прочитать токен
    for token in infix:
        # Если токен — число или переменная, то добавить его в очередь вывода
        if token.isalpha() or token.isnumeric():
            output.append(token)
        #Если токен — операция op1, то
        elif is_operation(token):
            while stack and is_operation(stack[-1]) and (get_priority(token) <= get_priority(stack[-1])):
                output.append(stack.pop())
            stack.append(token)
        elif token == "(":
            stack.append(token)
        elif token == ")":
            while len(stack) > 0 and stack[-1] != '(':
                output.append(stack.pop())
            if len(stack) == 0:
                raise SyntaxError("opening par is missing")
            else:
                stack.pop()
    while len(stack) > 0:
        if token == '(':
               raise SyntaxError("closing par is missing")
        output.append(stack.pop())
    return output


print(get_postfix('A|(B|C)'))