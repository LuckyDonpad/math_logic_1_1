class Expression(object):
    def __init__(self, infix=''):
        self.infix = infix
        self.postfix = self.get_postfix(infix)
        self.variables_dict = self.get_variables_dict()

    # принимает выражение в инфиксной записи и возвращает это выражение в ОПЗ
    def get_postfix(self, infix):
        infix = list(infix)
        output = []
        stack = []
        # прочитать токен
        for token in infix:
            token = Token(token)
            # Если токен — число или переменная, то добавить его в очередь вывода
            if token.is_variable() or token.isnumeric():
                output.append(token)
            # Если токен — операция op1, то
            elif token.is_operation():
                # Пока на вершине стека присутствует токен-операция op2, и у op1 приоритет
                # меньше либо равен приоритету op2, переложить op2 из стека в выходную
                # очередь.
                while stack and Token(stack[-1]).is_operation() and (
                        token.get_priority() <= Token(stack[-1]).get_priority()):
                    output.append(Token(stack.pop()))
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
            token = Token(token)
            # Если токен на вершине стека — открывающая скобка, то в выражении
            # присутствует незакрытая скобка
            if token.token == '(':
                raise SyntaxError("closing par is missing")
            # Переложить токен-операцию из стека в выходную очередь
            output.append(stack.pop())
        return output

    # принимает строку-выражение, возвращает словарь где переменные - ключи, значение - 0
    def get_variables_dict(self):
        expression = sorted(self.infix)
        variables = {}
        for symbol in expression:
            if symbol.isalpha():
                variables[symbol] = 0
        return variables

    def input_values(self):
        for key in self.variables_dict.keys():
            print("Введите значение переменной", key)
            self.variables_dict[key] = int(input())

    def evaluate_binary(self, a, op, b):
        if op == "&":
            return a and b
        elif op == '|':
            return a or b
        elif op == '>':
            return not a or b
        elif op == '~':
            return (not a or b) and (a or not b)
        else:
            raise Exception

    def evaluate_unary(self, a, op):
        if op == '-':
            return not a
        else:
            raise Exception

    def evaluate(self):
        stack = []
        for token in self.postfix:
            token = Token(token)
            if token.is_variable():
                stack.append(self.variables_dict[token.token])
            elif token.is_operation():
                if token.is_binary_operation():
                    b = stack.pop()
                    a = stack.pop()
                    stack.append(self.evaluate_binary(a, token.token, b))
                elif token.is_unary_operation():
                    a = stack.pop()
                    stack.append(self.evaluate_unary(a, token.token))
                else:
                    raise Exception
        return stack[-1]


class Token(str):
    def __init__(self, token):
        self.token = token.upper().replace(' ', '')

    # Принимает символ
    # Возвращает значение Истина, если токен - операция, иначе Ложь
    def is_operation(self):
        assert len(self.token) == 1
        return self.token in "~>|&-"

    def is_variable(self):
        assert len(self.token) == 1
        return self.token.isalpha()

    # Принимает символ обозначающий операцию
    # Возвращает приоритет операции
    # приоритет - число от одного до пяти включительно: чем больше число, тем выше приоритет
    def get_priority(self):
        assert len(self.token) == 1
        if not Token.is_operation(self):
            raise SyntaxError("Undefined operation")
        return "~>|?-".find(self.token) + 1

    def is_binary_operation(self):
        return self.token in "&|>~"

    def is_unary_operation(self):
        return self.token == '-'


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


# принимает словарь с переменными и заполняет его значениями введенными с клавиатуры
def input_values(variables) -> dict:
    for key in variables.keys():
        print("Введите значение переменной", key)
        variables[key] = int(input())
    return variables


expression = input_expression()
expression = Expression(expression)
expression.input_values()
print(expression.evaluate())
