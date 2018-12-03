import SampleOutput
import SmellIdentifier
from tkinter import messagebox
from tkinter.filedialog import askopenfilename
from tkinter import *
from tkinter import ttk

largeMethod = Tk()
longParameterList = Tk()
duplicateCode = Tk()
largeClass = Tk()
lackOfComments = Tk()
#root = Tk(  )

#This is where we lauch the file manager bar.
def OpenFile():
    name = askopenfilename(initialdir="/",
                           filetypes =(("C++ File", "*.cpp"),("All Files","*.*")),
                           title = "Choose a file."
                           )
    print (name)
    #Using try in case user types in unknown file or closes without choosing a file.
    try:
        with open(name,'r') as UseFile:
            print(name)
    except:
        print("No file exists")
    return name


#Title = root.title( "File Opener")
Title = largeMethod.title( "Large Methods")
Title = longParameterList.title( "Long Parameter Lists")
Title = duplicateCode.title( "Duplicate Code")
Title = largeClass.title( "Large Classes")
Title = lackOfComments.title( "Lack of Comments")
#label = ttk.Label(root, text ="Code Smell Identifier",foreground="black",font=("Helvetica", 16))
#label.pack()

#Menu Bar

#menu = Menu(root)
#root.config(menu=menu)

#file = Menu(menu)

#file.add_command(label = 'Open', command = OpenFile)
#file.add_command(label = 'Exit', command = lambda:exit())

#menu.add_cascade(label = 'File', menu = file)

Lb1 = Listbox(largeMethod)
Lb2 = Listbox(longParameterList)
Lb3 = Listbox(duplicateCode)
Lb4 = Listbox(largeClass)
Lb5 = Listbox(lackOfComments)



name = OpenFile()
smells = SmellIdentifier.get_smells(name)

for smell in smells:
    if smell.smell_type == "Large Method":
        Lb1.insert(END, smell.smell_type)
        Lb1.insert(END, smell.line_num)
        Lb1.insert(END, smell.description)
        Lb1.insert(END, "-------------------------")
    if smell.smell_type == "Long Parameter List":
        Lb2.insert(END, smell.smell_type)
        Lb2.insert(END, smell.line_num)
        Lb2.insert(END, smell.description)
        Lb2.insert(END, "-------------------------")
    if smell.smell_type == "Duplicate Code":
        Lb3.insert(END, smell.smell_type)
        Lb3.insert(END, smell.line_num)
        Lb3.insert(END, smell.description)
        Lb3.insert(END, "-------------------------")
    if smell.smell_type == "Large Class":
        Lb4.insert(END, smell.smell_type)
        Lb4.insert(END, smell.line_num)
        Lb4.insert(END, smell.description)
        Lb4.insert(END, "-------------------------")
    if smell.smell_type == "Lack of Comments":
        Lb5.insert(END, smell.smell_type)
        Lb5.insert(END, smell.line_num)
        Lb5.insert(END, smell.description)
        Lb5.insert(END, "-------------------------")

Lb1.pack(fill = BOTH, expand=1)
Lb2.pack(fill = BOTH, expand=1)
Lb3.pack(fill = BOTH, expand=1)
Lb4.pack(fill = BOTH, expand=1)
Lb5.pack(fill = BOTH, expand=1)
Lb1.mainloop()
Lb2.mainloop()
Lb3.mainloop()
Lb4.mainloop()
Lb5.mainloop()
#root.mainloop()
