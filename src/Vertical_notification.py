import ttkbootstrap as ttkb
from tkinter import Canvas
import tkinter as tk
from tkinter import font
from src.ImageFunctions import MyImage
from PIL import Image


class VerticalGui(ttkb.Toplevel):
    def __init__(self):
        super().__init__(
            title="HIDE THIS",
            resizable=(False, False),
            overrideredirect=True
        )
        self.geometry("280x500")

        # self.wm_attributes("-transparentcolor", 'white')

        # notification position
        self.set_window_position(self, position=(10, 0, 'e'))

        # notificaiton configuration
        self.rowconfigure(0, weight=1, uniform='a')
        self.rowconfigure(1, weight=2, uniform='a')
        self.columnconfigure(0, weight=1, uniform='a')

        ImageFrame(parent=self).grid(row=0, column=0, sticky='news')
        BottomContainer(parent=self).grid(
            row=1, column=0, sticky='news', padx=10)

        

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


class ImageFrame(ttkb.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(master=parent,
                         bootstyle='primary',
                         *args, **kwargs)
        
        self.create_canvas()
        
    def create_canvas(self):
        self.canvas= Canvas(self, bd=0, highlightthickness=0, relief='ridge')
        self.canvas.pack(expand=True,fill='both')
        self.canvas.configure(bg='red')
        self.canvas.bind('<Configure>',self.place_image)

    def place_image(self,event):
        path = r'C:\Users\prash\Downloads\running.jpg'
        myimage = MyImage()
        resized_image = myimage.resize_image(path,event.width,event.height,preserve_aspect=True,resize_percent_of_original=200)
        self.resized_image_tk = MyImage.to_tk(resized_image)
        self.canvas.create_image(event.width/2,event.height/2,image = self.resized_image_tk)
        
        
        


class BottomContainer(ttkb.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(master=parent,
                         bootstyle='white',
                         *args, **kwargs)

        # initialize
        self.h1 = None
        self.h2 = None
        self.h3 = None

        # fonts settings
        self._setup()

        text_frame = ttkb.Label(self,
                                text='Push-up',
                                bootstyle='black',
                                font=self.h1).pack(fill='x', pady=6)

        visuals_frame = ttkb.Frame(self, bootstyle='primary')
        visuals_frame.pack(fill='x')

        icon = ttkb.Label(master=visuals_frame, text='Icon-1',
                          bootstyle='inverse-primary')
        icon.pack(side='left', expand=True, fill='both', pady=10, padx=10)
        icon2 = ttkb.Label(master=visuals_frame, text='Icon-2',
                           bootstyle='inverse-primary')
        icon2.pack(side='left', expand=True, fill='both', pady=10, padx=10)
        icon3 = ttkb.Label(master=visuals_frame, text='Icon-3',
                           bootstyle='inverse-primary')
        icon3.pack(side='left', expand=True, fill='both', pady=10, padx=10)

        # Description Frame
        DescriptionFrame(parent=self).pack(expand=True, fill='both', pady=5)

        # Action Frame
        ActionButtonsFrame(parent=self).pack( fill='x', pady=5
        )

    def _setup(self):
        self.h1 = font.Font(
            family='Roboto', size=15, weight='bold')
        self.h2 = font.Font(family='Helvatica', size=15)
        return {'h1': self.h1,
                'h2': self.h2}


class DescriptionFrame(ttkb.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(master=parent,
                         bootstyle='dark',
                         *args, **kwargs)
        
        # Description heading
        description_heading_frame = ttkb.Frame(master=self, bootstyle='info')
        description_heading_frame.pack(fill='x', expand=True,anchor='n',pady=5)

        description_heading = ttkb.Label(bootstyle='inverse-info', foreground='#2c2c32',master=description_heading_frame,
                                         text="Advantages")
        description_heading.pack(side='left', anchor='nw', padx=5)

        # i Icon
        i_icon_label = ttkb.Label(master=description_heading_frame,text='i')
        i_icon_label.pack(side='right', anchor='ne', padx=5)




class ActionButtonsFrame(ttkb.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(master=parent,
                         bootstyle='primary',
                         *args, **kwargs)
        # buttons
        later_button = ttkb.Button(self, text='Later', bootstyle='link')
        later_button.pack(side='left', expand=True, fill='both')
        done_button = ttkb.Button(self, text='I Did It', bootstyle='success')
        done_button.pack(side='left', expand=True, fill='both')


if __name__ == '__main__':
    root = ttkb.Window()
    # root.config(bg='blue')

    VerticalGui()
    root.mainloop()
