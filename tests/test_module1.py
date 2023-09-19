import tkinter as tk
from PIL import Image,ImageTk
import ttkbootstrap as ttkb

root = ttkb.Window()
# root =tk.Tk()
root.geometry("600x200")
frame = ttkb.Frame(root)

frame.pack()
canvas = ttkb.Canvas(frame,bd=0,bg= 'red', highlightthickness=0, relief='ridge')

canvas.pack()
canvas.configure(bg='red')
img_tk = ImageTk.PhotoImage(Image.open(
            r'C:\Users\prash\Downloads\14455862_5466844 (Custom).jpg'))
canvas.create_image(0,0,image=img_tk)

root.mainloop()