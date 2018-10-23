import CodeParse

# TODO desc
class Expression:
    segments = list()
    def __init__(self, segments):
        self.segments = segments.copy()

# TODO desc
class Scope(Expression):
    category = str()
    expressions = list()

    def __init__(self, segments, expressions):
        super().__init__(segments)
        self.expressions = expressions

# TODO desc
def is_class(segments):
    for segment in segments:
        if (segment.category == "W" and segment.data in {"class", "struct"}):
            return True
    return False

# TODO desc
def parse_paren(segments, index):
    depth = 0
    acc_segments = list()
    while (index < len(segments)):
        acc_segments.append(segments[index])
        if (segments[index].category == "S"):
            if (segments[index].data == "("):
                depth += 1
            elif (segments[index].data == ")"):
                depth -= 1
                if (depth == 0):
                    return acc_segments, index
        index += 1
    return acc_segments, index

# TODO desc
# expecting {...} or ...;
def parse_scope(acc_segments, segments, index):
    while (index < len(segments)):
        if (segments[index].category == "S" and segments[index].data == "{"):
            # read in a scope thingy {}
            sub_expressions, index = create_method(segments, index + 1)
            scope = Scope(acc_segments, sub_expressions)
            return scope, index
        elif (not segments[index].category in {"//", "/*"}):
            sub_segments = list()
            while (index < len(segments)):
                sub_segments.append(segments[index])
                if (segments[index].category == "S" and segments[index].data == ";"):
                    scope = Scope(acc_segments, [Expression(sub_segments)])
                    return scope, index
                index += 1
        else:
            acc_segments.append(segments[index])
        index += 1

# TODO desc
def create_method(segments, index):

    expressions = list()
    acc_segments = list()

    while (index < len(segments)):
        segment = segments[index]
        acc_segments.append(segment)
        if (segment.category == "S"):
            if (segment.data == "{"):
                sub_expressions, index = create_method(segments, index + 1)
                expressions.append(Scope(acc_segments, sub_expressions))
                acc_segments.clear()
            elif (segment.data == "}"):
                return expressions, index
            elif (segment.data == ";"):
                expressions.append(Expression(acc_segments))
                acc_segments.clear()
        elif (segment.category == "W"):
            if (segment.data in {"if", "while", "for", "switch"}):
                sub_segments, index = parse_paren(segments, index + 1)
                acc_segments += sub_segments
                sub_scope, index = parse_scope(acc_segments, segments, index + 1)
                expressions.append(sub_scope)
                acc_segments.clear()
            elif (segment.data == "else"):
                index += 1
                while (index < len(segments)):
                    if (segments[index].category == "W" and segments[index].data == "if"):
                        acc_segments.append(segments[index])
                        sub_segments, index = parse_paren(segments, index + 1)
                        acc_segments += sub_segments
                        sub_scope, index = parse_scope(acc_segments, segments, index + 1)
                        expressions.append(sub_scope)
                        acc_segments.clear()
                        break
                    elif (segments[index].category in {"//", "/*"}):
                        acc_segments.append(segments[index])
                    else:
                        sub_scope, index = parse_scope(acc_segments, segments, index)
                        expressions.append(sub_scope)
                        break
                    index += 1
            elif (segment.data == "do"):
                sub_scope, index = parse_scope(acc_segments, segments, index + 1)
                index += 1
                while (index < len(segments) and not (segments[index].category == "W" and segments[index].data == "while")):
                    sub_scope.segments.append(segments[index])
                    index += 1
                sub_scope.segments.append(segments[index])
                sub_segments, index = parse_paren(segments, index + 1)
                sub_scope.segments += sub_segments
                index += 1
                while (index < len(segments) and not (segments[index].category == "S" and segments[index].data == ";")):
                    sub_scope.segments.append(segments[index])
                    index += 1
                expressions.append(sub_scope)
                acc_segments.clear()
        elif (segment.category == "H"):
            expressions.append(Expression(acc_segments))
            acc_segments.clear()
        index += 1
    return expressions, index

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
                if (is_class(acc_segments)):
                    sub_expressions, index = create_tree(segments, index + 1)
                    expressions.append(Scope(acc_segments, sub_expressions))
                    acc_segments.clear()
                else: # method OR array?
                    sub_expressions, index = create_method(segments, index + 1)
                    expressions.append(Scope(acc_segments, sub_expressions))
                    acc_segments.clear()
            elif (segment.data == "}"):
                return expressions, index
            elif (segment.data == ";"):
                expressions.append(Expression(acc_segments))
                acc_segments.clear()
        elif (segment.category == "H"):
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
