from src.Gui.components import ExerciseComboBox, IntervalIcon, IntervalEntry, LabelAndEntry
import tkinter as tk
from tkinter import ttk
from src.DbManager import ConfigReader
from src.utils.constants import DatabaseConstants, WebLinks
from src.GitCommands import GitCommands
from src.Gui.window_function import SetWindowPosition
import webbrowser
import sys
import threading
from src.SubprocessCommands import SubprocessCommands
# from testing_python import open_tray

class SettingGuiStandalone:
    def __init__(self,stop_scheduling_callback=None):
        self.close_gui_var = None
        self.stop_scheduling_callback = stop_scheduling_callback

    def start_gui(self):
        self.root = tk.Tk()
        self.close_gui_var = tk.BooleanVar(value=False)
        self.close_gui_var.trace_add('write', self._check_for_quit)
        gui_icon = tk.PhotoImage(file='resources\icons\gui icon\pawn with dumbell.png')
        self.root.iconphoto(True, gui_icon)
        self.root.attributes("-topmost", True)
        

        SettingFrame(parent=self.root,
                     stop_scheduling_callback=self.stop_scheduling_callback).pack(expand=True,fill='both')
        
        SetWindowPosition(window=self.root)
        self.root.mainloop()

    def get_close_gui_var(self):
        return self.close_gui_var

    def _check_for_quit(self, *args):
        if self.close_gui_var:
            self.root.destroy()

## most of the 
class SettingFrame(tk.Frame):
    def __init__(self, parent=None,stop_scheduling_callback = None):
        self.stop_scheduling_callback = stop_scheduling_callback
        

        super().__init__(master=parent)

        self.setting_notebook = SettingNotebook(parent=self,update_gui_callback= lambda:self.system_upadating_protocol(initialise=True))
        self.setting_notebook.pack(fill='both')
        self.save_button = ttk.Button(master=self, text='Save',
                                      command=self.save_command)
        self.save_button.pack(fill='x')

    def save_command(self):
        self.save_button.configure(text='Saving...', state='disabled')
        self.setting_notebook.save_all_data()
        self.after(500, lambda: self.save_button.configure(
            text='Save', state='normal'))
        self.system_upadating_protocol(initialise=False)
    
    def system_upadating_protocol(self,initialise = False):
        self.winfo_toplevel().destroy() # destroying the root
        if self.stop_scheduling_callback:
            self.stop_scheduling_callback()
        if initialise: # INitialise again only after update.      
            initialise_thread = threading.Thread(target=SubprocessCommands, args=('initialise', ))
            initialise_thread.start()
            initialise_thread.join()
        threading.Thread(target=SubprocessCommands, args=('schedule', )).start()
        sys.exit()



class SettingNotebook(ttk.Notebook):
    setting_dict = {}

    def __init__(self, parent=None, update_gui_callback=None):
        super().__init__(master=parent,
                         )

        ## {} if file not found ##
        setting_dict = ConfigReader.read_config_file(DatabaseConstants.SETTINGS_YAML_PATH,default_file=DatabaseConstants.DEFUALT_SETTINGS_YAML_PATH)

        self.tab = {}
        ## CREATE FRAME ##
        self.tab['Exercise'] = MuscleSetting(
            parent=self, setting_dict=setting_dict)
        self.tab['Save to'] = OnlineIntergration(
            parent=self, setting_dict=setting_dict)
        self.tab['update'] = update_feedback(
            parent=self, update_gui_callback=update_gui_callback)



        ## ADD FRAME TO NOTEBOOK ##
        for name, instance in self.tab.items():
            self.add(instance, text=name)
            self.add(instance, text=name)

    def save_all_data(self):
        all_dict_combined = {}
        for instance in self.tab.values():
            all_dict_combined.update(instance.get_info())

        ConfigReader().update_or_create_yaml_file(
            DatabaseConstants.SETTINGS_YAML_PATH, all_dict_combined)


