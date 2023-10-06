import tkinter as tk
from tkinter import ttk
# from ttkbootstrap import Floodgauge
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
                text = 'sunday',
                font = ('helvetica',12),
               )
    s.map('did_it.TButton',background = [('active','#38CC33')])



if __name__ == '__main__':
    root = tk.Tk()
    root.geometry('200x100-0-0')
    configure_styles()

    ttk.Button(root, style= 'did_it.TButton',text='one',name= 'btn_i_did_it').pack(expand=True,fill='x',)

    later_button= LaterButton(root)
    later_button.pack(
        # expand=True,fill='x',
                      padx=10,pady=10)
    # root.update()
    # print('width',later_button.winfo_width())
    root.mainloop()
    
