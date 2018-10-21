import CodeParse

class Expression:
    segments = list()
    def __init__(self, segments):
        self.segments = segments.copy()

class Scope(Expression):
    category = str()
    expressions = list()

    def __init__(self, segments, expressions):
        super().__init__(segments)
        self.expressions = expressions

# segments is a list of Segments
# returns a tree data structure
def create_tree(segments, index):

    expressions = list()
    acc_segments = list()

    while (index < len(segments)):
        segment = segments[index]
        acc_segments.append(segment)
        if (segment.category == "S"):
            if (segment.data == "{"):
                sub_expressions, index = create_tree(segments, index + 1)
                expressions.append(Scope(acc_segments, sub_expressions))
                acc_segments.clear()
            elif (segment.data == "}"):
                # TODO check for extra ;
                return expressions, index
            elif (segment.data == ";"):
                expressions.append(Expression(acc_segments))
                acc_segments.clear()
        index += 1
    return expressions, index

# TODO write description
def print_all_segments(segments, tabs):
    print(tabs * "\t", end = "")
    for segment in segments:
        if (segment.category not in {"//", "/*"}):
            print(segment.data, end = " ")
    print()

# TODO write description
def print_all_expressions(expressions, tabs):
    for expression in expressions:
        print_all_segments(expression.segments, tabs + 1)
        if (type(expression) == Scope):
            print_all_expressions(expression.expressions, tabs + 1)

# main
if (__name__ == '__main__'):

    segments = CodeParse.find_segments("main.cpp")

    scope = create_tree(segments, 0)[0]
    print_all_expressions(scope, 0)
