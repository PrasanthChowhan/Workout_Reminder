import tkinter as tk
from tkinter import ttk
import time
from src.Gui.gui_settings import *
from src.Gui.styles import configure_styles
from src.Gui.ImageFunctions import MyImage
from src.utils.SQLITE import SqliteDefs
from src.utils.constants import DatabaseConstants
import webbrowser


## FOR CHECKING SPEED OF DEF ##
def timing_decorator(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"{func.__name__} took {end_time - start_time:.2f} seconds to execute.")
        return result
    return wrapper


class CustomWidget(tk.Widget):
    def __init__(self, master=None, set_background='parent', *args, **kwargs):
        ## initialize ##
        if set_background == 'parent':
            color = master.cget('background')
        else:
            color = set_background

        super().__init__(master=master, background=color, *args, **kwargs)


class CustomFrame(CustomWidget, tk.Frame):
    ## DEFAULT COLOR IS PARENT COLOR ##
    # TO SET THE COLOR USE SET_BACKGROUND = 'COLOR' OR '#2C23C3'

    pass


class LabelWithParentBackground(CustomWidget, tk.Label):
    pass


class ButtonWithParentBackground(CustomWidget, tk.Button):
    pass


class CanvasWithParentBackground(CustomWidget, tk.Canvas):
    def __init__(self, master=None, borderwidth=0, highlightthickness=0, relief='ridge', *args, **kwargs):
        super().__init__(master=master,
                         borderwidth=borderwidth, highlightthickness=highlightthickness, relief=relief, *args, **kwargs)


class LaterButton(CanvasWithParentBackground):
    def __init__(self, master=None, text: str = None, callback_func=None, wait_time: int = 1, *args, **kwargs):
        '''
        text: str 
        callback_func: callback function
        wait_time: int in seconds
        '''
        super().__init__(master=master, *args, **kwargs)

        # initialize
        self.text = text
        self.callback_func = callback_func
        self.total_duration = wait_time  # in seconds

        # for reference only
        self.button_font = BUTTON_FONT
        self.locked_text_color = 'grey'
        self.unlocked_text_color = 'black'
        self.hover_text_color = '#0079FF'
        self.progress_bar_color = '#FF6969'

        self.bind('<Configure>', self._initialize_layout)

    def _initialize_layout(self, event):
        self.delete('all')
        root = self.winfo_toplevel()

        root.update_idletasks()
        self.width = event.width
        self.height = event.height
        # print(f'width = {self.width}, height = {self.height}')

        self._background_width = 0
        self._animation_id = None  # for cancelling .after fucntion

        # create text on canvas
        self.create_text(self.width/2, self.height/2,
                         text=self.text,
                         font=self.button_font,
                         fill=self.locked_text_color,
                         tags=('text_canvas'))

        ## bind event to tags ##
        self.bind('<Enter>', self._activate_button_for_click)
        # self.bind('<Enter>', self.callback_func) # no problem here
        self.bind('<Leave>', self._leaving_canvas_function, add='+')

    def _leaving_canvas_function(self, event):
        # revert to original
        self.delete('background')
        self.after_cancel(self._animation_id)
        self._background_width = 0
        self.itemconfigure('text_canvas', fill=self.locked_text_color)
        self.tag_unbind('text_canvas', "<Button-1>", None)
        self.configure(cursor='arrow')

    def _activate_button_for_click(self, event):
        self._background_animation()
        self.itemconfigure(
            'text_canvas', fill=self.locked_text_color, activefill='')

    def _background_animation(self):
        ## progress like animation ##
        self.distance_to_cover = self.width  # Total width to cover in pixels

        self.animation_speed = int(
            self.total_duration * 1000 / self.distance_to_cover)

        # print(f'{time.ctime()} speed = {self.animation_speed}')

        # print('inside background animation',self._background_width)
        if self._background_width <= self.width and self.winfo_exists():
            self.create_rectangle(0, 0, self._background_width, self.height,
                                  fill=self.progress_bar_color, width=0, tags=('background'))
            # self._background_width += step_size
            self._background_width += 1
            self._animation_id = self.after(
                self.animation_speed, self._background_animation)

        else:  # what to do after progress bar reaching end
            self.itemconfigure(
                'text_canvas',
                fill=self.unlocked_text_color,
                activefill=self.hover_text_color)
            self.configure(cursor='hand2')
            self.tag_bind('text_canvas', "<Button-1>", self.root_destroy)
            # print('canvas exists:',self.winfo_exists())

        self.tag_lower('background')

    def root_destroy(self, event):
        self.after(10, self.callback_func)


