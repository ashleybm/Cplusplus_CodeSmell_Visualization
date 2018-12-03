import SmellIdentifier
from tkinter import messagebox
from tkinter.filedialog import askopenfilename
from tkinter import *
from tkinter import ttk

smell_types = ["Large Method", "Long Parameter List", "Duplicate Code", "Large Class", "Lack of Comments"]
boxes = list()
labels = list()

def OpenFile():
    # try to open file
    try:
        name = askopenfilename(filetypes =(("C++ File", "*.cpp"),("All Files","*.*")),
                           title = "Choose a file.")
        smells = SmellIdentifier.get_smells(name)
        # clear listboxes
        for box in boxes:
            box.delete(0, END)
            box.config(bg="LIGHT GREY")
        
        button.config(bg="LIGHT GREY")
        for smell in smells:
            try:
                index = smell_types.index(smell.smell_type)
                boxes[index].insert(END, f"line #{smell.line_num}")
                boxes[index].insert(END, "    " + smell.description)
            except:
                print("Invalid Smell", smell.smell_type, smell.description)
    except Exception as e:
        print(str(e))

if (__name__ == "__main__"):

    window = Tk()
    window.config(width=1500, height=500)
    window.title("C++ Code Smells")
    window.state("zoomed")

    canvas = Canvas(window)
    canvas.place(relx=0.5, rely=0.0, anchor=N)

    button = Button(canvas, text="Choose File")
    button.config(width=20, height=2, command=OpenFile, bg="GREEN")
    button.grid(row=0, column=0, columnspan=5)

    for i in range(len(smell_types)):
        labels.append(Label(canvas, text=smell_types[i]))
        labels[i].grid(row=1, column=i)
        boxes.append(Listbox(canvas, width=50, height=20, bg="GREY"))
        boxes[i].grid(row=2, column=i)

    window.mainloop()
