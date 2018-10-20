import CodeParse

class Expression:
    segments = list()
    def __init__(self):
        self.segments = list()

class Scope(Expression):
    start = int()
    end = int()

    def __init__(self, start):
        self.start = start

# segments is a list of Segments
# returns a tree data structure
def create_tree(segments, start):

    # TODO turn segments into a tree data structure
    scope = Scope(start)
    expression = Expression()
    index = start
    while (index < len(segments)):
        if (segments[index].category == "S" and segments[index].data in {"{", ";", "}"}):
            if (segments[index].data == "{"):
                scope.segments.append(create_tree(segments, index + 1))
                index = scope.segments[-1].end
            elif (segments[index].data == "}"):
                scope.end = index
                return scope
            elif (segments[index].data == ";"):
                expression.segments.append(segments[index])
                scope.segments.append(expression)
                expression = Expression()
        else:
            expression.segments.append(segments[index])
        index += 1
    return scope

# main
if (__name__ == '__main__'):

    segments = CodeParse.find_segments("main.cpp")

    scope = create_tree(segments, 0)
    tabs = 0



    """for e in tree:
        for i in range(tabs):
            print(end="\t")
        for s in e:
            if (s.category not in {"/*", "//", "H"}):
                print(s.data, end=" ")
        if (e[len(e) - 1].data == "{"):
            tabs += 1
        elif (e[len(e) - 1].data == "}"):
            tabs -= 1
        print()"""
