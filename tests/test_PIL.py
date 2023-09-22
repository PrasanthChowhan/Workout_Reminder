from PIL import Image, ImageTk
import customtkinter as ctk
import ttkbootstrap as ttkb
from ttkbootstrap import Colors


class PilTest:
    def transparent_label():
        img = Image.new("RGBA", (128, 50), (0, 0, 0, 0))
        return ImageTk.PhotoImage(img)


class TTKBootstrap:
    def __init__(self):
        root = ttkb.Window()
        root.geometry("1000x200")
        img_tk = PilTest.transparent_label()
        frame = ttkb.Frame(root, bootstyle='secondary')
        frame.pack(expand=True, fill='both')
    

        style = ttkb.Style()
      
        for color_label in style.colors.label_iter():
            color = style.colors.get(color_label)
            print(color_label, color)




        label = ttkb.Label(frame, text='using ttkbootstrap',foreground='red',background='#e5e5e5',
                           image=img_tk, compound='center').pack()

        root.mainloop()


class UsingCTK:
    def __init__(self):
        root = ctk.CTk()

        img_tk = PilTest.transparent_label()
        frame = ctk.CTkFrame(root, fg_color='pink')
        frame.pack()
        label = ctk.CTkLabel(master=frame, text='hallo',
                             image=img_tk, compound='center').pack()

        root.mainloop()


if __name__ == '__main__':
    # UsingCTK()
    TTKBootstrap()