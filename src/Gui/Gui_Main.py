import tkinter as tk
from tkinter import ttk
from src.Gui.components import LaterButton, ExerciseIcon, ExerciseTitle, CustomFrame, DisableInteractionWithOtherWindow, ReasonTextGui
from src.Exerciselog import ExerciseLog
from src.Gui.styles import configure_styles
from src.Gui.gui_settings import BACKGROUND_COLOR, SEPARATOR_COLOR
from src.Gui.window_function import SetWindowPosition
import threading
from src.SubprocessCommands import SubprocessCommands

# import button_styling_and_functionality
default_information = {'name': 'Default_Push-up',
                       'difficulty': 'beginner',
                       'muscle': 'chest',
                       'equipment': 'bodyweight',
                       'url': 'https://www.youtube.com/@prasanthchowhan'
                       }


class NotificationGui(tk.Tk):
    def __init__(self, exercise_dict: dict = default_information,stop_scheduling_callabck=None):
        super().__init__()
        self.resizable(False, False)
        self.overrideredirect(True)
        self.geometry("400x250")
        self.attributes('-topmost', True)

        
        gui_icon = tk.PhotoImage(file='resources\icons\gui icon\pawn with dumbell.png')
        self.iconphoto(True,gui_icon)
       
       # INitialise
        self.stop_scheduling_callabck=stop_scheduling_callabck
        
        configure_styles()

        ## DISABLE USER INTERACTION WITH OTHER WINDOWS ##
        DisableInteractionWithOtherWindow(self)
        SetWindowPosition(window=self, position=(0, 0, 'c'))

        Container(parent=self, padx=10, exercise_dict=exercise_dict).pack(
            expand=True, fill='both')

        self.bind("<Button-3>", self.right_click) # disabling right click settings

    ## DISABLE RIGHT CLICK SETTINGS ##
  
    def right_click(self, event):
        # print("Right click", event.x_root, event.y_root)
        context_menu = tk.Menu(self, tearoff=0)
        context_menu.add_command(label="reload",command=self._reload_app)
        context_menu.add_command(label="exit",command=self._exit_app)
        context_menu.post(event.x_root, event.y_root)

    def _exit_app(self):
        if self.stop_scheduling_callabck:
            self.stop_scheduling_callabck()
        self.destroy()
    def _reload_app(self):
        threading.Thread(target=SubprocessCommands.run_subprocess,args=('schedule', )).start()
        self._exit_app()


class Container(tk.Frame):
    def __init__(self, parent, exercise_dict, *args, **kwargs):
        super().__init__(master=parent,
                         background=BACKGROUND_COLOR,
                         *args, **kwargs)
        title = ExerciseTitle(self,
                              text=exercise_dict['name'],
                              anchor='w',
                              url=exercise_dict['url'],
                              ).pack(fill='x', pady=(15, 2))

        separator = tk.Frame(self, borderwidth=10, relief='groove',
                             background=SEPARATOR_COLOR).pack(fill='x')

        VisualFrame(parent=self, exercise_dict=exercise_dict).pack(
            fill='both', expand=True)

        # Action Frame
        ActionButtonsFrame(parent=self, exercise_dict=exercise_dict).pack(
            # side='bottom',
            fill='x', pady=5)


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


class ActionButtonsFrame(CustomFrame):
    def __init__(self, parent, exercise_dict, height=30, set_background='parent', *args, **kwargs):

        super().__init__(master=parent,
                         set_background=set_background,
                         height=height,
                         *args, **kwargs)
        # using grid because LaterButton which is canvas isn't sharing equal space with pack
        self.rowconfigure((0), weight=1, uniform='a')
        self.columnconfigure((0, 1), weight=1, uniform='a')

        if height is not None:
            self.grid_propagate(0)  # forcing the frame to take assigned height

        # Later buttons
        later_button = LaterButton(master=self, text='Later', callback_func=lambda: self.create_entry(
            exercise_dict, is_completed=False))
        # lambda event: because it is tag_binded to text
        later_button.grid(row=0, column=0, sticky='nsew', padx=5,)

        # done button
        done_button = ttk.Button(self, text='I Did It',
                                 command=lambda: self.create_entry(
                                     exercise_dict, is_completed=True),
                                 style='did_it.TButton',
                                 cursor='hand2',
                                 )
        done_button.grid(row=0, column=1, sticky='nsew', padx=5)

    def create_entry(self, exercise_dict, is_completed):
        exercise_log = ExerciseLog()
        exercise_log.copy_values_from_dict(exercise_dict)
        exercise_log.set_completed(is_completed)
        # exercise_log.add_reason()

        if is_completed is False:  # Get REason for not doing ##
            root = self.winfo_toplevel()
            reason_gui = ReasonTextGui(parent=root, exercise_log=exercise_log)
            SetWindowPosition(reason_gui, (0, 0, 'c'))

        elif is_completed is True:
            exercise_log.add_entry_to_database()
            self.destroyed()

    def destroyed(self) -> None:
        try:
            root = self.nametowidget('.')
            root.destroy()
        except Exception as e:
            print(f"Error in my_job: {e}")


if __name__ == '__main__':
    # root = ttkb.Window()
    # root.config(bg='blue')
    a = NotificationGui()
    a.overrideredirect(False)
    a.mainloop()
    # root.mainloop()