class UpdateProgressBar(ttk.Labelframe):
    def __init__(self, parent=None):
        super().__init__(master=parent)

        self.progress_bar = ttk.Progressbar(
            self, mode='indeterminate', maximum=100)
        self.progress_bar.pack(fill='x', padx=2, pady=1)
        self.configure(text='Updating do not exit')

    def start(self, interval=10):
        self.progress_bar.start(interval)


class ReasonTextGui(tk.Toplevel):
    '''
    When user clicks on later, he/she is prompted with the reason gui. where one has to type the reason for not doing the exercise.
    - exercise_log is a custom class that has the format for the log table
    - take reason and update exercise_log and add it log_table
    - destroy the parent gui when submit button is clicked
    '''

    def __init__(self, parent=None, exercise_log=None):
        super().__init__(master=parent)
        # self.geometry("400x250")
        self.attributes('-topmost', True)
        self.title('why?')
        # Make the top-level window transient to the main window
        self.transient(parent)
        self.grab_set()  # Prevent interaction with the main window while the top-level window is open

        ## INITIALIZE ##
        self.text = ""
        self.parent = parent
        self.exercise_log = exercise_log

        ## FRAME ##
        button_title_frame = tk.Frame(master=self)
        button_title_frame.pack(padx=2, pady=2, fill='x')

        reason_label = tk.Label(master=button_title_frame,
                                text="Reason", font=TITLE_FONT)
        reason_label.pack(side='left', padx=5, pady=2)

        # notify label
        self.notify_label = tk.Label(
            master=button_title_frame, text="")
        self.notify_label.pack(side='left')

        submit_button = tk.Button(
            master=button_title_frame, text="Submit", command=self.save_reason)
        submit_button.pack(side='right', padx=5)

        # not in pixels but based on font size
        self.text_box = tk.Text(master=self, width=30,
                                height=10, font=REASON_TEXT)
        self.text_box.pack(padx=5, pady=2, fill='x')

        is_it_imp_label = tk.Label(master=self, text="Is It Important than your Health? \n V:8600",
                                   justify='center', font=BUTTON_FONT, foreground='#282a36')
        is_it_imp_label.pack(padx=2, pady=5)

    def save_reason(self):
        # Strip leading and trailing whitespace
        self.text = self.text_box.get(1.0, tk.END).strip()
        if self.text == "":
            self.notify_label.configure(text="Reason can't be empty !")
            self.notify_label.after(
                3000, lambda: self.notify_label.configure(text=""))
        else:
            self.exercise_log.add_reason(self.text)
            self.exercise_log.add_entry_to_database()
            self.parent.destroy()

    def get_text(self):
        return self.text


class ExerciseIcon(ttk.Label):
    # ADD ARGS AND KWARGS IF YOU WANT TO USE ttk.Label
    def __init__(self, parent=None, img_path: str = None, text: str = None, set_background: str = 'parent', icon_size: tuple = ICON_SIZE, *args, **kwargs):

        ## initialize ##
        if set_background == 'parent':
            color = parent.cget('background')
        else:
            color = set_background

        ## processing Image ##
        my_image = MyImage(*icon_size)  # UNPACKING TUPLE
        resized_image = my_image.resize_image(
            path=img_path, preserve_aspect=True, resize_percent_of_original=100)
        self.tk_image = my_image.to_tk(resized_image)

        # add to label
        super().__init__(master=parent, text=text,
                         image=self.tk_image,
                         compound=tk.TOP,
                         font=ICON_FONT,
                         background=color,
                         foreground=ICON_LABEL_COLOR,
                         padding=(0, 0),
                         anchor=tk.CENTER,
                         #  borderwidth=1,        ## FOR VISUALISATION ONLY ⬇
                         #  relief = 'groove',
                         *args, **kwargs)


class IntervalIcon(ExerciseIcon):  # SETTINGS GUI ##
    def __init__(self, parent=None, img_path: str = None, text: str = None, set_background: str = 'parent', icon_size: tuple = (20, 20)):
        super().__init__(parent, img_path, text, set_background, icon_size)
        self.configure(compound=tk.LEFT,
                       foreground='#2c2c2c',
                       anchor='w')


