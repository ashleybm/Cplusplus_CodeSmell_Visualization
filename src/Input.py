import SmellIdentifier
import tkinter.filedialog as filedialog
import tkinter as tk
import numpy as np
import matplotlib
matplotlib.use("TkAgg")
from matplotlib import pyplot as plt

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

cur_file_name = str()

def find_smell(name):
    for i in range(len(smell_types)):
        if (name == smell_types[i].name):
            return i
    return -1

def open_file():
    global cur_file_name
    # try to open file
    try:
        cur_file_name = filedialog.askopenfilename(filetypes =(("C++ File", "*.cpp"),("All Files","*.*")),
                           title = "Choose a file.")
        smells = SmellIdentifier.get_smells(cur_file_name)
        # clear listboxes
        for box in boxes:
            box.delete(0, tk.END)
            box.config(bg="LIGHT GREY")
        button2.config(bg="LIGHT GREEN")
        # add each smell
        for smell in smells:
            index = find_smell(smell.smell_type)
            if (index >= 0):
                boxes[index].insert(tk.END, f"line #{smell.line_num}")
                boxes[index].insert(tk.END, "    " + smell.description)
            else:
                print("Invalid Smell", smell.smell_type, smell.description)
    except Exception as e:
        button2.config(bg="GREY")
        cur_file_name = str()
        print(str(e))

def display_file():
    if (cur_file_name != ""):
        smells = SmellIdentifier.get_smells(cur_file_name)


        method_counter = 0
        parameter_counter = 0
        parameter_list_counter = 0
        duplicate_counter = 0
        class_counter = 0
        comment_counter = 0

        for smell in smells:
            if smell.smell_type == "Large Method":
                method_counter+=1
            if smell.smell_type == "Long Parameter List":
                parameter_counter+=1
            if smell.smell_type == "Duplicate Code":
                duplicate_counter+=1
            if smell.smell_type == "Large Class":
                class_counter+=1
            if smell.smell_type == "Lack of Comments":
                comment_counter+=1

        highest = max(method_counter, parameter_counter, duplicate_counter,
            class_counter, comment_counter)

        smell_counts = (method_counter, parameter_counter,
            duplicate_counter, class_counter, comment_counter)

        ind = np.arange(5)    # the x locations for the groups
        width = 0.35       # the width of the bars: can also be len(x) sequence

        p1 = plt.bar(ind, smell_counts, width, yerr=0)

        plt.ylabel('Number of Smells')
        plt.title('Visualization of Code Smells')
        plt.xticks(ind, ('Large \nMethod', 'Long \nParameter List', 'Duplicate \nCode',
            'Large \nClass', 'No \nComments'))
        if highest > 11:
            plt.yticks(np.arange(0, highest + 2, 10))
        else:
            plt.yticks(np.arange(0, 10, 1))

        plt.show()

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

    button2 = tk.Button(canvas, text="Show Graph")
    button2.config(width=20, height=2, command=display_file, bg="GREY")
    button2.grid(row=3, column=0, columnspan=5)

    window.mainloop()
