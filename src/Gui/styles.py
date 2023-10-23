import tkinter as tk
from tkinter import ttk
from tkinter import font

import src.Gui.gui_settings as GuiSettings
from src.Gui.gui_settings import *
class ConfigureStyle:
    def __init__(self):
        self.style = ttk.Style()
    
    def did_it_TButton(self):
        style_name = "did_it.TButton"
        self.style.configure(style_name,
                foreground=DID_IT_BUTTON_FOREGROUND,
                background=DID_IT_BUTTON_BACKGROUND,
                borderwidth = 0,
                highlightthickness=0, 
                relief='flat',
                font = BUTTON_FONT,
                # anchor = tk.CENTER,
               )
        self.style.map(style_name,background = [('active',DID_IT_BUTTON_BACKGROUND_ACTIVE)])
        return style_name
    
    def TNotebook(self):
        style_name ='setting.TNotebook' 
        self.style.configure(style_name,tabposition = 'w')
        return style_name
    
    def title_label(self):
        ## TITLE LABEL ##   
        self.style.configure('Title.TLabel',
                    foreground=TITLE_FOREGROUND_COLOR,
                    borderwidth = 0,
                    highlightthickness=0,
                    relief= 'ridge',
                    
                    font=TITLE_FONT)
        
        
        
        ## COMMENT OUT IF YOU DON'T WANT OUTLINE ON HOVER ##
        # s.map('Title.TLabel',    
        #       font = [('hover',GuiSettings.TITLE_FONT_HOVER)],
        #       )
            


    def theme_needed(self):
        '''
        sometimes you need to use theme to get desired effect
        '''
        self.style.theme_use('default')

        
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
                relief= 'ridge',
                
                font=TITLE_FONT)
    
    
    
    ## COMMENT OUT IF YOU DON'T WANT OUTLINE ON HOVER ##
    # s.map('Title.TLabel',    
    #       font = [('hover',GuiSettings.TITLE_FONT_HOVER)],
    #       )



if __name__ == '__main__':
    root = tk.Tk()
    root.geometry('200x100-0-0')
    configure_styles()
    ttk.Label(root,style='Title.TLabel',text='one is one').pack()
    

    ttk.Button(root, style= 'did_it.TButton',text='random text',name= 'btn_i_did_it',cursor='hand2').pack()
    root.mainloop()
    
