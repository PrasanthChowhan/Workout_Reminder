import ttkbootstrap as ttkb
from tkinter import ttk
import tkinter as tk
from tkinter import Canvas, font
from PIL import Image, ImageTk
from src.utils import helper_functions as helpers


class NotificationGui(ttkb.Toplevel):
    def __init__(self):
        super().__init__(
            title="HIDE THIS",
            resizable=(False, False),
            overrideredirect=True
        )
        self.geometry("280x500")
        # self.geometry("800x266")

        # Creating two frames

        right_frame = RightFrame(self)
        left_frame = LeftFrame(self)

        # Creating layout
        self.rowconfigure(0, weight=1, uniform='a')
        self.columnconfigure((0, 1, 2), weight=1, uniform='a')

        left_frame.grid(row=0, column=0, sticky="news")
        right_frame.grid(row=0, column=1, columnspan=2, sticky="news")

        self.bind('<Double-Button-1>', lambda event: self.destroy())
        self.set_window_position(window=self, position=(15, 25, 'se'))

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
        super().__init__(master=parent,
                         bootstyle='primary',
                         *args, **kwargs)

        self.personal_msg_font = None
        self.content_font = None
        self._setup()

        container = ttkb.Frame(master=self)
        container.pack(fill='both', expand=True,)
        container.rowconfigure((0), weight=1, uniform='b')
        container.rowconfigure((1), weight=5, uniform='b')
        container.columnconfigure((0, 1), weight=1, uniform='b')

        text = "Nothing is more important than your health ........"
        personal_message_label = ttkb.Label(master=container, text=text,
                                            anchor="w",
                                            font=self.personal_msg_font,)
        personal_message_label.grid(
            row=0, column=0, columnspan=2, sticky='nesw')

        description_container_frame = ttkb.Frame(
            master=container, bootstyle='dark')
        description_container_frame.grid(
            row=1, column=0, columnspan=2, sticky='nesw')
        description_container_frame.rowconfigure((0), weight=1, uniform='b')
        description_container_frame.rowconfigure((1), weight=5, uniform='b')
        description_container_frame.columnconfigure(
            (0, 1), weight=1, uniform='b')

        # labels
        muscle_group_label = ttkb.Label(master=description_container_frame,
                                        font=self.content_font,
                                        text='Chest',
                                        anchor='center')
        muscle_group_label.grid(row=0, column=0, sticky='news')
        print(description_container_frame.cget('height'))

        # reading exercises from json

    def _setup(self):
        self.personal_msg_font = font.Font(
            family='Helvatica', size=15, weight='bold')
        self.content_font = font.Font(family='Helvatica', size=15)


class LeftFrame(ttkb.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(master=parent, bootstyle='info',
                         *args, **kwargs)

        self.path = r'C:\Users\prash\Downloads\running.jpg'
        self.canvas = Canvas(
            master=self, bd=0, highlightthickness=0, relief='ridge')
        # self.canvas.configure(bg='red')
        self.canvas.pack(expand=True, fill="both",)

        self.canvas.bind("<Configure>", self.laod_and_place_image)

    # thumbnail work directly on the image
    def laod_and_place_image(self, event):
        canvas_width = event.width
        canvas_height = event.height

        self.img = Image.open(self.path)
        # self.resized_img=self.img.resize((canvas_width, canvas_height))
        self.img.thumbnail((event.width, event.height))
        self.img_tk = ImageTk.PhotoImage(self.img)
        self.canvas.create_image(
            canvas_width/2, canvas_height/2, image=self.img_tk)


if __name__ == "__main__":

    root = ttkb.Window(themename='darkly')
    NotificationGui()

    root.mainloop()
