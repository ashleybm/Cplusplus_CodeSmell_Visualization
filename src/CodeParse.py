
# used to split a string into segments of different meaning
class Segment:
    data = str()
    category = str()

    # constructor
    def __init__(self, code, prev_div, cur_div):
        self.data = code[prev_div.pos:cur_div.pos + len(prev_div.end)]
        self.category = prev_div.start

# used to tell that a symbol is at a position in a string
class Divider:
    pos = int()
    start = str()
    end = str()

    # constructor
    def __init__(self, pos, start, end):
        self.pos = pos
        self.start = start
        self.end = end

    # returns true if self is less than other
    def __lt__(self, other):
        return self.pos < other.pos

# code is a string of C++
# returns a list of Dividers, one for each instance of a symbol
def find_all_dividers(code):
    dividers = list()
    to_end = {"//":"\n", "/*":"*/", "\"":"\"", "\'":"\'", "*/":"", "\n":""}
    for symbol in {"//", "/*", "*/"}:
        dividers += find_dividers(code, symbol, to_end[symbol])
    for symbol in {"\"", "\'", "\n"}:
        pos_dividers = find_dividers(code, symbol, to_end[symbol])
        dividers += (d for d in pos_dividers if not is_escaped(code, d.pos))
    dividers.sort()
    return dividers

# code is a string of C++
# symbol is a string to look for
# returns a list of Dividers, one for each instance of symbol
def find_dividers(code, symbol, end):
    dividers = list()
    index = code.find(symbol, 0)
    while (0 <= index and index < len(code)):
        dividers.append(Divider(index, symbol, end))
        index = code.find(symbol, index + 1)
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
    prev_divider = Divider(0, "", "")
    for divider in dividers:
        if (prev_divider.start == ""):
            if (divider.start in {"//", "/*", "\""} or
                    (divider.start == "\'" and not code[divider.pos - 1].isdigit())):
                segments.append(Segment(code, prev_divider, divider))
                prev_divider = divider
        else:
            if (divider.start == prev_divider.end):
                segments.append(Segment(code, prev_divider, divider))
                prev_divider.pos = divider.pos + len(divider.start)
                prev_divider.start = ""
                prev_divider.end = ""
    segments.append(Segment(code, prev_divider, Divider(len(code), "", "")))
    return segments

# main
if (__name__ == '__main__'):

    path = "main.cpp"
    code = open(path, 'r').read()

    segments = find_segments(code)

    for seg in segments:
        if (seg.category in {"", "\'", "\""}):
            print(seg.data, end = "")
        elif (seg.category in {"//", "/*"}):
            print()
