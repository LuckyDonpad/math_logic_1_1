# Принимает символ
# Возвращает значение Истина, если токен - операция, иначе Ложь
def is_operation(token):
    assert len(token) == 1
    return token in "~>|?-"


# Принимает символ обозначающий операцию
# Возвращает приоритет операции
# приоритет - число от одного до пяти включительно: чем больше число, тем выше приоритет
def get_priority(token):
    assert len(token) == 1
    if not is_operation(token):
        raise SyntaxError("Undefined operation")
    return "~>|?-".find(token) + 1


# принимает выражение в инфиксной записи и возвращает это выражение в ОПЗ
def get_postfix(infix):
    infix = list(infix)
    output = []
    stack = []
    # прочитать токен
    for token in infix:
        # Если токен — число или переменная, то добавить его в очередь вывода
        if token.isalpha() or token.isnumeric():
            output.append(token)
        # Если токен — операция op1, то
        elif is_operation(token):
            # Пока на вершине стека присутствует токен-операция op2, и у op1 приоритет
            # меньше либо равен приоритету op2, переложить op2 из стека в выходную
            # очередь.
            while stack and is_operation(stack[-1]) and (get_priority(token) <= get_priority(stack[-1])):
                output.append(stack.pop())
            # Положить op1 в стек
            stack.append(token)
        # Если токен — открывающая скобка, то положить его в стек.
        elif token == "(":
            stack.append(token)
        # Если токен — закрывающая скобка:
        elif token == ")":
            # Пока токен на вершине стека не является открывающей скобкой, перекладывать
            # токены-операции из стека в выходную очередь.
            while len(stack) > 0 and stack[-1] != '(':
                output.append(stack.pop())
            # Если стек закончился до того, как был встречен токен-«открывающая скобка», то в
            # выражении пропущена открывающая скобка
            if len(stack) == 0:
                raise SyntaxError("opening par is missing")
            # Выкинуть открывающую скобку из стека, но не добавлять в очередь вывода.
            else:
                stack.pop()
    # Если больше не осталось токенов на входе
    # Пока есть токены в стеке
    for token in stack:
        # Если токен на вершине стека — открывающая скобка, то в выражении
        # присутствует незакрытая скобка
        if token == '(':
            raise SyntaxError("closing par is missing")
        # Переложить токен-операцию из стека в выходную очередь
        output.append(stack.pop())
    return output


# возвращает логическое выражение введенное с клавиатуры в верхнем регистре без пробелов
def input_expression():
    print("Please input logical expression\n",
          "'~' - equal\n",
          "'>' - implication\n",
          "'|' - or\n",
          "'&' - and\n",
          "'-' - not\n")
    expression = str(input()).upper().replace(' ', '')
    return expression


# принимает строку-выражение, возвращает словарь где переменные - ключи, значение - 0
def get_variables(expression):
    expression = sorted(expression)
    variables = {}
    for symbol in expression:
        if symbol.isalpha():
            variables[symbol] = 0
    return variables


# принимает словарь с переменными и заполняет его значениями введенными с клавиатуры
def input_values(variables) -> dict:
    for key in variables.keys():
        print("Введите значение переменной", key)
        variables[key] = int(input())
    return variables