class ExerciseTitle(ttk.Label):
    def __init__(self, parent=None, text=None, url: str = None, set_background: str = 'parent', *args, **kwargs):

        ## INITIALIZE ##
        configure_styles()
        self.url = url

        if set_background == 'parent':
            color = parent.cget('background')
        else:
            color = set_background

        ## OPERATIONS BEFORE CREATING ##
        text = text.title()  # TITLEING THE STRING

        super().__init__(master=parent,
                         text=text,
                         style='Title.TLabel',
                         cursor='hand2',
                         background=color,)

        ## BINDING EVENT ##
        self.bind('<Button-1>', self.open_link)

    def open_link(self, event):
        webbrowser.open(self.url)


class DisableInteractionWithOtherWindow(tk.Toplevel):
    def __init__(self, parent,):
        super().__init__(master=parent,
                         background='black',
                         cursor='pirate'
                         )

        ## INITIALIZE ##
        self.parent = parent

        ## Get the screen width and height ##
        screen_width = parent.winfo_screenwidth()
        screen_height = parent.winfo_screenheight()

        ## Customising TOP LEVEL WINDOW ##
        self.geometry(f"{screen_width}x{screen_height}")
        self.overrideredirect(True)
        self.attributes("-alpha", 0.5)
        self.attributes("-topmost", True)

        self.bind('<Any-Button>', self.below_parent)

        ## FOR DEVELOPMENT ONLY ##
        # self.bind('<Escape>',self.escape)
        # canva = tk.Canvas(master=self, background='teal')
        # canva.pack(expand=True,fill='both')
        # tk.Label(master=canva,text='howdy').pack()
        # tk.Label(master=canva,text='solar').pack(side='bottom')

    def below_parent(self, event):
        self.lower(belowThis=self.parent)

    def escape(self, event):
        root = self.winfo_toplevel()
        root.destroy()


class ThemeCombobox(ttk.Combobox):
    def __init__(self, parent=None, label_frame_text=None,default = None, widgets=None):
        self.widgets = widgets
        label_frame = ttk.Labelframe(master=parent, text=label_frame_text)
        label_frame.pack()
        validate = parent.register(self.__validate_function)
        super().__init__(master=label_frame, state='readonly', font=ICON_FONT,validate='focusin',validatecommand=(validate,'%P')) # since it read only we can't modify entry directly so not using index

        table_from_theme = SqliteDefs.get_table_names(DatabaseConstants.THEMED_DB_PATH)
        print(table_from_theme) 
        exercise_db_equipments :list =  SqliteDefs.get_distinct_column_values('Exercise',
                                                                              'equipment',
                                                         DatabaseConstants.EXERCISE_DB_PATH)
        values = ['none'] + table_from_theme 
        self.selection = tk.StringVar(value=default)
        self.__validate_function(default) # if theme none is selected then its not removing during initialization so calling this
        self.configure(values= values,textvariable=self.selection)
    
    def __validate_function(self,value):
        if self.widgets:
            for widget in self.widgets: 
                if value == 'none':
                    widget.grid() 
                else: 
                    widget.grid_remove()
                

            
        return True


