from tkinter import *
from tkinter import ttk
from tkinter.ttk import *



def mainscreen():
    def idono():
        es = Tk()
        es.update_idletasks()
        es.attributes('-fullscreen', True)
        es.state('iconic')
        Height = es.winfo_screenheight()
        Width = es.winfo_screenwidth()
        es.destroy()
        img = PhotoImage(file="assets/images/_t_6.png")
        def Image(img, newWidth, newHeight):
            oldWidth = img.width()
            oldHeight = img.height()
            newPhotoImage = PhotoImage(width=newWidth, height=newHeight)
            for x in range(newWidth):
                for y in range(newHeight):
                    xOld = int(x*oldWidth/newWidth)
                    yOld = int(y*oldHeight/newHeight)
                    rgb = '#%02x%02x%02x' % img.get(xOld, yOld)
                    newPhotoImage.put(rgb, (x, y))
            return newPhotoImage
        img3 = Image(img, Width, Height)
        return img3
    

    root = Tk()
    root.title("Project Exoplanet")
    root.attributes('-fullscreen', True)
    root.grid()
    img2 = idono()
    imgquit = PhotoImage(file="assets/images/UI_StartButton.png")
    background = ttk.Label(root, image=img2, ).grid(column=0, row=0,columnspan=100, rowspan=100)
    buttnquit = ttk.Button(root, text="QUIT", command=root.destroy, takefocus=1).grid(column=99, row=99)
    buttnplay = ttk .Button(root, text="play").grid(column=50, row=50)
    print(root.grid_size())
    root.mainloop()
    
   
    

mainscreen()
print("executed ")