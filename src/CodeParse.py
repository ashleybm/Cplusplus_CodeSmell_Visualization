
# used to split a string into segments of different meaning
class Segment:
    data = str()
    category = str()

    # constructor
    def __init__(self, code, prev_div, cur_div):
        self.data = code[prev_div.pos:cur_div.pos + len(prev_div.end)]
        self.category = prev_div.start

# used to tell which each divider should look for
class DividerType:
    start = str()
    end = str()

    # constructor
    def __init__(self, start = "", end = ""):
        self.start = start
        self.end = end

# used to tell that a symbol is at a position in a string
class Divider:
    pos = int()
    start = str()
    end = str()

    # constructor
    def __init__(self, pos = 0, divider_type = DividerType()):
        self.pos = pos
        self.start = divider_type.start
        self.end = divider_type.end

    # returns true if self is less than other
    def __lt__(self, other):
        return self.pos < other.pos

# code is a string of C++
# returns a list of Dividers, one for each instance of a symbol
def find_all_dividers(code):
    divider_types = {
        DividerType("//", "\n"),
        DividerType("/*", "*/"),
        DividerType("*/", ""),
        DividerType("\n", ""),
        DividerType("\"", "\""),
        DividerType("\'", "\'")
    }
    dividers = list()
    for divider_type in divider_types:
        if (divider_type.start in {"//", "/*", "*/", "\n"}):
            dividers += find_dividers(code, divider_type)
    for divider_type in divider_types:
        if (divider_type.start in {"\"", "\'"}):
            possible_dividers = find_dividers(code, divider_type)
            dividers += (d for d in possible_dividers if not is_escaped(code, d.pos))
    dividers.sort()
    return dividers

# code is a string of C++
# symbol is a string to look for
# returns a list of Dividers, one for each instance of symbol
def find_dividers(code, divider_type):
    dividers = list()
    index = code.find(divider_type.start, 0)
    while (0 <= index and index < len(code)):
        dividers.append(Divider(index, divider_type))
        index = code.find(divider_type.start, index + 1)
    return dividers

# code is a string of C++
# index is the index of a character that could be escaped
# returns true if there is an even number of backslashes before index
def is_escaped(code, index):
    prev_index = index - 1
    while (prev_index >= 0 and code[prev_index] == "\\"):
        prev_index -= 1
    return (index - prev_index) % 2 == 1

# code is a string of C++
# returns a list of Segments, one for each group of code in the same category
def find_segments(code):
    segments = list()
    dividers = find_all_dividers(code)
    prev_divider = Divider()
    for divider in dividers:
        if (prev_divider.start == ""):
            if (divider.start in {"//", "/*", "\""} or
                    (divider.start == "\'" and not code[divider.pos - 1].isdigit())):
                segments.append(Segment(code, prev_divider, divider))
                prev_divider = divider
        else:
            if (divider.start == prev_divider.end):
                segments.append(Segment(code, prev_divider, divider))
                prev_divider = Divider(divider.pos + len(divider.start))
    segments.append(Segment(code, prev_divider, Divider(len(code))))
    return segments

# returns C++ code from file at path with escaped new lines removed
def get_code(path):
    code = open(path, 'r').read()
    code = code.replace("\\\n", "")
    return code

# main
if (__name__ == '__main__'):

    path = "main.cpp"
    code = get_code(path)

    segments = find_segments(code)

    for seg in segments:
        if (seg.category in {"", "\'", "\""}):
            print(seg.data, end = "")
        elif (seg.category in {"//", "/*"}):
            print()
