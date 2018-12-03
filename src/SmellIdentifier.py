import DataStructure

class CodeSmell:
    def __init__(self, smell_type, expression, description):
        self.smell_type = smell_type
        self.line_num = expression.get_line_num()
        self.description = description

    def __lt__(self, other):
        return self.line_num < other.line_num

def get_large_methods(scope):
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
            perc = 100 * length / average - 100
            smells.append(CodeSmell("Large Method", methods[index], f"{perc:.0f}% above average of {max_length:.0f}"))
    return smells

def get_large_classes(scope):
    items = get_classes(scope)
    lengths = list()
    for item in items:
        lengths.append(len(item.expressions))
    smells = list()
    average = 0
    for length in lengths:
        average += length
    average /= len(items)
    max_length = average * 1.25
    for index, length in enumerate(lengths):
        if (length > max_length):
            perc = 100 * length / average - 100
            smells.append(CodeSmell("Large Class", items[index], f"{perc:.0f}% above average of {max_length:.0f}"))
    return smells

def get_lack_comments(scope):
    methods = get_methods(scope) + get_classes(scope)
    smells = list()
    for method in methods:
        for segment in method.segments:
            if (segment.category in {"/*", "//"}):
                break
        else:
            smells.append(CodeSmell("Lack of Comments", method, method.as_string()))
    return smells

def get_duplicate_code(scope):
    expressions = get_expressions(scope)
    smells = list()
    for i in range(len(expressions)):
        for j in range(i + 1, len(expressions) - 4):
            for k in range(5):
                if (expressions[i + k] != expressions[j + k] or expressions[i + k].is_header()):
                    break
            else:
                smells.append(CodeSmell("Duplicate Code", expressions[i], "with line #" + str(expressions[j].get_line_num())))
    return smells

def get_expressions(scope):
    expressions = list()
    for expression in scope:
        if (type(expression) == DataStructure.Scope):
            expressions += get_expressions(expression.expressions)
        else:
            expressions.append(expression)
    return expressions

def get_methods(scope):
    methods = list()
    for expression in scope:
        if (type(expression) == DataStructure.Scope):
            if (expression.category == "method"):
                methods.append(expression)
            else:
                methods += get_methods(expression.expressions)
    return methods

def get_classes(scope):
    methods = list()
    for expression in scope:
        if (type(expression) == DataStructure.Scope):
            if (expression.category == "class"):
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
    smells += get_large_methods(data_structure)
    smells += get_large_classes(data_structure)
    smells += get_lack_comments(data_structure)
    smells += get_duplicate_code(data_structure)
    smells.sort()
    return smells

if (__name__ == "__main__"):
    smells = get_smells("main2.cpp")
    for smell in smells:
        print("Line:", smell.line_num, ":", smell.smell_type, ":", smell.description)