class MuscleSetting(ttk.Frame):
    def __init__(self, parent=None, setting_dict: dict = {}):
        super().__init__(master=parent, style='TFrame')

        self.notify_var = tk.StringVar(value='')

        ## Timer settings ##
        timer_frame = tk.Frame(master=self)
        timer_frame.pack(fill='x')
        interval_icon = IntervalIcon(parent=timer_frame, img_path=r'resources\icons\setting_gui\clock.png',
                                     text='Interval (min)')
        interval_icon.pack(side='left', fill='x', padx=10, pady=10)

        self.interval_entry = IntervalEntry(
            timer_frame, default=setting_dict.get('schedule', 45))
        self.interval_entry.pack(side='left', fill='x', padx=10, pady=10)

        # MESSAGE
        self.notify_label = ttk.Label(master=self,
                                      textvariable=self.notify_var)
        self.notify_label.pack()

        ## COMBOBOX FRAME ##
        combi_setting: dict = setting_dict.get('database', {})

        self.combo_frame = tk.Frame(master=self)
        self.combo_frame.pack(expand=True, fill='x')

        self.equipment_combi = ExerciseComboBox(parent=self.combo_frame,
                                                column_name='equipment',
                                                string_var=self.notify_var,
                                                default=combi_setting.get('equipment', ''))
        self.equipment_combi.pack(fill='x', padx=5, pady=5)

        self.difficulty_combi = ExerciseComboBox(parent=self.combo_frame,
                                                 column_name='difficulty',
                                                 string_var=self.notify_var,
                                                 default=combi_setting.get('difficulty', ''))
        self.difficulty_combi.pack(fill='x', padx=5, pady=5)

        self.muscle_combi = ExerciseComboBox(parent=self.combo_frame,
                                             column_name='muscle',
                                             string_var=self.notify_var,
                                             default='' if combi_setting.get('muscle', 'default') == 'default' else combi_setting.get('muscle', ''))
        self.muscle_combi.pack(fill='x', padx=5, pady=5)

        ## This code will set self.cycle_muscle_var to True if the value of setting_dict['muscle'] is 'default', and it will set it to False for any other value. ##
        self.cycle_muscle_var = tk.BooleanVar(
            value=combi_setting.get('muscle', '') == 'default')
        self.cycle_muscle = ttk.Checkbutton(master=self.combo_frame,
                                            text='Target all Muscles',
                                            command=self.save_all_muscles_setting,
                                            onvalue=True, offvalue=False, variable=self.cycle_muscle_var)
        self.cycle_muscle.pack(padx=5, pady=5)

        ## BUTTONS FRAME ##
        button_frame = tk.Frame(master=self)
        button_frame.pack(fill='x', padx=5, pady=2)

    def check_interval_entry(self):
        entry_text = self.interval_entry.get()
        if not entry_text:
            self.notify_var.set("Interval cannot be Empty")
            return False

        elif entry_text.isdigit():
            return True
        else:
            self.notify_var.set("Interval cannot be a string")
            return False

    def get_info(self):

        if self.cycle_muscle_var.get():
            muscle = 'default'
        else:
            muscle = self.muscle_combi.get()

        setting_data = {'equipment': self.equipment_combi.get(),
                        'muscle': muscle,
                        'difficulty': self.difficulty_combi.get()}

        for_data_base = {'database': setting_data,
                         'schedule': self.interval_entry.get()}

        # ConfigReader().update_or_create_yaml_file(
        #     DatabaseConstants.SETTINGS_YAML_PATH, for_data_base)
        return for_data_base

    def save_user_settings(self):

        if self.check_interval_entry():  # if interval entry is int then TRUE
            if self.equipment_combi.get() and self.difficulty_combi.get() and self.muscle_combi.get():
                self.get_info(cyle_muscle_group=True)
            else:
                self.notify_var.set('Select all the fields')

    def save_all_muscles_setting(self):
        equipment_entry_value = self.equipment_combi.get()
        # check if the user selected equipment or not

        if self.check_interval_entry():
            if self.cycle_muscle_var.get():
                # disable muscle combi if target all muscle is selected
                self.muscle_combi.configure(state='disabled')
            else:
                self.muscle_combi.configure(
                    state='normal')  # enable muscle combi
            if self.equipment_combi.get() and self.difficulty_combi.get():
                pass
            else:
                self.notify_var.set('Select Equipment and Difficulty')


