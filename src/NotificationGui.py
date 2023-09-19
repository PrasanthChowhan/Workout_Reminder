import ttkbootstrap as ttkb
from tkinter import ttk
from tkinter import Canvas
from PIL import Image, ImageTk


class NotificationGui(ttkb.Window):
    def __init__(self):
        super().__init__(themename='darkly',
                         title="HIDE THIS",
                         resizable=(False, False),
                         overrideredirect=True
                         )
        self.geometry("600x200")


        


        # Creating two frames
        
        right_frame = RightFrame(self)
        # left_frame = ttkb.Frame(self, bootstyle="info")
        left_frame = LeftFrame(self)

        # Creating layout
        self.rowconfigure(0, weight=1, uniform='a')
        self.columnconfigure((0, 1, 2), weight=1, uniform='a')

        # right_frame.pack(side= 'left',fill='both',expand='true')
        left_frame.grid(row=0, column=0, sticky="news")
        right_frame.grid(row=0, column=1, columnspan=2, sticky="news")

        self.bind('<Double-Button-1>', lambda event: self.destroy())
        self.set_window_position(window=self,position=(15, 25, 'se'))

        self.mainloop()

    def set_window_position(self, window, position=(15, 25, 'se')):
        """
        Set the geometry of a window based on a specified position and anchor.

        Args:
            window (Tk or Toplevel): The window for which to set the geometry.
            position (tuple, optional): A tuple specifying the initial position and anchor.
                Default is (100, 10, 'n').

        Returns:
            None
        """
        window.update_idletasks()  # Actualize geometry
        anchor = position[-1]
        x_anchor = "-" if "w" not in anchor else "+"
        y_anchor = "-" if "n" not in anchor else "+"
        screen_w = window.winfo_screenwidth() // 2
        screen_h = window.winfo_screenheight() // 2
        top_w = window.winfo_width() // 2
        top_h = window.winfo_height() // 2

        if all(["e" not in anchor, "w" not in anchor]):
            xpos = screen_w - top_w
        else:
            xpos = position[0]

        if all(["n" not in anchor, "s" not in anchor]):
            ypos = screen_h - top_h
        else:
            ypos = position[1]

        window.geometry(f"{x_anchor}{xpos}{y_anchor}{ypos}")


class RightFrame(ttkb.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(master=parent, bootstyle='primary',
                         *args, **kwargs)


class LeftFrame(ttkb.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(master=parent, bootstyle='success',
                         *args, **kwargs)
        
        self.path = r'C:\Users\prash\Downloads\running.jpg'
        self.canvas = Canvas(master=self,bd=0, highlightthickness=0, relief='ridge')
        self.canvas.configure(bg= 'blue')
        self.canvas.pack(expand=True,fill="both",padx=5,pady=5)
        
        self.canvas.bind("<Configure>", self.laod_and_place_image)


    def laod_and_place_image(self,event):  # thumbnail work directly on the image 
        canvas_width = event.width
        canvas_height = event.height

        self.img = Image.open(self.path)
        
        self.img.thumbnail((event.width,event.height))
        self.img_tk = ImageTk.PhotoImage(self.img)
        self.canvas.create_image(canvas_width/2,canvas_height/2,image=self.img_tk)


if __name__ == "__main__":
    NotificationGui()
    # root = ttkb.Window()

    # root.mainloop()
