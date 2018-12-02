import CodeParse

# Expressions are a list of segments that do not have relevance
# to the structure of the actual code. Generally, these also
# do not affect our code smell identification.
class Expression:
    segments = list()
    def __init__(self, segments):
        self.segments = segments.copy()

    def get_line_num(self):
        if (len(self.segments) == 0):
            return -1
        return self.segments[0].line

    def as_string(self):
        data = str()
        for segment in self.segments:
            if (segment.category not in {"//", "/*"}):
                data += segment.data + " "
        return data

# A Scope is generally something within brackets, or a loop (without brackets)
# where we can expect something to happen more than once/or not at all.
# Style generally dictates that these are things that are indented from code.
class Scope(Expression):
    category = str()
    expressions = list()

    def __init__(self, segments, expressions, category = ""):
        super().__init__(segments)
        self.expressions = expressions
        self.category = category

# This Method identifies whether or not the segements contain the
# key words struct or class, which lets us identify the function of
# the potential scope.
def is_class(segments):
    for segment in segments:
        if (segment.category == "W" and segment.data in {"class", "struct"}):
            return True
    return False

# This function parses segements with parenthesis to identify the beginning
# and end of parenthesis sets.
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

# This function is recursively called to identify the beginning and end of
# scopes identified by brackets (ie {...}) or single lined scopes {ie: ...;}
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

# This function is used to parse a segment list if it is identified as a
# method. This is done by identifying the parameters, body, and name of the
# function. This then returns the formated expression list and new index.
def create_method(segments, index):

    expressions = list()
    acc_segments = list()

    while (index < len(segments)):
        segment = segments[index]
        acc_segments.append(segment)
        if (segment.category == "S"):
            if (segment.data == "{"):
                sub_expressions, index = create_method(segments, index + 1)
                expressions.append(Scope(acc_segments, sub_expressions, "method"))
                acc_segments.clear()
            elif (segment.data == "}"):
                acc_segments.pop()
                if (len(acc_segments) > 0):
                    expressions.append(Expression(acc_segments))
                return expressions, index
            elif (segment.data == ";"):
                expressions.append(Expression(acc_segments))
                acc_segments.clear()
        elif (segment.category == "W"):
            if (segment.data in {"if", "while", "for", "switch"}):
                sub_segments, index = parse_paren(segments, index + 1)
                acc_segments += sub_segments
                sub_scope, index = parse_scope(acc_segments, segments, index + 1)
                if (segment.data in {"if", "switch"}):
                    sub_scope.category = "conditional"
                else:
                    sub_scope.category = "loop"
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
                        sub_scope.category = "conditional"
                        expressions.append(sub_scope)
                        acc_segments.clear()
                        break
                    elif (segments[index].category in {"//", "/*"}):
                        acc_segments.append(segments[index])
                    else:
                        sub_scope, index = parse_scope(acc_segments, segments, index)
                        sub_scope.category = "conditional"
                        expressions.append(sub_scope)
                        acc_segments.clear()
                        break
                    index += 1
            elif (segment.data == "do"):
                sub_scope, index = parse_scope(acc_segments, segments, index + 1)
                sub_scope.category = "loop"
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
                acc_segments.pop()
                if (is_class(acc_segments)):
                    sub_expressions, index = create_tree(segments, index + 1)
                    expressions.append(Scope(acc_segments, sub_expressions, "class"))
                    acc_segments.clear()
                else: # method OR array?
                    sub_expressions, index = create_method(segments, index + 1)
                    expressions.append(Scope(acc_segments, sub_expressions, "method"))
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

# Prints Segments with the corresponding lines tabs.
def print_min_segments(segments, tabs):
    print(tabs * "\t", end = "")
    for segment in segments:
        if (segment.category not in {"//", "/*"}):
            print(segment.data, end = " ")
    print()

# Prints Segments by calling "print_min_segments", this function keeps track
# of the lines amount of tabs.
def print_all_segments(segments, tabs):
    for segment in segments:
        print(tabs * "\t", end = "")
        print(segment.data)
    print()

# Prints all expressions by printing all segments with an expression call.
def print_all_expressions(expressions, tabs, print_segments):
    for expression in expressions:
        print_segments(expression.segments, tabs + 1)
        if (type(expression) == Scope):
            print_all_expressions(expression.expressions, tabs + 1, print_segments)

# TODO
def parse_file(path):
    segments = CodeParse.find_segments(path)
    scope = create_tree(segments, 0)[0]
    return scope

# main
if (__name__ == '__main__'):

    segments = CodeParse.find_segments("main.cpp")

    scope = create_tree(segments, 0)[0]
    print_all_expressions(scope, 0, print_min_segments)
