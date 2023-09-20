import tkinter as tk
from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk

class MyGUI(Frame):
    def __init__(self):
        tk.Frame.__init__(self)
        self.pack()
        self.master.title("My GUI Window")
        self.master.geometry("400x300")
        
        
        # Create the image widget
        self.img = Image.open(r'C:\Users\prash\Downloads\running.jpg')
        self.image = ImageTk.PhotoImage(self.img)
        self.image_label = Label(self, image=self.image)
        self.image_label.grid(row=0, column=0,  sticky=W+E+N+S)
        
        # Create the information widget
        info_label = Label(self, text="Some information about your card")
        info_label.grid(row=0, column=1, sticky=W+E+N+S)

# Create an instance of the MyGUI class
my_gui = MyGUI()

# Start the main event loop
my_gui.mainloop()
