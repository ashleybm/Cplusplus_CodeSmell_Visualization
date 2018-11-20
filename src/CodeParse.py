
class Segment:
    """
    used to split a string into segments of different meaning
        data - chracters from file that are in this segment
        line - line number this segment starts on
        category - how the characters should be dealt with
            '' - undefined code (internal use only)
            'H' - header
            'S' - symbol
            'W' - word
            'N' - number literal
            '/*' or '//' - comment
            '"' - string literal
            ''' - character literal
    """

    def __init__(self, category, line, data):
        self.category = category
        self.line = line
        self.data = data

class DividerType:
    """
    a type of divider that starts a new segment of code
        start - starting character
        end - ending character
        expand - does this divider expand into the end character
    """

    def __init__(self, start = "", end = "", expand = 0):
        self.start = start
        self.end = end
        self.expand = expand

class Divider(DividerType):
    """
    used to tell that a symbol is at a position in a string
        pos - the position of this divider
        start - the starting symbol
        end - the ending symbol
        expand - does this divider expand into the end character
    """

    def __init__(self, pos = 0, divider_type = DividerType()):
        self.pos = pos
        self.start = divider_type.start
        self.end = divider_type.end
        self.expand = divider_type.expand

    def __lt__(self, other):
        """
        overrides < op, returns true if self is less than other
        """
        return self.pos < other.pos

class SegmentManager:
    """
    used to manage segments and split further into words
        segments - individual segments between each type of code
        overhand - remainder segment not completed
        line_num - line number next segment will be on
    """

    def __init__(self):
        self.segments = list()
        self.overhang = str()
        self.line_num = 1

    def append(self, code, category):
        """
        splits the code into multiple segments if necessary and stores them as seperate segments
            code - a string of C++
            category - the type of code {"", "//", "/*", "\"", "\'"}
        """
        if (category == ""):
            code = self.overhang + code
            self.overhang = str()
            index = 0
            while (index < len(code)):
                index = self.append_code(code, index)
        else:
            self.segments.append(Segment(category, self.line_num, code))
            self.line_num += code.count("\n")

    def append_code(self, code, index):
        """
        adds the segment starting at index to segments,
        returns the index of the next character to check
            code - string of C++
            index - next character to check
        """
        if (code[index] == "\n"):
            self.line_num += 1
            return index + 1
        if (code[index] in {" ", "\t"}):
            return index + 1
        elif (code[index] == "#"):
            end_index = code.find("\n", index)
            if (end_index == -1):
                self.overhang = code[index:]
                return len(code)
            else:
                self.segments.append(Segment("H", self.line_num, code[index:end_index]))
                return end_index
        elif (code[index].isalpha() or code[index] == "_"):
            return self.add_group(code, index, is_word, "W")
        elif (code[index].isdigit()):
            return self.add_group(code, index, is_num, "N")
        elif (code[index:index + 3] in {"<<=", ">>="}):
            self.segments.append(Segment("S", self.line_num, code[index:index + 3]))
            return index + 3
        elif (code[index:index + 2] in {"++", "--", "==", "!=", ">=", "<=", "&&", "||",
                "<<", ">>", "+=", "-=", "*=", "/=", "%=", "|=", "^=", "->", "::"}):
            self.segments.append(Segment("S", self.line_num, code[index:index + 2]))
            return index + 2
        else:
            self.segments.append(Segment("S", self.line_num, code[index]))
            return index + 1


    def add_group(self, code, index, method, symbol):
        """
        finds the end of a word or number,
        returns the index of the next character to check
            code - a string of C++
            index - the first character
            method - a method that returns true if you are still in the segment
            symbol - the category of this segment
        """
        end_index = index + 1
        while (end_index < len(code) and method(code[end_index])):
            end_index += 1
        self.segments.append(Segment(symbol, self.line_num, code[index:end_index]))
        return end_index

def is_word(char):
    """
    returns true if char can be in a variable name
        char - a character
    """
    return char.isalnum() or char == "_"

def is_num(char):
    """
    returns true if char can be in a number
        char - a character
    """
    return char.isalnum() or char in {"'", "."}

def find_all_dividers(code):
    """
    returns a list of Dividers, one for each isntance of a symbol
        code - a string of C++
    """
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

def find_dividers(code, divider_type):
    """
    returns a list of Dividers, one for each instance of symbol
        code - a string of C++
        divider_type - the divider to search for
    """
    dividers = list()
    index = code.find(divider_type.start, 0)
    while (0 <= index and index < len(code)):
        dividers.append(Divider(index, divider_type))
        index = code.find(divider_type.start, index + 1)
    return dividers

def is_escaped(code, index):
    """
    returns true if there is an odd number of backslashes before index
        code - a string of C++
        index - the index for a character that could be escaped
    """
    prev_index = index - 1
    while (prev_index >= 0 and code[prev_index] == "\\"):
        prev_index -= 1
    return (index - prev_index) % 2 == 0

def find_segments(path):
    """
    returns a list of Segments, one for each group of code in the same category
        path - a .cpp file
    """
    code = open(path, 'r').read()
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
            if (divider.start == prev_divider.end and (divider.start != "\n" or code[divider.pos - 1] != "\\")):
                segment_manager.append(code[prev_divider.pos:divider.pos + prev_divider.expand], prev_divider.start)
                prev_divider = Divider(divider.pos + prev_divider.expand)
    segment_manager.append(code[prev_divider.pos:], prev_divider.start)
    return segment_manager.segments

def print_all_segments(segments):
    """
    prints all of the segments with what type of segment they are
        segments - list of Segments
    """
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
        print(seg.line, ":", category, ":", seg.data.replace("\n", " "))

def print_min_segments(segments):
    """
    prints the minimal amount needed to still have runnable code
        segments - list of Segments
    """
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
