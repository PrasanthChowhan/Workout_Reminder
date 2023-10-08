import tkinter as tk
from tkinter import ttk

from src.Gui.gui_settings import *
from src.Gui.components import LaterButton
def configure_styles():
    s = ttk.Style()
    s.theme_use('default')
    
    s.configure('did_it.TButton',
                foreground='#2c2c2d',
                background='#27bb22',
                borderwidth = 0,
                highlightthickness=0, 
                relief='ridge',
                font = BUTTON_FONT,
                anchor = tk.CENTER,
               )
    s.map('did_it.TButton',background = [('active','#38CC33')])



if __name__ == '__main__':
    root = tk.Tk()
    root.geometry('200x100-0-0')
    configure_styles()

    ttk.Button(root, style= 'did_it.TButton',text='no padding',name= 'btn_i_did_it').pack()

    # later_button= LaterButton(root)
    # later_button.pack(
    #     # expand=True,fill='x',
    #                   padx=10,pady=10)
    # root.update()
    # print('width',later_button.winfo_width())
    root.mainloop()
    