class ExerciseComboBox(ttk.Combobox):
    user_conditions = []
    combo_boxes_instances = []
    table_name = 'Exercise'

    def __init__(self, parent=None, column_name=None, string_var=None, default=''):
        label_frame = ttk.Labelframe(master=parent, text=column_name)
        label_frame.pack()

        super().__init__(master=label_frame, state='readonly', font=ICON_FONT,)
        # COMMUNICATION BETWEEN INSTANCES
        ## CHECK THE LENGTH OF USER_CONDITIONS ##
        self.this_instance_index = len(ExerciseComboBox.user_conditions)
        ExerciseComboBox.combo_boxes_instances.append(
            self)  # append this instance to the list ##
        # To avoid getting list index out of range error ##
        ExerciseComboBox.user_conditions.append(None)

        # INITIALIZE, using in class methods
        self.column_name = column_name
        # self.selection = tk.StringVar(value=column_name) ## use this to have default name
        self.selection = tk.StringVar(value=default)
        self.string_var = string_var

        self['textvariable'] = self.selection

        if self.this_instance_index % 3 == 0:
            list = SqliteDefs.get_distinct_column_values(ExerciseComboBox.table_name,
                                                         column_name,
                                                         DatabaseConstants.EXERCISE_DB_PATH)

            self['values'] = sorted(list)
        else:
            # Exept first initialize other instances with disabled state
            self['state'] = 'disabled'

        self.bind('<<ComboboxSelected>>', self.do_after_combobox_selected)

    def do_after_combobox_selected(self, event):
        selected_option = self.selection.get()  # WHAT USER SELECTED
        # SEARCH CRITERIA FOR QUERY "muscle = 'chest'"
        condition = f"{self.column_name}='{selected_option}'"
        ExerciseComboBox.user_conditions[self.this_instance_index] = condition

        ExerciseComboBox.update_list_of_next_instance(self.this_instance_index)
        ExerciseComboBox.clear_selection_after_instance(
            self.this_instance_index)

        if self.string_var:
            exercise_available = ExerciseComboBox.available_exercises()
            self.string_var.set(f'Available Exercise {exercise_available}')

    @classmethod
    # Enable it as well
    def update_list_of_next_instance(cls, current_instance_index):
        if current_instance_index + 1 < len(cls.combo_boxes_instances):
            # change the list of next instance
            instance = cls.combo_boxes_instances[current_instance_index+1]

            # you want the conditions untill the current instance
            conditions = cls.user_conditions[:current_instance_index+1]
            # print(conditions)

            list = SqliteDefs.get_distinct_column_values(cls.table_name,
                                                         instance.column_name,
                                                         DatabaseConstants.EXERCISE_DB_PATH,
                                                         conditions=conditions)
            instance['values'] = sorted(list)
            instance['state'] = 'normal'

    @classmethod
    def available_exercises(cls) -> int:
        # remove None that we defined, if they are present
        conditions = [item for item in cls.user_conditions if item is not None]
        available_exercises = SqliteDefs.retrieve_data(DatabaseConstants.EXERCISE_DB_PATH,
                                                       cls.table_name, conditions)
        return (len(available_exercises))

    @classmethod
    def clear_selection_after_instance(cls, instance_index):
        '''
        If the first combo box is changed we have to clear the selection of subsequent combo boxes 
        '''
        ## +1 because we don't want to clear the current instance index ##
        for i in range(instance_index+1, len(cls.combo_boxes_instances)):
            instance = cls.combo_boxes_instances[i]

            # instance.selection.set(instance.column_name)
            instance.selection.set('')
            cls.user_conditions[i] = None
            ## same as self.selection.set()  for tk.StringVar##


class LabelAndEntry(tk.Frame):
    def __init__(self, parent, label_name="test", tk_var=None, **kwargs):
        super().__init__(parent)

        self.rowconfigure(0, weight=1, uniform='a')
        self.columnconfigure(0, weight=1, uniform='a')
        self.columnconfigure(1, weight=2, uniform='a')

        self.label = ttk.Label(self, text=label_name)
        self.label.grid(row=0, column=0, sticky='news')

        self.entry = tk.Entry(self, textvariable=tk_var, **kwargs)
        self.entry.grid(row=0, column=1, sticky='news')

    def get(self):
        return self.entry.get()

    def is_entry_empty(self):
        """
        Check if the entry is empty.
        Returns:
            bool: True if the entry is empty, False otherwise.
        """
        entry_string = self.entry.get()
        if not entry_string:
            return True
        else:
            return False


class IntervalEntry(ttk.Entry):
    def __init__(self, parent=None, default='', *args, **kwargs):
        super().__init__(master=parent, *args, **kwargs)
        self.time_entry = tk.StringVar(value=default)
        validation = parent.register(self.validate_input)
        self.configure(textvariable=self.time_entry,
                       #    relief='ridge',
                       validate="key", validatecommand=(validation, "%P"),
                       justify=tk.CENTER)
    def validate_input(self,new_value):
    # Your validation logic goes here
    # For example, let's say we only allow digits
        if new_value.isdigit() or new_value == "":
            return True
    def is_int(self):
        try:
            int(self.time_entry.get())
            return int
        except ValueError:
            return False


if __name__ == '__main__':
    root = tk.Tk()
    root.geometry('200x200')
    root.attributes("-topmost", True)
    # UpdateProgressBar(root).pack()
    ThemeCombobox(root).pack()
    # IntervalEntry(parent=root).pack()
    # ReasonTextGui(root)
    root.mainloop()
