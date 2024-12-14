from tkinter import *
from tkinter.ttk import * 
from time import strftime
root = Tk()
root.title("Digital Clock")

def clock():
    string = strftime('%I:%M:%S:%p') # %I là hệ 12h, còn %H là 24h
    label.config(text = string)
    label.after(1000,clock) # 1s 

label = Label(root, font = ("digital-7",100), background = 'black', foreground = 'green')
label.pack(anchor = 'center')
clock()
root.mainloop()