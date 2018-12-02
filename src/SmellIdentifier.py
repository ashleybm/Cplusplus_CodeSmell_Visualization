import DataStructure

class CodeSmell:
    def __init__(self, smell_type, expression, description):
        self.smell_type = smell_type
        self.line_num = expression.get_line_num()
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
            smells.append(CodeSmell("Large Method", methods[index], "Contains " + str(length) + " lines which is above the max of " + str(max_length)))
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

def get_smells(path):
    data_structure = DataStructure.parse_file(path)
    smells = list()
    smells += get_long_methods(data_structure)
    return smells

if (__name__ == "__main__"):
    smells = get_smells("main2.cpp")
    for smell in smells:
        print("Line:", smell.line_num, ":", smell.smell_type, ":", smell.description)
