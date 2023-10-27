import tkinter as tk
from tkinter import ttk
from src.Gui.gui_settings import *


        
def configure_styles():
    s = ttk.Style()
    s.theme_use('default')
    ## Did it Button ##
    s.configure('did_it.TButton',
                foreground=DID_IT_BUTTON_FOREGROUND,
                background=DID_IT_BUTTON_BACKGROUND,
                borderwidth = 0,
                highlightthickness=0, 
                relief='flat',
                font = BUTTON_FONT,
                # anchor = tk.CENTER,
               )
    s.map('did_it.TButton',background = [('active',DID_IT_BUTTON_BACKGROUND_ACTIVE)])
    
    ## TITLE LABEL ##   
    s.configure('Title.TLabel',
                foreground=TITLE_FOREGROUND_COLOR,
                borderwidth = 0,
                highlightthickness=0,
                relief= 'flat',
                
                font=TITLE_FONT)
    
    ## COMMENT OUT IF YOU DON'T WANT OUTLINE ON HOVER ##
    # s.map('Title.TLabel',    
    #       font = [('hover',GuiSettings.TITLE_FONT_HOVER)],
    #       )

    s.configure("Exercise.TCombobox", 
        background="lightgray", 
        foreground="black",
        selectbackground="lightblue",
        selectforeground="black",
        font=("Segoe UI", 12),
        fieldbackground="lightgray",
        fieldforeground="black",
        borderwidth = 1,
        ridge= 'flat'
    )

    s.map("Exercise.TCombobox", 
        arrowcolor=[("active", "blue"), ("disabled", "gray")]
    )

    
    
    



if __name__ == '__main__':
    root = tk.Tk()
    root.geometry('200x100-0-0')
    configure_styles()
    ttk.Label(root,style='Title.TLabel',text='one is one').pack()
    

    ttk.Button(root, style= 'did_it.TButton',text='random text',name= 'btn_i_did_it',cursor='hand2').pack()
    root.mainloop()
    
