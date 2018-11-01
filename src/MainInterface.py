import DataStructure

class CodeSmell:
    description = str()

    def __init__(self, expression, description):
        self.expression = expression
        self.description = description

def get_long_methods(scope):
    method_lengths = parse_method_lengths(scope)
    smells = list()
    average = 0
    for method in method_lengths:
        average += method[1]
    average /= len(method_lengths)
    max_length = average * 1.5
    for method in method_lengths:
        if (method[1] > max_length):
            smells.append(CodeSmell(method[0], "Large Method: Contains " + str(method[1]) + " lines which is above the max of " + str(max_length)))
    return smells

def parse_method_lengths(scope):
    method_lengths = list()
    for expression in scope:
        if (type(expression) == DataStructure.Scope):
            if (expression.category == "method"):
                count = count_expressions(expression.expressions)
                method_lengths.append([expression, count])
            else:
                method_lengths += parse_method_lengths(expression.expressions)
    return method_lengths

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
        print(smell.description, smell.expression.as_string())
