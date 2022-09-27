from tkinter import *  
from PIL import Image, ImageTk  
root = Tk()
root.geometry("500x500")

b_im = Image.open("imag/electriquiz.png")
b_im.thumbnail((100,100))
b_photo = ImageTk.PhotoImage(b_im)

def b_call():
    print("Callback")

b = Button(root, image=b_photo, command=b_call, borderwidth=0)
b.pack()

b_label = Label(root, image=b_photo)
b_label.pack()

root.mainloop()