class OnlineIntergration(ttk.Notebook):
    def __init__(self, parent=None, setting_dict: dict = {}):
        super().__init__(master=parent, style='TNotebook')

        self.name_in_dict = 'Integration setting'
        self.integrate_obj_dict = {}  # Frame Instances are stored ##

        online_integration = setting_dict.get(self.name_in_dict, {})

        ## Create frame ##
        self.integrate_obj_dict['Notion'] = self.NotionTab(
            self, notion_setting=online_integration.get('Notion', {}))
        # self.integrate_obj_dict['Potion'] = self.NotionTab(self)

        ## Add frames to notebook ##
        for name, frame_obj in self.integrate_obj_dict.items():
            self.add(frame_obj, text=name)

    def get_info(self):
        data = {}
        for name, frame_obj in self.integrate_obj_dict.items():
            data[name] = (frame_obj.get_info())
        return {self.name_in_dict: data}

    class NotionTab(ttk.Frame):
        '''
        sample_dict = {
        "notion": {
            'save' : True,
            'api_key' : 'edadt03f-dga3-5e32-secret',
            'page_id' : '3etadgggaerasd'
        }
    }
        '''

        def __init__(self, parent, notion_setting: dict = {}):
            super().__init__(parent, style='TFrame')

            self.widgets = {}
            self.vars = {}

            self.vars['save'] = tk.BooleanVar(
                value=notion_setting.get('save', False))
            self.vars['api'] = tk.StringVar(
                value=notion_setting.get('api', ''))
            self.vars['page_id'] = tk.StringVar(
                value=notion_setting.get('page_id', ''))
            self.vars['database_id'] = tk.StringVar(
                value=notion_setting.get('database_id', ''))

            self.widgets['save'] = ttk.Checkbutton(self, text="Save to notion",
                                                   variable=self.vars['save'],
                                                   command=self.show, onvalue=True,
                                                   offvalue=False)
            self.widgets['save'].pack(pady=5)

            self.widgets['api'] = LabelAndEntry(self, label_name='Api-key',
                                                tk_var=self.vars['api'])
            self.widgets['api'].pack(fill='x', padx=5, pady=5)

            self.widgets['page_id'] = LabelAndEntry(self, label_name='Page-id',
                                                    tk_var=self.vars['page_id'])
            self.widgets['page_id'].pack(fill='x', padx=5, pady=5)

            self.widgets['database_id'] = LabelAndEntry(
                self, label_name='Database-id', tk_var=self.vars['database_id'], state='disabled')
            self.widgets['database_id'].pack(fill='x', padx=5, pady=5)

            ## NOTIFY LABEL ##
            self.notify_label = ttk.Label(self, text='', anchor=tk.CENTER)
            self.notify_label.pack(fill='x', padx=5, pady=5)

        def show(self):
            if self.widgets['api'].is_entry_empty() or self.widgets['page_id'].is_entry_empty():
                self.notify_label.configure(text='Fields cannot be empty')
                self.after(3000, lambda: self.notify_label.configure(text=''))

        def get_info(self):
            dict = {}
            for widget_name in self.widgets.keys():
                dict[widget_name] = self.vars[widget_name].get()
            return dict


class update_feedback(ttk.Frame):
    def __init__(self, parent=None, update_gui_callback=None):
        super().__init__(master=parent)
        self.update_gui_callback = update_gui_callback

        ttk.Button(self, text='Check for updates',
                   command=self.check_for_updates, cursor='hand2').pack(padx=5, pady=5)

        self.msg_var = tk.StringVar(value='')
        self.label = ttk.Label(self, textvariable=self.msg_var,
                               justify='center', anchor='center')
        self.update_button = ttk.Button(self, textvariable=self.msg_var,
                                        command=self.update_gui_callback)
        # self.update_button.pack(padx=5, pady=5)

        ttk.Button(self, text='help us improve by providing your feedback',
                   command=self.open_feedback, cursor='hand2').pack(side='bottom', pady=2)

   
    # IF UPDATE IS AVAILABLE BUTTON IS SHOWN FOR PULLING/UPDATIN ##
    def check_for_updates(self):
        status = GitCommands.check_for_update()
        self.msg_var.set(value=status)

        if status == 'Update available':
            self.update_button.pack(padx=5, pady=5)
        else:
            self.label.pack(padx=5, pady=5, fill='x')

    def open_feedback(self):
        webbrowser.open(WebLinks.GOOGLE_FORMS)

    def get_info(self):  # mandatory
        return {}


if __name__ == '__main__':
    SettingGuiStandalone().start_gui()
    # root = tk.Tk()
    # SettingFrame(root)
    # root.mainloop()
