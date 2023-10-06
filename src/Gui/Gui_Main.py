
from tkinter import Canvas
import tkinter as tk
from tkinter import ttk
from tkinter import font
from src.Gui.ImageFunctions import MyImage, CircleImgIcon, CanvasWithShape
from src.Gui.components import FrameWithParentBackground, LabelWithParentBackground,ButtonWithParentBackground,LaterButton
from src.DbManager import ExerciseLog
from src.Gui.styles import configure_styles


# import button_styling_and_functionality

default_information = {'name': 'Default_Push-up',
                       'difficulty': 'beginner',
                       'muscle': 'chest',
                       'equipment': 'bodyweight'}


class NotificationGui(tk.Tk):
    def __init__(self, exercise_dict:dict=default_information):
        super().__init__()
        self.title("HIDE THIS")
        # self.resizable(False, False)
        # self.overrideredirect(True)
        self.geometry("400x250")
        # self.attributes('-topmost', True)
        # configure_styles()

        
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

                         *args, **kwargs)

        # initialize
        self.h1 = None
        self.h2 = None
        self.h3 = None

        # fonts settings
        self.setup()

        text_frame = ttk.Label(self,
                              text=exercise_dict['name'],
                              anchor='w',
                              #   background='magenta',
                              font=self.h1,

                              ).pack(fill='x', pady=10)

        VisualFrame(parent=self, exercise_dict=exercise_dict).pack(
            fill='both', expand=True, pady=30)

        # Description Frame
        # DescriptionFrame(parent=self).pack(expand=True, fill='both')

        # Action Frame
        ActionButtonsFrame(parent=self, exercise_dict=exercise_dict).pack(
            side='bottom', fill='x', pady=10, ipady=5)

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


class VisualFrame(tk.Frame):
    def __init__(self, parent, exercise_dict, *args, **kwargs):
        super().__init__(master=parent,
                         background='red',
                         *args, **kwargs)

        # values of recieved dict and icon name
        icons_list = ['difficulty', 'muscle', 'equipment']

        for icon_name in icons_list:
            path = f"resources\icons\{icon_name}.png"
            IconStructure(master=self, text=exercise_dict[icon_name], path=path
                          ).pack(side='left', expand=True, fill='both')

        # icon = IconStructure(master=self, text=exercise_dict['difficulty'], path=path)
        # icon.pack(side='left', expand=True, fill='both')

        # icon2 = IconStructure(master=self, text=exercise_dict['muscle_targetted'], path=path)
        # icon2.pack(side='left', expand=True, fill='both')

        # icon3 = IconStructure(master=self, text=exercise_dict['equipment'], path=path)
        # icon3.pack(side='left', expand=True, fill='both')


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


class ActionButtonsFrame(tk.Frame):
    def __init__(self, parent, exercise_dict, *args, **kwargs):
        super().__init__(master=parent,
                        #  background='yellow',
                         *args, **kwargs)
        # using grid because LaterButton which is canvas isn't sharing equal space with pack 
        self.rowconfigure(0,weight=1,uniform='a')
        self.columnconfigure((0,1),weight=1,uniform='a')

        # Later buttons
        self.update()
        later_button = LaterButton(master=self, text='Later',
                                  callback_func=lambda event: self.update_database(exercise_dict,is_completed = False))
        # lambda event: because it is tag_binded to text
        later_button.grid(row=0,column=0, sticky='news')


        # done button
        done_button = ttk.Button(
            self,text='I Did It', command=lambda: self.update_database(exercise_dict,is_completed = True),style='did_it.TButton')
        done_button.grid(row=0,column=1, sticky='news')



    def update_database(self, exercise_dict,is_completed):
        
        exercise_log = ExerciseLog()

        exercise_log.copy_values_from_dict(exercise_dict)

        exercise_log.set_completed(is_completed)
        # exercise_log.add_reason()
        
        exercise_log.add_entry_to_database()
        print(exercise_log.get_log_entry())


        self.destroyed()

    def destroyed(self) -> None:
        root = self.nametowidget('.')
        # root.geometry('1000x1000')
        root.destroy()


if __name__ == '__main__':
    # root = ttkb.Window()
    # root.config(bg='blue')
    a = NotificationGui()
    a.mainloop()
    # root.mainloop()
