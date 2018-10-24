 
# used to split a string into segments of different meaning
class Segment:
    data = str()
    category = str()

    # constructor
    def __init__(self, category, data):
        self.category = category
        self.data = data

# used to tell which each divider should look for
class DividerType:
    start = str()
    end = str()
    expand = int()

    # constructor
    def __init__(self, start = "", end = "", expand = 0):
        self.start = start
        self.end = end
        self.expand = expand

# used to tell that a symbol is at a position in a string
class Divider(DividerType):
    pos = int()

    # constructor
    def __init__(self, pos = 0, divider_type = DividerType()):
        self.pos = pos
        self.start = divider_type.start
        self.end = divider_type.end
        self.expand = divider_type.expand

    # returns true if self is less than other
    def __lt__(self, other):
        return self.pos < other.pos

# used to manage segments and split further into words
class SegmentManager:
    segments = list()
    overhang = str()

    # code is a string of C++
    # category is the type of code 
    # splits the code into multiple segments if necessary and stores them as seperate segments
    def append(self, code, category):
        if (category == ""):
            code = self.overhang + code
            self.overhang = str()
            index = 0
            while (index < len(code)):
                index = self.append_code(code, index)
        else:
            self.segments.append(Segment(category, code))

    # code is a string of C++
    # index is the next character to check
    # adds the segment starting at index to segments
    # returns the index of the next character to check
    def append_code(self, code, index):
        # TODO add in reserved word dictionary?
        if (code[index] in {" ", "\t", "\n"}):
            return index + 1
        elif (code[index] == "#"):
            end_index = code.find("\n", index)
            if (end_index == -1):
                self.overhang = code[index:]
                return len(code)
            else:
                self.segments.append(Segment("H", code[index:end_index]))
                return end_index
        elif (code[index].isalpha() or code[index] == "_"):
            return self.add_group(code, index, is_word, "W")
        elif (code[index].isdigit()):
            return self.add_group(code, index, is_num, "N")
        elif (code[index:index + 3] in {"<<=", ">>="}):
            self.segments.append(Segment("S", code[index:index + 3]))
            return index + 3
        elif (code[index:index + 2] in {"++", "--", "==", "!=", ">=", "<=", "&&", "||",
                "<<", ">>", "+=", "-=", "*=", "/=", "%=", "|=", "^=", "->", "::"}):
            self.segments.append(Segment("S", code[index:index + 2]))
            return index + 2
        else:
            self.segments.append(Segment("S", code[index]))
            return index + 1

    # code is a string of C++
    # index is the first character
    # method is a method that returns true if you are still in the segment
    # symbol is the category of this segment
    # finds the end of a word or number
    # returns the index of the next character to check
    def add_group(self, code, index, method, symbol):
        end_index = index + 1
        while (end_index < len(code) and method(code[end_index])):
            end_index += 1
        self.segments.append(Segment(symbol, code[index:end_index]))
        return end_index

# char is a character
# returns true if char can be in a variable name
def is_word(char):
    return char.isalnum() or char == "_"

# char is a character
# returns true if char can be in a number
def is_num(char):
    return char.isalnum() or char in {"'", "."}

# code is a string of C++
# returns a list of Dividers, one for each instance of a symbol
def find_all_dividers(code):
    divider_types = {
        DividerType("//", "\n", 0),
        DividerType("/*", "*/", 2),
        DividerType("*/", "", 0),
        DividerType("\n", "", 0),
        DividerType("\"", "\"", 1),
        DividerType("\'", "\'", 1)
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
# divider_type is the divider to search for
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
# returns true if there is an odd number of backslashes before index
def is_escaped(code, index):
    prev_index = index - 1
    while (prev_index >= 0 and code[prev_index] == "\\"):
        prev_index -= 1
    return (index - prev_index) % 2 == 0

# path is a .cpp file
# returns a list of Segments, one for each group of code in the same category
def find_segments(path):
    code = get_code(path)
    segment_manager = SegmentManager()
    dividers = find_all_dividers(code)
    prev_divider = Divider()
    for divider in dividers:
        if (prev_divider.start == ""):
            if (divider.start in {"//", "/*", "\""} or
                    (divider.start == "\'" and not code[divider.pos - 1].isdigit())):
                segment_manager.append(code[prev_divider.pos:divider.pos], prev_divider.start)
                prev_divider = divider
        else:
            if (divider.start == prev_divider.end):
                segment_manager.append(code[prev_divider.pos:divider.pos + prev_divider.expand], prev_divider.start)
                prev_divider = Divider(divider.pos + prev_divider.expand)
    segment_manager.append(code[prev_divider.pos:], prev_divider.start)
    return segment_manager.segments

# returns C++ code from file at path with escaped new lines removed
def get_code(path):
    code = open(path, 'r').read()
    code = code.replace("\\\n", "")
    return code

# segments is a list of Segment
# prints all of the segments with what type of segment
def print_all_segments(segments):
    for seg in segments:
        category = str()
        if (seg.category == ""):
            category = "BLANK    "
        elif (seg.category == "\'"):
            category = "CHAR     "
        elif (seg.category == "\""):
            category = "STRING   "
        elif (seg.category == "S"):
            category = "SYMBOL   "
        elif (seg.category == "W"):
            category = "WORD     "
        elif (seg.category == "N"):
            category = "NUMBER   "
        elif (seg.category == "H"):
            category = "HEADER   "
        elif (seg.category in {"//", "/*"}):
            category = "COMMENT  "
        else:
            category = seg.category
        print(category, ":", seg.data.replace("\n", " "))

# segments is a list of Segment
# prints the minimal amount needed to still have runnable code
def print_min_segments(segments):
    prev_is_word = False
    line_empty = True
    for seg in segments:
        if (seg.category in {"", "\'", "\"", "S"}):
            print(seg.data, end = "")
            prev_is_word = False
            line_empty = False
        elif (seg.category in {"W", "N"}):
            if (prev_is_word):
                print(end = " ")
            print(seg.data, end = "")
            prev_is_word = True
            line_empty = False
        elif (seg.category in {"H"}):
            if (line_empty == False):
                print()
            print(seg.data)
            prev_is_word = False
            line_empty = True
        elif (seg.category in {"//", "/*"}):
            print(end = "")
