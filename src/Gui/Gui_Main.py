
from tkinter import Canvas
import tkinter as tk
from tkinter import ttk
from tkinter import font
from src.Gui.ImageFunctions import MyImage, CircleImgIcon, CanvasWithShape
from src.Gui.components import LaterButton, ExerciseIcon, ExerciseTitle,CustomFrame
from src.DbManager import ExerciseLog
from src.Gui.styles import configure_styles
from src.Gui.gui_settings import BACKGROUND_COLOR


# import button_styling_and_functionality

default_information = {'name': 'Default_Push-up',
                       'difficulty': 'beginner',
                       'muscle': 'chest',
                       'equipment': 'bodyweight',
                       'url': 'https://youtu.be/tD4HCZe-tew?si=YeGGkId2NMo0fHB0'
                       }


class NotificationGui(tk.Tk):
    def __init__(self, exercise_dict: dict = default_information):
        super().__init__()
        self.title("HIDE THIS")
        # self.resizable(False, False)
        # self.overrideredirect(True)
        self.geometry("400x250")
        self.attributes('-topmost', True)
        configure_styles()
        # self['bg'] = 'cyan'

        SetWindowPosition.for_tk(window=self, position=(0, 0, 'e'))

        # # notificaiton configuration
        # self.rowconfigure(0, weight=1, uniform='a')
        # self.rowconfigure(1, weight=2, uniform='a')
        # self.columnconfigure(0, weight=1, uniform='a')

        # ImageFrame(parent=self).grid(row=0, column=0, sticky='news')
        BottomContainer(parent=self, padx=10, exercise_dict=exercise_dict).pack(
            expand=True, fill='both')
        # ).grid(row=1, column=0, sticky='news' )


class SetWindowPosition:
    @staticmethod
    def for_tk(window, position=(15, 25, 'se')):
        """
        Set the geometry of a window based on a specified position and anchor.

        Args:
            window (Tk or Toplevel): The window for which to set the geometry.
            position (tuple, optional): A tuple specifying the initial position and anchor.
                Default is (15, 25, 'se').

        Returns:
            None
        """
        window.update_idletasks()  # Actualize geometry
        anchor = position[-1]
        x_anchor = "-" if "w" not in anchor else "+"
        y_anchor = "-" if "n" not in anchor else "+"
        screen_w = window.winfo_screenwidth() // 2
        screen_h = window.winfo_screenheight() // 2
        # print(window.winfo_width())
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
        # window.geometry(f"{x_anchor}{xpos}{y_anchor}{ypos}")

    @staticmethod
    def for_ctk(window, position=(15, 25, 'se')):
        '''
        # ignore this not yet implemented
        '''
        print('pending work setwindow position for ctk')
        window.update()  # Actualize geometry
        anchor = position[-1]
        screen_w = window.winfo_screenwidth()
        screen_h = window.winfo_screenheight()
        # print(window.winfo_width())
        top_w = window.winfo_width()  # // 2
        top_h = window.winfo_height()  # // 2

        # x_anchor = "-" if "w" not in anchor else 1
        # y_anchor = "-" if "n" not in anchor else "+"

        if 'e' in anchor:
            xpos = screen_w - top_w
        elif 'w' in anchor:
            xpos = position[0] - top_w
        else:
            xpos = position[0]

        # Calculate vertical position
        if 's' in anchor:
            ypos = screen_h - top_h
        elif 'n' in anchor:
            ypos = position[1] - top_h
        else:
            ypos = position[1]
        window.geometry(f"{xpos}+{ypos}")
        # window.geometry(f"{x_anchor}{xpos}{y_anchor}{ypos}")

# top section


