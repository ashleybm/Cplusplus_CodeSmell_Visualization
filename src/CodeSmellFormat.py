#used to identify a smell type and define the issue for later reporting
class SmellType:
    name = str()
    fix = str()
    cause = str()
    scope_applied = str()

    def __init__(self, name, fix, cause, scope):
        self.name = this.name
        self.fix = this.fix
        self.cause = this.cause
        self.scope_applied = this.scope

def gen_list_code_smells():
    smellType = [SmellType("Long Method", "Break the method down into multiple methods", "Method is 50% larger than the average method length", "method"),
                 SmellType("Long Parameter List", "Break method into multiple methods", "Method contains 5 or more parameters", "method"),
                 SmellType("Duplicate Code", "Turn duplicate code into a function and call it in multiple places.", "Code segments contain the same text for 5 or more lines", "anywhere"),
                 SmellType("Large Class", "Break class into sub/super class", "Classes that contain 25% more methods/variables from the average count", ""),
                 SmellType("Lack of Comments", "Add Comments before Classes are Methods.", "Identify Classes or Methods taht do not have comments.")]

    smellDict = dict([(s.name, s.fix, s.cause) for s in smellType])


def get_code_smell(smell_type):
        return smellDict[smell_type]
