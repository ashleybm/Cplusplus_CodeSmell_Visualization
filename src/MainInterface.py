import DataStructure

class CodeSmell:
    description = str()

    def get_line_num(self):
        return self.expression.get_line_num()

    def __init__(self, expression, description):
        self.expression = expression
        self.description = description

def get_long_methods(scope):
    methods = get_methods(scope)
    lengths = list()
    for method in methods:
        lengths.append(count_expressions(method.expressions))
    smells = list()
    average = 0
    for length in lengths:
        average += length
    average /= len(methods)
    max_length = average * 1.5
    for index, length in enumerate(lengths):
        if (length > max_length):
            smells.append(CodeSmell(methods[index], "Large Method: Contains " + str(length) + " lines which is above the max of " + str(max_length)))
    return smells

def get_methods(scope):
    methods = list()
    for expression in scope:
        if (type(expression) == DataStructure.Scope):
            if (expression.category == "method"):
                methods.append(expression)
            else:
                methods += get_methods(expression.expressions)
    return methods

def count_expressions(scope):
    count = 0
    for expression in scope:
        count += 1
        if (type(expression) == DataStructure.Scope):
            count += count_expressions(expression.expressions)
    return count

if (__name__ == "__main__"):
    dataStructure = DataStructure.parse_file("main2.cpp")

    smells = list()
    smells += get_long_methods(dataStructure)

    for smell in smells:
        print("Line:", smell.get_line_num(), ":", smell.description, smell.expression.as_string())