class ImageFrame(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(master=parent,

                         *args, **kwargs)

        self.create_canvas()

    def create_canvas(self):
        self.canvas = Canvas(self, bd=0, highlightthickness=0, relief='ridge')
        self.canvas.pack(expand=True, fill='both')
        self.canvas.configure(bg='red')
        self.canvas.bind('<Configure>', self.place_image)

    def place_image(self, event):
        path = r'C:\Users\prash\Downloads\running.jpg'
        myimage = MyImage()
        resized_image = myimage.resize_image(
            path, event.width, event.height, preserve_aspect=True, resize_percent_of_original=200)
        self.resized_image_tk = MyImage.to_tk(resized_image)
        self.canvas.create_image(
            event.width/2, event.height/2, image=self.resized_image_tk)

# bottom section


class BottomContainer(tk.Frame):
    def __init__(self, parent, exercise_dict, *args, **kwargs):
        super().__init__(master=parent,
                        background=BACKGROUND_COLOR,
                         *args, **kwargs)

        text_frame = ExerciseTitle(self,
                                   text=exercise_dict['name'],
                                   anchor='w',
                                   url=exercise_dict['url'],
                                   ).pack(fill='x', pady=(15, 2))

        # separator = ttk.Separator(self, orient='horizontal').pack(fill='x')
        separator = tk.Frame(self,borderwidth=10, relief='groove',background='grey').pack(fill='x')

        VisualFrame(parent=self, exercise_dict=exercise_dict).pack(
            fill='both', expand=True)

        # Description Frame
        # DescriptionFrame(parent=self).pack(expand=True, fill='both')

        # Action Frame
        ActionButtonsFrame(parent=self, exercise_dict=exercise_dict).pack(
            # side='bottom',
            fill='x', pady=5)

    def setup(self):
        self.h1 = font.Font(
            family='Roboto', size=17, weight='bold')
        self.h2 = font.Font(family='Helvatica', size=15)
        return {'h1': self.h1,
                'h2': self.h2}


class IconStructure(tk.Frame):
    def __init__(self, master, text, path, *args, **kwargs):
        super().__init__(master=master,
                         #  background='red',  # TODO change this
                         *args, **kwargs)

        icon1 = CircleImgIcon(master=self, width=40,
                              height=40, fg_img_path=path)
        icon1.pack()

        ttk.Label(master=self, text=text,
                  ).pack(pady=5)


class VisualFrame(CustomFrame): 
    def __init__(self, parent, exercise_dict, *args, **kwargs):
        super().__init__(master=parent,
                         *args, **kwargs)

        # values of recieved dict and icon name
        icons_list = ['difficulty', 'muscle', 'equipment']
        columns = tuple(range(len(icons_list)))

        # USING GRID AND BECAUSE SOME IMAGES ARE NOT SHARING EQUAL SPACE
        self.rowconfigure((0), weight=1, uniform='anytext')
        self.columnconfigure(columns, weight=1, uniform='anytext')

        for index, icon_name in enumerate(icons_list):
            path = f"resources\icons\{icon_name}.png"
            ExerciseIcon(parent=self,
                         img_path=path,
                         # CAPITALIZE THE TEXT
                         text=exercise_dict[icon_name].capitalize()
                         ).grid(row=0, column=index, sticky='news')

            # IconStructure(master=self, text=exercise_dict[icon_name], path=path
            #               ).grid(row=0,column=index,sticky='news')


## MAY BE IN FUTURE UPDATES ##
class DescriptionFrame(tk.Frame):

    def __init__(self, parent, *args, **kwargs):
        super().__init__(master=parent,
                         #  background='magenta',
                         *args, **kwargs)
        # initialize
        self.color = '#d0d3d4'
        # rectangular_background = Canvas(master=self,background='yellow',confine=True)
        # rectangular_background=Canvas(self,background='yellow')
        rectangular_background = CanvasWithShape(
            master=self, shape='rounded_rectangle', fill=self.color, radius=15)

        rectangular_background.pack(expand=True, fill='both')


class ActionButtonsFrame(CustomFrame):
    def __init__(self, parent, exercise_dict, height=30,set_background = 'parent', *args, **kwargs):

        super().__init__(master=parent,
                        set_background=set_background,
                         height=height,
                         *args, **kwargs)
        # using grid because LaterButton which is canvas isn't sharing equal space with pack
        # self.rowconfigure((0,2),weight=1,uniform='a')
        # self.rowconfigure((1),weight=2,uniform='a')
        self.rowconfigure((0), weight=1, uniform='a')
        self.columnconfigure((0, 1), weight=1, uniform='a')

        if height is not None:
            self.grid_propagate(0)  # forcing the frame to take assigned height

        # Later buttons
        later_button = LaterButton(master=self, text='Later',
                                   callback_func=lambda: self.update_database(exercise_dict, is_completed=False))
        # lambda event: because it is tag_binded to text
        later_button.grid(row=0, column=0, sticky='nsew', padx=5)

        # done button
        done_button = ttk.Button(self, text='I Did It',
                                 command=lambda: self.update_database(exercise_dict, is_completed=True),
                                 style='did_it.TButton',
                                 cursor='hand2'
                                 )
        done_button.grid(row=0, column=1, sticky='nsew', padx=5)

    def update_database(self, exercise_dict, is_completed):

        exercise_log = ExerciseLog()

        exercise_log.copy_values_from_dict(exercise_dict)

        exercise_log.set_completed(is_completed)
        # exercise_log.add_reason()

        exercise_log.add_entry_to_database()
        # print(exercise_log.get_log_entry())

        self.destroyed()

    def destroyed(self) -> None:
        try:
            root = self.nametowidget('.')
            # root.geometry('1000x1000')
            root.destroy()
            # root.withdraw()
        except Exception as e:
            print(f"Error in my_job: {e}")


if __name__ == '__main__':
    # root = ttkb.Window()
    # root.config(bg='blue')
    a = NotificationGui()
    a.mainloop()
    # root.mainloop()
