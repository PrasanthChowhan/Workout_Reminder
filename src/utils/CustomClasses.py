import tkinter as tk

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