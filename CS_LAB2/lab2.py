
from tkinter import *
from tkinter import filedialog as fd
from tkinter import ttk
from tkinter.font import Font
import glob
import json
import tarfile
import requests
import audit_handler as audit_handler
import import_audit
import re
global perv

main = Tk()
main.resizable(False, False)
app_font = Font(family="Courier New", size=7)
s = ttk.Style()
s.configure('TFrame', background='#17C47D')
main.title("App")
main.geometry("1024x600")
frame = ttk.Frame(main, width=200, height=768, style='TFrame')
frame.grid(column=0, row=0)


querry = StringVar()
vars = StringVar()
index = 0
arr = []
isMatch = []
prev = []
tofile = []
struct = []



def isSelected(word):
    global prev
    global idx 
    w = word.widget
    actual = w.curselection()

    diff = [item for item in actual if item not in prev]
    if len(diff) > 0:
        idx = [item for item in actual if item not in prev][0]
    prev = w.curselection()

    text.delete(1.0, END)
    str = '\n'
    for key in isMatch[idx]:
        str += key + ':' + isMatch[idx][key] + '\n'
    text.insert(END,str)

def audtiHandler():
    global arr
    file_name = fd.askopenfilename(initialdir="../portal_audits")
    if file_name:
        arr = []
    global struct
    struct = import_audit.main(file_name)
    for element in struct:
        for key in element:
            str = ''
            for char in element[key]:
                if char != '"' and char != "'":
                    str += char
            isspacefirst = True
            str2 = ''
            for char in str:
                if char == ' ' and isspacefirst:
                    continue
                else:
                    str2 += char
                    isspacefirst = False
            element[key] = str2

    global isMatch
    isMatch = struct
    if len(struct) == 0:
        f = open(file_name, 'r')
        struct = json.loads(f.read())
        f.close()
    for struct in struct:
        if 'description' in struct:
            arr.append(struct['description'])
        else:
            arr.append('Error in selecting')
    vars.set(arr)



def select_all():
    lstbox.select_set(0, END)
    for st in struct:
        lstbox.insert(END, st)

def deselect_all():
    for st in struct:
        lstbox.selection_clear(0, END)

lstbox = Listbox(frame, bg = "#FFFFFF", font = app_font, fg = "black", listvariable = vars, selectmode = MULTIPLE, width = 150, selectbackground = 'gray', height = 34, highlightthickness = 3)
lstbox.grid(row = 0, column = 0, columnspan = 3, padx = 130, pady = 50)
lstbox.bind('<<ListboxSelect>>', isSelected)

def save_config():
    file_name = fd.asksaveasfilename(filetypes=(("AUDIT FILES", ".audit"), ("All files", ".")))
    file_name += '.audit'
    file = open(file_name, 'w')
    selection = lstbox.curselection()
    for i in selection:
        tofile.append(isMatch[i])
    json.dump(tofile, file)
    file.close()

text = Text(frame, bg="#000000", fg="white", font=app_font, width=105, height=45, highlightthickness=3)
buttonButton = Font(family="Courier New", size=10)
saveButton = Button(frame, bg="gray", fg="white", font=buttonButton, text="Save", width=13, height=1, command=save_config).place(relx=0.01, rely=0.14)
importButton = Button(frame, bg="gray", fg="white", font=buttonButton, text="Import", width=13, height=1,command=audtiHandler).place(relx=0.01, rely=0.21)
selectAll = Button(frame, bg="gray", fg="white", font=buttonButton, text="Select All", width=13, height=1,command=select_all).place(relx=0.01, rely=0.28)
deselectAll = Button(frame, bg="gray", fg="white", font=buttonButton, text="Deselect All", width=13, height=1,command=deselect_all).place(relx=0.01, rely=0.35)
exit_btn = Button(frame, bg="gray", fg="white", font=buttonButton, text="Exit", width=13, height=1,command=main.quit).place(relx=0.88, rely=0.93)
global e
main.mainloop()