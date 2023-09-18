import ttkbootstrap as ttkb
from ttkbootstrap.style import Bootstyle


class NotificationGui(ttkb.Window):
    def __init__(self):
        super().__init__(themename='darkly',
                         title="HIDE THIS",
                         minsize=(600, 200),
                         resizable=(False,False),
                         alpha=0.95,
                         overrideredirect=False
                        )  

        # Creating two frames
        right_frame = ttkb.Frame(self, bootstyle='danger')
        # left_frame = ttkb.Frame(self, bootstyle="info")
        left_frame = LeftFrame(self)

        # Creating layout
        self.rowconfigure(0, weight=1, uniform='a')
        self.columnconfigure((0, 1, 2), weight=1, uniform='a')

        # right_frame.pack(side= 'left',fill='both',expand='true')
        right_frame.grid(row=0, column=0, sticky="news")
        left_frame.grid(row=0, column=1, columnspan=2, sticky="news")

        self.bind('<Double-Button-1>',lambda event : self.destroy())
        self.set_geometry(window=self)

        self.mainloop()

    def set_geometry(self, window, position=(15, 25, 'se')):
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

class LeftFrame(ttkb.Frame):
    def __init__(self,parent,*args,**kwargs):
        super().__init__(master=parent,bootstyle= 'primary',*args,**kwargs)
        
        


if __name__ == "__main__":
    NotificationGui()
    # root = ttkb.Window()

    # root.mainloop()


