from tkinter import *
from tkinter import ttk
from tkinter.ttk import *


def mainscreen():
    root = Tk()
    root.title("Project Exoplanet")
    root.geometry("750x375")
    img1 = PhotoImage(file="assets/images/wheel.png")
    stl = ttk.Style(root)
    stl.element_create('Frame.frame', 'image', img1)
    frm = ttk.Frame(root, style='Frame.frame')
    
    root.mainloop()
    
   
    

mainscreen()
print("executed ")