import SmellIdentifier
import tkinter.filedialog as filedialog
import tkinter as tk

class SmellType:
    name = str()
    fix = str()
    cause = str()

    def __init__(self, name, fix, cause):
        self.name = name
        self.fix = fix
        self.cause = cause

smell_types = [SmellType("Large Method", "Break method into multiple methods\n", "Method is 50% larger\nthan the average method length"),
                 SmellType("Long Parameter List", "Break method into multiple methods\n", "Method contains 5 or more parameters\n"),
                 SmellType("Duplicate Code", "Turn duplicate code into a function\n and call it in multiple places", "Code segments contain the same text\nfor 5 or more lines"),
                 SmellType("Large Class", "Break class into sub/super class\n", "Class contains 25% more methods/variables\nthan the average count"),
                 SmellType("Lack of Comments", "Add Comments before Class or Method\n", "Identify Classes or Methods\nthat do not have comments")]

labels = list()
boxes = list()

def find_smell(name):
    for i in range(len(smell_types)):
        if (name == smell_types[i].name):
            return i
    return -1

def open_file():
    # try to open file
    try:
        name = filedialog.askopenfilename(filetypes =(("C++ File", "*.cpp"),("All Files","*.*")),
                           title = "Choose a file.")
        smells = SmellIdentifier.get_smells(name)
        
        # clear listboxes
        for box in boxes:
            box.delete(0, tk.END)
            box.config(bg="LIGHT GREY")
        # add each smell
        for smell in smells:
            index = find_smell(smell.smell_type)
            if (index >= 0):
                boxes[index].insert(tk.END, f"line #{smell.line_num}")
                boxes[index].insert(tk.END, "    " + smell.description)
            else:
                print("Invalid Smell", smell.smell_type, smell.description)
    except Exception as e:
        print(str(e))

if (__name__ == "__main__"):

    window = tk.Tk()
    window.config(width=1300, height=500)
    window.title("C++ Code Smells")
    #window.state("zoomed")

    canvas = tk.Canvas(window)
    canvas.place(relx=0.5, rely=0.0, anchor=tk.N)

    button = tk.Button(canvas, text="Choose File")
    button.config(width=20, height=2, command=open_file, bg="GREEN")
    button.grid(row=0, column=0, columnspan=5)

    for i, smell_type in enumerate(smell_types):
        header = f"{smell_type.name}\n\n{smell_type.cause}\n\nSolution:\n{smell_type.fix}"
        labels.append(tk.Label(canvas, text=header))
        labels[i].grid(row=1, column=i)
        boxes.append(tk.Listbox(canvas, width=40, height=10, bg="GREY"))
        boxes[i].grid(row=2, column=i)

    window.mainloop()
