import tkinter as tk
import time
from src.Gui.gui_settings import *


def timing_decorator(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"{func.__name__} took {end_time - start_time:.2f} seconds to execute.")
        return result
    return wrapper


class CustomWidget(tk.Widget):
    def __init__(self, master=None, *args, **kwargs):
        parent_background_color = master.cget('background')
        super().__init__(master=master, background=parent_background_color, *args, **kwargs)


class FrameWithParentBackground(CustomWidget, tk.Frame):
    pass


class LabelWithParentBackground(CustomWidget, tk.Label):
    pass


class ButtonWithParentBackground(CustomWidget, tk.Button):
    pass


class CanvasWithParentBackground(CustomWidget, tk.Canvas):
    def __init__(self, master=None, borderwidth=0, highlightthickness=0, relief='ridge', *args, **kwargs):
        super().__init__(master=master,
                         borderwidth=borderwidth, highlightthickness=highlightthickness, relief=relief, *args, **kwargs)

# class LaterButton(tk.Button):
#     def __init__(self, master=None,background : str =False, *args,**kwargs):

#         if not background:
#             background = master.cget('background')

#         super().__init__(master=master, background=background, *args, **kwargs)


class LaterButton(CanvasWithParentBackground):
    def __init__(self, master=None,text :str = None, callback_func= None,wait_time :int = 1, *args, **kwargs):
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
        root= self.winfo_toplevel()

        root.update_idletasks()
        self.width = event.width
        self.height = event.height
        print(f'width = {self.width}, height = {self.height}')

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
        self.tag_unbind('text_canvas', "<Button-1>", None )

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
            self._animation_id = self.after(self.animation_speed, self._background_animation)

        else:  # what to do after progress bar reaching end
            print('unlocked later button')
            self.itemconfigure(
                'text_canvas', fill=self.unlocked_text_color, activefill=self.hover_text_color)
            self.tag_bind('text_canvas', "<Button-1>",self.root_destroy)
            # print('canvas exists:',self.winfo_exists())

        self.tag_lower('background')

    def root_destroy(self,event):
        self.after(100,self.callback_func)

