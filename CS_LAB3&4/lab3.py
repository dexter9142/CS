
from tkinter import *
from tkinter import filedialog as fd
from tkinter import ttk
from tkinter.font import Font
import glob
import json
import tarfile
import requests
import import_audit
import re
import sys
global perv


main = Tk()
main.resizable(False, False)
app_font = Font(family="Arial", size=7)
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
structure = []
success = []
succ = []
failed = []
unknown = []
vars1 = StringVar()
vars2 = StringVar()
array1 = []
array2 = []
array2copy = []


def make_query(struct):
    query = 'reg query ' + struct['reg_key'] + ' /v ' + struct['reg_item']
    out = subprocess.Popen(query, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    output = out.communicate()[0].decode('ascii', 'ignore')
    str = ''
    for char in output:
        if char.isprintable() and char != '\n' and char != '\r':
            str += char
    output = str
    output = output.split(' ')
    output = [x for x in output if len(x) > 0]
    value = ''

    if 'ERROR' in output[0]:
        unknown.append(struct['reg_key'] + struct ['reg_item'])
    for i in range(len(output)):
        if 'REG_' in output[i]:
            for element in output[i + 1:]:
                value = value + element + ' '
            value = value [:len(value) - 1]
            if struct ['value_data'][:2] == '0x':
                struct ['value_data'] = struct ['value_data'][2:]
            struct['value_data'] = hex(int(struct ['value_data']))
            p = re.compile('.*' + struct ['value_data'] + '.*')
            if p.match(value):
                print('PASSED Policy desc:'+struct['description'])
                print('Patern:', struct['value_data'])
                print('Value:', value)
                success.append(struct['reg_key'] + struct['reg_item'] + '\n' + 'Value:' + value)
                succ.append([struct,value])

            else:
                print('failedED Policy desc:' + struct['description'])
                print('Did not pass: ', struct['value_data'])
                print('Value which did not pass: ', value)
                failed.append([struct, value])

def check():

    for struct in structure:
        if 'reg_key' in struct and 'reg_item' in struct and 'value_data' in struct:
            make_query(struct)

    for i in range(len(succ)):
        item1 = succ[i]
        array1.append(' PASSED POLICY Description' + item1[0]['description'])


    for i in range(len(failed)):
        item2 = failed[i]
        array2.append(' failedED POLICY Description' + item2[0]['description'])
        global array2copy
        array2copy = array2

    print("succ = ", succ)
    print("failed = ", failed)
    procent = int((len(succ)/(len(succ) + len(failed)))*100)
    
    print(procent)
    array1.append('The system is securised :' + str(procent) + ' % ')
    array2.append('The system is securised :' + str(procent) + ' % ')
    vars1.set(array1)
    vars2.set(array2)

    frame2 = Frame(main, bd=10, bg='#000000', highlightthickness=5)
    frame2.config(highlightbackground="gray")
    frame2.place(relx=0.535, rely=0.1, width=375, relwidth=0.4, relheight=0.8, anchor='n')
    listbox_succes = Listbox(frame2, bg="#4A945B", font=app_font, fg="black", listvariable=vars1, selectmode=MULTIPLE,width=50, height=27, highlightthickness=3)
    listbox_succes.place(relx=0.0, rely=0.03, relwidth=0.45, relheight=0.9)
    listbox_succes.config(highlightbackground="green")
    listbox_failed = Listbox(frame2, bg="#C75A63", font=app_font, fg="black", listvariable=vars2, selectmode=MULTIPLE,width=50, height=27, highlightthickness=3)
    listbox_failed.place(relx=0.55, rely=0.03, relwidth=0.45, relheight=0.9)
    listbox_failed.config(highlightbackground="red")

    changeBtn= Button(frame2, text='Change', command=change_failures, bg="#519487", fg="white", font=app_font, padx='10px', pady='3px')
    changeBtn.place(relx=0.745, rely=0.93)

    backupBtn = Button(frame2, text='Restore', command=restore, bg="#519487", fg="white", font=app_font, padx='10px', pady='3px')
    backupBtn.place(relx=0.835, rely=0.93)

    def exit():
        frame2.destroy()

    exit_btn = Button(frame2, text='Back', command=exit, bg="gray", fg="white", font=app_font, padx='10px',
                      pady='3px')
    exit_btn.place(relx=0.93, rely=0.93)

def change_failures():
    global arr2copy
    global arr2
    backup()
    for i in range(len(failed_selcted)):
        struct = failed_selcted[i][0]
        query = 'reg add "' + struct['reg_key'] + '" /v ' + struct['reg_item'] + ' /d "' + struct['value_data'] + '" /f'
        print(query)
        out = subprocess.Popen(query, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        output = out.communicate()[0].decode('ascii', 'ignore')
        str = ''
        for char in output:
            if char.isprintable() and char != '\n' and char != '\r':
                str += char
        output = str
        print(output)
        vars2.set(arr2)
        arr2copy = arr2

def restore():
        f = open('backup.txt')
        fail = json.loads(f.read())
        print(fail)
        f.close()

        for i in range(len(fail)):
            struct = fail[i][0]
            query = 'reg add ' + struct['reg_key'] + ' /v ' + struct['reg_item'] + ' /d ' + fail[i][1] + ' /f'
            print('Query:', query)
            out = subprocess.Popen(query,
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.STDOUT)
            output = out.communicate()[0].decode('ascii', 'ignore')
            str = ''
            for char in output:
                if char.isprintable() and char != '\n' and char != '\r':
                    str += char
            output = str
            print(output)

def backup():
        f=open('backup.txt','w')
        backupString=json.dumps(fail)
        f.write(backupString)
        f.close()

def on_select_failed(evt):
    w = evt.widget
    actual = w.curselection()

    global failed_selected
    global arr2
    failed_selected=[]
    for i in actual:
        failed_selected.append(fail[i])
    localarr2=[]
    for i in actual:
        localarr2.append(arr2copy[i])
    arr2=localarr2
    arr2=[x for x in arr2copy if x not in arr2]
    print(failed_selected)



def input_find(term):
    find()

def find():
    global struct
    q = querry.get()
    arr = [st['description'] for st in struct if q.lower() in st['description'].lower()]
    global matching
    matching = [st for st in struct if q in st['description']]
    vars.set(arr)

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
        tofile.append(matching[i])
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
e = Entry(frame, bg="gray", font=buttonButton, width=25, textvariable=querry).place(relx=0.57, rely=0.04)
find_btn = Button(frame, bg="gray", fg="white", font=buttonButton, text="Find", width=13, height=1,command=find).place(relx=0.01, rely=0.42)
check_btn = Button(frame, bg="gray", fg="white", font=buttonButton, text="Check", width=8, height=1,command=check).place(relx=0.485, rely=0.035)
main.bind('<Return>', input_find)
main.mainloop()
